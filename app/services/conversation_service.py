from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Dict, Any
from app.models.models import User, Conversation, Message, ConversationSummary
from app.schemas.schemas import ConversationCreate, MessageCreate
from app.services.external_api_service import external_api_service
from app.core.config import settings
import time

class ConversationService:
    """
    Servicio para manejar conversaciones y mensajes
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_user(self, username: str, email: str, full_name: str = None) -> User:
        """Obtener o crear un usuario"""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            user = User(
                username=username,
                email=email,
                full_name=full_name
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def create_conversation(self, user_id: int, title: str = None, model: str = None) -> Conversation:
        """Crear una nueva conversación"""
        conversation = Conversation(
            title=title or "Nueva conversación",
            user_id=user_id,
            model_used=model or settings.DEFAULT_MODEL
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
    
    def get_conversation(self, conversation_id: int, user_id: int = None) -> Optional[Conversation]:
        """Obtener una conversación específica"""
        query = self.db.query(Conversation).filter(Conversation.id == conversation_id)
        if user_id:
            query = query.filter(Conversation.user_id == user_id)
        return query.first()
    
    def get_user_conversations(self, user_id: int, limit: int = 50, offset: int = 0) -> List[Conversation]:
        """Obtener conversaciones de un usuario"""
        return (
            self.db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .filter(Conversation.is_active == True)
            .order_by(desc(Conversation.updated_at))
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    def add_message(self, conversation_id: int, role: str, content: str, 
                   tokens_used: int = 0, model_used: str = None, 
                   response_time: float = None, metadata: Dict = None) -> Message:
        """Agregar un mensaje a una conversación"""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tokens_used=tokens_used,
            model_used=model_used,
            response_time=response_time,
            metadata=metadata
        )
        self.db.add(message)
        
        # Actualizar estadísticas de la conversación
        conversation = self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if conversation:
            conversation.total_messages += 1
            conversation.total_tokens += tokens_used
            
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_conversation_messages(self, conversation_id: int, limit: int = 50, offset: int = 0) -> List[Message]:
        """Obtener mensajes de una conversación"""
        return (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .offset(offset)
            .limit(limit)
            .all()
        )
    
    def get_conversation_history_for_ai(self, conversation_id: int, limit: int = 10) -> List[Dict[str, str]]:
        """Obtener historial de conversación formateado para IA"""
        messages = (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
            .all()
        )
        
        # Invertir para tener orden cronológico
        messages.reverse()
        
        history = []
        for message in messages:
            history.append({
                "role": message.role,
                "content": message.content
            })
        
        return history
    
    async def process_chat_message(self, user_id: int, message_content: str, 
                                 conversation_id: int = None, model: str = None,
                                 max_tokens: int = 150, temperature: float = 0.7) -> Dict[str, Any]:
        """Procesar un mensaje de chat y obtener respuesta de IA"""
        start_time = time.time()
        
        # Crear conversación si no existe
        if not conversation_id:
            conversation = self.create_conversation(
                user_id=user_id,
                title=message_content[:50] + "..." if len(message_content) > 50 else message_content,
                model=model
            )
            conversation_id = conversation.id
        else:
            conversation = self.get_conversation(conversation_id, user_id)
            if not conversation:
                raise ValueError("Conversación no encontrada")
        
        # Agregar mensaje del usuario
        user_message = self.add_message(
            conversation_id=conversation_id,
            role="user",
            content=message_content
        )
        
        # Obtener historial para contexto
        history = self.get_conversation_history_for_ai(conversation_id, limit=settings.MAX_CONVERSATION_HISTORY)
        
        try:
            # Llamar a la IA
            ai_response = await external_api_service.openai_request(
                messages=history,
                model=model or settings.DEFAULT_MODEL,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extraer respuesta
            response_content = ai_response["choices"][0]["message"]["content"]
            tokens_used = ai_response.get("usage", {}).get("total_tokens", 0)
            
            response_time = time.time() - start_time
            
            # Agregar respuesta del asistente
            assistant_message = self.add_message(
                conversation_id=conversation_id,
                role="assistant",
                content=response_content,
                tokens_used=tokens_used,
                model_used=model or settings.DEFAULT_MODEL,
                response_time=response_time,
                metadata={
                    "max_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            
            return {
                "message": message_content,
                "response": response_content,
                "conversation_id": conversation_id,
                "model_used": model or settings.DEFAULT_MODEL,
                "tokens_used": tokens_used,
                "response_time": response_time
            }
            
        except Exception as e:
            # Agregar mensaje de error
            self.add_message(
                conversation_id=conversation_id,
                role="system",
                content=f"Error: {str(e)}",
                metadata={"error": True}
            )
            raise e
    
    def delete_conversation(self, conversation_id: int, user_id: int) -> bool:
        """Marcar conversación como inactiva"""
        conversation = self.get_conversation(conversation_id, user_id)
        if conversation:
            conversation.is_active = False
            self.db.commit()
            return True
        return False
    
    def update_conversation_title(self, conversation_id: int, user_id: int, new_title: str) -> bool:
        """Actualizar título de conversación"""
        conversation = self.get_conversation(conversation_id, user_id)
        if conversation:
            conversation.title = new_title
            self.db.commit()
            return True
        return False
    
    def get_conversation_stats(self, user_id: int = None) -> Dict[str, Any]:
        """Obtener estadísticas de conversaciones"""
        if user_id:
            conversations = self.db.query(Conversation).filter(Conversation.user_id == user_id).all()
        else:
            conversations = self.db.query(Conversation).all()
        
        total_conversations = len(conversations)
        total_messages = sum(conv.total_messages for conv in conversations)
        total_tokens = sum(conv.total_tokens for conv in conversations)
        
        # Modelo más usado
        models = [conv.model_used for conv in conversations if conv.model_used]
        most_used_model = max(set(models), key=models.count) if models else "N/A"
        
        # Tiempo promedio de respuesta
        messages_with_time = self.db.query(Message).filter(Message.response_time.isnot(None)).all()
        avg_response_time = sum(msg.response_time for msg in messages_with_time) / len(messages_with_time) if messages_with_time else 0
        
        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "total_tokens": total_tokens,
            "most_used_model": most_used_model,
            "avg_response_time": round(avg_response_time, 2)
        }

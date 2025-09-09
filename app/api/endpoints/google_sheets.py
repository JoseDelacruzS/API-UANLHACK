from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.schemas import (
    UserCreate, UserResponse, ConversationResponse, ConversationWithMessages,
    ChatRequest, ChatResponse, ConversationHistoryRequest, MessageResponse,
    ConversationStats, MessageResponse as GenericMessageResponse
)
from app.services.conversation_service import ConversationService
from app.database.connection import get_db
from datetime import datetime

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crear o obtener un usuario
    """
    try:
        service = ConversationService(db)
        db_user = service.get_or_create_user(
            username=user.username,
            email=user.email,
            full_name=user.full_name
        )
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando usuario: {str(e)}")

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Enviar mensaje y obtener respuesta de IA
    """
    try:
        service = ConversationService(db)
        response = await service.process_chat_message(
            user_id=request.user_id,
            message_content=request.message,
            conversation_id=request.conversation_id,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        return ChatResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando chat: {str(e)}")

@router.get("/conversations/{user_id}", response_model=List[ConversationResponse])
async def get_user_conversations(user_id: int, limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    """
    Obtener conversaciones de un usuario
    """
    try:
        service = ConversationService(db)
        conversations = service.get_user_conversations(user_id, limit, offset)
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo conversaciones: {str(e)}")

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(conversation_id: int, limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    """
    Obtener mensajes de una conversación
    """
    try:
        service = ConversationService(db)
        messages = service.get_conversation_messages(conversation_id, limit, offset)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo mensajes: {str(e)}")

@router.get("/conversations/{conversation_id}/full", response_model=ConversationWithMessages)
async def get_conversation_with_messages(conversation_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Obtener conversación completa con mensajes
    """
    try:
        service = ConversationService(db)
        conversation = service.get_conversation(conversation_id, user_id)
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversación no encontrada")
        
        messages = service.get_conversation_messages(conversation_id)
        
        return ConversationWithMessages(
            **conversation.__dict__,
            messages=messages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo conversación: {str(e)}")

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Eliminar (desactivar) una conversación
    """
    try:
        service = ConversationService(db)
        success = service.delete_conversation(conversation_id, user_id)
        
        if success:
            return GenericMessageResponse(message="Conversación eliminada exitosamente")
        else:
            raise HTTPException(status_code=404, detail="Conversación no encontrada")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando conversación: {str(e)}")

@router.put("/conversations/{conversation_id}/title")
async def update_conversation_title(conversation_id: int, user_id: int, new_title: str, db: Session = Depends(get_db)):
    """
    Actualizar título de conversación
    """
    try:
        service = ConversationService(db)
        success = service.update_conversation_title(conversation_id, user_id, new_title)
        
        if success:
            return GenericMessageResponse(message="Título actualizado exitosamente")
        else:
            raise HTTPException(status_code=404, detail="Conversación no encontrada")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando título: {str(e)}")

@router.get("/conversations/stats/{user_id}", response_model=ConversationStats)
async def get_user_conversation_stats(user_id: int, db: Session = Depends(get_db)):
    """
    Obtener estadísticas de conversaciones de un usuario
    """
    try:
        service = ConversationService(db)
        stats = service.get_conversation_stats(user_id)
        return ConversationStats(**stats, api_calls_today=0)  # TODO: implementar api_calls_today
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

@router.get("/conversations/stats", response_model=ConversationStats)
async def get_global_conversation_stats(db: Session = Depends(get_db)):
    """
    Obtener estadísticas globales de conversaciones
    """
    try:
        service = ConversationService(db)
        stats = service.get_conversation_stats()
        return ConversationStats(**stats, api_calls_today=0)  # TODO: implementar api_calls_today
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

@router.post("/conversations")
async def create_conversation(user_id: int, title: str = None, model: str = None, db: Session = Depends(get_db)):
    """
    Crear una nueva conversación
    """
    try:
        service = ConversationService(db)
        conversation = service.create_conversation(user_id, title, model)
        return ConversationResponse(
            id=conversation.id,
            title=conversation.title,
            user_id=conversation.user_id,
            model_used=conversation.model_used,
            total_messages=conversation.total_messages,
            total_tokens=conversation.total_tokens,
            is_active=conversation.is_active,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando conversación: {str(e)}")

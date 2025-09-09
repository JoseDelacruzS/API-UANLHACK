from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base

class User(Base):
    """
    Modelo para usuarios del sistema
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    """
    Modelo para conversaciones
    """
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    model_used = Column(String(100), default="gpt-3.5-turbo")
    total_messages = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    """
    Modelo para mensajes dentro de conversaciones
    """
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, default=0)
    model_used = Column(String(100))
    response_time = Column(Float)  # tiempo en segundos
    metadata = Column(JSON)  # información adicional como temperatura, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    conversation = relationship("Conversation", back_populates="messages")

class APICall(Base):
    """
    Modelo para almacenar llamadas a APIs externas
    """
    __tablename__ = "api_calls"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    api_name = Column(String(100), nullable=False)  # 'openai', 'weather', 'news', etc.
    endpoint = Column(String(500))
    method = Column(String(10), default="GET")
    request_data = Column(JSON)
    response_data = Column(JSON)
    status_code = Column(Integer)
    response_time = Column(Float)
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)  # costo estimado de la llamada
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    user = relationship("User")

class ConversationSummary(Base):
    """
    Modelo para resúmenes de conversaciones largas
    """
    __tablename__ = "conversation_summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    summary = Column(Text, nullable=False)
    summary_model = Column(String(100))
    messages_summarized = Column(Integer)  # número de mensajes resumidos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    conversation = relationship("Conversation")

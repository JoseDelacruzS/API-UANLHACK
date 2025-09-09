from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime

# === Schemas para Usuarios ===

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# === Schemas para Conversaciones ===

class ConversationBase(BaseModel):
    title: Optional[str] = None
    model_used: Optional[str] = "gpt-3.5-turbo"

class ConversationCreate(ConversationBase):
    user_id: int

class ConversationResponse(ConversationBase):
    id: int
    user_id: int
    total_messages: int
    total_tokens: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ConversationWithMessages(ConversationResponse):
    messages: List["MessageResponse"] = []

# === Schemas para Mensajes ===

class MessageBase(BaseModel):
    role: str  # 'user', 'assistant', 'system'
    content: str

class MessageCreate(MessageBase):
    conversation_id: int
    tokens_used: Optional[int] = 0
    model_used: Optional[str] = None
    response_time: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    tokens_used: int
    model_used: Optional[str] = None
    response_time: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# === Schemas para Chat/IA ===

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    user_id: int
    model: Optional[str] = "gpt-3.5-turbo"
    max_tokens: Optional[int] = 150
    temperature: Optional[float] = 0.7

class ChatResponse(BaseModel):
    message: str
    response: str
    conversation_id: int
    model_used: str
    tokens_used: int
    response_time: float

class ConversationHistoryRequest(BaseModel):
    conversation_id: int
    limit: Optional[int] = 50
    offset: Optional[int] = 0

# === Schemas para APIs Externas ===

class APIRequest(BaseModel):
    url: str
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None

class APIResponse(BaseModel):
    status_code: int
    data: Dict[str, Any]
    response_time: float
    cached: bool = False

class WeatherRequest(BaseModel):
    city: str
    units: Optional[str] = "metric"

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float

class NewsRequest(BaseModel):
    query: str
    language: Optional[str] = "es"
    page_size: Optional[int] = 10

class NewsResponse(BaseModel):
    articles: List[Dict[str, Any]]
    total_results: int
    query: str

# === Schemas para Estadísticas ===

class ConversationStats(BaseModel):
    total_conversations: int
    total_messages: int
    total_tokens: int
    most_used_model: str
    avg_response_time: float
    api_calls_today: int

class UserStats(BaseModel):
    user_id: int
    username: str
    total_conversations: int
    total_messages: int
    total_tokens: int
    most_active_day: Optional[str] = None

# === Schemas para Caché ===

class CacheStats(BaseModel):
    total_files: int
    total_size_bytes: int
    expired_files: int
    active_files: int

# === Schemas de Respuesta Genérica ===

class MessageResponse(BaseModel):
    message: str
    status: str = "success"
    timestamp: datetime = datetime.now()

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = datetime.now()

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    service: str
    version: str
    database: Optional[str] = None
    cache_status: Optional[str] = None
    external_apis: Optional[Dict[str, str]] = None

# Resolver forward references
ConversationWithMessages.model_rebuild()

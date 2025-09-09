from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TicketStatus(str, Enum):
    """Estados de tickets"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    """Prioridades de tickets"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketBase(BaseModel):
    """Esquema base para tickets"""
    title: str = Field(..., max_length=255)
    description: Optional[str] = None
    priority: TicketPriority = TicketPriority.MEDIUM
    client_id: int


class TicketCreate(TicketBase):
    """Esquema para crear ticket"""
    call_id: Optional[int] = None
    assigned_operator_id: Optional[int] = None
    watson_session_id: Optional[str] = None
    watson_metadata: Optional[Dict[str, Any]] = None


class TicketUpdate(BaseModel):
    """Esquema para actualizar ticket"""
    title: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    assigned_operator_id: Optional[int] = None


class TicketResponse(TicketBase):
    """Esquema de respuesta para ticket"""
    ticket_id: int
    status: TicketStatus
    call_id: Optional[int] = None
    assigned_operator_id: Optional[int] = None
    watson_session_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class TicketWithDetails(TicketResponse):
    """Esquema de ticket con detalles relacionados"""
    assigned_operator_name: Optional[str] = None
    client_external_ref: Optional[str] = None
    call_label: Optional[str] = None


class TicketList(BaseModel):
    """Esquema para lista de tickets"""
    tickets: List[TicketWithDetails]
    total: int
    page: int
    page_size: int


class TicketStats(BaseModel):
    """Esquema para estadísticas de tickets"""
    total_tickets: int
    open_tickets: int
    in_progress_tickets: int
    resolved_tickets: int
    closed_tickets: int
    tickets_by_priority: Dict[str, int]
    tickets_by_operator: Dict[str, int]
    average_resolution_time: Optional[float] = None


class WatsonTicketRequest(BaseModel):
    """Esquema para solicitud de ticket desde Watson"""
    session_id: str
    user_input: str
    context: Dict[str, Any]
    client_external_ref: str
    metadata: Optional[Dict[str, Any]] = None

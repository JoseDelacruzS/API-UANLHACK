from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import date


class CallBase(BaseModel):
    """Esquema base para llamadas"""
    call_label: Optional[str] = None
    operator_id: int
    client_id: int
    call_date: date
    conversation: Optional[str] = None
    sentimiento: Optional[str] = None
    impacto: Optional[str] = None
    urgencia: Optional[str] = None
    tema: Optional[str] = None


class CallCreate(CallBase):
    """Esquema para crear llamada"""
    pass


class CallUpdate(BaseModel):
    """Esquema para actualizar llamada"""
    call_label: Optional[str] = None
    conversation: Optional[str] = None
    sentimiento: Optional[str] = None
    impacto: Optional[str] = None
    urgencia: Optional[str] = None
    tema: Optional[str] = None


class CallResponse(CallBase):
    """Esquema de respuesta para llamada"""
    call_id: int
    
    model_config = ConfigDict(from_attributes=True)


class CallWithDetails(CallResponse):
    """Esquema de llamada con detalles de operador y cliente"""
    operator_name: Optional[str] = None
    client_external_ref: Optional[str] = None


class CallList(BaseModel):
    """Esquema para lista de llamadas"""
    calls: List[CallWithDetails]
    total: int
    page: int
    page_size: int


class CallAnalytics(BaseModel):
    """Esquema para análisis de llamadas"""
    total_calls: int
    calls_by_operator: dict
    calls_by_sentiment: dict
    calls_by_urgency: dict
    calls_by_impact: dict
    calls_by_date: dict
    average_conversation_length: Optional[float] = None

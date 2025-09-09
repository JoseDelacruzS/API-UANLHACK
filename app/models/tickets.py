from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.config.database import Base


class TicketStatus(PyEnum):
    """Estados de tickets"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(PyEnum):
    """Prioridades de tickets"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Ticket(Base):
    """Modelo para tickets generados automáticamente"""
    __tablename__ = "tickets"
    
    ticket_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM, nullable=False)
    
    # Relación con llamada que generó el ticket
    call_id = Column(
        Integer,
        ForeignKey("calls.call_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True
    )
    
    # Operador asignado
    assigned_operator_id = Column(
        Integer,
        ForeignKey("operators.operator_id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True
    )
    
    # Cliente relacionado
    client_id = Column(
        Integer,
        ForeignKey("clients.client_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False
    )
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Datos de Watson
    watson_session_id = Column(String(255), nullable=True)
    watson_metadata = Column(Text, nullable=True)  # JSON string
    
    # Relaciones
    call = relationship("Call")
    assigned_operator = relationship("Operator")
    client = relationship("Client")
    
    def __repr__(self):
        return f"<Ticket(ticket_id={self.ticket_id}, title='{self.title}', status='{self.status}')>"

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.config.database import Base


class TimestampMixin:
    """Mixin para agregar timestamps a los modelos"""
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BaseModel(Base, TimestampMixin):
    """Modelo base abstracto"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.config.database import Base


class Operator(Base):
    """Modelo para operadores"""
    __tablename__ = "operators"
    __table_args__ = {'schema': 'uanl'}
    
    operator_id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False, unique=True, index=True)
    
    # Relación con llamadas
    calls = relationship("Call", back_populates="operator")
    
    def __repr__(self):
        return f"<Operator(operator_id={self.operator_id}, name='{self.name}')>"

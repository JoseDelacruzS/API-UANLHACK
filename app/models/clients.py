from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database import Base


class Client(Base):
    """Modelo para clientes"""
    __tablename__ = "clients"
    
    client_id = Column(Integer, primary_key=True, index=True)
    external_ref = Column(String(64), nullable=False, unique=True, index=True)
    
    # Relación con llamadas
    calls = relationship("Call", back_populates="client")
    
    def __repr__(self):
        return f"<Client(client_id={self.client_id}, external_ref='{self.external_ref}')>"

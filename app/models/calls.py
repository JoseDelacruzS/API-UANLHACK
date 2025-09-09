from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.config.database import Base


class Call(Base):
    """Modelo para llamadas"""
    __tablename__ = "calls"
    
    call_id = Column(BigInteger, primary_key=True, index=True)
    call_label = Column(Text, nullable=True)
    operator_id = Column(
        Integer, 
        ForeignKey("operators.operator_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False
    )
    client_id = Column(
        Integer,
        ForeignKey("clients.client_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False
    )
    call_date = Column(Date, nullable=False)
    conversation = Column(Text, nullable=True)
    
    # Relaciones
    operator = relationship("Operator", back_populates="calls")
    client = relationship("Client", back_populates="calls")
    
    def __repr__(self):
        return f"<Call(call_id={self.call_id}, call_date='{self.call_date}')>"

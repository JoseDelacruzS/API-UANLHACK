from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.config.database import Base


class Call(Base):
    """Modelo para llamadas"""
    __tablename__ = "calls"
    __table_args__ = {'schema': 'uanl'}
    
    call_id = Column(BigInteger, primary_key=True, index=True)
    call_label = Column(Text, nullable=True)
    operator_id = Column(
        Integer, 
        ForeignKey("uanl.operators.operator_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False
    )
    client_id = Column(
        Integer,
        ForeignKey("uanl.clients.client_id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False
    )
    call_date = Column(Date, nullable=False)
    conversation = Column(Text, nullable=True)
    
    # Campos adicionales para análisis de Watson
    sentimiento = Column(Text, nullable=True)  # positivo, negativo, neutral
    impacto = Column(Text, nullable=True)      # alto, medio, bajo
    urgencia = Column(Text, nullable=True)     # alta, media, baja
    tema = Column(Text, nullable=True)         # tema principal de la llamada
    
    # Relaciones
    operator = relationship("Operator", back_populates="calls")
    client = relationship("Client", back_populates="calls")
    
    def __repr__(self):
        return f"<Call(call_id={self.call_id}, call_date='{self.call_date}', tema='{self.tema}')>"

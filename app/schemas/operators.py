from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class OperatorBase(BaseModel):
    """Esquema base para operadores"""
    name: str


class OperatorCreate(OperatorBase):
    """Esquema para crear operador"""
    pass


class OperatorUpdate(BaseModel):
    """Esquema para actualizar operador"""
    name: Optional[str] = None


class OperatorResponse(OperatorBase):
    """Esquema de respuesta para operador"""
    operator_id: int
    
    model_config = ConfigDict(from_attributes=True)


class OperatorList(BaseModel):
    """Esquema para lista de operadores"""
    operators: List[OperatorResponse]
    total: int
    page: int
    page_size: int

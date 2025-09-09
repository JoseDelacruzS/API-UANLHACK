from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List


class ClientBase(BaseModel):
    """Esquema base para clientes"""
    external_ref: str = Field(..., max_length=64, description="Referencia externa del cliente")


class ClientCreate(ClientBase):
    """Esquema para crear cliente"""
    pass


class ClientUpdate(BaseModel):
    """Esquema para actualizar cliente"""
    external_ref: Optional[str] = Field(None, max_length=64)


class ClientResponse(ClientBase):
    """Esquema de respuesta para cliente"""
    client_id: int
    
    model_config = ConfigDict(from_attributes=True)


class ClientList(BaseModel):
    """Esquema para lista de clientes"""
    clients: List[ClientResponse]
    total: int
    page: int
    page_size: int

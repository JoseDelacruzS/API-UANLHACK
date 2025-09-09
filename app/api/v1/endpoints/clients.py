from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_db, get_pagination_params

router = APIRouter()


@router.get("/", response_model=dict)
async def get_clients(
    pagination: dict = Depends(get_pagination_params),
    db: Session = Depends(get_current_db)
):
    """Obtener lista de clientes con paginación"""
    # Implementación básica - expandir según necesidades
    return {
        "clients": [],
        "total": 0,
        "page": pagination["page"],
        "page_size": pagination["page_size"]
    }


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_client(
    client_data: dict,
    db: Session = Depends(get_current_db)
):
    """Crear nuevo cliente"""
    return {"message": "Cliente creado", "client": client_data}

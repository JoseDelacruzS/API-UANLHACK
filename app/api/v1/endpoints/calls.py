from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_db

router = APIRouter()


@router.get("/", response_model=dict)
async def get_calls(db: Session = Depends(get_current_db)):
    """Obtener lista de llamadas"""
    return {"calls": [], "total": 0}


@router.post("/", response_model=dict)
async def create_call(call_data: dict, db: Session = Depends(get_current_db)):
    """Crear nueva llamada"""
    return {"message": "Llamada creada", "call": call_data}

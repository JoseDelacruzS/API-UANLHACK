from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_current_db

router = APIRouter()


@router.get("/", response_model=dict)
async def get_tickets(db: Session = Depends(get_current_db)):
    """Obtener lista de tickets"""
    return {"tickets": [], "total": 0}


@router.post("/", response_model=dict)
async def create_ticket(ticket_data: dict, db: Session = Depends(get_current_db)):
    """Crear nuevo ticket"""
    return {"message": "Ticket creado", "ticket": ticket_data}


@router.get("/stats", response_model=dict)
async def get_ticket_stats(db: Session = Depends(get_current_db)):
    """Obtener estadísticas de tickets"""
    return {
        "total_tickets": 0,
        "open_tickets": 0,
        "in_progress_tickets": 0,
        "resolved_tickets": 0,
        "closed_tickets": 0
    }

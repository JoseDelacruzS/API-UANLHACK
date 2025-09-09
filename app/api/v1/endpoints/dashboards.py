from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional
from app.api.deps import get_current_db

router = APIRouter()


@router.get("/metrics", response_model=dict)
async def get_dashboard_metrics(db: Session = Depends(get_current_db)):
    """Obtener métricas principales para dashboard"""
    return {
        "total_calls_today": 0,
        "total_tickets_open": 0,
        "total_operators_active": 0,
        "total_clients": 0,
        "ticket_resolution_rate": 0.0,
        "average_call_duration": 0.0
    }


@router.get("/charts/calls-by-date", response_model=dict)
async def get_calls_by_date_chart(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_current_db)
):
    """Datos para gráfico de llamadas por fecha"""
    return {
        "labels": [],
        "data": [],
        "chart_type": "line"
    }


@router.get("/charts/tickets-by-status", response_model=dict)
async def get_tickets_by_status_chart(db: Session = Depends(get_current_db)):
    """Datos para gráfico de tickets por estado"""
    return {
        "labels": ["Abierto", "En Progreso", "Resuelto", "Cerrado"],
        "data": [0, 0, 0, 0],
        "chart_type": "pie"
    }


@router.get("/charts/calls-by-operator", response_model=dict)
async def get_calls_by_operator_chart(db: Session = Depends(get_current_db)):
    """Datos para gráfico de llamadas por operador"""
    return {
        "labels": [],
        "data": [],
        "chart_type": "bar"
    }


@router.get("/real-time", response_model=dict)
async def get_real_time_data(db: Session = Depends(get_current_db)):
    """Datos en tiempo real para dashboard"""
    return {
        "active_calls": 0,
        "pending_tickets": 0,
        "operators_online": 0,
        "last_updated": datetime.now().isoformat()
    }

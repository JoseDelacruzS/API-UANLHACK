from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.api.deps import get_current_db
from app.schemas.tickets import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    TicketList,
    TicketStats,
    WatsonTicketRequest
)
from app.services.watson_service import WatsonService

router = APIRouter()
watson_service = WatsonService()


@router.post("/webhook", response_model=Dict[str, Any])
async def watson_webhook(
    request: WatsonTicketRequest,
    db: Session = Depends(get_current_db)
):
    """
    Webhook para recibir datos de Watson Orchestrate
    
    Este endpoint recibe solicitudes de Watson y puede:
    - Crear tickets automáticamente
    - Procesar conversaciones
    - Generar reportes
    - Enviar notificaciones
    """
    try:
        # Procesar la solicitud de Watson
        result = await watson_service.process_watson_request(request, db)
        
        return {
            "status": "success",
            "message": "Solicitud procesada correctamente",
            "ticket_created": result.get("ticket_created", False),
            "ticket_id": result.get("ticket_id"),
            "actions_taken": result.get("actions", [])
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando solicitud de Watson: {str(e)}"
        )


@router.get("/status")
async def watson_status():
    """Estado de la integración con Watson Orchestrate"""
    status_info = await watson_service.get_integration_status()
    
    return {
        "status": status_info.get("status", "unknown"),
        "last_connection": status_info.get("last_connection"),
        "version": status_info.get("version"),
        "endpoints_available": [
            "/api/v1/watson/webhook",
            "/api/v1/watson/status",
            "/api/v1/watson/sessions",
            "/api/v1/watson/test-connection"
        ]
    }


@router.get("/sessions")
async def get_watson_sessions(
    db: Session = Depends(get_current_db),
    limit: int = 50
):
    """Obtener sesiones recientes de Watson"""
    sessions = await watson_service.get_recent_sessions(db, limit)
    
    return {
        "sessions": sessions,
        "total": len(sessions)
    }


@router.post("/test-connection")
async def test_watson_connection():
    """Probar conexión con Watson Orchestrate"""
    try:
        result = await watson_service.test_connection()
        return {
            "status": "success" if result else "failed",
            "message": "Conexión exitosa" if result else "Error de conexión",
            "timestamp": result.get("timestamp") if result else None
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error probando conexión: {str(e)}"
        )


@router.post("/manual-ticket", response_model=TicketResponse)
async def create_manual_ticket_from_watson(
    ticket_data: TicketCreate,
    db: Session = Depends(get_current_db)
):
    """Crear ticket manualmente desde datos de Watson"""
    try:
        ticket = await watson_service.create_ticket_from_watson(ticket_data, db)
        return ticket
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creando ticket: {str(e)}"
        )

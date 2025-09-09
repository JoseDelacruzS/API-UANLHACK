from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from app.api.deps import get_current_db
from app.services.watson_service import WatsonService

router = APIRouter()
watson_service = WatsonService()


# Esquemas para Watson Orchestrate
class WatsonWebhookRequest(BaseModel):
    """Solicitud del webhook de Watson Orchestrate"""
    session_id: str = Field(..., description="ID de sesión de Watson")
    user_id: str = Field(..., description="ID del usuario")
    message: str = Field(..., description="Mensaje del usuario")
    intent: str = Field(None, description="Intención detectada")
    entities: Dict[str, Any] = Field(default_factory=dict, description="Entidades extraídas")
    context: Dict[str, Any] = Field(default_factory=dict, description="Contexto de la conversación")

# Modelos para OpenAPI simplificado (siguiendo patrón que funciona)
class CreateTicketRequest(BaseModel):
    title: str
    description: str
    priority: str = "medium"
    client_ref: str = "CLI-DEFAULT"

class ScheduleVisitRequest(BaseModel):
    client_ref: str
    visit_type: str
    preferred_date: str = None
    description: str = None

class GetStatusRequest(BaseModel):
    query_type: str
    entity_id: str = None

class SimpleResponse(BaseModel):
    success: bool
    message: str
    ticket_id: str = None
    visit_id: str = None
    status: str = None
    details: Dict[str, Any] = None
    timestamp: str = Field(..., description="Timestamp del mensaje")


class WatsonWebhookResponse(BaseModel):
    """Respuesta del webhook para Watson"""
    response: str = Field(..., description="Respuesta a enviar al usuario")
    actions: List[Dict[str, Any]] = Field(default_factory=list, description="Acciones realizadas")
    context_update: Dict[str, Any] = Field(default_factory=dict, description="Actualización del contexto")
    should_end_session: bool = Field(False, description="Si debe terminar la sesión")


@router.post("/webhook", response_model=WatsonWebhookResponse)
async def watson_webhook(
    request: WatsonWebhookRequest,
    raw_request: Request,
    db: Session = Depends(get_current_db)
):
    """
    🤖 Webhook principal para Watson Orchestrate
    
    Este endpoint recibe las solicitudes de Watson y procesa:
    - Creación automática de tickets
    - Programación de visitas
    - Consultas de estado
    - Generación de reportes
    
    Ejemplo de payload de Watson:
    ```json
    {
        "session_id": "session_123",
        "user_id": "user_456", 
        "message": "Necesito crear un ticket por un problema con el sistema",
        "intent": "crear_ticket",
        "entities": {
            "problema": "sistema no funciona",
            "prioridad": "alta"
        },
        "context": {
            "cliente_id": "CLI-001"
        },
        "timestamp": "2024-01-01T10:00:00Z"
    }
    ```
    """
    try:
        # Log de la solicitud
        print(f"📨 Webhook Watson recibido: {request.session_id}")
        
        # Procesar según la intención
        response_data = await watson_service.process_watson_webhook(request, db)
        
        return WatsonWebhookResponse(**response_data)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando webhook de Watson: {str(e)}"
        )


@router.get("/openapi-spec")
async def get_openapi_spec():
    """
    📋 Obtener especificación OpenAPI para Watson
    
    Watson puede consumir esta especificación para entender
    qué endpoints están disponibles y cómo usarlos.
    """
    from app.main import app
    
    # Filtrar solo endpoints relevantes para Watson
    openapi_spec = app.openapi()
    
    watson_spec = {
        "openapi": openapi_spec["openapi"],
        "info": {
            "title": "UANL API - Watson Integration",
            "version": "1.0.0",
            "description": "API endpoints disponibles para Watson Orchestrate"
        },
        "servers": [
            {"url": "http://localhost:8000", "description": "Desarrollo"},
            {"url": "https://api.uanl.mx", "description": "Producción"}
        ],
        "paths": {
            # Solo endpoints útiles para Watson
            "/api/v1/tickets/": openapi_spec["paths"].get("/api/v1/tickets/", {}),
            "/api/v1/watson/webhook": openapi_spec["paths"].get("/api/v1/watson/webhook", {}),
            "/api/v1/watson/actions": openapi_spec["paths"].get("/api/v1/watson/actions", {}),
            "/api/v1/dashboards/metrics": openapi_spec["paths"].get("/api/v1/dashboards/metrics", {}),
        },
        "components": openapi_spec.get("components", {})
    }
    
    return watson_spec


@router.post("/actions/{action_type}")
async def execute_watson_action(
    action_type: str,
    action_data: Dict[str, Any],
    db: Session = Depends(get_current_db)
):
    """
    ⚡ Ejecutar acciones específicas desde Watson
    
    Acciones disponibles:
    - create_ticket: Crear ticket
    - schedule_visit: Programar visita
    - send_notification: Enviar notificación
    - generate_report: Generar reporte
    - get_status: Obtener estado de un recurso
    """
    try:
        result = await watson_service.execute_action(action_type, action_data, db)
        return {
            "action": action_type,
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error ejecutando acción {action_type}: {str(e)}"
        )


@router.get("/status")
async def watson_integration_status():
    """📊 Estado de la integración con Watson Orchestrate"""
    return {
        "status": "active",
        "version": "1.0.0",
        "webhook_url": "/api/v1/watson/webhook",
        "openapi_url": "/api/v1/watson/openapi-spec",
        "supported_intents": [
            "crear_ticket",
            "programar_visita", 
            "consultar_estado",
            "generar_reporte",
            "enviar_notificacion"
        ],
        "supported_actions": [
            "create_ticket",
            "schedule_visit",
            "send_notification", 
            "generate_report",
            "get_status"
        ]
    }


@router.get("/test-connection")
async def test_watson_connection():
    """🔍 Probar conexión con Watson (simulado)"""
    return {
        "status": "connected",
        "timestamp": "2024-01-01T10:00:00Z",
        "response_time_ms": 150,
        "watson_version": "2023-09-01"
    }


# 🔌 Endpoints OpenAPI simplificados para Watson (siguiendo patrón que funciona)

@router.post("/create-ticket", response_model=SimpleResponse)
async def create_ticket_simple(
    request: CreateTicketRequest,
    db: Session = Depends(get_current_db)
) -> SimpleResponse:
    """✅ Crear ticket de soporte - Endpoint simplificado para Watson"""
    try:
        # Generar ID único para el ticket
        ticket_id = f"TKT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Simular creación de ticket
        return SimpleResponse(
            success=True,
            message=f"Ticket #{ticket_id} creado exitosamente: {request.title}",
            ticket_id=ticket_id
        )
    except Exception as e:
        return SimpleResponse(
            success=False,
            message=f"Error creando ticket: {str(e)}"
        )


@router.post("/schedule-visit", response_model=SimpleResponse)
async def schedule_visit_simple(
    request: ScheduleVisitRequest,
    db: Session = Depends(get_current_db)
) -> SimpleResponse:
    """📅 Programar visita técnica - Endpoint simplificado para Watson"""
    try:
        # Generar ID único para la visita
        visit_id = f"VIS-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return SimpleResponse(
            success=True,
            message=f"Visita #{visit_id} programada: {request.visit_type} para cliente {request.client_ref}",
            visit_id=visit_id
        )
    except Exception as e:
        return SimpleResponse(
            success=False,
            message=f"Error programando visita: {str(e)}"
        )


@router.post("/get-status", response_model=SimpleResponse)
async def get_status_simple(
    request: GetStatusRequest,
    db: Session = Depends(get_current_db)
) -> SimpleResponse:
    """📋 Consultar estado - Endpoint simplificado para Watson"""
    try:
        if request.entity_id:
            # Estado específico
            return SimpleResponse(
                success=True,
                message=f"Estado de {request.query_type} {request.entity_id}",
                status="open",
                details={
                    "type": request.query_type,
                    "id": request.entity_id,
                    "created": "2024-12-01",
                    "priority": "medium"
                }
            )
        else:
            # Estado general
            return SimpleResponse(
                success=True,
                message="Estado general del sistema",
                status="operational",
                details={
                    "open_tickets": 15,
                    "pending_visits": 8,
                    "active_reports": 3
                }
            )
    except Exception as e:
        return SimpleResponse(
            success=False,
            message=f"Error consultando estado: {str(e)}"
        )

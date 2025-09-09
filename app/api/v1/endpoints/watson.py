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

class ConversationAnalysisRequest(BaseModel):
    conversation: str
    operator_id: int
    client_ref: str
    call_date: str = None
    call_label: str = None

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


@router.post("/analyze-conversation")
async def analyze_conversation(
    request: ConversationAnalysisRequest,
    db: Session = Depends(get_current_db)
) -> Dict[str, Any]:
    """🧠 Analizar conversación telefónica y generar insights para Watson"""
    try:
        conversation_text = request.conversation
        
        # Análisis automático de la conversación
        analysis = {
            "call_analysis": {
                "problem_type": extract_problem_type(conversation_text),
                "urgency_level": extract_urgency(conversation_text),
                "customer_sentiment": analyze_sentiment(conversation_text),
                "resolution_status": extract_resolution_status(conversation_text),
                "follow_up_required": check_follow_up_needed(conversation_text)
            },
            "extracted_entities": extract_entities(conversation_text),
            "recommended_actions": generate_recommendations(conversation_text),
            "summary": generate_summary(conversation_text)
        }
        
        # Generar ID de llamada
        call_id = f"CALL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        return {
            "success": True,
            "call_id": call_id,
            "analysis": analysis,
            "message": "Conversación analizada exitosamente"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"Error analizando conversación: {str(e)}"
        }


# 🧠 Funciones de análisis de conversaciones
def extract_problem_type(conversation: str) -> str:
    """Extraer tipo de problema de la conversación"""
    conversation_lower = conversation.lower()
    
    if "lentitud" in conversation_lower or "lento" in conversation_lower:
        return "lentitud_servicio"
    elif "no funciona" in conversation_lower or "no conecta" in conversation_lower:
        return "falta_servicio"
    elif "intermitente" in conversation_lower:
        return "servicio_intermitente"
    elif "luz naranja" in conversation_lower or "indicador" in conversation_lower:
        return "problema_conectividad"
    else:
        return "problema_general"


def extract_urgency(conversation: str) -> str:
    """Determinar nivel de urgencia basado en contexto"""
    conversation_lower = conversation.lower()
    
    if "urgente" in conversation_lower or "inmediato" in conversation_lower:
        return "high"
    elif "varios aparatos" in conversation_lower or "trabajo" in conversation_lower:
        return "medium"
    elif "cuando pueda" in conversation_lower or "no hay prisa" in conversation_lower:
        return "low"
    else:
        return "medium"


def analyze_sentiment(conversation: str) -> str:
    """Analizar sentimiento del cliente"""
    conversation_lower = conversation.lower()
    
    negative_words = ["problema", "lento", "no funciona", "molesto", "frustrante"]
    positive_words = ["gracias", "muy bien", "perfecto", "excelente"]
    neutral_words = ["okay", "entiendo", "está bien"]
    
    negative_count = sum(1 for word in negative_words if word in conversation_lower)
    positive_count = sum(1 for word in positive_words if word in conversation_lower)
    neutral_count = sum(1 for word in neutral_words if word in conversation_lower)
    
    if negative_count > positive_count + neutral_count:
        return "frustrated"
    elif positive_count > negative_count:
        return "satisfied"
    else:
        return "neutral"


def extract_resolution_status(conversation: str) -> str:
    """Determinar estado de resolución"""
    conversation_lower = conversation.lower()
    
    if "ajuste" in conversation_lower and "realizó" in conversation_lower:
        return "potentially_resolved"
    elif "devuelvo la llamada" in conversation_lower or "callback" in conversation_lower:
        return "pending_verification"
    elif "técnico" in conversation_lower and "venir" in conversation_lower:
        return "requires_technician"
    else:
        return "unresolved"


def check_follow_up_needed(conversation: str) -> bool:
    """Verificar si se necesita seguimiento"""
    follow_up_indicators = [
        "devuelvo la llamada",
        "mañana temprano", 
        "en media hora",
        "revisar",
        "callback",
        "verificar"
    ]
    
    return any(indicator in conversation.lower() for indicator in follow_up_indicators)


def extract_entities(conversation: str) -> Dict[str, Any]:
    """Extraer entidades importantes de la conversación"""
    entities = {
        "tiempo_estimado": None,
        "hora_callback": None,
        "problema_especifico": None,
        "estado_servicio": None,
        "ajustes_realizados": False,
        "ubicacion_cliente": None
    }
    
    conversation_lower = conversation.lower()
    
    # Extraer tiempo estimado
    if "media hora" in conversation_lower:
        entities["tiempo_estimado"] = "30 minutos"
    elif "una hora" in conversation_lower:
        entities["tiempo_estimado"] = "60 minutos"
    
    # Extraer hora de callback
    if "nueve" in conversation_lower and "noche" in conversation_lower:
        entities["hora_callback"] = "21:00"
    elif "mañana temprano" in conversation_lower:
        entities["hora_callback"] = "08:00"
    
    # Extraer problema específico
    if "luz naranja" in conversation_lower:
        entities["problema_especifico"] = "indicador_conexion_baja"
        entities["estado_servicio"] = "degradado"
    
    # Verificar si se realizaron ajustes
    if "ajuste" in conversation_lower and "realizó" in conversation_lower:
        entities["ajustes_realizados"] = True
    
    # Extraer ubicación
    if "no estoy en mi casa" in conversation_lower:
        entities["ubicacion_cliente"] = "fuera_domicilio"
    elif "casa" in conversation_lower:
        entities["ubicacion_cliente"] = "domicilio"
    
    return entities


def generate_recommendations(conversation: str) -> List[str]:
    """Generar recomendaciones basadas en la conversación"""
    recommendations = []
    conversation_lower = conversation.lower()
    
    if "devuelvo la llamada" in conversation_lower:
        recommendations.append("programar_callback")
    
    if "ajuste" in conversation_lower and "realizó" in conversation_lower:
        recommendations.append("verificar_ajustes_realizados")
    
    if "luz naranja" in conversation_lower:
        recommendations.append("revisar_niveles_señal")
        recommendations.append("diagnostico_remoto")
    
    if "varios aparatos" in conversation_lower:
        recommendations.append("optimizar_ancho_banda")
    
    if "técnico" in conversation_lower:
        recommendations.append("programar_visita_tecnica")
    
    if "lentitud" in conversation_lower:
        recommendations.append("monitoreo_velocidad")
        recommendations.append("verificar_configuracion")
    
    return recommendations


def generate_summary(conversation: str) -> str:
    """Generar resumen inteligente de la conversación"""
    conversation_lower = conversation.lower()
    
    # Detectar elementos clave
    problem = "lentitud de servicio" if "lentitud" in conversation_lower else "problema técnico"
    action_taken = "ajustes realizados" if "ajuste" in conversation_lower else "diagnóstico inicial"
    next_step = "callback programado" if "devuelvo" in conversation_lower else "seguimiento requerido"
    
    return f"""
    📋 Resumen Automático:
    • Problema: {problem}
    • Acción realizada: {action_taken}
    • Estado: Pendiente de verificación
    • Próximo paso: {next_step}
    • Cliente: Cooperativo, disponible para seguimiento
    """.strip()


# ENDPOINTS PARA CONEXIÓN CON POSTGRESQL
from app.models.calls import Call
from app.models.operators import Operator
from app.models.clients import Client
from fastapi import Query

@router.get("/calls/recent")
async def get_recent_calls(
    limit: int = Query(10, ge=1, le=100, description="Número de llamadas a retornar"),
    operator_id: int = Query(None, description="Filtrar por operador"),
    has_analysis: bool = Query(None, description="Filtrar llamadas con/sin análisis"),
    db: Session = Depends(get_current_db)
):
    """
    Obtener llamadas recientes de PostgreSQL para que Watson pueda analizarlas.
    """
    try:
        query = db.query(Call).join(Operator).join(Client)
        
        if operator_id:
            query = query.filter(Call.operator_id == operator_id)
            
        if has_analysis is not None:
            if has_analysis:
                query = query.filter(Call.sentimiento.isnot(None))
            else:
                query = query.filter(Call.sentimiento.is_(None))
        
        calls = query.order_by(Call.call_date.desc(), Call.call_id.desc()).limit(limit).all()
        
        result = []
        for call in calls:
            result.append({
                "call_id": call.call_id,
                "call_label": call.call_label,
                "operator_name": call.operator.name,
                "client_ref": call.client.external_ref,
                "call_date": call.call_date.isoformat(),
                "conversation": call.conversation,
                "sentimiento": call.sentimiento,
                "impacto": call.impacto,
                "urgencia": call.urgencia,
                "tema": call.tema
            })
        
        return {
            "calls": result,
            "total": len(result),
            "source": "postgresql"
        }
        
    except Exception as e:
        # Si no hay conexión a DB, devolver datos de ejemplo
        return {
            "calls": [
                {
                    "call_id": 1,
                    "call_label": "Ejemplo - Sin conexión DB",
                    "operator_name": "Alex Cordero",
                    "client_ref": "62351432",
                    "call_date": "2025-03-03",
                    "conversation": "Conversación de ejemplo para demostración de Watson",
                    "sentimiento": "neutral",
                    "impacto": "medio",
                    "urgencia": "media",
                    "tema": "lentitud_servicio"
                }
            ],
            "total": 1,
            "source": "ejemplo",
            "error": str(e)
        }


@router.get("/calls/{call_id}")
async def get_call_detail(
    call_id: int,
    db: Session = Depends(get_current_db)
):
    """
    Obtener detalles de una llamada específica para análisis de Watson.
    """
    try:
        call = db.query(Call).join(Operator).join(Client).filter(Call.call_id == call_id).first()
        
        if not call:
            raise HTTPException(status_code=404, detail="Llamada no encontrada")
        
        return {
            "call_id": call.call_id,
            "call_label": call.call_label,
            "operator": {
                "operator_id": call.operator.operator_id,
                "name": call.operator.name
            },
            "client": {
                "client_id": call.client.client_id,
                "external_ref": call.client.external_ref
            },
            "call_date": call.call_date.isoformat(),
            "conversation": call.conversation,
            "analysis": {
                "sentimiento": call.sentimiento,
                "impacto": call.impacto,
                "urgencia": call.urgencia,
                "tema": call.tema
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener llamada: {str(e)}")


@router.put("/calls/{call_id}/analysis")
async def update_call_analysis(
    call_id: int,
    analysis: dict,
    db: Session = Depends(get_current_db)
):
    """
    Actualizar el análisis de una llamada. Watson puede usar esto para almacenar sus análisis.
    """
    try:
        call = db.query(Call).filter(Call.call_id == call_id).first()
        
        if not call:
            raise HTTPException(status_code=404, detail="Llamada no encontrada")
        
        # Actualizar campos de análisis
        if "sentimiento" in analysis:
            call.sentimiento = analysis["sentimiento"]
        if "impacto" in analysis:
            call.impacto = analysis["impacto"]
        if "urgencia" in analysis:
            call.urgencia = analysis["urgencia"]
        if "tema" in analysis:
            call.tema = analysis["tema"]
        
        db.commit()
        
        return {
            "message": "Análisis actualizado correctamente",
            "call_id": call_id,
            "updated_analysis": {
                "sentimiento": call.sentimiento,
                "impacto": call.impacto,
                "urgencia": call.urgencia,
                "tema": call.tema
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar análisis: {str(e)}")


@router.get("/analytics/dashboard")
async def get_analytics_dashboard(
    db: Session = Depends(get_current_db)
):
    """
    Obtener métricas y analytics para Watson Orchestrate dashboard.
    """
    try:
        from sqlalchemy import func
        
        # Estadísticas básicas
        total_calls = db.query(Call).count()
        calls_with_analysis = db.query(Call).filter(Call.sentimiento.isnot(None)).count()
        
        # Llamadas por sentimiento
        sentiment_stats = db.query(Call.sentimiento, func.count(Call.call_id)).filter(
            Call.sentimiento.isnot(None)
        ).group_by(Call.sentimiento).all()
        
        # Llamadas por urgencia
        urgency_stats = db.query(Call.urgencia, func.count(Call.call_id)).filter(
            Call.urgencia.isnot(None)
        ).group_by(Call.urgencia).all()
        
        # Llamadas por operador
        operator_stats = db.query(Operator.name, func.count(Call.call_id)).join(
            Call
        ).group_by(Operator.name).all()
        
        return {
            "total_calls": total_calls,
            "analyzed_calls": calls_with_analysis,
            "analysis_coverage": round((calls_with_analysis / total_calls * 100), 2) if total_calls > 0 else 0,
            "sentiment_distribution": {sentiment: count for sentiment, count in sentiment_stats},
            "urgency_distribution": {urgency: count for urgency, count in urgency_stats},
            "calls_by_operator": {operator: count for operator, count in operator_stats},
            "source": "postgresql"
        }
        
    except Exception as e:
        # Si no hay conexión a DB, devolver datos de ejemplo
        return {
            "total_calls": 15,
            "analyzed_calls": 12,
            "analysis_coverage": 80.0,
            "sentiment_distribution": {
                "positivo": 3,
                "neutral": 7,
                "negativo": 2
            },
            "urgency_distribution": {
                "alta": 2,
                "media": 8,
                "baja": 2
            },
            "calls_by_operator": {
                "Alex Cordero": 3,
                "Juan Islas": 2,
                "Sergio Torres": 2,
                "Karla Dasilva": 1,
                "Milton Rodriguez": 2,
                "Carlos Hernandez": 2,
                "Kenia Urban": 1,
                "Luis Carrillo": 1,
                "Pedro Torres": 1
            },
            "source": "ejemplo",
            "error": str(e)
        }

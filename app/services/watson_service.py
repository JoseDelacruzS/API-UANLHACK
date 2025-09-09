import httpx
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from loguru import logger

from app.config.settings import settings
from app.schemas.tickets import WatsonTicketRequest, TicketCreate
from app.models.tickets import Ticket
from app.models.clients import Client
from app.services.ticket_service import TicketService


class WatsonService:
    """Servicio para integración con Watson Orchestrate"""
    
    def __init__(self):
        self.api_key = settings.WATSON_API_KEY
        self.base_url = settings.WATSON_URL
        self.version = settings.WATSON_VERSION
        self.ticket_service = TicketService()
    
    async def process_watson_request(
        self, 
        request: WatsonTicketRequest, 
        db: Session
    ) -> Dict[str, Any]:
        """
        Procesar solicitud de Watson Orchestrate
        
        Args:
            request: Datos de la solicitud de Watson
            db: Sesión de base de datos
            
        Returns:
            Resultado del procesamiento
        """
        try:
            logger.info(f"Procesando solicitud de Watson: {request.session_id}")
            
            # Buscar o crear cliente
            client = await self._get_or_create_client(request.client_external_ref, db)
            
            # Analizar el input del usuario para determinar acción
            action = await self._analyze_user_input(request.user_input, request.context)
            
            result = {
                "session_id": request.session_id,
                "client_id": client.client_id,
                "action": action,
                "actions": []
            }
            
            # Ejecutar acciones según el análisis
            if action == "create_ticket":
                ticket = await self._create_ticket_from_request(request, client, db)
                result.update({
                    "ticket_created": True,
                    "ticket_id": ticket.ticket_id
                })
                result["actions"].append("ticket_created")
            
            elif action == "send_notification":
                await self._send_notification(request, client)
                result["actions"].append("notification_sent")
            
            elif action == "schedule_visit":
                visit_info = await self._schedule_visit(request, client, db)
                result.update({"visit_scheduled": visit_info})
                result["actions"].append("visit_scheduled")
            
            elif action == "generate_report":
                report = await self._generate_automated_report(request, client, db)
                result.update({"report_generated": report})
                result["actions"].append("report_generated")
            
            # Registrar actividad
            await self._log_watson_activity(request, result, db)
            
            return result
            
        except Exception as e:
            logger.error(f"Error procesando solicitud de Watson: {str(e)}")
            raise
    
    async def _get_or_create_client(
        self, 
        external_ref: str, 
        db: Session
    ) -> Client:
        """Obtener o crear cliente"""
        client = db.query(Client).filter(
            Client.external_ref == external_ref
        ).first()
        
        if not client:
            client = Client(external_ref=external_ref)
            db.add(client)
            db.commit()
            db.refresh(client)
            logger.info(f"Cliente creado: {external_ref}")
        
        return client
    
    async def _analyze_user_input(
        self, 
        user_input: str, 
        context: Dict[str, Any]
    ) -> str:
        """
        Analizar input del usuario para determinar acción requerida
        
        Esta función podría usar NLP o reglas simples para determinar
        qué acción tomar basándose en el input del usuario
        """
        input_lower = user_input.lower()
        
        # Palabras clave para crear ticket
        ticket_keywords = ["problema", "error", "falla", "ayuda", "soporte", "ticket"]
        if any(keyword in input_lower for keyword in ticket_keywords):
            return "create_ticket"
        
        # Palabras clave para notificaciones
        notification_keywords = ["notificar", "avisar", "enviar", "comunicar"]
        if any(keyword in input_lower for keyword in notification_keywords):
            return "send_notification"
        
        # Palabras clave para visitas
        visit_keywords = ["visita", "cita", "agendar", "programar"]
        if any(keyword in input_lower for keyword in visit_keywords):
            return "schedule_visit"
        
        # Palabras clave para reportes
        report_keywords = ["reporte", "informe", "analisis", "estadistica"]
        if any(keyword in input_lower for keyword in report_keywords):
            return "generate_report"
        
        # Acción por defecto
        return "create_ticket"
    
    async def _create_ticket_from_request(
        self, 
        request: WatsonTicketRequest, 
        client: Client, 
        db: Session
    ) -> Ticket:
        """Crear ticket basado en solicitud de Watson"""
        ticket_data = TicketCreate(
            title=f"Solicitud de Watson - {request.session_id[:8]}",
            description=request.user_input,
            client_id=client.client_id,
            watson_session_id=request.session_id,
            watson_metadata=request.metadata
        )
        
        return await self.ticket_service.create_ticket(ticket_data, db)
    
    async def _send_notification(
        self, 
        request: WatsonTicketRequest, 
        client: Client
    ):
        """Enviar notificación"""
        # Implementar lógica de notificaciones
        logger.info(f"Enviando notificación para cliente {client.external_ref}")
        # Aquí iría la integración con servicio de email/SMS
        pass
    
    async def _schedule_visit(
        self, 
        request: WatsonTicketRequest, 
        client: Client, 
        db: Session
    ) -> Dict[str, Any]:
        """Programar visita"""
        # Implementar lógica de programación de visitas
        logger.info(f"Programando visita para cliente {client.external_ref}")
        
        return {
            "client_id": client.client_id,
            "scheduled_date": "TBD",
            "visit_type": "maintenance",
            "status": "scheduled"
        }
    
    async def _generate_automated_report(
        self, 
        request: WatsonTicketRequest, 
        client: Client, 
        db: Session
    ) -> Dict[str, Any]:
        """Generar reporte automático"""
        # Implementar generación de reportes
        logger.info(f"Generando reporte para cliente {client.external_ref}")
        
        return {
            "report_id": f"RPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "client_id": client.client_id,
            "type": "automated",
            "generated_at": datetime.now().isoformat()
        }
    
    async def _log_watson_activity(
        self, 
        request: WatsonTicketRequest, 
        result: Dict[str, Any], 
        db: Session
    ):
        """Registrar actividad de Watson"""
        # Implementar logging de actividades
        logger.info(f"Actividad Watson registrada: {request.session_id}")
        pass
    
    async def get_integration_status(self) -> Dict[str, Any]:
        """Obtener estado de la integración"""
        return {
            "status": "active" if self.api_key else "inactive",
            "version": self.version,
            "last_connection": datetime.now().isoformat(),
            "endpoints": 4
        }
    
    async def get_recent_sessions(
        self, 
        db: Session, 
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Obtener sesiones recientes de Watson"""
        # Consultar tickets con watson_session_id
        tickets = db.query(Ticket).filter(
            Ticket.watson_session_id.isnot(None)
        ).order_by(Ticket.created_at.desc()).limit(limit).all()
        
        sessions = []
        for ticket in tickets:
            sessions.append({
                "session_id": ticket.watson_session_id,
                "ticket_id": ticket.ticket_id,
                "created_at": ticket.created_at.isoformat(),
                "status": ticket.status.value,
                "client_id": ticket.client_id
            })
        
        return sessions
    
    async def test_connection(self) -> Optional[Dict[str, Any]]:
        """Probar conexión con Watson"""
        if not self.api_key or not self.base_url:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/health",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    return {
                        "status": "success",
                        "timestamp": datetime.now().isoformat(),
                        "response_time": response.elapsed.total_seconds()
                    }
                
        except Exception as e:
            logger.error(f"Error probando conexión Watson: {str(e)}")
        
        return None
    
    async def create_ticket_from_watson(
        self, 
        ticket_data: TicketCreate, 
        db: Session
    ) -> Ticket:
        """Crear ticket desde Watson manualmente"""
        return await self.ticket_service.create_ticket(ticket_data, db)

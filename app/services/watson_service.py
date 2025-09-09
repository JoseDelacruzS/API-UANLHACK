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
    
    async def process_watson_webhook(
        self, 
        request, # WatsonWebhookRequest
        db: Session
    ) -> Dict[str, Any]:
        """
        🤖 Procesar webhook de Watson Orchestrate
        
        Maneja diferentes tipos de intenciones:
        - crear_ticket: Crear un nuevo ticket
        - programar_visita: Programar una visita técnica
        - consultar_estado: Consultar estado de tickets/visitas
        - generar_reporte: Generar reportes automáticos
        - enviar_notificacion: Enviar notificaciones
        """
        try:
            logger.info(f"🔄 Procesando webhook Watson: {request.session_id}")
            
            # Analizar intención y entidades
            intent = request.intent or await self._detect_intent(request.message)
            entities = request.entities or await self._extract_entities(request.message)
            
            # Inicializar respuesta
            response_data = {
                "response": "",
                "actions": [],
                "context_update": {},
                "should_end_session": False
            }
            
            # Procesar según la intención
            if intent == "crear_ticket":
                result = await self._handle_create_ticket_intent(request, entities, db)
                response_data.update(result)
                
            elif intent == "programar_visita":
                result = await self._handle_schedule_visit_intent(request, entities, db)
                response_data.update(result)
                
            elif intent == "consultar_estado":
                result = await self._handle_status_inquiry_intent(request, entities, db)
                response_data.update(result)
                
            elif intent == "generar_reporte":
                result = await self._handle_generate_report_intent(request, entities, db)
                response_data.update(result)
                
            elif intent == "enviar_notificacion":
                result = await self._handle_send_notification_intent(request, entities, db)
                response_data.update(result)
                
            else:
                # Intención no reconocida
                response_data["response"] = (
                    "🤔 No estoy seguro de cómo ayudarte con eso. "
                    "Puedo ayudarte a:\n"
                    "• Crear tickets de soporte\n"
                    "• Programar visitas técnicas\n" 
                    "• Consultar el estado de tickets\n"
                    "• Generar reportes\n"
                    "• Enviar notificaciones"
                )
            
            # Registrar actividad
            await self._log_watson_activity(request, response_data, db)
            
            return response_data
            
        except Exception as e:
            logger.error(f"❌ Error procesando webhook Watson: {str(e)}")
            return {
                "response": "❌ Lo siento, ocurrió un error procesando tu solicitud. Por favor intenta de nuevo.",
                "actions": [],
                "context_update": {"error": str(e)},
                "should_end_session": False
            }
    
    async def _handle_create_ticket_intent(
        self, 
        request, 
        entities: Dict[str, Any], 
        db: Session
    ) -> Dict[str, Any]:
        """🎫 Manejar intención de crear ticket"""
        try:
            # Extraer información del ticket
            problema = entities.get("problema", request.message)
            prioridad = entities.get("prioridad", "medium")
            cliente_ref = request.context.get("cliente_id") or entities.get("cliente_id", "CLI-DEFAULT")
            
            # Buscar o crear cliente
            client = await self._get_or_create_client(cliente_ref, db)
            
            # Crear ticket
            ticket_data = TicketCreate(
                title=f"Solicitud desde Watson - {request.session_id[:8]}",
                description=problema,
                priority=self._map_priority(prioridad),
                client_id=client.client_id,
                watson_session_id=request.session_id,
                watson_metadata={"user_id": request.user_id, "entities": entities}
            )
            
            ticket = await self.ticket_service.create_ticket(ticket_data, db)
            
            return {
                "response": f"✅ He creado el ticket #{ticket.ticket_id} para tu problema: '{problema}'. Te notificaré cuando haya actualizaciones.",
                "actions": [
                    {
                        "type": "ticket_created",
                        "ticket_id": ticket.ticket_id,
                        "priority": ticket.priority.value
                    }
                ],
                "context_update": {
                    "last_ticket_id": ticket.ticket_id,
                    "action_completed": "ticket_created"
                }
            }
            
        except Exception as e:
            logger.error(f"Error creando ticket desde Watson: {str(e)}")
            return {
                "response": "❌ No pude crear el ticket. Por favor proporciona más detalles sobre el problema.",
                "actions": [],
                "context_update": {"error": "ticket_creation_failed"}
            }
    
    async def _handle_schedule_visit_intent(
        self, 
        request, 
        entities: Dict[str, Any], 
        db: Session
    ) -> Dict[str, Any]:
        """📅 Manejar intención de programar visita"""
        try:
            fecha = entities.get("fecha", "próxima semana")
            tipo_visita = entities.get("tipo", "mantenimiento")
            cliente_ref = request.context.get("cliente_id") or entities.get("cliente_id", "CLI-DEFAULT")
            
            # Simular programación de visita
            visit_info = {
                "visit_id": f"VIS-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "client_ref": cliente_ref,
                "scheduled_date": fecha,
                "visit_type": tipo_visita,
                "status": "programada"
            }
            
            return {
                "response": f"📅 He programado una visita de {tipo_visita} para {fecha}. Recibirás una confirmación por email con los detalles.",
                "actions": [
                    {
                        "type": "visit_scheduled",
                        "visit_id": visit_info["visit_id"],
                        "date": fecha
                    }
                ],
                "context_update": {
                    "last_visit_id": visit_info["visit_id"],
                    "action_completed": "visit_scheduled"
                }
            }
            
        except Exception as e:
            logger.error(f"Error programando visita desde Watson: {str(e)}")
            return {
                "response": "❌ No pude programar la visita. ¿Podrías especificar la fecha y tipo de visita?",
                "actions": [],
                "context_update": {"error": "visit_scheduling_failed"}
            }
    
    async def _handle_status_inquiry_intent(
        self, 
        request, 
        entities: Dict[str, Any], 
        db: Session
    ) -> Dict[str, Any]:
        """📊 Manejar consulta de estado"""
        try:
            ticket_id = entities.get("ticket_id") or request.context.get("last_ticket_id")
            
            if ticket_id:
                # Buscar ticket específico
                ticket = await self.ticket_service.get_ticket_by_id(ticket_id, db)
                if ticket:
                    return {
                        "response": f"📋 Estado del ticket #{ticket_id}:\n• Estado: {ticket.status.value}\n• Prioridad: {ticket.priority.value}\n• Creado: {ticket.created_at.strftime('%d/%m/%Y %H:%M')}",
                        "actions": [
                            {
                                "type": "status_provided",
                                "ticket_id": ticket_id,
                                "status": ticket.status.value
                            }
                        ],
                        "context_update": {"last_queried_ticket": ticket_id}
                    }
            
            # Estado general si no hay ticket específico
            stats = await self.ticket_service.get_ticket_stats(db)
            return {
                "response": f"📊 Estado general:\n• Tickets abiertos: {stats['open_tickets']}\n• En progreso: {stats['in_progress_tickets']}\n• Resueltos hoy: {stats['resolved_tickets']}",
                "actions": [
                    {
                        "type": "general_status_provided",
                        "stats": stats
                    }
                ],
                "context_update": {"last_action": "status_inquiry"}
            }
            
        except Exception as e:
            logger.error(f"Error consultando estado desde Watson: {str(e)}")
            return {
                "response": "❌ No pude obtener la información de estado. ¿Podrías especificar un número de ticket?",
                "actions": [],
                "context_update": {"error": "status_inquiry_failed"}
            }
    
    async def _handle_generate_report_intent(
        self, 
        request, 
        entities: Dict[str, Any], 
        db: Session
    ) -> Dict[str, Any]:
        """📈 Manejar generación de reportes"""
        try:
            tipo_reporte = entities.get("tipo", "general")
            periodo = entities.get("periodo", "semanal")
            
            # Simular generación de reporte
            report_id = f"RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            return {
                "response": f"📊 Generando reporte {tipo_reporte} {periodo}... Te enviaré el reporte #{report_id} por email cuando esté listo.",
                "actions": [
                    {
                        "type": "report_generated",
                        "report_id": report_id,
                        "type": tipo_reporte,
                        "period": periodo
                    }
                ],
                "context_update": {
                    "last_report_id": report_id,
                    "action_completed": "report_generated"
                }
            }
            
        except Exception as e:
            logger.error(f"Error generando reporte desde Watson: {str(e)}")
            return {
                "response": "❌ No pude generar el reporte. ¿Podrías especificar qué tipo de reporte necesitas?",
                "actions": [],
                "context_update": {"error": "report_generation_failed"}
            }
    
    async def _handle_send_notification_intent(
        self, 
        request, 
        entities: Dict[str, Any], 
        db: Session
    ) -> Dict[str, Any]:
        """📧 Manejar envío de notificaciones"""
        try:
            mensaje = entities.get("mensaje", request.message)
            destinatario = entities.get("destinatario", "equipo")
            
            # Simular envío de notificación
            notification_id = f"NOT-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            return {
                "response": f"📧 He enviado la notificación #{notification_id} a {destinatario}: '{mensaje}'",
                "actions": [
                    {
                        "type": "notification_sent",
                        "notification_id": notification_id,
                        "recipient": destinatario,
                        "message": mensaje
                    }
                ],
                "context_update": {
                    "last_notification_id": notification_id,
                    "action_completed": "notification_sent"
                }
            }
            
        except Exception as e:
            logger.error(f"Error enviando notificación desde Watson: {str(e)}")
            return {
                "response": "❌ No pude enviar la notificación. ¿Podrías especificar el mensaje y destinatario?",
                "actions": [],
                "context_update": {"error": "notification_failed"}
            }
    
    async def execute_action(
        self, 
        action_type: str, 
        action_data: Dict[str, Any], 
        db: Session
    ) -> Dict[str, Any]:
        """⚡ Ejecutar acción específica (para API calls directas)"""
        try:
            if action_type == "create_ticket":
                return await self._execute_create_ticket_action(action_data, db)
            elif action_type == "schedule_visit":
                return await self._execute_schedule_visit_action(action_data, db)
            elif action_type == "send_notification":
                return await self._execute_send_notification_action(action_data, db)
            elif action_type == "generate_report":
                return await self._execute_generate_report_action(action_data, db)
            elif action_type == "get_status":
                return await self._execute_get_status_action(action_data, db)
            else:
                raise ValueError(f"Acción no soportada: {action_type}")
                
        except Exception as e:
            logger.error(f"Error ejecutando acción {action_type}: {str(e)}")
            raise
    
    async def _detect_intent(self, message: str) -> str:
        """🧠 Detectar intención usando NLP básico"""
        message_lower = message.lower()
        
        # Palabras clave para diferentes intenciones
        intent_keywords = {
            "crear_ticket": ["problema", "error", "falla", "ayuda", "soporte", "ticket", "incidencia"],
            "programar_visita": ["visita", "cita", "agendar", "programar", "técnico", "revisar"],
            "consultar_estado": ["estado", "status", "cómo va", "avance", "progreso", "información"],
            "generar_reporte": ["reporte", "informe", "análisis", "estadística", "resumen"],
            "enviar_notificacion": ["notificar", "avisar", "comunicar", "enviar", "mensaje"]
        }
        
        # Buscar coincidencias
        for intent, keywords in intent_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        
        return "unknown"
    
    async def _extract_entities(self, message: str) -> Dict[str, Any]:
        """🔍 Extraer entidades usando NLP básico"""
        entities = {}
        message_lower = message.lower()
        
        # Extraer prioridad
        if any(word in message_lower for word in ["urgente", "crítico", "inmediato"]):
            entities["prioridad"] = "high"
        elif any(word in message_lower for word in ["normal", "medio"]):
            entities["prioridad"] = "medium"
        elif any(word in message_lower for word in ["bajo", "baja"]):
            entities["prioridad"] = "low"
        
        # Extraer tipo de problema
        if any(word in message_lower for word in ["sistema", "aplicación", "software"]):
            entities["tipo"] = "sistema"
        elif any(word in message_lower for word in ["red", "internet", "conexión"]):
            entities["tipo"] = "red"
        elif any(word in message_lower for word in ["hardware", "equipo", "computadora"]):
            entities["tipo"] = "hardware"
        
        # El problema es el mensaje completo (simplificado)
        entities["problema"] = message
        
        return entities
    
    async def _map_priority(self, priority_str: str) -> TicketPriority:
        """🎯 Mapear string de prioridad a enum"""
        priority_map = {
            "low": TicketPriority.LOW,
            "medium": TicketPriority.MEDIUM,
            "high": TicketPriority.HIGH,
            "urgent": TicketPriority.URGENT
        }
        return priority_map.get(priority_str.lower(), TicketPriority.MEDIUM)
    
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

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from loguru import logger

from app.models.tickets import Ticket, TicketStatus, TicketPriority
from app.models.clients import Client
from app.models.operators import Operator
from app.schemas.tickets import TicketCreate, TicketUpdate


class TicketService:
    """Servicio para gestión de tickets"""
    
    async def create_ticket(
        self, 
        ticket_data: TicketCreate, 
        db: Session
    ) -> Ticket:
        """Crear nuevo ticket"""
        try:
            # Crear ticket
            ticket = Ticket(
                title=ticket_data.title,
                description=ticket_data.description,
                priority=ticket_data.priority,
                client_id=ticket_data.client_id,
                call_id=ticket_data.call_id,
                assigned_operator_id=ticket_data.assigned_operator_id,
                watson_session_id=ticket_data.watson_session_id,
                watson_metadata=str(ticket_data.watson_metadata) if ticket_data.watson_metadata else None
            )
            
            db.add(ticket)
            db.commit()
            db.refresh(ticket)
            
            logger.info(f"Ticket creado: {ticket.ticket_id}")
            
            # Enviar notificaciones si es necesario
            await self._send_ticket_notifications(ticket, db)
            
            return ticket
            
        except Exception as e:
            logger.error(f"Error creando ticket: {str(e)}")
            db.rollback()
            raise
    
    async def update_ticket(
        self, 
        ticket_id: int, 
        ticket_data: TicketUpdate, 
        db: Session
    ) -> Optional[Ticket]:
        """Actualizar ticket"""
        try:
            ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
            
            if not ticket:
                return None
            
            # Actualizar campos
            for field, value in ticket_data.model_dump(exclude_unset=True).items():
                setattr(ticket, field, value)
            
            # Si se marca como resuelto, agregar timestamp
            if ticket_data.status == TicketStatus.RESOLVED and not ticket.resolved_at:
                ticket.resolved_at = datetime.now()
            
            db.commit()
            db.refresh(ticket)
            
            logger.info(f"Ticket actualizado: {ticket.ticket_id}")
            
            return ticket
            
        except Exception as e:
            logger.error(f"Error actualizando ticket: {str(e)}")
            db.rollback()
            raise
    
    async def get_ticket_by_id(
        self, 
        ticket_id: int, 
        db: Session
    ) -> Optional[Ticket]:
        """Obtener ticket por ID"""
        return db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()
    
    async def get_tickets_list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        status: Optional[TicketStatus] = None,
        priority: Optional[TicketPriority] = None,
        client_id: Optional[int] = None,
        assigned_operator_id: Optional[int] = None
    ) -> List[Ticket]:
        """Obtener lista de tickets con filtros"""
        query = db.query(Ticket)
        
        # Aplicar filtros
        if status:
            query = query.filter(Ticket.status == status)
        
        if priority:
            query = query.filter(Ticket.priority == priority)
        
        if client_id:
            query = query.filter(Ticket.client_id == client_id)
        
        if assigned_operator_id:
            query = query.filter(Ticket.assigned_operator_id == assigned_operator_id)
        
        return query.order_by(Ticket.created_at.desc()).offset(skip).limit(limit).all()
    
    async def get_ticket_stats(self, db: Session) -> Dict[str, Any]:
        """Obtener estadísticas de tickets"""
        total_tickets = db.query(Ticket).count()
        open_tickets = db.query(Ticket).filter(Ticket.status == TicketStatus.OPEN).count()
        in_progress_tickets = db.query(Ticket).filter(
            Ticket.status == TicketStatus.IN_PROGRESS
        ).count()
        resolved_tickets = db.query(Ticket).filter(
            Ticket.status == TicketStatus.RESOLVED
        ).count()
        closed_tickets = db.query(Ticket).filter(Ticket.status == TicketStatus.CLOSED).count()
        
        # Estadísticas por prioridad
        priorities = db.query(Ticket.priority, db.func.count(Ticket.ticket_id)).group_by(
            Ticket.priority
        ).all()
        
        tickets_by_priority = {priority.value: count for priority, count in priorities}
        
        # Estadísticas por operador
        operators = db.query(
            Operator.name, 
            db.func.count(Ticket.ticket_id)
        ).join(
            Ticket, Ticket.assigned_operator_id == Operator.operator_id, isouter=True
        ).group_by(Operator.name).all()
        
        tickets_by_operator = {name: count for name, count in operators}
        
        return {
            "total_tickets": total_tickets,
            "open_tickets": open_tickets,
            "in_progress_tickets": in_progress_tickets,
            "resolved_tickets": resolved_tickets,
            "closed_tickets": closed_tickets,
            "tickets_by_priority": tickets_by_priority,
            "tickets_by_operator": tickets_by_operator
        }
    
    async def auto_assign_ticket(
        self, 
        ticket_id: int, 
        db: Session
    ) -> Optional[Ticket]:
        """Asignar automáticamente ticket a operador disponible"""
        try:
            ticket = await self.get_ticket_by_id(ticket_id, db)
            if not ticket or ticket.assigned_operator_id:
                return ticket
            
            # Lógica de asignación automática
            # Por ejemplo, asignar al operador con menos tickets activos
            operator = db.query(Operator).join(
                Ticket, 
                and_(
                    Ticket.assigned_operator_id == Operator.operator_id,
                    Ticket.status.in_([TicketStatus.OPEN, TicketStatus.IN_PROGRESS])
                ),
                isouter=True
            ).group_by(Operator.operator_id).order_by(
                db.func.count(Ticket.ticket_id)
            ).first()
            
            if operator:
                ticket.assigned_operator_id = operator.operator_id
                db.commit()
                db.refresh(ticket)
                
                logger.info(f"Ticket {ticket_id} asignado automáticamente a {operator.name}")
            
            return ticket
            
        except Exception as e:
            logger.error(f"Error en asignación automática: {str(e)}")
            raise
    
    async def _send_ticket_notifications(
        self, 
        ticket: Ticket, 
        db: Session
    ):
        """Enviar notificaciones de ticket"""
        # Implementar notificaciones por email/SMS
        logger.info(f"Enviando notificaciones para ticket {ticket.ticket_id}")
        
        # Aquí iría la lógica de envío de emails, SMS, etc.
        # Por ejemplo:
        # - Notificar al cliente que se creó el ticket
        # - Notificar al operador asignado
        # - Notificar a supervisores si es prioridad alta
        
        pass
    
    async def escalate_ticket(
        self, 
        ticket_id: int, 
        reason: str, 
        db: Session
    ) -> Optional[Ticket]:
        """Escalar ticket a prioridad mayor"""
        try:
            ticket = await self.get_ticket_by_id(ticket_id, db)
            if not ticket:
                return None
            
            # Aumentar prioridad
            if ticket.priority == TicketPriority.LOW:
                ticket.priority = TicketPriority.MEDIUM
            elif ticket.priority == TicketPriority.MEDIUM:
                ticket.priority = TicketPriority.HIGH
            elif ticket.priority == TicketPriority.HIGH:
                ticket.priority = TicketPriority.URGENT
            
            # Agregar nota de escalación
            if ticket.description:
                ticket.description += f"\n\n[ESCALADO] {reason} - {datetime.now().isoformat()}"
            else:
                ticket.description = f"[ESCALADO] {reason} - {datetime.now().isoformat()}"
            
            db.commit()
            db.refresh(ticket)
            
            logger.info(f"Ticket {ticket_id} escalado a {ticket.priority.value}")
            
            return ticket
            
        except Exception as e:
            logger.error(f"Error escalando ticket: {str(e)}")
            raise

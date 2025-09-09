from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from loguru import logger

from app.models.calls import Call
from app.models.tickets import Ticket, TicketStatus
from app.models.operators import Operator
from app.models.clients import Client


class DashboardService:
    """Servicio para datos de dashboard"""
    
    async def get_main_metrics(self, db: Session) -> Dict[str, Any]:
        """Obtener métricas principales"""
        today = datetime.now().date()
        
        # Métricas básicas
        total_calls_today = db.query(Call).filter(Call.call_date == today).count()
        total_tickets_open = db.query(Ticket).filter(
            Ticket.status.in_([TicketStatus.OPEN, TicketStatus.IN_PROGRESS])
        ).count()
        total_operators_active = db.query(Operator).count()
        total_clients = db.query(Client).count()
        
        # Tasa de resolución de tickets
        total_tickets = db.query(Ticket).count()
        resolved_tickets = db.query(Ticket).filter(
            Ticket.status == TicketStatus.RESOLVED
        ).count()
        
        resolution_rate = (resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0
        
        # Duración promedio de llamadas
        avg_duration = db.query(func.avg(Call.duration_seconds)).filter(
            Call.duration_seconds.isnot(None)
        ).scalar() or 0
        
        return {
            "total_calls_today": total_calls_today,
            "total_tickets_open": total_tickets_open,
            "total_operators_active": total_operators_active,
            "total_clients": total_clients,
            "ticket_resolution_rate": round(resolution_rate, 2),
            "average_call_duration": round(avg_duration, 2)
        }
    
    async def get_calls_by_date_chart(
        self, 
        db: Session, 
        days: int = 30
    ) -> Dict[str, Any]:
        """Datos para gráfico de llamadas por fecha"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Consultar llamadas por fecha
        calls_data = db.query(
            Call.call_date,
            func.count(Call.call_id).label('count')
        ).filter(
            and_(
                Call.call_date >= start_date,
                Call.call_date <= end_date
            )
        ).group_by(Call.call_date).order_by(Call.call_date).all()
        
        # Generar todas las fechas en el rango
        all_dates = []
        current_date = start_date
        while current_date <= end_date:
            all_dates.append(current_date)
            current_date += timedelta(days=1)
        
        # Crear diccionario de datos
        calls_dict = {date: count for date, count in calls_data}
        
        labels = [date.strftime('%Y-%m-%d') for date in all_dates]
        data = [calls_dict.get(date, 0) for date in all_dates]
        
        return {
            "labels": labels,
            "data": data,
            "chart_type": "line",
            "title": f"Llamadas de los últimos {days} días"
        }
    
    async def get_tickets_by_status_chart(self, db: Session) -> Dict[str, Any]:
        """Datos para gráfico de tickets por estado"""
        tickets_data = db.query(
            Ticket.status,
            func.count(Ticket.ticket_id).label('count')
        ).group_by(Ticket.status).all()
        
        status_labels = {
            TicketStatus.OPEN: "Abierto",
            TicketStatus.IN_PROGRESS: "En Progreso", 
            TicketStatus.RESOLVED: "Resuelto",
            TicketStatus.CLOSED: "Cerrado"
        }
        
        labels = []
        data = []
        colors = []
        
        color_map = {
            TicketStatus.OPEN: "#ff6b6b",
            TicketStatus.IN_PROGRESS: "#ffd93d",
            TicketStatus.RESOLVED: "#6bcf7f",
            TicketStatus.CLOSED: "#4ecdc4"
        }
        
        for status, count in tickets_data:
            labels.append(status_labels.get(status, status.value))
            data.append(count)
            colors.append(color_map.get(status, "#95a5a6"))
        
        return {
            "labels": labels,
            "data": data,
            "colors": colors,
            "chart_type": "doughnut",
            "title": "Distribución de Tickets por Estado"
        }
    
    async def get_calls_by_operator_chart(self, db: Session) -> Dict[str, Any]:
        """Datos para gráfico de llamadas por operador"""
        calls_data = db.query(
            Operator.name,
            func.count(Call.call_id).label('count')
        ).join(
            Call, Call.operator_id == Operator.operator_id
        ).group_by(Operator.name).order_by(
            func.count(Call.call_id).desc()
        ).all()
        
        labels = [name for name, count in calls_data]
        data = [count for name, count in calls_data]
        
        return {
            "labels": labels,
            "data": data,
            "chart_type": "bar",
            "title": "Llamadas por Operador"
        }
    
    async def get_real_time_data(self, db: Session) -> Dict[str, Any]:
        """Datos en tiempo real para dashboard"""
        now = datetime.now()
        today = now.date()
        
        # Llamadas activas (simulado - en implementación real sería desde sistema telefónico)
        active_calls = 0
        
        # Tickets pendientes
        pending_tickets = db.query(Ticket).filter(
            Ticket.status.in_([TicketStatus.OPEN, TicketStatus.IN_PROGRESS])
        ).count()
        
        # Operadores online (simulado)
        operators_online = db.query(Operator).count()
        
        # Llamadas de hoy
        calls_today = db.query(Call).filter(Call.call_date == today).count()
        
        # Tickets creados hoy
        tickets_today = db.query(Ticket).filter(
            func.date(Ticket.created_at) == today
        ).count()
        
        return {
            "active_calls": active_calls,
            "pending_tickets": pending_tickets,
            "operators_online": operators_online,
            "calls_today": calls_today,
            "tickets_today": tickets_today,
            "last_updated": now.isoformat()
        }
    
    async def get_performance_summary(
        self, 
        db: Session, 
        period_days: int = 7
    ) -> Dict[str, Any]:
        """Resumen de rendimiento"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=period_days)
        
        # Llamadas en el período
        calls_period = db.query(Call).filter(
            and_(
                Call.call_date >= start_date,
                Call.call_date <= end_date
            )
        ).count()
        
        # Tickets en el período
        tickets_period = db.query(Ticket).filter(
            and_(
                func.date(Ticket.created_at) >= start_date,
                func.date(Ticket.created_at) <= end_date
            )
        ).count()
        
        # Tickets resueltos en el período
        resolved_period = db.query(Ticket).filter(
            and_(
                func.date(Ticket.resolved_at) >= start_date,
                func.date(Ticket.resolved_at) <= end_date
            )
        ).count()
        
        # Tiempo promedio de resolución
        resolved_tickets = db.query(Ticket).filter(
            and_(
                Ticket.resolved_at.isnot(None),
                func.date(Ticket.resolved_at) >= start_date,
                func.date(Ticket.resolved_at) <= end_date
            )
        ).all()
        
        if resolved_tickets:
            resolution_times = []
            for ticket in resolved_tickets:
                if ticket.resolved_at and ticket.created_at:
                    delta = ticket.resolved_at - ticket.created_at
                    resolution_times.append(delta.total_seconds() / 3600)  # Horas
            
            avg_resolution_time = sum(resolution_times) / len(resolution_times)
        else:
            avg_resolution_time = 0
        
        return {
            "period_days": period_days,
            "calls_period": calls_period,
            "tickets_period": tickets_period,
            "resolved_period": resolved_period,
            "resolution_rate": (resolved_period / tickets_period * 100) if tickets_period > 0 else 0,
            "avg_resolution_time_hours": round(avg_resolution_time, 2),
            "daily_average_calls": round(calls_period / period_days, 1),
            "daily_average_tickets": round(tickets_period / period_days, 1)
        }

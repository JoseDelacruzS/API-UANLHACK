import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
from jinja2 import Template
from loguru import logger
from app.config.settings import settings


class EmailService:
    """Servicio de envío de emails"""
    
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM
    
    async def send_email(
        self,
        to_emails: List[str],
        subject: str,
        body: str,
        is_html: bool = False,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """Enviar email"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_from
            msg['To'] = ", ".join(to_emails)
            msg['Subject'] = subject
            
            if cc_emails:
                msg['Cc'] = ", ".join(cc_emails)
            
            # Agregar cuerpo del mensaje
            msg.attach(MIMEText(body, 'html' if is_html else 'plain', 'utf-8'))
            
            # Agregar archivos adjuntos
            if attachments:
                for file_path in attachments:
                    await self._attach_file(msg, file_path)
            
            # Enviar email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                
                all_recipients = to_emails + (cc_emails or []) + (bcc_emails or [])
                server.send_message(msg, to_addrs=all_recipients)
            
            logger.info(f"Email enviado exitosamente a {to_emails}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando email: {str(e)}")
            return False
    
    async def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """Adjuntar archivo al email"""
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {file_path.split("/")[-1]}'
            )
            msg.attach(part)
            
        except Exception as e:
            logger.error(f"Error adjuntando archivo {file_path}: {str(e)}")
    
    async def send_ticket_notification(
        self,
        ticket_data: Dict[str, Any],
        recipient_email: str,
        template_type: str = "ticket_created"
    ) -> bool:
        """Enviar notificación de ticket"""
        templates = {
            "ticket_created": {
                "subject": "Nuevo Ticket Creado - #{ticket_id}",
                "body": """
                <h2>Nuevo Ticket Creado</h2>
                <p><strong>Ticket ID:</strong> #{ticket_id}</p>
                <p><strong>Título:</strong> {title}</p>
                <p><strong>Prioridad:</strong> {priority}</p>
                <p><strong>Descripción:</strong></p>
                <p>{description}</p>
                <p><strong>Fecha de creación:</strong> {created_at}</p>
                """
            },
            "ticket_assigned": {
                "subject": "Ticket Asignado - #{ticket_id}",
                "body": """
                <h2>Ticket Asignado</h2>
                <p>Se le ha asignado un nuevo ticket:</p>
                <p><strong>Ticket ID:</strong> #{ticket_id}</p>
                <p><strong>Título:</strong> {title}</p>
                <p><strong>Prioridad:</strong> {priority}</p>
                """
            },
            "ticket_resolved": {
                "subject": "Ticket Resuelto - #{ticket_id}",
                "body": """
                <h2>Ticket Resuelto</h2>
                <p>Su ticket ha sido resuelto:</p>
                <p><strong>Ticket ID:</strong> #{ticket_id}</p>
                <p><strong>Título:</strong> {title}</p>
                <p><strong>Fecha de resolución:</strong> {resolved_at}</p>
                """
            }
        }
        
        if template_type not in templates:
            logger.error(f"Template de email no encontrado: {template_type}")
            return False
        
        template = templates[template_type]
        subject = Template(template["subject"]).render(**ticket_data)
        body = Template(template["body"]).render(**ticket_data)
        
        return await self.send_email(
            to_emails=[recipient_email],
            subject=subject,
            body=body,
            is_html=True
        )
    
    async def send_bulk_notification(
        self,
        recipients: List[str],
        subject: str,
        template: str,
        context: Dict[str, Any]
    ) -> Dict[str, int]:
        """Enviar notificación masiva"""
        results = {"sent": 0, "failed": 0}
        
        body = Template(template).render(**context)
        
        for email in recipients:
            success = await self.send_email(
                to_emails=[email],
                subject=subject,
                body=body,
                is_html=True
            )
            
            if success:
                results["sent"] += 1
            else:
                results["failed"] += 1
        
        return results
    
    async def send_report_email(
        self,
        recipient_email: str,
        report_name: str,
        report_path: str,
        summary: Dict[str, Any]
    ) -> bool:
        """Enviar reporte por email"""
        subject = f"Reporte: {report_name}"
        
        body = f"""
        <h2>Reporte Generado</h2>
        <p><strong>Nombre:</strong> {report_name}</p>
        <p><strong>Fecha de generación:</strong> {summary.get('generated_at', 'N/A')}</p>
        <p><strong>Resumen:</strong></p>
        <ul>
        """
        
        for key, value in summary.items():
            if key != 'generated_at':
                body += f"<li><strong>{key}:</strong> {value}</li>"
        
        body += """
        </ul>
        <p>El reporte completo se encuentra adjunto.</p>
        """
        
        return await self.send_email(
            to_emails=[recipient_email],
            subject=subject,
            body=body,
            is_html=True,
            attachments=[report_path]
        )

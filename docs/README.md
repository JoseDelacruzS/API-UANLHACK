# API UANL HACK - Documentación

## Arquitectura del Sistema

### Resumen Ejecutivo

Esta API REST construida con FastAPI está diseñada para automatizar servicios empresariales, gestionar tickets, generar dashboards y facilitar la integración con Watson Orchestrate.

### Componentes Principales

#### 1. **Gestión de Tickets Automatizada**
- Creación automática de tickets desde Watson Orchestrate
- Sistema de prioridades y estados
- Asignación automática a operadores
- Notificaciones por email
- Escalación automática

#### 2. **Dashboards en Tiempo Real**
- Métricas de llamadas y tickets
- Gráficos interactivos
- Datos de rendimiento por operador
- Estadísticas de resolución

#### 3. **Sistema de Reportes**
- Reportes de llamadas por período
- Análisis de rendimiento de operadores
- Reportes de tickets por estado/prioridad
- Exportación en múltiples formatos (JSON, CSV, XLSX)

#### 4. **Integración con Watson Orchestrate**
- Webhook para recibir solicitudes
- Procesamiento de lenguaje natural básico
- Creación automática de acciones
- Seguimiento de sesiones

#### 5. **Automatización de Servicios**
- Programación de visitas
- Envío automatizado de notificaciones
- Generación de reportes programados
- Tareas asíncronas con Celery

### Stack Tecnológico

- **Backend**: FastAPI (Python 3.11+)
- **Base de Datos**: PostgreSQL con esquema `uanl`
- **Cache/Colas**: Redis
- **Tareas Asíncronas**: Celery
- **ORM**: SQLAlchemy
- **Validación**: Pydantic
- **Autenticación**: JWT
- **Containerización**: Docker
- **Monitoreo**: Flower (Celery), Logs con Loguru

### Estructura de Base de Datos

```sql
uanl.operators          -- Operadores del sistema
uanl.clients            -- Clientes/empresas
uanl.calls              -- Registro de llamadas
uanl.tickets            -- Tickets de soporte
uanl.scheduled_visits   -- Visitas programadas
uanl.notifications      -- Notificaciones enviadas
uanl.reports            -- Reportes generados
uanl.watson_activities  -- Actividad de Watson
```

### Endpoints Principales

#### Watson Orchestrate
```
POST /api/v1/watson/webhook          -- Recibir solicitudes de Watson
GET  /api/v1/watson/status           -- Estado de integración
GET  /api/v1/watson/sessions         -- Sesiones recientes
POST /api/v1/watson/test-connection  -- Probar conexión
```

#### Tickets
```
GET  /api/v1/tickets/                -- Listar tickets
POST /api/v1/tickets/                -- Crear ticket
GET  /api/v1/tickets/{id}            -- Obtener ticket
PUT  /api/v1/tickets/{id}            -- Actualizar ticket
GET  /api/v1/tickets/stats           -- Estadísticas
```

#### Dashboards
```
GET /api/v1/dashboards/metrics       -- Métricas principales
GET /api/v1/dashboards/charts/*      -- Datos para gráficos
GET /api/v1/dashboards/real-time     -- Datos en tiempo real
```

#### Reportes
```
GET  /api/v1/reports/calls           -- Reporte de llamadas
GET  /api/v1/reports/tickets         -- Reporte de tickets
POST /api/v1/reports/custom          -- Reporte personalizado
GET  /api/v1/reports/analytics       -- Datos para BI
```

### Flujo de Trabajo con Watson

1. **Recepción**: Watson envía solicitud al webhook
2. **Análisis**: Se analiza el input del usuario usando NLP básico
3. **Clasificación**: Se determina la acción requerida:
   - Crear ticket
   - Programar visita
   - Enviar notificación
   - Generar reporte
4. **Ejecución**: Se ejecuta la acción correspondiente
5. **Respuesta**: Se envía confirmación a Watson
6. **Seguimiento**: Se registra la actividad para análisis

### Automatizaciones Implementadas

#### Tickets
- ✅ Creación automática desde Watson
- ✅ Asignación automática a operadores
- ✅ Escalación por tiempo o prioridad
- ✅ Notificaciones por email

#### Visitas
- ✅ Programación automática
- ✅ Notificaciones a clientes y operadores
- ✅ Seguimiento de estado

#### Reportes
- ✅ Generación programada
- ✅ Envío automático por email
- ✅ Exportación en múltiples formatos

#### Notificaciones
- ✅ Email automático para tickets
- ✅ Notificaciones de escalación
- ✅ Alertas de visitas programadas

### Configuración para Producción

#### Variables de Entorno Críticas
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0
SECRET_KEY=your-secure-secret-key
WATSON_API_KEY=your-watson-api-key
SMTP_USER=your-email@domain.com
SMTP_PASSWORD=your-app-password
```

#### Consideraciones de Seguridad
- Autenticación JWT para endpoints protegidos
- Validación de datos con Pydantic
- Rate limiting para APIs externas
- Logs de seguridad y auditoría
- Encriptación de datos sensibles

#### Escalabilidad
- Docker para containerización
- Redis para cache y distribución de tareas
- Celery para procesamiento asíncrono
- Base de datos optimizada con índices
- Monitoreo con métricas en tiempo real

### Próximas Funcionalidades

1. **IA/ML Integration**
   - Análisis de sentimientos en conversaciones
   - Predicción de escalación de tickets
   - Recomendaciones automáticas

2. **Integraciones Adicionales**
   - Microsoft Teams/Slack
   - Sistemas de telefonía (Asterisk, Twilio)
   - CRM externos (Salesforce, HubSpot)

3. **Análisis Avanzado**
   - Dashboard predictivo
   - Análisis de tendencias
   - KPIs automatizados

4. **Mobile Support**
   - App móvil para operadores
   - Notificaciones push
   - Trabajo offline

### Soporte y Mantenimiento

- Logs centralizados con Loguru
- Monitoreo de performance
- Backup automatizado de base de datos
- Actualizaciones de seguridad
- Documentación de API automática con FastAPI

---

*Para más información técnica, consulte la documentación de la API en `/api/v1/docs`*

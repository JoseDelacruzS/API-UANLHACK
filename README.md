# 🚀 API UANL HACK - Sistema de Automatización

![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Redis](https://img.shields.io/badge/Redis-7+-red.svg)

API REST construida con FastAPI para automatización de servicios, gestión de tickets, dashboards y reportes con integración a Watson Orchestrate.

## ✨ Características

- 🎫 **Gestión de tickets automatizada** - Creación automática desde Watson Orchestrate
- 📊 **Dashboards en tiempo real** - Métricas y gráficos interactivos
- 📈 **Reportes y análisis** - Exportación en múltiples formatos (JSON, CSV, XLSX)
- 🤖 **Integración con Watson Orchestrate** - Procesamiento de solicitudes via webhook
- 📧 **Automatización de correos** - Notificaciones automáticas por email
- 🗄️ **Alimentación de datos para BI** - Datos estructurados para análisis
- 🔄 **Automatización de servicios y visitas** - Programación automática

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│ Watson          │───▶│ FastAPI         │───▶│ PostgreSQL      │
│ Orchestrate     │    │ Application     │    │ Database        │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │                 │
                       │ Redis           │
                       │ (Cache/Queue)   │
                       │                 │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │                 │
                       │ Celery          │
                       │ (Background)    │
                       │                 │
                       └─────────────────┘
```

## 📁 Estructura del Proyecto

```
API-UANLHACK/
├── 📁 app/                          # Código principal de la aplicación
│   ├── 📁 api/v1/endpoints/         # Endpoints de la API REST
│   │   ├── 🔗 operators.py          # CRUD de operadores
│   │   ├── 🔗 clients.py            # CRUD de clientes
│   │   ├── 🔗 calls.py              # CRUD de llamadas
│   │   ├── 🔗 tickets.py            # CRUD de tickets
│   │   ├── 📊 dashboards.py         # Endpoints de dashboards
│   │   ├── 📈 reports.py            # Endpoints de reportes
│   │   └── 🤖 watson.py             # Integración Watson Orchestrate
│   │
│   ├── 📁 models/                   # Modelos SQLAlchemy
│   │   ├── 👥 operators.py          # Modelo de operadores
│   │   ├── 🏢 clients.py            # Modelo de clientes
│   │   ├── 📞 calls.py              # Modelo de llamadas
│   │   └── 🎫 tickets.py            # Modelo de tickets
│   │
│   ├── 📁 schemas/                  # Esquemas Pydantic
│   │   ├── ✅ operators.py          # Validación de operadores
│   │   ├── ✅ clients.py            # Validación de clientes
│   │   ├── ✅ calls.py              # Validación de llamadas
│   │   └── ✅ tickets.py            # Validación de tickets
│   │
│   ├── 📁 services/                 # Lógica de negocio
│   │   ├── 🎫 ticket_service.py     # Servicio de tickets
│   │   ├── 📊 dashboard_service.py  # Servicio de dashboards
│   │   ├── 📧 email_service.py      # Servicio de emails
│   │   └── 🤖 watson_service.py     # Servicio de Watson
│   │
│   ├── 📁 config/                   # Configuración
│   │   ├── ⚙️ settings.py           # Configuración de la app
│   │   └── 🗄️ database.py          # Configuración de BD
│   │
│   ├── 📁 core/                     # Funcionalidad core
│   │   ├── 🔐 security.py           # Autenticación y autorización
│   │   └── ⚠️ exceptions.py         # Excepciones personalizadas
│   │
│   ├── 📁 utils/                    # Utilidades
│   │   └── 🛠️ helpers.py            # Funciones auxiliares
│   │
│   └── 🚀 main.py                   # Punto de entrada
│
├── 📁 scripts/                      # Scripts de utilidad
│   └── 🗄️ init.sql                 # Script de inicialización de BD
│
├── 📁 tests/                        # Pruebas unitarias
├── 📁 docs/                         # Documentación
├── 📁 migrations/                   # Migraciones de BD
│
├── 📋 requirements.txt              # Dependencias Python
├── 🐳 Dockerfile                    # Configuración Docker
├── 🐙 docker-compose.yml           # Orquestación de servicios
├── ⚙️ alembic.ini                  # Configuración de migraciones
├── 🔧 setup.sh                     # Script de configuración
├── 🌍 .env                         # Variables de entorno
└── 📖 README.md                    # Documentación principal
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- **Python 3.9+** 🐍
- **PostgreSQL 15+** 🐘
- **Redis 7+** 🗄️
- **Docker & Docker Compose** (opcional) 🐳

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/JoseDelacruzS/API-UANLHACK.git
cd API-UANLHACK
```

2. **Crear entorno virtual**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar la aplicación**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Instalación con Docker

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Solo la aplicación
docker-compose up api

# En segundo plano
docker-compose up -d
```

## 🌐 API Endpoints

### 🏠 Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información de la API |
| `GET` | `/health` | Estado de salud |
| `GET` | `/api/v1/docs` | Documentación Swagger |
| `GET` | `/api/v1/redoc` | Documentación ReDoc |

### 🤖 Watson Orchestrate

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v1/watson/webhook` | Webhook para recibir datos de Watson |
| `GET` | `/api/v1/watson/status` | Estado de la integración |
| `GET` | `/api/v1/watson/sessions` | Sesiones recientes |
| `POST` | `/api/v1/watson/test-connection` | Probar conexión |

### 🎫 Tickets

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/tickets/` | Listar tickets |
| `POST` | `/api/v1/tickets/` | Crear ticket |
| `GET` | `/api/v1/tickets/{id}` | Obtener ticket específico |
| `PUT` | `/api/v1/tickets/{id}` | Actualizar ticket |
| `GET` | `/api/v1/tickets/stats` | Estadísticas de tickets |

### 📊 Dashboards

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/dashboards/metrics` | Métricas principales |
| `GET` | `/api/v1/dashboards/charts/calls-by-date` | Gráfico de llamadas |
| `GET` | `/api/v1/dashboards/charts/tickets-by-status` | Gráfico de tickets |
| `GET` | `/api/v1/dashboards/real-time` | Datos en tiempo real |

### 📈 Reportes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/reports/calls` | Reporte de llamadas |
| `GET` | `/api/v1/reports/tickets` | Reporte de tickets |
| `GET` | `/api/v1/reports/operators-performance` | Rendimiento de operadores |
| `POST` | `/api/v1/reports/custom` | Reporte personalizado |
| `GET` | `/api/v1/reports/analytics` | Datos para BI |

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Versión | Propósito |
|------------|------------|---------|-----------|
| **Backend** | FastAPI | 0.104.1 | Framework web asíncrono |
| **Base de Datos** | PostgreSQL | 15+ | Base de datos principal |
| **Cache/Colas** | Redis | 7+ | Cache y colas de tareas |
| **ORM** | SQLAlchemy | 2.0.23 | Mapeo objeto-relacional |
| **Validación** | Pydantic | 2.5.0 | Validación de datos |
| **Migraciones** | Alembic | 1.12.1 | Migraciones de BD |
| **Tareas Asíncronas** | Celery | 5.3.4 | Procesamiento en segundo plano |
| **Autenticación** | JWT | - | Tokens de acceso |
| **Logs** | Loguru | 0.7.2 | Sistema de logging |
| **Testing** | Pytest | 7.4.3 | Pruebas unitarias |
| **Containerización** | Docker | - | Despliegue |

## 🗄️ Esquema de Base de Datos

```sql
-- Esquema principal: uanl
uanl.operators           -- 👥 Operadores del sistema
uanl.clients             -- 🏢 Clientes/empresas  
uanl.calls               -- 📞 Registro de llamadas
uanl.tickets             -- 🎫 Tickets de soporte
uanl.scheduled_visits    -- 📅 Visitas programadas
uanl.notifications       -- 📧 Notificaciones enviadas
uanl.reports             -- 📊 Reportes generados
uanl.watson_activities   -- 🤖 Actividad de Watson
```

## 🔄 Flujo de Trabajo con Watson

1. **📥 Recepción**: Watson envía solicitud al webhook
2. **🧠 Análisis**: Se analiza el input del usuario usando NLP básico
3. **🏷️ Clasificación**: Se determina la acción requerida:
   - ✅ Crear ticket
   - 📅 Programar visita  
   - 📧 Enviar notificación
   - 📊 Generar reporte
4. **⚡ Ejecución**: Se ejecuta la acción correspondiente
5. **✅ Respuesta**: Se envía confirmación a Watson
6. **📝 Seguimiento**: Se registra la actividad para análisis

## 🚀 Uso Rápido

### Iniciar servidor de desarrollo

```bash
# Método 1: Directo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Método 2: Con script de configuración
./setup.sh dev

# Método 3: Con Docker
docker-compose up
```

### Acceder a la documentación

- **Swagger UI**: http://localhost:8000/api/v1/docs
- **ReDoc**: http://localhost:8000/api/v1/redoc  
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

### Probar la API

```bash
# Probar endpoint de salud
curl http://localhost:8000/health

# Obtener información de la API
curl http://localhost:8000/

# Listar operadores
curl http://localhost:8000/api/v1/operators/

# Ejecutar script de pruebas
python test_api.py
```

## 🔧 Configuración

### Variables de Entorno Principales

```bash
# Base de datos
DATABASE_URL=postgresql://user:pass@host:5432/db
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=uanl_db
DATABASE_USER=postgres
DATABASE_PASSWORD=password

# Redis
REDIS_URL=redis://localhost:6379/0

# Seguridad
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Watson Orchestrate
WATSON_API_KEY=your-watson-api-key
WATSON_URL=your-watson-url

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Entorno
ENVIRONMENT=development
LOG_LEVEL=INFO
```

## 🧪 Testing

```bash
# Ejecutar todas las pruebas
pytest tests/ -v

# Ejecutar pruebas con cobertura
pytest tests/ --cov=app

# Ejecutar script de pruebas de API
python test_api.py

# Ejecutar pruebas específicas
pytest tests/test_tickets.py -v
```

## 📈 Monitoreo y Logs

- **📋 Logs de aplicación**: Logs con Loguru en `/logs/`
- **🌸 Monitor Celery**: Flower en http://localhost:5555
- **📊 Métricas FastAPI**: Integradas en `/api/v1/docs`
- **🔍 Trazabilidad**: Logs estructurados con request ID

## 🚀 Despliegue en Producción

### Con Docker

```bash
# Construir imagen de producción
docker build -t uanl-api:latest .

# Ejecutar en producción
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Variables de Entorno de Producción

```bash
ENVIRONMENT=production
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://prod_user:prod_pass@prod_host:5432/prod_db
REDIS_URL=redis://prod_redis:6379/0
SECRET_KEY=super-secure-production-key
```

## 🤝 Contribución

1. Fork el repositorio
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit tus cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crea un Pull Request

## 📞 Soporte

- **📧 Email**: soporte@uanl.mx
- **🐛 Issues**: GitHub Issues
- **📖 Docs**: `/docs/README.md`
- **💬 Slack**: #uanl-api-support

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

**🏆 Desarrollado para UANL Hack 2024** 

*Automatización inteligente de servicios con Watson Orchestrate*

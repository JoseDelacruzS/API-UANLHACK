# 🚀 API UANL Hack - Sistema de Conversaciones con IA

API desarrollada en FastAPI que proporciona un sistema completo de gestión de conversaciones con modelos de IA y integración con APIs externas. Utiliza PostgreSQL para almacenar conversaciones y mensajes.

## 📋 Características

- **🤖 Integración con IA**: OpenAI GPT, Hugging Face Transformers
- **💬 Sistema de Conversaciones**: Gestión completa de conversaciones y mensajes
- **🗄️ Base de Datos**: PostgreSQL para persistencia de datos
- **🌐 APIs Externas**: Clima, noticias, mapas y más
- **📄 Documentación Automática**: Swagger UI integrado
- **🐳 Docker**: Contenedorización completa
- **⚡ Caché**: Sistema de caché local para optimización
- **🔧 Testing**: Suite de pruebas automatizadas

## 🏗️ Arquitectura

```
API-UANLHACK/
├── app/
│   ├── api/endpoints/          # Endpoints de la API
│   │   ├── ai.py              # Endpoints de IA
│   │   ├── conversations.py   # Gestión de conversaciones
│   │   ├── external.py        # APIs externas
│   │   └── health.py          # Salud del sistema
│   ├── database/              # Configuración de base de datos
│   │   └── connection.py      # Conexión PostgreSQL
│   ├── models/                # Modelos de datos
│   │   └── models.py          # Modelos SQLAlchemy
│   ├── services/              # Lógica de negocio
│   │   ├── ai_service.py      # Servicios de IA
│   │   ├── conversation_service.py  # Gestión de conversaciones
│   │   ├── external_api_service.py  # APIs externas
│   │   └── cache_service.py   # Sistema de caché
│   └── core/                  # Configuración central
│       └── config.py          # Configuraciones
├── tests/                     # Pruebas automatizadas
├── cache/                     # Directorio de caché
├── docker-compose.yml         # Configuración Docker
├── requirements.txt           # Dependencias Python
├── init_db.py                # Inicialización de DB
└── start.sh                  # Script de inicio rápido
```

## 🛠️ Instalación y Configuración

### Inicio Rápido

```bash
# Clonar repositorio
git clone <tu-repositorio>
cd API-UANLHACK

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar script de inicio automático
./start.sh
```

### Opción 1: Docker Compose (Recomendado)

1. **Configurar variables de entorno**:
```bash
cp .env.example .env
# Edita .env con tus credenciales reales
```

2. **Iniciar con Docker**:
```bash
docker-compose up --build
```

3. **Inicializar base de datos**:
```bash
docker-compose exec api python init_db.py
```

### Opción 2: Instalación Local

1. **Prerrequisitos**:
   - Python 3.8+
   - PostgreSQL 12+
   - pip

2. **Instalar dependencias**:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configurar PostgreSQL**:
```bash
# Crear base de datos
createdb uanl_hack_db
```

4. **Inicializar base de datos**:
```bash
python init_db.py
```

5. **Ejecutar la aplicación**:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📚 Uso de la API

### Documentación Interactiva
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principales

#### 1. Gestión de Usuarios
```bash
# Crear usuario
POST /api/v1/conversations/users
{
  "username": "usuario123",
  "email": "usuario@email.com",
  "full_name": "Usuario Completo"
}
```

#### 2. Conversaciones
```bash
# Crear conversación
POST /api/v1/conversations?user_id=1&title=Mi Conversación

# Obtener conversaciones de usuario
GET /api/v1/conversations/{user_id}

# Chat con IA
POST /api/v1/conversations/chat
{
  "user_id": 1,
  "conversation_id": 1,
  "message": "Hola, ¿cómo estás?",
  "model": "gpt-3.5-turbo"
}
```

#### 3. Generación de Texto con IA
```bash
POST /api/v1/ai/generate-text
{
  "prompt": "Escribe un poema sobre la programación",
  "model": "gpt-3.5-turbo",
  "max_tokens": 100,
  "temperature": 0.7
}
```

#### 4. APIs Externas
```bash
# Clima
GET /api/v1/external/weather?city=Monterrey

# Noticias
GET /api/v1/external/news?category=technology

# Búsqueda en mapas
GET /api/v1/external/maps/search?query=UANL Monterrey
```

## 🗄️ Esquema de Base de Datos

### Tablas Principales

- **users**: Información de usuarios
- **conversations**: Conversaciones de usuarios  
- **messages**: Mensajes en conversaciones
- **api_calls**: Registro de llamadas a APIs
- **conversation_summaries**: Resúmenes de conversaciones

### Relaciones
- Usuario → Múltiples Conversaciones
- Conversación → Múltiples Mensajes
- Conversación → Resúmenes opcionales

## 🧪 Testing

```bash
# Todas las pruebas
pytest

# Con cobertura
pytest --cov=app

# Pruebas específicas
pytest tests/test_main.py::test_create_conversation
```

## 🔧 Configuración

### Variables de Entorno (.env)

```bash
# Base de Datos
DATABASE_URL=postgresql://postgres:password@localhost:5432/uanl_hack_db

# APIs de IA
OPENAI_API_KEY=tu-clave-openai
HUGGINGFACE_API_KEY=tu-clave-huggingface

# APIs Externas
WEATHER_API_KEY=tu-clave-clima
NEWS_API_KEY=tu-clave-noticias
MAPS_API_KEY=tu-clave-mapas

# Configuración
CACHE_DIR=./cache
CACHE_DURATION=300
DEFAULT_MODEL=gpt-3.5-turbo
```

## 🚨 Troubleshooting

### Problemas Comunes

1. **Error de conexión a PostgreSQL**:
```bash
# Verificar que PostgreSQL esté corriendo
brew services start postgresql  # macOS
sudo service postgresql start   # Linux
```

2. **Docker no inicia**:
```bash
# Limpiar contenedores
docker-compose down
docker-compose up --build
```

## 📈 Monitoreo

### Health Checks
- **Básico**: GET `/api/v1/health`
- **Detallado**: GET `/api/v1/health/detailed`

### Logs
```bash
# Docker logs
docker-compose logs -f api

# Estadísticas de caché
GET /api/v1/cache/stats
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

**Desarrollado para UANL Hack 2024** 🎓

## 🚀 Características

- **FastAPI**: Framework moderno y rápido para APIs
- **Google Sheets**: Como base de datos en la nube
- **APIs de IA**: OpenAI, Hugging Face, Anthropic
- **APIs Externas**: Clima, Noticias, Geolocalización
- **Caché Local**: Sistema de caché con archivos JSON
- **Documentación automática**: Swagger UI y ReDoc incluidos
- **Validación de datos**: Con Pydantic schemas
- **Contenedores**: Docker y Docker Compose

## 📁 Estructura del Proyecto

```
API-UANLHACK/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── health.py              # Endpoints de salud
│   │       ├── ai_model.py            # Endpoints para IA
│   │       ├── google_sheets.py       # Endpoints para Google Sheets
│   │       ├── external_apis.py       # Endpoints para APIs externas
│   │       └── cache.py               # Endpoints para caché
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py                  # Configuración
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py                 # Esquemas Pydantic
│   └── services/
│       ├── __init__.py
│       ├── google_sheets_service.py   # Servicio Google Sheets
│       ├── external_api_service.py    # Servicio APIs externas
│       └── cache_service.py           # Servicio de caché local
├── docs/
│   ├── google-sheets-setup.md         # Configuración Google Sheets
│   └── external-apis-setup.md         # Configuración APIs externas
├── tests/
│   ├── __init__.py
│   └── test_main.py                   # Pruebas
├── cache/                             # Directorio de caché local
├── main.py                            # Punto de entrada
├── requirements.txt                   # Dependencias
├── Dockerfile                         # Imagen Docker
├── docker-compose.yml                 # Servicios Docker
├── .env.example                       # Variables de entorno ejemplo
├── credentials.json.example           # Ejemplo credenciales Google
├── .gitignore                         # Archivos ignorados por Git
└── README.md                          # Este archivo
```

## 🛠️ Instalación y Configuración

### Prerequisitos

1. **Google Sheets configurado** (Ver [docs/google-sheets-setup.md](docs/google-sheets-setup.md))
2. **API Keys de servicios externos** (Ver [docs/external-apis-setup.md](docs/external-apis-setup.md))

### Opción 1: Instalación Local

1. **Clona el repositorio**:
```bash
git clone https://github.com/JoseDelacruzS/API-UANLHACK.git
cd API-UANLHACK
```

2. **Crea un entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala las dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configura las variables de entorno**:
```bash
cp .env.example .env
# Edita el archivo .env con tus configuraciones
```

5. **Coloca las credenciales de Google**:
```bash
# Coloca tu archivo credentials.json en la raíz del proyecto
cp /path/to/your/credentials.json ./credentials.json
```

6. **Ejecuta la aplicación**:
```bash
uvicorn main:app --reload
```

### Opción 2: Docker Compose (Recomendado)

1. **Clona el repositorio**:
```bash
git clone https://github.com/JoseDelacruzS/API-UANLHACK.git
cd API-UANLHACK
```

2. **Configura variables de entorno**:
```bash
cp .env.example .env
# Edita .env con tus API keys
```

3. **Ejecuta con Docker Compose**:
```bash
docker-compose up --build
```

## 📦 Dependencias Principales

### Core
- **fastapi**: Framework web moderno para Python
- **uvicorn**: Servidor ASGI para ejecutar FastAPI
- **pydantic**: Validación de datos y serialización
- **python-dotenv**: Manejo de variables de entorno

### Google Sheets
- **gspread**: Cliente de Google Sheets
- **google-auth**: Autenticación con Google
- **pandas**: Manipulación de datos
- **openpyxl**: Lectura de archivos Excel

### APIs Externas
- **httpx**: Cliente HTTP asíncrono
- **requests**: Cliente HTTP síncronoś

### Utilidades
- **aiofiles**: Operaciones de archivos asíncronas
- **pytest**: Framework de testing

## 🔗 Endpoints Disponibles

### Endpoints Generales
- `GET /` - Página de inicio con información de la API
- `GET /docs` - Documentación Swagger UI
- `GET /redoc` - Documentación ReDoc

### Endpoints de Salud
- `GET /api/v1/health` - Estado básico de la API
- `GET /api/v1/health/detailed` - Estado detallado con servicios

### Endpoints de Google Sheets
- `POST /api/v1/sheets/data` - Obtener datos de la hoja
- `POST /api/v1/sheets/add` - Agregar una fila
- `PUT /api/v1/sheets/update` - Actualizar una fila
- `POST /api/v1/sheets/search` - Buscar registros con filtros
- `GET /api/v1/sheets/columns/{sheet_name}` - Obtener columnas
- `POST /api/v1/sheets/refresh/{sheet_name}` - Refrescar caché

### Endpoints de IA
- `POST /api/v1/ai/generate-text` - Generar texto con OpenAI
- `POST /api/v1/ai/sentiment-analysis` - Análisis de sentimientos
- `POST /api/v1/ai/custom-model` - Modelo personalizado
- `GET /api/v1/ai/models` - Listar modelos disponibles
- `GET /api/v1/ai/status` - Estado de servicios de IA

### Endpoints de APIs Externas
- `POST /api/v1/weather` - Datos del clima
- `POST /api/v1/news` - Obtener noticias
- `POST /api/v1/location` - Geolocalización
- `POST /api/v1/custom-api` - Llamar API personalizada
- `GET /api/v1/external-api/status` - Estado de APIs externas

### Endpoints de Caché
- `GET /api/v1/cache/stats` - Estadísticas del caché
- `DELETE /api/v1/cache/clear` - Limpiar todo el caché
- `GET /api/v1/cache/{key}` - Obtener valor específico
- `POST /api/v1/cache/{key}` - Guardar valor
- `DELETE /api/v1/cache/{key}` - Eliminar clave

## 📝 Ejemplos de Uso

### Obtener Datos de Google Sheets

```bash
curl -X POST "http://localhost:8000/api/v1/sheets/data" \
  -H "Content-Type: application/json" \
  -d '{"sheet_name": "Sheet1", "force_refresh": false}'
```

### Generar Texto con IA

```bash
curl -X POST "http://localhost:8000/api/v1/ai/generate-text" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explica qué es FastAPI",
    "model": "gpt-3.5-turbo",
    "max_tokens": 100
  }'
```

### Obtener Datos del Clima

```bash
curl -X POST "http://localhost:8000/api/v1/weather" \
  -H "Content-Type: application/json" \
  -d '{"city": "Monterrey"}'
```

### Buscar Noticias

```bash
curl -X POST "http://localhost:8000/api/v1/news" \
  -H "Content-Type: application/json" \
  -d '{"query": "tecnología", "language": "es"}'
```

## 🧪 Testing

Ejecutar las pruebas:

```bash
# Todas las pruebas
pytest

# Pruebas con coverage
pytest --cov=app

# Pruebas específicas
pytest tests/test_main.py -v
```

## 🔧 Configuración

### Variables de Entorno Principales

```bash
# Google Sheets
GOOGLE_SHEET_ID=1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P7Q8R9S0T
GOOGLE_CREDENTIALS_FILE=credentials.json

# APIs de IA
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# APIs Externas
WEATHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
MAPS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Caché
CACHE_DIR=./cache
CACHE_DURATION=300
```

## 🚀 Despliegue

### Docker

```bash
# Construir imagen
docker build -t api-uanl-hack .

# Ejecutar contenedor
docker run -p 8000:8000 -v $(pwd)/cache:/app/cache api-uanl-hack
```

### Docker Compose

```bash
# Desarrollo
docker-compose up --build

# Producción (detached)
docker-compose up -d
```

## 📚 Documentación Adicional

Una vez que la API esté ejecutándose:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

Documentación específica:
- [Configuración de Google Sheets](docs/google-sheets-setup.md)
- [Configuración de APIs Externas](docs/external-apis-setup.md)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 🔍 Monitoreo y Logs

La API incluye logging automático y endpoints de monitoreo:

- **Estado general**: `GET /api/v1/health/detailed`
- **Estadísticas de caché**: `GET /api/v1/cache/stats`
- **Estado de APIs externas**: `GET /api/v1/external-api/status`
- **Estado de Google Sheets**: `GET /api/v1/sheets/status`

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👥 Equipo

Desarrollado para el Hackathon UANL 2024

## 📞 Contacto

Para preguntas o soporte, contacta al equipo de desarrollo. 

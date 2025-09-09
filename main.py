from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import health, ai_model, conversations, external_apis, cache
from app.core.config import settings
from app.services.external_api_service import external_api_service
from app.database.connection import connect_db, disconnect_db, Base, engine
import os

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API UANL Hack",
    description="API con PostgreSQL que maneja conversaciones y consume APIs externas para el hackathon",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear directorio de caché al iniciar
os.makedirs(settings.CACHE_DIR, exist_ok=True)

# Incluir routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(conversations.router, prefix="/api/v1/conversations", tags=["conversations"])
app.include_router(ai_model.router, prefix="/api/v1", tags=["ai-models"])
app.include_router(external_apis.router, prefix="/api/v1", tags=["external-apis"])
app.include_router(cache.router, prefix="/api/v1", tags=["cache"])

@app.get("/")
async def root():
    return {
        "message": "API UANL Hack - ¡Bienvenido!",
        "version": "1.0.0",
        "description": "API con PostgreSQL que maneja conversaciones y consume APIs externas",
        "features": [
            "Sistema de conversaciones con IA",
            "Base de datos PostgreSQL",
            "APIs de Inteligencia Artificial (OpenAI, Hugging Face)",
            "APIs externas (Clima, Noticias, Maps)",
            "Sistema de caché local",
            "Historial de conversaciones",
            "Documentación automática"
        ],
        "main_endpoints": {
            "chat": "/api/v1/conversations/chat",
            "conversations": "/api/v1/conversations",
            "ai_models": "/api/v1/ai",
            "external_apis": "/api/v1/weather, /api/v1/news",
            "docs": "/docs"
        }
    }

@app.on_event("startup")
async def startup_event():
    """Eventos de inicio de la aplicación"""
    print("🚀 Iniciando API UANL Hack...")
    print(f"📂 Directorio de caché: {settings.CACHE_DIR}")
    print(f"�️ Base de datos: PostgreSQL")
    print(f"🤖 OpenAI configurado: {'✅' if settings.OPENAI_API_KEY else '❌'}")
    print(f"🤗 Hugging Face configurado: {'✅' if settings.HUGGINGFACE_API_KEY else '❌'}")
    
    # Conectar a la base de datos
    await connect_db()
    print("🗄️ Conectado a PostgreSQL")

@app.on_event("shutdown")
async def shutdown_event():
    """Eventos de cierre de la aplicación"""
    print("🛑 Cerrando API UANL Hack...")
    
    # Cerrar sesión HTTP si existe
    if external_api_service.session:
        await external_api_service.close_session()
    
    # Desconectar de la base de datos
    await disconnect_db()
    print("✅ Aplicación cerrada correctamente")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

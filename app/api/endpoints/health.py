from fastapi import APIRouter, Depends
from datetime import datetime
from sqlalchemy.orm import Session
from app.schemas.schemas import HealthResponse
from app.services.cache_service import cache_service
from app.database.connection import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Endpoint para verificar el estado básico de la API
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        service="API UANL Hack",
        version="1.0.0"
    )

@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Endpoint para verificar el estado detallado de la API
    """
    # Verificar base de datos
    database_status = "unknown"
    try:
        # Hacer una consulta simple para verificar la conexión
        db.execute("SELECT 1")
        database_status = "connected"
    except Exception:
        database_status = "error"
    
    # Verificar caché
    cache_status = "unknown"
    try:
        stats = await cache_service.get_cache_stats()
        cache_status = "active" if "error" not in stats else "error"
    except Exception:
        cache_status = "error"
    
    # Verificar APIs externas
    external_apis = {
        "openai": "configured" if settings.OPENAI_API_KEY else "not_configured",
        "huggingface": "configured" if settings.HUGGINGFACE_API_KEY else "not_configured",
        "weather": "configured" if settings.WEATHER_API_KEY else "not_configured",
        "news": "configured" if settings.NEWS_API_KEY else "not_configured",
        "maps": "configured" if settings.MAPS_API_KEY else "not_configured"
    }
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        service="API UANL Hack",
        version="1.0.0",
        database=database_status,
        cache_status=cache_status,
        external_apis=external_apis
    )

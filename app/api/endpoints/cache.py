from fastapi import APIRouter, HTTPException
from app.schemas.schemas import CacheStats, MessageResponse
from app.services.cache_service import cache_service

router = APIRouter()

@router.get("/cache/stats", response_model=CacheStats)
async def get_cache_stats():
    """
    Obtener estadísticas del caché
    """
    try:
        stats = await cache_service.get_cache_stats()
        
        if "error" in stats:
            raise HTTPException(status_code=500, detail=stats["error"])
        
        return CacheStats(**stats)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estadísticas: {str(e)}")

@router.delete("/cache/clear", response_model=MessageResponse)
async def clear_cache():
    """
    Limpiar todo el caché
    """
    try:
        success = await cache_service.clear_all()
        
        if success:
            return MessageResponse(message="Caché limpiado exitosamente")
        else:
            raise HTTPException(status_code=500, detail="Error limpiando caché")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error limpiando caché: {str(e)}")

@router.delete("/cache/{key}")
async def delete_cache_key(key: str):
    """
    Eliminar una clave específica del caché
    """
    try:
        success = await cache_service.delete(key)
        
        if success:
            return MessageResponse(message=f"Clave '{key}' eliminada del caché")
        else:
            return MessageResponse(message=f"Clave '{key}' no encontrada", status="warning")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando clave: {str(e)}")

@router.get("/cache/{key}")
async def get_cache_value(key: str):
    """
    Obtener valor específico del caché
    """
    try:
        value = await cache_service.get(key)
        
        if value is not None:
            return {"key": key, "value": value, "found": True}
        else:
            return {"key": key, "value": None, "found": False}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo valor: {str(e)}")

@router.post("/cache/{key}")
async def set_cache_value(key: str, value: dict, duration: int = 300):
    """
    Establecer valor en el caché
    """
    try:
        success = await cache_service.set(key, value, duration)
        
        if success:
            return MessageResponse(message=f"Valor guardado en caché con clave '{key}'")
        else:
            raise HTTPException(status_code=500, detail="Error guardando en caché")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando valor: {str(e)}")

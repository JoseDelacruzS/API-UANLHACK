from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.schemas.schemas import (
    WeatherRequest, WeatherResponse, NewsRequest, NewsResponse,
    LocationRequest, LocationResponse, APIRequest, APIResponse
)
from app.services.external_api_service import external_api_service
from app.services.cache_service import cache_service
import time

router = APIRouter()

@router.post("/weather", response_model=WeatherResponse)
async def get_weather(request: WeatherRequest):
    """
    Obtener datos del clima
    """
    try:
        # Verificar caché primero
        cache_key = f"weather_{request.city}_{request.units}"
        cached_data = await cache_service.get(cache_key)
        
        if cached_data:
            return WeatherResponse(**cached_data)
        
        # Hacer petición a la API
        start_time = time.time()
        weather_data = await external_api_service.get_weather_data(request.city)
        
        # Extraer datos relevantes
        response_data = {
            "city": weather_data["name"],
            "temperature": weather_data["main"]["temp"],
            "description": weather_data["weather"][0]["description"],
            "humidity": weather_data["main"]["humidity"],
            "wind_speed": weather_data["wind"]["speed"]
        }
        
        # Guardar en caché
        await cache_service.set(cache_key, response_data, duration=1800)  # 30 minutos
        
        return WeatherResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo datos del clima: {str(e)}")

@router.post("/news", response_model=NewsResponse)
async def get_news(request: NewsRequest):
    """
    Obtener noticias
    """
    try:
        # Verificar caché
        cache_key = f"news_{request.query}_{request.language}"
        cached_data = await cache_service.get(cache_key)
        
        if cached_data:
            return NewsResponse(**cached_data)
        
        # Hacer petición a la API
        news_data = await external_api_service.get_news_data(
            query=request.query,
            language=request.language
        )
        
        # Procesar artículos
        articles = []
        for article in news_data.get("articles", [])[:request.page_size]:
            articles.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "url": article.get("url"),
                "source": article.get("source", {}).get("name"),
                "published_at": article.get("publishedAt"),
                "image_url": article.get("urlToImage")
            })
        
        response_data = {
            "articles": articles,
            "total_results": news_data.get("totalResults", 0),
            "query": request.query
        }
        
        # Guardar en caché
        await cache_service.set(cache_key, response_data, duration=900)  # 15 minutos
        
        return NewsResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo noticias: {str(e)}")

@router.post("/location", response_model=LocationResponse)
async def get_location(request: LocationRequest):
    """
    Obtener datos de geolocalización
    """
    try:
        # Verificar caché
        cache_key = f"location_{request.address}"
        cached_data = await cache_service.get(cache_key)
        
        if cached_data:
            return LocationResponse(**cached_data)
        
        # Hacer petición a la API
        location_data = await external_api_service.get_maps_data(request.address)
        
        if not location_data.get("results"):
            raise HTTPException(status_code=404, detail="Dirección no encontrada")
        
        result = location_data["results"][0]
        location = result["geometry"]["location"]
        
        response_data = {
            "address": request.address,
            "latitude": location["lat"],
            "longitude": location["lng"],
            "formatted_address": result["formatted_address"]
        }
        
        # Guardar en caché
        await cache_service.set(cache_key, response_data, duration=86400)  # 24 horas
        
        return LocationResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo ubicación: {str(e)}")

@router.post("/custom-api", response_model=APIResponse)
async def call_custom_api(request: APIRequest):
    """
    Llamar a una API personalizada
    """
    try:
        start_time = time.time()
        
        # Verificar caché para requests GET
        cache_key = None
        if request.method.upper() == "GET":
            cache_key = f"custom_api_{hash(str(request.dict()))}"
            cached_data = await cache_service.get(cache_key)
            
            if cached_data:
                return APIResponse(
                    status_code=200,
                    data=cached_data,
                    response_time=0.001,
                    cached=True
                )
        
        # Hacer petición
        response_data = await external_api_service.custom_api_request(
            url=request.url,
            method=request.method,
            headers=request.headers,
            params=request.params,
            data=request.data
        )
        
        processing_time = time.time() - start_time
        
        # Guardar en caché si es GET
        if cache_key:
            await cache_service.set(cache_key, response_data, duration=600)  # 10 minutos
        
        return APIResponse(
            status_code=200,
            data=response_data,
            response_time=processing_time,
            cached=False
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en API personalizada: {str(e)}")

@router.get("/external-api/status")
async def get_external_apis_status():
    """
    Verificar estado de APIs externas
    """
    status = {
        "openai": "configured" if external_api_service.session else "not_configured",
        "huggingface": "configured" if external_api_service.session else "not_configured",
        "weather": "configured" if hasattr(external_api_service, 'get_weather_data') else "not_configured",
        "news": "configured" if hasattr(external_api_service, 'get_news_data') else "not_configured",
        "maps": "configured" if hasattr(external_api_service, 'get_maps_data') else "not_configured"
    }
    
    return {
        "external_apis": status,
        "session_active": external_api_service.session is not None,
        "last_check": time.time()
    }

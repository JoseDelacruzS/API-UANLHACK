import httpx
import asyncio
from typing import Dict, List, Any, Optional
from app.core.config import settings
import json
import time

class ExternalAPIService:
    """
    Servicio para consumir APIs externas
    """
    
    def __init__(self):
        self.session = None
        
    async def get_session(self):
        """Obtener sesión HTTP asíncrona"""
        if not self.session:
            self.session = httpx.AsyncClient(timeout=settings.API_TIMEOUT)
        return self.session
    
    async def close_session(self):
        """Cerrar sesión HTTP"""
        if self.session:
            await self.session.aclose()
            self.session = None
    
    async def make_request(self, 
                          method: str, 
                          url: str, 
                          headers: Optional[Dict] = None, 
                          params: Optional[Dict] = None, 
                          data: Optional[Dict] = None,
                          retries: int = 3) -> Dict[str, Any]:
        """
        Hacer una petición HTTP con reintentos
        """
        session = await self.get_session()
        
        for attempt in range(retries):
            try:
                if method.upper() == "GET":
                    response = await session.get(url, headers=headers, params=params)
                elif method.upper() == "POST":
                    response = await session.post(url, headers=headers, params=params, json=data)
                elif method.upper() == "PUT":
                    response = await session.put(url, headers=headers, params=params, json=data)
                elif method.upper() == "DELETE":
                    response = await session.delete(url, headers=headers, params=params)
                else:
                    raise ValueError(f"Método HTTP no soportado: {method}")
                
                response.raise_for_status()
                return response.json()
                
            except httpx.RequestError as e:
                if attempt == retries - 1:
                    raise Exception(f"Error de conexión después de {retries} intentos: {e}")
                await asyncio.sleep(2 ** attempt)  # Backoff exponencial
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code >= 500 and attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                raise Exception(f"Error HTTP {e.response.status_code}: {e.response.text}")

    # === APIs de Inteligencia Artificial ===
    
    async def openai_request(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo", max_tokens: int = 100, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Hacer petición a OpenAI API con historial de mensajes
        """
        if not settings.OPENAI_API_KEY:
            raise Exception("OpenAI API key no configurada")
        
        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        return await self.make_request(
            "POST", 
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=data
        )
    
    async def huggingface_request(self, text: str, model: str = "sentiment-analysis") -> Dict[str, Any]:
        """
        Hacer petición a Hugging Face API
        """
        if not settings.HUGGINGFACE_API_KEY:
            raise Exception("Hugging Face API key no configurada")
        
        headers = {
            "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {"inputs": text}
        
        return await self.make_request(
            "POST",
            f"https://api-inference.huggingface.co/models/{model}",
            headers=headers,
            data=data
        )
    
    # === APIs de Datos Externos ===
    
    async def get_weather_data(self, city: str) -> Dict[str, Any]:
        """
        Obtener datos del clima
        """
        if not settings.WEATHER_API_KEY:
            raise Exception("Weather API key no configurada")
        
        params = {
            "q": city,
            "appid": settings.WEATHER_API_KEY,
            "units": "metric",
            "lang": "es"
        }
        
        return await self.make_request(
            "GET",
            "https://api.openweathermap.org/data/2.5/weather",
            params=params
        )
    
    async def get_news_data(self, query: str, language: str = "es") -> Dict[str, Any]:
        """
        Obtener noticias
        """
        if not settings.NEWS_API_KEY:
            raise Exception("News API key no configurada")
        
        params = {
            "q": query,
            "apiKey": settings.NEWS_API_KEY,
            "language": language,
            "sortBy": "publishedAt"
        }
        
        return await self.make_request(
            "GET",
            "https://newsapi.org/v2/everything",
            params=params
        )
    
    async def get_maps_data(self, address: str) -> Dict[str, Any]:
        """
        Obtener datos de geolocalización
        """
        if not settings.MAPS_API_KEY:
            raise Exception("Maps API key no configurada")
        
        params = {
            "address": address,
            "key": settings.MAPS_API_KEY
        }
        
        return await self.make_request(
            "GET",
            "https://maps.googleapis.com/maps/api/geocode/json",
            params=params
        )
    
    # === APIs Personalizadas ===
    
    async def custom_api_request(self, 
                                url: str, 
                                method: str = "GET", 
                                headers: Optional[Dict] = None,
                                params: Optional[Dict] = None,
                                data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Hacer petición a API personalizada
        """
        return await self.make_request(method, url, headers, params, data)

# Instancia global del servicio
external_api_service = ExternalAPIService()

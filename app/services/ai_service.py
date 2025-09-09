import httpx
from typing import Dict, Any
from app.core.config import settings

class AIModelService:
    """
    Servicio para interactuar con el modelo de IA
    """
    
    def __init__(self):
        self.base_url = settings.AI_MODEL_URL
        self.api_key = settings.AI_MODEL_API_KEY
        self.timeout = settings.EXTERNAL_API_TIMEOUT
    
    async def generate_text(self, prompt: str, max_tokens: int = 100, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generar texto usando el modelo de IA
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json={
                        "prompt": prompt,
                        "max_tokens": max_tokens,
                        "temperature": temperature
                    },
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise Exception(f"Error de conexión con el modelo de IA: {e}")
            except httpx.HTTPStatusError as e:
                raise Exception(f"Error HTTP del modelo de IA: {e.response.status_code}")
    
    async def make_prediction(self, data: Dict[str, Any], model_type: str = "classification") -> Dict[str, Any]:
        """
        Hacer predicción usando el modelo de IA
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/predict",
                    json={
                        "data": data,
                        "model_type": model_type
                    },
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise Exception(f"Error de conexión con el modelo de IA: {e}")
            except httpx.HTTPStatusError as e:
                raise Exception(f"Error HTTP del modelo de IA: {e.response.status_code}")
    
    async def check_status(self) -> Dict[str, Any]:
        """
        Verificar el estado del modelo de IA
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/status",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                return {"status": "offline", "error": str(e)}
            except httpx.HTTPStatusError as e:
                return {"status": "error", "error": f"HTTP {e.response.status_code}"}

# Instancia global del servicio
ai_service = AIModelService()

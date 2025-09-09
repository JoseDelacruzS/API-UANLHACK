from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from app.schemas.schemas import AITextRequest, AITextResponse, SentimentRequest, SentimentResponse
from app.services.external_api_service import external_api_service
from app.services.cache_service import cache_service
import time

router = APIRouter()

@router.post("/ai/generate-text", response_model=AITextResponse)
async def generate_text(request: AITextRequest):
    """
    Generar texto usando modelos de IA (OpenAI) - Deprecated, usar /conversations/chat
    """
    try:
        # Verificar caché
        cache_key = f"ai_text_{hash(request.prompt)}_{request.model}_{request.max_tokens}"
        cached_response = await cache_service.get(cache_key)
        
        if cached_response:
            return AITextResponse(**cached_response)
        
        start_time = time.time()
        
        # Llamar a OpenAI con formato de mensaje simple
        messages = [{"role": "user", "content": request.prompt}]
        openai_response = await external_api_service.openai_request(
            messages=messages,
            model=request.model,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        processing_time = time.time() - start_time
        
        # Extraer respuesta
        generated_text = openai_response["choices"][0]["message"]["content"]
        tokens_used = openai_response.get("usage", {}).get("total_tokens", 0)
        
        response_data = {
            "response": generated_text,
            "model": request.model,
            "tokens_used": tokens_used,
            "processing_time": processing_time
        }
        
        # Guardar en caché
        await cache_service.set(cache_key, response_data, duration=3600)  # 1 hora
        
        return AITextResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando texto: {str(e)}")

@router.post("/ai/sentiment-analysis", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """
    Analizar sentimiento usando Hugging Face
    """
    try:
        # Verificar caché
        cache_key = f"sentiment_{hash(request.text)}_{request.model}"
        cached_response = await cache_service.get(cache_key)
        
        if cached_response:
            return SentimentResponse(**cached_response)
        
        # Llamar a Hugging Face
        hf_response = await external_api_service.huggingface_request(
            text=request.text,
            model=request.model
        )
        
        # Procesar respuesta
        if isinstance(hf_response, list) and len(hf_response) > 0:
            result = hf_response[0]
            sentiment = result.get("label", "unknown")
            confidence = result.get("score", 0.0)
        else:
            sentiment = "unknown"
            confidence = 0.0
        
        response_data = {
            "sentiment": sentiment,
            "confidence": confidence,
            "model": request.model
        }
        
        # Guardar en caché
        await cache_service.set(cache_key, response_data, duration=1800)  # 30 minutos
        
        return SentimentResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analizando sentimiento: {str(e)}")

@router.get("/ai/models")
async def list_available_ai_models():
    """
    Listar modelos de IA disponibles
    """
    return {
        "text_generation": {
            "openai": [
                "gpt-3.5-turbo",
                "gpt-4",
                "gpt-4-turbo-preview"
            ]
        },
        "sentiment_analysis": {
            "huggingface": [
                "cardiffnlp/twitter-roberta-base-sentiment-latest",
                "nlptown/bert-base-multilingual-uncased-sentiment",
                "sentiment-analysis"
            ]
        },
        "classification": {
            "huggingface": [
                "facebook/bart-large-mnli",
                "microsoft/DialoGPT-medium"
            ]
        }
    }

@router.post("/ai/custom-model")
async def call_custom_ai_model(model_url: str, payload: Dict[str, Any]):
    """
    Llamar a un modelo de IA personalizado
    """
    try:
        # Verificar caché
        cache_key = f"custom_ai_{hash(str(payload))}_{model_url}"
        cached_response = await cache_service.get(cache_key)
        
        if cached_response:
            return cached_response
        
        start_time = time.time()
        
        # Hacer petición al modelo personalizado
        response = await external_api_service.custom_api_request(
            url=model_url,
            method="POST",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        
        processing_time = time.time() - start_time
        
        result = {
            "response": response,
            "processing_time": processing_time,
            "model_url": model_url
        }
        
        # Guardar en caché
        await cache_service.set(cache_key, result, duration=1800)  # 30 minutos
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en modelo personalizado: {str(e)}")

@router.get("/ai/status")
async def check_ai_services_status():
    """
    Verificar estado de servicios de IA
    """
    from app.core.config import settings
    
    status = {
        "openai": {
            "configured": bool(settings.OPENAI_API_KEY),
            "status": "available" if settings.OPENAI_API_KEY else "not_configured"
        },
        "huggingface": {
            "configured": bool(settings.HUGGINGFACE_API_KEY),
            "status": "available" if settings.HUGGINGFACE_API_KEY else "not_configured"
        },
        "anthropic": {
            "configured": bool(settings.ANTHROPIC_API_KEY),
            "status": "available" if settings.ANTHROPIC_API_KEY else "not_configured"
        }
    }
    
    return {
        "ai_services": status,
        "last_check": time.time(),
        "note": "Para chat con historial, usar /conversations/chat"
    }

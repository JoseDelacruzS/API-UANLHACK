"""
🔧 Endpoints para generar especificación OpenAPI para Watson Orchestrate
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import json

router = APIRouter()

@router.get("/watson-openapi.json")
async def get_watson_openapi_spec() -> JSONResponse:
    """
    📋 Generar especificación OpenAPI específica para Watson Orchestrate
    
    Esta especificación incluye solo las operaciones que Watson puede ejecutar:
    - Crear tickets
    - Programar visitas
    - Enviar notificaciones
    - Generar reportes
    - Consultar estados
    """
    
    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "UANL Automation System",
            "version": "1.0.0",
            "description": "API para Watson Orchestrate - Sistema de automatización UANL. Crear tickets, programar visitas, enviar notificaciones y generar reportes."
        },
        "servers": [
            {
                "url": "http://localhost:8001/api/v1"
            }
        ],
        "paths": {
            "/watson/create-ticket": {
                "post": {
                    "summary": "Crear ticket de soporte",
                    "operationId": "create_ticket_post",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["title", "description"],
                                    "properties": {
                                        "title": {
                                            "type": "string",
                                            "description": "Título del ticket"
                                        },
                                        "description": {
                                            "type": "string",
                                            "description": "Descripción del problema"
                                        },
                                        "priority": {
                                            "type": "string",
                                            "description": "Prioridad del ticket",
                                            "enum": ["low", "medium", "high", "urgent"]
                                        },
                                        "client_ref": {
                                            "type": "string", 
                                            "description": "Referencia del cliente"
                                        }
                                    }
                                },
                                "example": {
                                    "title": "Problema con el sistema",
                                    "description": "El sistema no responde correctamente",
                                    "priority": "medium",
                                    "client_ref": "CLI-001"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Ticket creado exitosamente",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {
                                                "type": "boolean",
                                                "description": "Indica si la operación fue exitosa"
                                            },
                                            "ticket_id": {
                                                "type": "string",
                                                "description": "ID del ticket creado"
                                            },
                                            "message": {
                                                "type": "string",
                                                "description": "Mensaje de confirmación"
                                            }
                                        }
                                    },
                                    "example": {
                                        "success": True,
                                        "ticket_id": "TKT-20241201001",
                                        "message": "Ticket creado exitosamente"
                                    }
                                }
                            }
                        },
                        "422": {
                            "description": "Error de validación"
                        }
                    }
                }
            },
            "/watson/schedule-visit": {
                "post": {
                    "summary": "Programar visita técnica",
                    "operationId": "schedule_visit_post",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["client_ref", "visit_type"],
                                    "properties": {
                                        "client_ref": {
                                            "type": "string",
                                            "description": "Referencia del cliente"
                                        },
                                        "visit_type": {
                                            "type": "string",
                                            "description": "Tipo de visita"
                                        },
                                        "preferred_date": {
                                            "type": "string",
                                            "description": "Fecha preferida"
                                        },
                                        "description": {
                                            "type": "string",
                                            "description": "Descripción de la visita"
                                        }
                                    }
                                },
                                "example": {
                                    "client_ref": "CLI-001",
                                    "visit_type": "mantenimiento",
                                    "preferred_date": "2024-12-15",
                                    "description": "Mantenimiento preventivo"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Visita programada exitosamente",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {
                                                "type": "boolean"
                                            },
                                            "visit_id": {
                                                "type": "string"
                                            },
                                            "message": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "example": {
                                        "success": True,
                                        "visit_id": "VIS-20241201001",
                                        "message": "Visita programada exitosamente"
                                    }
                                }
                            }
                        },
                        "422": {
                            "description": "Error de validación"
                        }
                    }
                }
            },
            "/watson/get-status": {
                "post": {
                    "summary": "Consultar estado de tickets",
                    "operationId": "get_status_post",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["query_type"],
                                    "properties": {
                                        "query_type": {
                                            "type": "string",
                                            "description": "Tipo de consulta"
                                        },
                                        "entity_id": {
                                            "type": "string",
                                            "description": "ID de la entidad a consultar"
                                        }
                                    }
                                },
                                "example": {
                                    "query_type": "ticket",
                                    "entity_id": "TKT-001"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Estado consultado exitosamente",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {
                                                "type": "boolean"
                                            },
                                            "status": {
                                                "type": "string"
                                            },
                                            "details": {
                                                "type": "object"
                                            }
                                        }
                                    },
                                    "example": {
                                        "success": True,
                                        "status": "open",
                                        "details": {"priority": "medium", "created": "2024-12-01"}
                                    }
                                }
                            }
                        },
                        "422": {
                            "description": "Error de validación"
                        }
                    }
                }
            },
            "/watson/analyze-conversation": {
                "post": {
                    "summary": "Analizar conversación telefónica",
                    "operationId": "analyze_conversation_post",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["conversation", "operator_id", "client_ref"],
                                    "properties": {
                                        "conversation": {
                                            "type": "string",
                                            "description": "Texto completo de la conversación"
                                        },
                                        "operator_id": {
                                            "type": "integer",
                                            "description": "ID del operador"
                                        },
                                        "client_ref": {
                                            "type": "string",
                                            "description": "Referencia del cliente"
                                        },
                                        "call_date": {
                                            "type": "string",
                                            "description": "Fecha de la llamada"
                                        },
                                        "call_label": {
                                            "type": "string",
                                            "description": "Etiqueta de la llamada"
                                        }
                                    }
                                },
                                "example": {
                                    "conversation": "Operador: Sí, muy buenas noches, caballero. Me comunico por parte de soporte técnico...",
                                    "operator_id": 1,
                                    "client_ref": "CLI-001",
                                    "call_date": "2025-03-03",
                                    "call_label": "llamada 1"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Conversación analizada exitosamente",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {
                                                "type": "boolean"
                                            },
                                            "call_id": {
                                                "type": "string"
                                            },
                                            "analysis": {
                                                "type": "object",
                                                "properties": {
                                                    "call_analysis": {
                                                        "type": "object",
                                                        "properties": {
                                                            "problem_type": {"type": "string"},
                                                            "urgency_level": {"type": "string"},
                                                            "customer_sentiment": {"type": "string"},
                                                            "resolution_status": {"type": "string"},
                                                            "follow_up_required": {"type": "boolean"}
                                                        }
                                                    },
                                                    "extracted_entities": {"type": "object"},
                                                    "recommended_actions": {
                                                        "type": "array",
                                                        "items": {"type": "string"}
                                                    },
                                                    "summary": {"type": "string"}
                                                }
                                            },
                                            "message": {
                                                "type": "string"
                                            }
                                        }
                                    },
                                    "example": {
                                        "success": True,
                                        "call_id": "CALL-20241201001",
                                        "analysis": {
                                            "call_analysis": {
                                                "problem_type": "lentitud_servicio",
                                                "urgency_level": "medium",
                                                "customer_sentiment": "neutral",
                                                "resolution_status": "pending_verification",
                                                "follow_up_required": True
                                            },
                                            "extracted_entities": {
                                                "hora_callback": "21:00",
                                                "problema_especifico": "indicador_conexion_baja",
                                                "ajustes_realizados": True
                                            },
                                            "recommended_actions": ["programar_callback", "verificar_ajustes_realizados"],
                                            "summary": "Cliente reporta lentitud. Ajustes realizados. Callback programado 21:00."
                                        },
                                        "message": "Conversación analizada exitosamente"
                                    }
                                }
                            }
                        },
                        "422": {
                            "description": "Error de validación"
                        }
                    }
                }
            }
        }
    }
    
    return JSONResponse(content=openapi_spec)

@router.get("/watson-integration-guide")
async def get_watson_integration_guide() -> Dict[str, Any]:
    """
    📚 Guía de integración con Watson Orchestrate
    
    Proporciona documentación sobre cómo integrar Watson con el sistema
    """
    
    guide = {
        "integration_types": {
            "webhooks": {
                "description": "Watson envía requests HTTP a nuestros endpoints",
                "pros": [
                    "Push-based: Watson inicia la comunicación",
                    "Tiempo real: Respuesta inmediata",
                    "Contexto conversacional: Mantiene estado de sesión",
                    "Flexibilidad: Manejo completo del flujo"
                ],
                "cons": [
                    "Requiere configuración de webhooks en Watson",
                    "Necesita manejo de autenticación",
                    "Más complejo para debugging"
                ],
                "endpoint": "/api/v1/watson/webhook",
                "setup_steps": [
                    "1. Configurar webhook URL en Watson Orchestrate",
                    "2. Establecer autenticación (API Key o Bearer Token)",
                    "3. Configurar payload format en Watson",
                    "4. Testear con payloads de ejemplo"
                ]
            },
            "openapi_consumption": {
                "description": "Watson consume nuestras APIs usando especificación OpenAPI",
                "pros": [
                    "Pull-based: Watson llama nuestras APIs cuando necesita",
                    "Estándar: Usa OpenAPI 3.0 estándar",
                    "Simple: Watson maneja la orquestación",
                    "Escalable: Fácil agregar nuevas acciones"
                ],
                "cons": [
                    "Sin contexto conversacional persistente",
                    "Watson debe manejar la lógica de flujo",
                    "Menos control sobre la experiencia"
                ],
                "openapi_url": "/api/v1/openapi/watson-openapi.json",
                "setup_steps": [
                    "1. Obtener especificación OpenAPI de este endpoint",
                    "2. Importar spec en Watson Orchestrate",
                    "3. Configurar autenticación en Watson",
                    "4. Mapear acciones a skills de Watson"
                ]
            }
        },
        "recommended_approach": {
            "hybrid": {
                "description": "Combinar ambos enfoques para máxima flexibilidad",
                "use_webhook_for": [
                    "Conversaciones complejas que requieren contexto",
                    "Flujos de múltiples pasos",
                    "Casos donde necesitamos controlar la experiencia"
                ],
                "use_openapi_for": [
                    "Acciones simples y directas",
                    "Consultas de información",
                    "Operaciones CRUD básicas"
                ]
            }
        },
        "authentication": {
            "api_key": {
                "header": "X-API-Key",
                "description": "API Key para autenticación simple"
            },
            "bearer_token": {
                "header": "Authorization: Bearer <token>",
                "description": "JWT token para autenticación avanzada"
            }
        },
        "examples": {
            "webhook_request": {
                "url": "/api/v1/watson/webhook",
                "method": "POST",
                "payload": {
                    "session_id": "session_123",
                    "user_id": "watson_user",
                    "message": "Crear un ticket para problema de red",
                    "intent": "crear_ticket",
                    "entities": {
                        "problema": "problema de red",
                        "prioridad": "medium"
                    },
                    "context": {
                        "cliente_id": "CLI-001"
                    }
                }
            },
            "openapi_action": {
                "url": "/api/v1/watson/action/create-ticket",
                "method": "POST", 
                "payload": {
                    "title": "Problema de red",
                    "description": "La red no funciona correctamente",
                    "priority": "medium",
                    "client_ref": "CLI-001",
                    "watson_session_id": "session_123"
                }
            }
        },
        "testing": {
            "webhook_test": "curl -X POST http://localhost:8000/api/v1/watson/webhook -H 'Content-Type: application/json' -d '{...}'",
            "openapi_test": "curl -X POST http://localhost:8000/api/v1/watson/action/create-ticket -H 'Content-Type: application/json' -d '{...}'"
        }
    }
    
    return guide

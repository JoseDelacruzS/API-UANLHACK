from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from loguru import logger


async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """Manejador personalizado de excepciones HTTP"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "message": exc.detail,
            "path": str(request.url.path)
        }
    )


class APIException(Exception):
    """Excepción base para la API"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(APIException):
    """Error de validación"""
    def __init__(self, message: str):
        super().__init__(message, 400)


class NotFoundError(APIException):
    """Error de recurso no encontrado"""
    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message, 404)


class UnauthorizedError(APIException):
    """Error de autorización"""
    def __init__(self, message: str = "No autorizado"):
        super().__init__(message, 401)


class ForbiddenError(APIException):
    """Error de permisos"""
    def __init__(self, message: str = "Acceso prohibido"):
        super().__init__(message, 403)


class ConflictError(APIException):
    """Error de conflicto"""
    def __init__(self, message: str = "Conflicto"):
        super().__init__(message, 409)

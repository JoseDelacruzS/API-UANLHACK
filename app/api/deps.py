from fastapi import Depends
from sqlalchemy.orm import Session
from app.config.database import get_db


def get_current_db(db: Session = Depends(get_db)) -> Session:
    """Dependencia para obtener la sesión de base de datos"""
    return db


def get_pagination_params(page: int = 1, page_size: int = 20) -> dict:
    """Dependencia para parámetros de paginación"""
    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 20
    
    return {
        "page": page,
        "page_size": page_size,
        "offset": (page - 1) * page_size
    }

from typing import Any, Dict, List, Optional
from datetime import datetime, date
import json
import re


def format_response(
    data: Any, 
    message: str = "Success", 
    status_code: int = 200
) -> Dict[str, Any]:
    """Formatear respuesta estándar de la API"""
    return {
        "status_code": status_code,
        "message": message,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }


def paginate_response(
    items: List[Any],
    page: int,
    page_size: int,
    total: int
) -> Dict[str, Any]:
    """Formatear respuesta paginada"""
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }


def sanitize_filename(filename: str) -> str:
    """Sanitizar nombre de archivo"""
    # Remover caracteres especiales
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limitar longitud
    if len(filename) > 100:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:95] + ('.' + ext if ext else '')
    
    return filename


def calculate_percentage(part: int, total: int) -> float:
    """Calcular porcentaje"""
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)


def format_duration(seconds: int) -> str:
    """Formatear duración en segundos a formato legible"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{hours}h {remaining_minutes}m"


def safe_json_loads(json_string: Optional[str]) -> Optional[Dict[str, Any]]:
    """Cargar JSON de forma segura"""
    if not json_string:
        return None
    
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return None


def safe_json_dumps(data: Any) -> str:
    """Convertir a JSON de forma segura"""
    try:
        return json.dumps(data, default=str, ensure_ascii=False)
    except (TypeError, ValueError):
        return "{}"


def generate_ticket_number() -> str:
    """Generar número de ticket único"""
    now = datetime.now()
    return f"TKT-{now.strftime('%Y%m%d')}-{now.strftime('%H%M%S')}"


def extract_keywords(text: str) -> List[str]:
    """Extraer palabras clave de texto"""
    if not text:
        return []
    
    # Palabras comunes a ignorar
    stop_words = {
        'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le',
        'da', 'su', 'por', 'son', 'con', 'para', 'como', 'las', 'si', 'al', 'del', 'los',
        'una', 'me', 'mi', 'tu', 'yo', 'él', 'ella', 'nos', 'os', 'ellos', 'ellas'
    }
    
    # Extraer palabras (solo letras, mínimo 3 caracteres)
    words = re.findall(r'\b[a-záéíóúñ]{3,}\b', text.lower())
    
    # Filtrar stop words
    keywords = [word for word in words if word not in stop_words]
    
    # Remover duplicados manteniendo orden
    unique_keywords = []
    seen = set()
    for keyword in keywords:
        if keyword not in seen:
            unique_keywords.append(keyword)
            seen.add(keyword)
    
    return unique_keywords[:10]  # Máximo 10 palabras clave


def mask_sensitive_data(data: str, mask_char: str = "*") -> str:
    """Enmascarar datos sensibles"""
    if not data or len(data) < 4:
        return mask_char * len(data) if data else ""
    
    # Mostrar primeros 2 y últimos 2 caracteres
    return data[:2] + mask_char * (len(data) - 4) + data[-2:]


def format_phone_number(phone: str) -> str:
    """Formatear número telefónico"""
    # Remover todos los caracteres no numéricos
    digits = re.sub(r'\D', '', phone)
    
    # Formatear según longitud
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return phone  # Devolver original si no coincide con formato esperado

import os
import json
import aiofiles
from datetime import datetime, timedelta
from typing import Any, Optional
from app.core.config import settings

class LocalCacheService:
    """
    Servicio de caché local usando archivos
    """
    
    def __init__(self):
        self.cache_dir = settings.CACHE_DIR
        self._ensure_cache_dir()
    
    def _ensure_cache_dir(self):
        """Crear directorio de caché si no existe"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _get_cache_file_path(self, key: str) -> str:
        """Obtener ruta del archivo de caché"""
        safe_key = key.replace("/", "_").replace(":", "_")
        return os.path.join(self.cache_dir, f"{safe_key}.json")
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Obtener valor del caché
        """
        try:
            file_path = self._get_cache_file_path(key)
            
            if not os.path.exists(file_path):
                return None
            
            async with aiofiles.open(file_path, 'r') as f:
                content = await f.read()
                cache_data = json.loads(content)
            
            # Verificar si el caché ha expirado
            expiry_time = datetime.fromisoformat(cache_data['expiry'])
            if datetime.now() > expiry_time:
                await self.delete(key)
                return None
            
            return cache_data['value']
            
        except Exception as e:
            print(f"Error leyendo caché para {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, duration: Optional[int] = None) -> bool:
        """
        Guardar valor en el caché
        """
        try:
            if duration is None:
                duration = settings.CACHE_DURATION
            
            expiry_time = datetime.now() + timedelta(seconds=duration)
            
            cache_data = {
                'value': value,
                'expiry': expiry_time.isoformat(),
                'created': datetime.now().isoformat()
            }
            
            file_path = self._get_cache_file_path(key)
            
            async with aiofiles.open(file_path, 'w') as f:
                await f.write(json.dumps(cache_data, default=str))
            
            return True
            
        except Exception as e:
            print(f"Error guardando caché para {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Eliminar valor del caché
        """
        try:
            file_path = self._get_cache_file_path(key)
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return True
            
        except Exception as e:
            print(f"Error eliminando caché para {key}: {e}")
            return False
    
    async def clear_all(self) -> bool:
        """
        Limpiar todo el caché
        """
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(self.cache_dir, filename)
                    os.remove(file_path)
            
            return True
            
        except Exception as e:
            print(f"Error limpiando caché: {e}")
            return False
    
    async def get_cache_stats(self) -> dict:
        """
        Obtener estadísticas del caché
        """
        try:
            files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
            total_files = len(files)
            total_size = 0
            expired_files = 0
            
            for filename in files:
                file_path = os.path.join(self.cache_dir, filename)
                total_size += os.path.getsize(file_path)
                
                # Verificar si está expirado
                try:
                    async with aiofiles.open(file_path, 'r') as f:
                        content = await f.read()
                        cache_data = json.loads(content)
                    
                    expiry_time = datetime.fromisoformat(cache_data['expiry'])
                    if datetime.now() > expiry_time:
                        expired_files += 1
                except:
                    expired_files += 1
            
            return {
                'total_files': total_files,
                'total_size_bytes': total_size,
                'expired_files': expired_files,
                'active_files': total_files - expired_files
            }
            
        except Exception as e:
            return {'error': str(e)}

# Instancia global del servicio de caché
cache_service = LocalCacheService()

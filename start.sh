#!/bin/bash

# Script de inicio rápido para API UANL Hack

echo "🚀 Iniciando API UANL Hack..."

# Verificar si existe el archivo .env
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde .env.example..."
    cp .env.example .env
    echo "⚠️  Por favor, edita el archivo .env con tus credenciales reales"
fi

# Crear directorio de caché si no existe
if [ ! -d "cache" ]; then
    echo "📁 Creando directorio de caché..."
    mkdir cache
fi

# Opción 1: Ejecutar con Docker
echo ""
echo "Selecciona una opción de ejecución:"
echo "1) Docker Compose (Recomendado)"
echo "2) Local (requiere PostgreSQL instalado)"
read -p "Opción (1 o 2): " option

case $option in
    1)
        echo "🐳 Iniciando con Docker Compose..."
        
        # Verificar si Docker está corriendo
        if ! docker info > /dev/null 2>&1; then
            echo "❌ Docker no está corriendo. Por favor, inicia Docker Desktop."
            exit 1
        fi
        
        # Construir e iniciar servicios
        echo "🏗️  Construyendo contenedores..."
        docker-compose build
        
        echo "▶️  Iniciando servicios..."
        docker-compose up -d
        
        echo "⏳ Esperando que los servicios estén listos..."
        sleep 10
        
        # Ejecutar script de inicialización de la base de datos
        echo "🗄️  Inicializando base de datos..."
        docker-compose exec api python init_db.py
        
        echo ""
        echo "✅ API iniciada correctamente!"
        echo "📖 Documentación: http://localhost:8000/docs"
        echo "🔍 API: http://localhost:8000"
        echo "🗄️  PostgreSQL: localhost:5432"
        
        # Mostrar logs
        echo ""
        echo "📋 Logs en tiempo real (Ctrl+C para salir):"
        docker-compose logs -f api
        ;;
    2)
        echo "💻 Iniciando en modo local..."
        
        # Verificar si existe el entorno virtual
        if [ ! -d "venv" ]; then
            echo "🐍 Creando entorno virtual..."
            python3 -m venv venv
        fi
        
        # Activar entorno virtual
        echo "📦 Activando entorno virtual..."
        source venv/bin/activate
        
        # Instalar dependencias
        echo "📥 Instalando dependencias..."
        pip install -r requirements.txt
        
        # Verificar PostgreSQL
        echo "🔍 Verificando conexión a PostgreSQL..."
        python -c "
import psycopg2
try:
    conn = psycopg2.connect('postgresql://postgres:password@localhost:5432/uanl_hack_db')
    print('✅ Conexión a PostgreSQL exitosa')
    conn.close()
except Exception as e:
    print(f'❌ Error conectando a PostgreSQL: {e}')
    print('Por favor, asegúrate de que PostgreSQL esté corriendo')
    exit(1)
"
        
        # Inicializar base de datos
        echo "🗄️  Inicializando base de datos..."
        python init_db.py
        
        # Iniciar servidor
        echo "▶️  Iniciando servidor FastAPI..."
        echo ""
        echo "✅ API iniciada correctamente!"
        echo "📖 Documentación: http://localhost:8000/docs"
        echo "🔍 API: http://localhost:8000"
        
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    *)
        echo "❌ Opción inválida"
        exit 1
        ;;
esac

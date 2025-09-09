#!/bin/bash

# Script de inicialización y configuración del proyecto
# UANL Automation API

echo "🚀 Iniciando configuración del proyecto UANL Automation API"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor, instale Docker primero."
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado. Por favor, instale Docker Compose primero."
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    print_message "Creando archivo .env desde .env.example..."
    cp .env.example .env
    print_warning "¡IMPORTANTE! Edita el archivo .env con tus configuraciones reales antes de continuar."
    print_message "Archivo .env creado. Configurando valores por defecto..."
    
    # Generar SECRET_KEY
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    sed -i '' "s/your-super-secret-key-change-this/$SECRET_KEY/" .env
    
    print_message "SECRET_KEY generada automáticamente."
else
    print_message "Archivo .env ya existe."
fi

# Crear directorios necesarios
print_message "Creando directorios necesarios..."
mkdir -p logs
mkdir -p uploads
mkdir -p temp
mkdir -p backups

# Dar permisos de escritura
chmod 755 logs uploads temp backups

print_message "Estructura de directorios creada."

# Función para mostrar ayuda
show_help() {
    echo "Uso: $0 [OPCIÓN]"
    echo ""
    echo "Opciones:"
    echo "  dev         Iniciar en modo desarrollo"
    echo "  prod        Iniciar en modo producción"
    echo "  build       Construir imágenes Docker"
    echo "  stop        Detener todos los servicios"
    echo "  restart     Reiniciar todos los servicios"
    echo "  logs        Ver logs de todos los servicios"
    echo "  db-init     Inicializar base de datos"
    echo "  db-migrate  Ejecutar migraciones"
    echo "  test        Ejecutar pruebas"
    echo "  help        Mostrar esta ayuda"
}

# Función para iniciar en modo desarrollo
start_dev() {
    print_message "Iniciando servicios en modo desarrollo..."
    docker-compose -f docker-compose.yml up --build
}

# Función para iniciar en modo producción
start_prod() {
    print_message "Iniciando servicios en modo producción..."
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
}

# Función para construir imágenes
build_images() {
    print_message "Construyendo imágenes Docker..."
    docker-compose build
}

# Función para detener servicios
stop_services() {
    print_message "Deteniendo todos los servicios..."
    docker-compose down
}

# Función para reiniciar servicios
restart_services() {
    print_message "Reiniciando servicios..."
    docker-compose restart
}

# Función para ver logs
show_logs() {
    print_message "Mostrando logs de servicios..."
    docker-compose logs -f
}

# Función para inicializar base de datos
init_db() {
    print_message "Inicializando base de datos..."
    docker-compose up -d db
    sleep 10
    docker-compose exec api python -c "
from app.config.database import engine
from app.models import *
import app.models.base
app.models.base.Base.metadata.create_all(bind=engine)
print('Base de datos inicializada')
"
}

# Función para ejecutar migraciones
run_migrations() {
    print_message "Ejecutando migraciones..."
    docker-compose exec api alembic upgrade head
}

# Función para ejecutar pruebas
run_tests() {
    print_message "Ejecutando pruebas..."
    docker-compose exec api python -m pytest tests/ -v
}

# Verificar argumentos
case ${1} in
    dev)
        start_dev
        ;;
    prod)
        start_prod
        ;;
    build)
        build_images
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        show_logs
        ;;
    db-init)
        init_db
        ;;
    db-migrate)
        run_migrations
        ;;
    test)
        run_tests
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_message "Configuración completada."
        echo ""
        print_message "Comandos disponibles:"
        show_help
        echo ""
        print_message "Para iniciar en modo desarrollo: ./setup.sh dev"
        print_message "Para ver la documentación: http://localhost:8000/api/v1/docs"
        ;;
esac

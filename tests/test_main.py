import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connection import Base, get_db
from main import app

# Base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas de prueba
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_root_endpoint():
    """Test del endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    assert "API UANL Hack" in response.json()["message"]

def test_health_endpoint():
    """Test del endpoint de salud"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_detailed_health_endpoint():
    """Test del endpoint de salud detallado"""
    response = client.get("/api/v1/health/detailed")
    assert response.status_code == 200
    assert "database" in response.json()

def test_ai_models_endpoint():
    """Test del endpoint de modelos de IA"""
    response = client.get("/api/v1/ai/models")
    assert response.status_code == 200
    assert "text_generation" in response.json()

def test_create_user():
    """Test crear usuario"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User"
    }
    response = client.post("/api/v1/conversations/users", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_create_conversation():
    """Test crear conversación"""
    # Primero crear un usuario
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com"
    }
    user_response = client.post("/api/v1/conversations/users", json=user_data)
    user_id = user_response.json()["id"]
    
    # Crear conversación
    response = client.post(f"/api/v1/conversations?user_id={user_id}&title=Test Conversation")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Conversation"

def test_get_conversations():
    """Test obtener conversaciones"""
    # Usar el usuario creado anteriormente
    response = client.get("/api/v1/conversations/1")  # user_id = 1
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_ai_generate_text():
    """Test generar texto con IA (sin API key real)"""
    test_data = {
        "prompt": "Hola, ¿cómo estás?",
        "model": "gpt-3.5-turbo",
        "max_tokens": 50,
        "temperature": 0.7
    }
    response = client.post("/api/v1/ai/generate-text", json=test_data)
    # Esperamos error por falta de API key, pero el endpoint debe existir
    assert response.status_code in [200, 500]  # 500 por falta de API key

def test_cache_stats():
    """Test estadísticas de caché"""
    response = client.get("/api/v1/cache/stats")
    assert response.status_code == 200
    assert "total_files" in response.json()

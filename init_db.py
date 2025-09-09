"""
Script para inicializar la base de datos con datos de ejemplo
"""
from sqlalchemy.orm import sessionmaker
from app.database.connection import engine, Base
from app.models.models import User, Conversation, Message
from datetime import datetime

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def create_sample_data():
    """Crear datos de ejemplo"""
    
    # Verificar si ya existen datos
    existing_user = session.query(User).first()
    if existing_user:
        print("Los datos de ejemplo ya existen.")
        return
    
    print("Creando datos de ejemplo...")
    
    # Crear usuarios de ejemplo
    user1 = User(
        username="admin",
        email="admin@uanl.hack",
        full_name="Administrador UANL Hack",
        is_active=True
    )
    
    user2 = User(
        username="demo_user",
        email="demo@uanl.hack",
        full_name="Usuario Demo",
        is_active=True
    )
    
    session.add_all([user1, user2])
    session.commit()
    session.refresh(user1)
    session.refresh(user2)
    
    # Crear conversación de ejemplo
    conversation1 = Conversation(
        title="Conversación de prueba con IA",
        user_id=user1.id,
        model_used="gpt-3.5-turbo",
        total_messages=2,
        total_tokens=150,
        is_active=True
    )
    
    session.add(conversation1)
    session.commit()
    session.refresh(conversation1)
    
    # Crear mensajes de ejemplo
    message1 = Message(
        conversation_id=conversation1.id,
        role="user",
        content="¡Hola! ¿Cómo puedes ayudarme?",
        tokens_used=25,
        model_used="gpt-3.5-turbo"
    )
    
    message2 = Message(
        conversation_id=conversation1.id,
        role="assistant",
        content="¡Hola! Soy un asistente de IA. Puedo ayudarte con preguntas, generar texto, analizar información y mucho más. ¿En qué te puedo ayudar hoy?",
        tokens_used=125,
        model_used="gpt-3.5-turbo",
        response_time=1.2,
        metadata={"temperature": 0.7, "max_tokens": 150}
    )
    
    session.add_all([message1, message2])
    session.commit()
    
    print("✅ Datos de ejemplo creados exitosamente:")
    print(f"   - Usuario 1: {user1.username} ({user1.email})")
    print(f"   - Usuario 2: {user2.username} ({user2.email})")
    print(f"   - Conversación: {conversation1.title}")
    print(f"   - Mensajes: {len([message1, message2])}")

if __name__ == "__main__":
    try:
        create_sample_data()
        print("\n🚀 Base de datos inicializada correctamente")
        print("Puedes iniciar la API con: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error inicializando la base de datos: {e}")
    finally:
        session.close()

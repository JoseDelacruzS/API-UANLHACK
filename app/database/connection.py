from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from app.core.config import settings

# Configuración de la base de datos
database = Database(settings.DATABASE_URL)
metadata = MetaData()

# Para SQLAlchemy ORM
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

async def connect_db():
    """Conectar a la base de datos"""
    await database.connect()

async def disconnect_db():
    """Desconectar de la base de datos"""
    await database.disconnect()

def get_db():
    """
    Dependencia para obtener la sesión de la base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_database():
    """
    Dependencia para obtener la conexión async de la base de datos
    """
    return database

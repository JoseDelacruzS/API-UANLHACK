from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.config.settings import settings

# Metadatos para el esquema (sin schema por defecto para evitar errores si no existe)
metadata = MetaData()

# Base para modelos SQLAlchemy
Base = declarative_base(metadata=metadata)

# Motor síncrono (inicialización perezosa)
engine = None

# Sesión síncrona
SessionLocal = None

# Motor asíncrono (inicialización perezosa) 
async_engine = None

def initialize_database():
    """Inicializar la base de datos solo cuando sea necesario"""
    global engine, SessionLocal, async_engine
    
    if engine is None:
        try:
            engine = create_engine(
                settings.database_url_sync,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
                echo=settings.ENVIRONMENT == "development"
            )
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            
            async_engine = create_async_engine(
                settings.database_url_async,
                pool_pre_ping=True,
                pool_size=10,
                max_overflow=20,
                echo=settings.ENVIRONMENT == "development"
            )
        except Exception as e:
            print(f"Warning: No se pudo conectar a la base de datos: {e}")
            # Para desarrollo sin BD, usar SQLite en memoria
            engine = create_engine("sqlite:///./test.db", echo=True)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependencia para obtener sesión de base de datos síncrona"""
    initialize_database()
    if SessionLocal is None:
        raise RuntimeError("Base de datos no inicializada")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    """Dependencia para obtener sesión de base de datos asíncrona"""
    initialize_database()
    if async_engine is None:
        raise RuntimeError("Motor asíncrono no inicializado")
        
    AsyncSessionLocal = sessionmaker(
        async_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with AsyncSessionLocal() as session:
        yield session

from app.database.connection import engine
from app.core.config import settings

if __name__ == "__main__":
    print(f"Cadena de conexión: {settings.DATABASE_URL}")
    try:
        conn = engine.connect()
        print("Conexión exitosa a la base de datos Hackaton-IBM.")
        conn.close()
    except Exception as e:
        import traceback
        print("Error al conectar:")
        traceback.print_exc()

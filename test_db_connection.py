from app.config.database import initialize_database

if __name__ == "__main__":
    try:
        initialize_database()
        print("Conexión exitosa a la base de datos PostgreSQL en Supabase.")
    except Exception as e:
        print(f"Error al conectar: {e}")

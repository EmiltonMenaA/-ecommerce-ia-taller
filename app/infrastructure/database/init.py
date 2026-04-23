"""Script para inicializar la base de datos.

Uso:
    python -m app.infrastructure.database.init
"""

def create_tables() -> None:
    """Crea todas las tablas en la base de datos.
    
    Esta función debe ejecutarse una sola vez al iniciar la aplicación
    o cuando sea necesario reinicializar la base de datos.
    """
    from app.infrastructure.database import engine, Base
    
    print("📦 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")


if __name__ == "__main__":
    create_tables()

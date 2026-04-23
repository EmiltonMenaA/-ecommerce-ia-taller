"""Configuración de conexión a la base de datos SQLite."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

load_dotenv()

# Crear engine SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    """Obtiene una sesión de base de datos.

    Crea una nueva sesión de SQLAlchemy y la cede al consumidor.
    Asegura que la sesión se cierre correctamente al finalizar.

    Retorna:
        Session: Sesión de SQLAlchemy para ejecutar operaciones de BD.

    Ejemplo:
        for db in get_session():
            # usar db
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

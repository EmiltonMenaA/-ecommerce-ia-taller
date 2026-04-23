"""Configuración de base de datos."""

def __getattr__(name: str):
    """Lazy loading para evitar importar SQLAlchemy en startup."""
    if name == "engine":
        from app.infrastructure.database.connection import engine
        return engine
    elif name == "SessionLocal":
        from app.infrastructure.database.connection import SessionLocal
        return SessionLocal
    elif name == "get_session":
        from app.infrastructure.database.connection import get_session
        return get_session
    elif name == "Base":
        from app.infrastructure.database.models import Base
        return Base
    elif name == "ProductModel":
        from app.infrastructure.database.models import ProductModel
        return ProductModel
    elif name == "ChatMessageModel":
        from app.infrastructure.database.models import ChatMessageModel
        return ChatMessageModel
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["engine", "SessionLocal", "get_session", "Base", "ProductModel", "ChatMessageModel"]

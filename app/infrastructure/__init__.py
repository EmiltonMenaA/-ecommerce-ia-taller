"""Capa de infraestructura."""

def __getattr__(name: str):
    """Lazy loading de módulos de infraestructura para evitar importar SQLAlchemy en startup."""
    if name == "engine":
        from app.infrastructure.database import engine
        return engine
    elif name == "SessionLocal":
        from app.infrastructure.database import SessionLocal
        return SessionLocal
    elif name == "get_session":
        from app.infrastructure.database import get_session
        return get_session
    elif name == "Base":
        from app.infrastructure.database import Base
        return Base
    elif name == "ProductModel":
        from app.infrastructure.database import ProductModel
        return ProductModel
    elif name == "ChatMessageModel":
        from app.infrastructure.database import ChatMessageModel
        return ChatMessageModel
    elif name == "ProductRepository":
        from app.infrastructure.repositories import ProductRepository
        return ProductRepository
    elif name == "ChatRepository":
        from app.infrastructure.repositories import ChatRepository
        return ChatRepository
    elif name == "GeminiService":
        from app.infrastructure.external import GeminiService
        return GeminiService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "engine",
    "SessionLocal",
    "get_session",
    "Base",
    "ProductModel",
    "ChatMessageModel",
    "ProductRepository",
    "ChatRepository",
    "GeminiService",
]

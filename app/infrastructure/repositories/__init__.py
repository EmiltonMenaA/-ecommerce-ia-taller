"""Repositorios de infraestructura."""

def __getattr__(name: str):
    """Lazy loading para evitar imports circulares."""
    if name == "ProductRepository":
        from app.infrastructure.repositories.product_repository import ProductRepository
        return ProductRepository
    elif name == "ChatRepository":
        from app.infrastructure.repositories.chat_repository import ChatRepository
        return ChatRepository
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["ProductRepository", "ChatRepository"]

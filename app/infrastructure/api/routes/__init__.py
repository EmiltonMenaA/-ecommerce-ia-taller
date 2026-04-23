"""Rutas de la API."""
from app.infrastructure.api.routes.products import router as products_router
from app.infrastructure.api.routes.chat import router as chat_router

__all__ = ["products_router", "chat_router"]

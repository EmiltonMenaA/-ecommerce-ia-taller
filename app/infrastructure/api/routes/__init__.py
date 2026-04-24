"""Rutas de la API."""
from app.infrastructure.api.routes.products import router as products_router
from app.infrastructure.api.routes.chat import router as chat_router
from app.infrastructure.api.routes.chat_simple import router as chat_simple_router

__all__ = ["products_router", "chat_router", "chat_simple_router"]

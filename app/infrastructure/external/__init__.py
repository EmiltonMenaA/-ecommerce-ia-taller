"""Servicios externos."""

def __getattr__(name: str):
    """Lazy loading para evitar imports circulares."""
    if name == "GeminiService":
        from app.infrastructure.external.gemini_service import GeminiService
        return GeminiService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["GeminiService"]

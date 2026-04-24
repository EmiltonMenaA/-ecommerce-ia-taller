"""Ruta simple para verificar disponibilidad del modulo de chat."""
from fastapi import APIRouter, status


router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/test", status_code=status.HTTP_200_OK)
async def chat_test() -> dict[str, str]:
    """Verifica rapidamente que las rutas de chat esten operativas."""
    return {
        "status": "ok",
        "message": "Chat endpoint operativo",
    }

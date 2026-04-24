"""Rutas de API para el chat inteligente con IA."""
import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.application import ChatHistoryDTO, ChatRequestDTO, ChatResponseDTO, ChatService
from app.domain import ChatSessionNotFoundError, GeminiAPIError
from app.infrastructure.database.connection import get_session
from app.infrastructure.repositories import ChatRepository, ProductRepository

router = APIRouter(prefix="/chat", tags=["Chat"])


def get_chat_service(
    session: Annotated[Session, Depends(get_session)],
) -> ChatService:
    """Inyecta ChatService con todas sus dependencias.

    Construye una instancia de ChatService configurando los repositorios
    y el servicio de Gemini necesarios para procesar mensajes de chat.

    Parámetros:
        session: Sesión de base de datos inyectada.

    Retorna:
        ChatService: Instancia del servicio configurada.

    Excepciones:
        ValueError: Si GEMINI_API_KEY no está configurada en variables de entorno.
    """
    chat_repo = ChatRepository(session)
    product_repo = ProductRepository(session)
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GEMINI_API_KEY no configurada en variables de entorno",
        )

    try:
        from app.infrastructure.external import GeminiService
    except ImportError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Dependencias de Gemini no disponibles en el entorno.",
        ) from exc

    gemini_service = GeminiService(gemini_api_key)
    return ChatService(
        product_repository=product_repo,
        chat_repository=chat_repo,
        gemini_service=gemini_service,
    )


@router.post("", response_model=ChatResponseDTO, status_code=status.HTTP_200_OK)
async def send_message(
    request: ChatRequestDTO,
    service: Annotated[ChatService, Depends(get_chat_service)],
) -> ChatResponseDTO:
    """Envía un mensaje al chat y obtiene respuesta de la IA.

    Procesa un mensaje del usuario, lo guarda en el historial de la sesión,
    obtiene una respuesta de Google Gemini basada en el contexto (productos
    disponibles e historial), y retorna la respuesta junto con datos de la sesión.

    Parámetros:
        request: ChatRequestDTO con session_id y message del usuario.
        service: ChatService inyectado mediante dependencias.

    Retorna:
        ChatResponseDTO: Respuesta del asistente con detalles de la sesión.

    Excepciones:
        HTTPException: Si hay error en la API de Gemini (código 500).

    Códigos HTTP:
        200: Mensaje procesado exitosamente, respuesta obtenida.
        500: Error en la comunicación con Google Gemini API.
        422: Datos de entrada inválidos (validación Pydantic fallida).
    """
    try:
        return service.process_message(request)
    except GeminiAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Error al procesar mensaje: {str(e)}",
        ) from e


@router.get(
    "/history/{session_id}",
    response_model=ChatHistoryDTO,
    status_code=status.HTTP_200_OK,
)
async def get_chat_history(
    session_id: str,
    service: Annotated[ChatService, Depends(get_chat_service)],
) -> ChatHistoryDTO:
    """Obtiene el historial completo de chat de una sesión.

    Recupera todos los mensajes intercambiados en una sesión de chat específica,
    tanto mensajes del usuario como respuestas del asistente, ordenados
    cronológicamente del más antiguo al más reciente.

    Parámetros:
        session_id: Identificador único de la sesión de chat.
        service: ChatService inyectado mediante dependencias.

    Retorna:
        ChatHistoryDTO: Historial con session_id y lista de mensajes.
                       Retorna lista vacía si no hay historial.

    Códigos HTTP:
        200: Operación exitosa, historial retornado (puede estar vacío).
    """
    try:
        return service.get_chat_history(session_id)
    except ChatSessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.delete(
    "/history/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_chat_history(
    session_id: str,
    service: Annotated[ChatService, Depends(get_chat_service)],
) -> Response:
    """Elimina todo el historial de una sesión de chat.

    Remueve permanentemente todos los mensajes asociados a una sesión,
    limpiando completamente el historial de conversación.

    Parámetros:
        session_id: Identificador único de la sesión a eliminar.
        service: ChatService inyectado mediante dependencias.

    Retorna:
        Dict: Mensaje de confirmación con la session_id.

    Códigos HTTP:
        200: Historial eliminado exitosamente.
    """
    try:
        service.delete_chat_history(session_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ChatSessionNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

"""Rutas de API para el chat inteligente con IA."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
import os
from app.application import (
    ChatService,
    ChatRequestDTO,
    ChatResponseDTO,
    ChatHistoryDTO,
)

router = APIRouter(prefix="/chat", tags=["Chat"])


def get_chat_service(session=None) -> ChatService:
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
    if session is None:
        from app.infrastructure.database import SessionLocal
        session = SessionLocal()
    
    from app.infrastructure.repositories import ChatRepository, ProductRepository
    from app.infrastructure.external import GeminiService
    
    chat_repo = ChatRepository(session)
    product_repo = ProductRepository(session)
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY no configurada en variables de entorno")
    gemini_service = GeminiService(gemini_api_key)
    return ChatService(
        product_repository=product_repo,
        chat_repository=chat_repo,
        gemini_service=gemini_service,
    )


@router.post("", response_model=ChatResponseDTO, status_code=status.HTTP_200_OK)
async def send_message(
    request: ChatRequestDTO,
    service: ChatService = Depends(get_chat_service),
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar mensaje: {str(e)}",
        )


@router.get(
    "/history/{session_id}",
    response_model=ChatHistoryDTO,
    status_code=status.HTTP_200_OK,
)
async def get_chat_history(
    session_id: str,
    service: ChatService = Depends(get_chat_service),
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
    return service.get_chat_history(session_id)


@router.delete(
    "/history/{session_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_chat_history(
    session_id: str,
    service: ChatService = Depends(get_chat_service),
) -> Dict[str, Any]:
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
    service.delete_chat_history(session_id)
    return {
        "message": "Historial eliminado correctamente",
        "session_id": session_id,
    }

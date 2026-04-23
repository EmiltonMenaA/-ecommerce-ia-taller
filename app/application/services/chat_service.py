from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4

from app.application.dtos import (
    ChatHistoryDTO,
    ChatMessageDTO,
    ChatRequestDTO,
    ChatResponseDTO,
)
from app.domain import (
    ChatMessage,
    ChatSessionNotFoundError,
    GeminiAPIError,
    IChatRepository,
    IGeminiService,
    IProductRepository,
    Product,
)


@dataclass(slots=True)
class ChatContext:
    """Contiene la informacion necesaria para construir el prompt de conversacion.

    Atributos:
        session_id: Identificador de la sesion en proceso.
        history: Historial previo de mensajes de la sesion.
        products: Catalogo actual de productos disponibles.
    """

    session_id: str
    history: List[ChatMessage]
    products: List[Product]


class ChatService:
    """Servicio de aplicacion para coordinar la conversacion del asistente."""

    def __init__(
        self,
        product_repository: IProductRepository,
        chat_repository: IChatRepository,
        gemini_service: IGeminiService,
    ) -> None:
        """Inicializa el servicio con sus dependencias inyectadas.

        Parametros:
            product_repository: Repositorio para consultar catalogo de productos.
            chat_repository: Repositorio para persistir y consultar mensajes.
            gemini_service: Servicio encargado de generar respuestas con IA.
        """
        self.product_repository = product_repository
        self.chat_repository = chat_repository
        self.gemini_service = gemini_service

    def process_message(self, request: ChatRequestDTO) -> ChatResponseDTO:
        """Procesa un mensaje de usuario y retorna la respuesta del asistente.

        Flujo:
            1. Recupera productos del repositorio.
            2. Recupera historial de la sesion.
            3. Construye ChatContext(session_id, historial, productos).
            4. Solicita respuesta a la IA.
            5. Guarda mensaje de usuario y respuesta del asistente.

        Parametros:
            request: DTO con session_id y mensaje del usuario.

        Retorna:
            DTO con la respuesta de la conversacion.

        Lanza:
            GeminiAPIError: Si el servicio de IA no retorna una respuesta valida.
        """
        products = self.product_repository.get_all()
        history = self.chat_repository.get_history(request.session_id)
        context = ChatContext(
            session_id=request.session_id,
            history=history,
            products=products,
        )

        assistant_response = self._generate_assistant_response(
            user_message=request.message,
            context=context,
        )

        user_entity = ChatMessage.create(
            session_id=request.session_id,
            role="user",
            message=request.message,
        )
        self.chat_repository.save_message(user_entity)

        assistant_entity = ChatMessage.create(
            session_id=request.session_id,
            role="assistant",
            message=assistant_response,
        )
        saved_assistant = self.chat_repository.save_message(assistant_entity)

        return ChatResponseDTO(
            session_id=request.session_id,
            user_message=request.message,
            assistant_response=assistant_response,
            timestamp=saved_assistant.timestamp,
        )

    def get_chat_history(self, session_id: str) -> ChatHistoryDTO:
        """Obtiene el historial de una sesion y lo transforma a DTO.

        Parametros:
            session_id: Identificador de la sesion de chat.

        Retorna:
            Historial completo con mensajes serializables.

        Lanza:
            ChatSessionNotFoundError: Si no existen mensajes para la sesion.
        """
        history = self.chat_repository.get_history(session_id)
        if not history:
            raise ChatSessionNotFoundError(
                f"No existe historial para la sesion '{session_id}'."
            )

        return ChatHistoryDTO(
            session_id=session_id,
            messages=[self._message_to_dto(message) for message in history],
        )

    def _build_prompt(self, context: ChatContext, user_message: str) -> str:
        """Construye un prompt enriquecido con catalogo e historial de conversacion.

        Parametros:
            context: Contexto con productos e historial de la sesion.
            user_message: Consulta actual del usuario.

        Retorna:
            Prompt final para enviar al servicio de IA.
        """
        products_section = self._format_products(context.products)
        history_section = self._format_history(context.history)
        return (
            "Eres un asistente de ecommerce especializado en calzado. "
            "Responde de forma util, breve y basada en el catalogo.\n\n"
            f"Catalogo de productos:\n{products_section}\n\n"
            f"Historial de conversacion:\n{history_section}\n\n"
            f"Mensaje del usuario:\n{user_message}\n\n"
            "Instrucciones: recomienda opciones relevantes, incluye marca, categoria, "
            "precio y disponibilidad cuando aplique."
        )

    def _generate_assistant_response(self, user_message: str, context: ChatContext) -> str:
        """Solicita al servicio Gemini la respuesta textual para un mensaje y contexto.

        Parametros:
            user_message: Mensaje actual del usuario.
            context: Contexto de conversacion con historial y catalogo.

        Retorna:
            Texto generado por el asistente.

        Lanza:
            GeminiAPIError: Si ocurre un error o la respuesta es vacia.
        """
        try:
            response = self.gemini_service.get_response(user_message, context.history, context.products)
        except Exception as exc:
            raise GeminiAPIError("Error al generar respuesta con Gemini.") from exc

        cleaned_response = response.strip() if response else ""
        if not cleaned_response:
            raise GeminiAPIError("Gemini devolvio una respuesta vacia.")
        return cleaned_response

    def _serialize_context(self, context: ChatContext) -> Dict[str, Any]:
        """Serializa ChatContext en una estructura util para servicios de IA.

        Parametros:
            context: Contexto de sesion que incluye historial y productos.

        Retorna:
            Diccionario con datos listos para consumir por IGeminiService.
        """
        return {
            "session_id": context.session_id,
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "brand": product.brand,
                    "category": product.category,
                    "size": product.size,
                    "color": product.color,
                    "price": product.price,
                    "stock": product.stock,
                }
                for product in context.products
            ],
            "history": [
                {
                    "session_id": message.session_id,
                    "role": message.role,
                    "message": message.message,
                    "timestamp": message.timestamp.astimezone(timezone.utc).isoformat(),
                }
                for message in context.history
            ],
        }

    def _format_products(self, products: List[Product]) -> str:
        """Convierte el catalogo a texto legible para incluirlo en el prompt."""
        if not products:
            return "No hay productos disponibles en este momento."

        lines = []
        for product in products:
            availability = "disponible" if product.stock > 0 else "sin stock"
            lines.append(
                f"- {product.name} (id: {product.id}), marca: {product.brand}, "
                f"categoria: {product.category}, talla: {product.size}, "
                f"color: {product.color}, precio: {product.price:.2f}, "
                f"stock: {product.stock} ({availability})"
            )
        return "\n".join(lines)

    def _format_history(self, history: List[ChatMessage]) -> str:
        """Convierte historial de mensajes a texto para contexto conversacional."""
        if not history:
            return "Sin historial previo."

        lines = []
        for message in history:
            iso_timestamp = message.timestamp.astimezone(timezone.utc).isoformat()
            lines.append(f"[{iso_timestamp}] {message.role}: {message.message}")
        return "\n".join(lines)

    def _message_to_dto(self, message: ChatMessage) -> ChatMessageDTO:
        """Transforma una entidad ChatMessage en ChatMessageDTO."""
        message_id = self._resolve_message_id(message)
        return ChatMessageDTO(
            id=message_id,
            session_id=message.session_id,
            role=message.role,
            message=message.message,
            timestamp=message.timestamp,
        )

    @staticmethod
    def _resolve_message_id(message: ChatMessage) -> str:
        """Obtiene un id estable para un mensaje aunque la entidad no lo defina."""
        dynamic_id = getattr(message, "id", None)
        if isinstance(dynamic_id, str) and dynamic_id.strip():
            return dynamic_id

        timestamp_fragment = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        return f"msg_{timestamp_fragment}_{uuid4().hex[:6]}"

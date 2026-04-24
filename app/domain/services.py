from abc import ABC, abstractmethod

from app.domain.entities import ChatMessage, Product


class IGeminiService(ABC):
    """Contrato para servicios que generan respuestas usando un modelo Gemini."""

    @abstractmethod
    def get_response(
        self,
        user_message: str,
        history: list[ChatMessage],
        products: list[Product],
    ) -> str:
        """Genera una respuesta de texto usando mensaje, historial y catalogo.

        Parametros:
            user_message: Mensaje actual del usuario.
            history: Historial de conversacion de la sesion.
            products: Productos disponibles en el catalogo.

        Retorna:
            Respuesta generada por el modelo.
        """

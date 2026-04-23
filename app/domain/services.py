from abc import ABC, abstractmethod
from typing import Any, Dict


class IGeminiService(ABC):
    """Contrato para servicios que generan respuestas usando un modelo Gemini."""

    @abstractmethod
    def get_response(self, message: str, context: Dict[str, Any]) -> str:
        """Genera una respuesta de texto usando mensaje y contexto conversacional.

        Parametros:
            message: Mensaje actual del usuario.
            context: Informacion de apoyo para responder (historial, productos, etc.).

        Retorna:
            Respuesta generada por el modelo.
        """

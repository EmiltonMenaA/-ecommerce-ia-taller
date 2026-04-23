from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal


@dataclass(slots=True)
class ChatMessage:
    """Representa un mensaje dentro de una conversacion de chat.

    Atributos:
        session_id: Identificador de la sesion de conversacion.
        role: Rol del emisor del mensaje; puede ser 'user' o 'assistant'.
        message: Contenido textual del mensaje.
        timestamp: Fecha y hora en que se creo el mensaje.
    """

    session_id: str
    role: Literal["user", "assistant"]
    message: str
    timestamp: datetime

    @classmethod
    def create(
        cls,
        session_id: str,
        role: Literal["user", "assistant"],
        message: str,
        timestamp: datetime | None = None,
    ) -> "ChatMessage":
        """Crea un mensaje usando la hora UTC actual si no se recibe timestamp.

        Parametros:
            session_id: Identificador de la sesion de chat.
            role: Rol del emisor del mensaje.
            message: Texto del mensaje.
            timestamp: Momento del mensaje; si es None se usa la hora actual.

        Retorna:
            Una instancia de ChatMessage inicializada.
        """
        resolved_timestamp = timestamp or datetime.now(timezone.utc)
        return cls(
            session_id=session_id,
            role=role,
            message=message,
            timestamp=resolved_timestamp,
        )

    def is_user_message(self) -> bool:
        """Indica si el mensaje fue enviado por el usuario.

        Retorna:
            True cuando el rol es 'user'; False para otros roles.
        """
        return self.role == "user"

    def is_assistant_message(self) -> bool:
        """Indica si el mensaje fue enviado por el asistente.

        Retorna:
            True cuando el rol es 'assistant'; False para otros roles.
        """
        return self.role == "assistant"

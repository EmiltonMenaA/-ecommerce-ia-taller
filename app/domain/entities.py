from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal


@dataclass(slots=True)
class Product:
    """Representa un producto del catalogo de ecommerce."""

    id: str
    name: str
    brand: str
    category: str
    size: float
    color: str
    price: float
    stock: int

    def is_available(self) -> bool:
        """Indica si el producto tiene unidades disponibles."""
        return self.stock > 0

    def total_value_in_stock(self) -> float:
        """Calcula el valor total del inventario de este producto."""
        return self.price * self.stock


@dataclass(slots=True)
class ChatMessage:
    """Representa un mensaje en una sesion de chat."""

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
        """Crea un mensaje usando UTC actual cuando no se envia timestamp."""
        return cls(
            session_id=session_id,
            role=role,
            message=message,
            timestamp=timestamp or datetime.now(timezone.utc),
        )

    def is_user_message(self) -> bool:
        """Indica si el mensaje fue emitido por el usuario."""
        return self.role == "user"

    def is_assistant_message(self) -> bool:
        """Indica si el mensaje fue emitido por el asistente."""
        return self.role == "assistant"
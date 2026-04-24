from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


class ProductDTO(BaseModel):
    """DTO de salida para un producto."""

    id: str = Field(..., min_length=1, max_length=64)
    name: str = Field(..., min_length=1, max_length=200)
    brand: str = Field(..., min_length=1, max_length=80)
    category: str = Field(..., min_length=1, max_length=80)
    size: float = Field(..., gt=0)
    color: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class CreateProductDTO(BaseModel):
    """DTO de entrada para crear un producto."""

    name: str = Field(..., min_length=1, max_length=200)
    brand: str = Field(..., min_length=1, max_length=80)
    category: str = Field(..., min_length=1, max_length=80)
    size: float = Field(..., gt=0)
    color: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class UpdateProductDTO(BaseModel):
    """DTO de entrada para actualizar un producto."""

    name: str = Field(..., min_length=1, max_length=200)
    brand: str = Field(..., min_length=1, max_length=80)
    category: str = Field(..., min_length=1, max_length=80)
    size: float = Field(..., gt=0)
    color: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class ChatMessageDTO(BaseModel):
    """DTO de salida para un mensaje individual de chat."""

    id: str = Field(..., min_length=1, max_length=64)
    session_id: str = Field(..., min_length=1, max_length=64)
    role: Literal["user", "assistant"] = Field(...)
    message: str = Field(..., min_length=1, max_length=4000)
    timestamp: datetime = Field(...)


class ChatRequestDTO(BaseModel):
    """DTO de entrada para enviar un mensaje de chat."""

    session_id: str = Field(..., min_length=1, max_length=64)
    message: str = Field(..., min_length=1, max_length=4000)


class ChatResponseDTO(BaseModel):
    """DTO de salida para la respuesta del asistente."""

    session_id: str = Field(..., min_length=1, max_length=64)
    user_message: str = Field(..., min_length=1, max_length=4000)
    assistant_response: str = Field(..., min_length=1, max_length=4000)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChatHistoryDTO(BaseModel):
    """DTO de salida para historial de chat por sesion."""

    session_id: str = Field(..., min_length=1, max_length=64)
    messages: list[ChatMessageDTO] = Field(default_factory=list)
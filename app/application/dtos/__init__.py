from datetime import datetime, timezone
from typing import List, Literal

from pydantic import BaseModel, Field


class ProductDTO(BaseModel):
    """DTO para retornar la informacion completa de un producto."""

    id: str = Field(..., min_length=1, max_length=64)
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Nombre del producto",
    )
    brand: str = Field(..., min_length=1, max_length=80)
    category: str = Field(..., min_length=1, max_length=80)
    size: float = Field(..., gt=0)
    color: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0, description="Precio debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="Stock no puede ser negativo")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "prod_001",
                "name": "Air Zoom Runner",
                "brand": "Nike",
                "category": "running",
                "size": 42.5,
                "color": "negro",
                "price": 129.99,
                "stock": 15,
            }
        }


class CreateProductDTO(BaseModel):
    """DTO para recibir datos al crear un producto nuevo."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Nombre del producto",
    )
    brand: str = Field(..., min_length=1, max_length=80)
    category: str = Field(..., min_length=1, max_length=80)
    size: float = Field(..., gt=0)
    color: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0, description="Precio debe ser mayor a 0")
    stock: int = Field(..., ge=0, description="Stock no puede ser negativo")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Gel Pulse 14",
                "brand": "Asics",
                "category": "running",
                "size": 41.0,
                "color": "azul",
                "price": 109.5,
                "stock": 8,
            }
        }


class ChatMessageDTO(BaseModel):
    """DTO para retornar un mensaje individual de chat."""

    id: str = Field(..., min_length=1, max_length=64)
    session_id: str = Field(..., min_length=1, max_length=64)
    role: Literal["user", "assistant"] = Field(...)
    message: str = Field(..., min_length=1, max_length=4000)
    timestamp: datetime = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "msg_001",
                "session_id": "session_123",
                "role": "user",
                "message": "Busco zapatillas para correr en asfalto",
                "timestamp": "2026-04-23T15:30:00Z",
            }
        }


class ChatRequestDTO(BaseModel):
    """DTO para recibir un mensaje del usuario en una sesion de chat."""

    session_id: str = Field(..., min_length=1, max_length=64)
    message: str = Field(..., min_length=1, max_length=4000)

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "message": "Quiero opciones de zapatillas blancas talla 42",
            }
        }


class ChatResponseDTO(BaseModel):
    """DTO para retornar la respuesta del chat al usuario."""

    session_id: str = Field(..., min_length=1, max_length=64)
    user_message: str = Field(..., min_length=1, max_length=4000)
    assistant_response: str = Field(..., min_length=1, max_length=4000)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "user_message": "Necesito zapatillas para trail",
                "assistant_response": "Te recomiendo modelos con suela de alto agarre y drop medio.",
                "timestamp": "2026-04-23T15:31:15Z",
            }
        }


class ChatHistoryDTO(BaseModel):
    """DTO para retornar el historial completo de una sesion de chat."""

    session_id: str = Field(..., min_length=1, max_length=64)
    messages: List[ChatMessageDTO] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_123",
                "messages": [
                    {
                        "id": "msg_001",
                        "session_id": "session_123",
                        "role": "user",
                        "message": "Busco algo para gimnasio",
                        "timestamp": "2026-04-23T15:28:00Z",
                    },
                    {
                        "id": "msg_002",
                        "session_id": "session_123",
                        "role": "assistant",
                        "message": "Te sugiero un modelo con buena amortiguacion lateral.",
                        "timestamp": "2026-04-23T15:28:04Z",
                    },
                ],
            }
        }

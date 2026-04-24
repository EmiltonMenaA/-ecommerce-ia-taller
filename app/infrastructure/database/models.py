"""Modelos ORM de SQLAlchemy para mapeo de entidades a tablas SQL."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from typing import Any

Base = declarative_base()


class IsoDateTime(TypeDecorator):
    """Tipo custom que maneja datetime serializado en formato ISO para SQLite."""
    impl = String
    cache_ok = True
    
    def process_bind_param(self, value: Any, dialect: Any) -> str | None:
        """Convierte datetime a string ISO para SQLite."""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)
    
    def process_result_value(self, value: Any, dialect: Any) -> datetime | None:
        """Convierte string ISO desde SQLite a datetime."""
        if value is None:
            return None
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return datetime.fromisoformat(value[:19])
        return value


class ProductModel(Base):
    """Modelo ORM para la tabla products."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    size = Column(Float, nullable=False)
    color = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(IsoDateTime(), nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_products_brand", "brand"),
        Index("ix_products_category", "category"),
    )

    def __repr__(self) -> str:
        """Representación legible del modelo."""
        return f"<ProductModel(id={self.id}, name='{self.name}', brand='{self.brand}')>"


class ChatMessageModel(Base):
    """Modelo ORM para la tabla chat_messages."""

    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(200), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(IsoDateTime(), nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_chat_messages_session_id", "session_id"),
    )

    def __repr__(self) -> str:
        """Representación legible del modelo."""
        return f"<ChatMessageModel(id={self.id}, session_id='{self.session_id}', role='{self.role}')>"

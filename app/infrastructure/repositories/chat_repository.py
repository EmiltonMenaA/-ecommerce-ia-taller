"""Implementación de repositorio de mensajes de chat con SQLite y SQLAlchemy."""
from sqlalchemy.orm import Session
from typing import List
from app.domain.entities.chat_message import ChatMessage
from app.domain.repositories import IChatRepository
from app.infrastructure.database.models import ChatMessageModel
from datetime import datetime


class ChatRepository(IChatRepository):
    """Implementación de IChatRepository usando SQLite.

    Proporciona operaciones de persistencia para mensajes de chat
    permitiendo guardar, recuperar y eliminar conversaciones.
    """

    def __init__(self, session: Session) -> None:
        """Inicializa el repositorio con una sesión de base de datos.

        Parámetros:
            session: Sesión de SQLAlchemy para ejecutar operaciones de BD.
        """
        self.session = session

    def _model_to_entity(self, model: ChatMessageModel) -> ChatMessage:
        """Convierte un modelo ORM ChatMessageModel a una entidad ChatMessage.

        Parámetros:
            model: Instancia de ChatMessageModel de la base de datos.

        Retorna:
            ChatMessage: Entidad de dominio equivalente.
        """
        return ChatMessage(
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp,
        )

    def _entity_to_model(self, message: ChatMessage) -> ChatMessageModel:
        """Convierte una entidad ChatMessage a un modelo ORM ChatMessageModel.

        Parámetros:
            message: Entidad de dominio a convertir.

        Retorna:
            ChatMessageModel: Modelo ORM listo para persistir.
        """
        return ChatMessageModel(
            session_id=message.session_id,
            role=message.role,
            message=message.message,
            timestamp=message.timestamp,
        )

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Guarda un mensaje de chat en la base de datos.

        Persiste un nuevo mensaje en la sesión de chat correspondiente.

        Parámetros:
            message: Entidad ChatMessage a guardar.

        Retorna:
            Entidad ChatMessage persistida con todos sus datos.
        """
        model = self._entity_to_model(message)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._model_to_entity(model)

    def get_all(self) -> List[ChatMessage]:
        """Obtiene todos los mensajes de chat almacenados.

        Retorna:
            Lista de mensajes ordenados por timestamp ascendente.
        """
        models = (
            self.session.query(ChatMessageModel)
            .order_by(ChatMessageModel.timestamp.asc())
            .all()
        )
        return [self._model_to_entity(model) for model in models]

    def get_history(self, session_id: str) -> List[ChatMessage]:
        """Obtiene el historial completo de mensajes de una sesión de chat.

        Recupera todos los mensajes de una sesión ordenados por timestamp
        de forma cronológica (del más antiguo al más reciente).

        Parámetros:
            session_id: Identificador único de la sesión de chat.

        Retorna:
            Lista de entidades ChatMessage ordenadas cronológicamente.
        """
        models = (
            self.session.query(ChatMessageModel)
            .filter(ChatMessageModel.session_id == session_id)
            .order_by(ChatMessageModel.timestamp.asc())
            .all()
        )
        return [self._model_to_entity(model) for model in models]

    def delete_session(self, session_id: str) -> bool:
        """Elimina todos los mensajes asociados a una sesión de chat.

        Remueve completamente el historial de una sesión específica
        de la base de datos.

        Parámetros:
            session_id: Identificador único de la sesión a eliminar.

        Retorna:
            True si la sesión fue eliminada (existía), False si no existía.
        """
        count = (
            self.session.query(ChatMessageModel)
            .filter(ChatMessageModel.session_id == session_id)
            .delete()
        )
        self.session.commit()
        return count > 0

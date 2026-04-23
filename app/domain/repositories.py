from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.chat_message import ChatMessage
from app.domain.entities.product import Product


class IProductRepository(ABC):
    """Contrato para operaciones de persistencia y consulta de productos."""

    @abstractmethod
    def get_all(self) -> List[Product]:
        """Obtiene todos los productos disponibles en el repositorio.

        Retorna:
            Lista de productos registrados.
        """

    @abstractmethod
    def get_by_id(self, product_id: str) -> Optional[Product]:
        """Busca un producto por su identificador unico.

        Parametros:
            product_id: Identificador del producto a consultar.

        Retorna:
            El producto si existe, o None si no se encuentra.
        """

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """Filtra productos por marca.

        Parametros:
            brand: Marca por la que se desea filtrar.

        Retorna:
            Lista de productos que coinciden con la marca.
        """

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """Filtra productos por categoria.

        Parametros:
            category: Categoria de productos a consultar.

        Retorna:
            Lista de productos pertenecientes a la categoria.
        """

    @abstractmethod
    def save(self, product: Product) -> Product:
        """Guarda o actualiza un producto en el repositorio.

        Parametros:
            product: Instancia de producto a persistir.

        Retorna:
            El producto persistido.
        """


class IChatRepository(ABC):
    """Contrato para operaciones de persistencia de conversaciones de chat."""

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Guarda un mensaje en la sesion de chat correspondiente.

        Parametros:
            message: Mensaje de chat a persistir.

        Retorna:
            El mensaje guardado.
        """

    @abstractmethod
    def get_history(self, session_id: str) -> List[ChatMessage]:
        """Obtiene el historial completo de mensajes de una sesion.

        Parametros:
            session_id: Identificador de la sesion de chat.

        Retorna:
            Lista ordenada de mensajes de la sesion.
        """

    @abstractmethod
    def delete_session(self, session_id: str) -> bool:
        """Elimina todos los mensajes asociados a una sesion de chat.

        Parametros:
            session_id: Identificador de la sesion a eliminar.

        Retorna:
            True si la sesion fue eliminada, False si no existia.
        """

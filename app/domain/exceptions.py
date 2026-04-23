class DomainException(Exception):
    """Excepcion base del dominio para errores de reglas de negocio."""


class ProductNotFoundError(DomainException):
    """Se lanza cuando no existe un producto con el identificador solicitado."""


class InsufficientStockError(DomainException):
    """Se lanza cuando el stock disponible no alcanza para la operacion solicitada."""


class InvalidPriceError(DomainException):
    """Se lanza cuando el precio de un producto es invalido para las reglas del negocio."""


class ChatSessionNotFoundError(DomainException):
    """Se lanza cuando no existe la sesion de chat consultada."""


class GeminiAPIError(DomainException):
    """Se lanza cuando ocurre un error al comunicarse con Google Gemini API."""

from dataclasses import dataclass


@dataclass(slots=True)
class Product:
    """Representa un zapato dentro del catalogo de ecommerce.

    Atributos:
        id: Identificador unico del producto.
        name: Nombre comercial del zapato.
        brand: Marca del producto.
        category: Categoria del zapato (por ejemplo, running o casual).
        size: Talla numerica del zapato.
        color: Color principal del zapato.
        price: Precio unitario del producto.
        stock: Cantidad de unidades disponibles en inventario.
    """

    id: str
    name: str
    brand: str
    category: str
    size: float
    color: str
    price: float
    stock: int

    def is_available(self) -> bool:
        """Indica si el producto esta disponible para venta.

        Retorna:
            True si hay al menos una unidad en stock, False en caso contrario.
        """
        return self.stock > 0

    def total_value_in_stock(self) -> float:
        """Calcula el valor total del inventario para este producto.

        Retorna:
            El resultado de multiplicar el precio unitario por el stock.
        """
        return self.price * self.stock

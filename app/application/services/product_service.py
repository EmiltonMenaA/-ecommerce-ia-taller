from typing import List
from uuid import uuid4

from app.application.dtos import CreateProductDTO, ProductDTO
from app.domain import IProductRepository, InvalidPriceError, Product, ProductNotFoundError


class ProductService:
    """Servicio de aplicacion para gestionar casos de uso de productos."""

    def __init__(self, product_repository: IProductRepository) -> None:
        """Inicializa el servicio con un repositorio inyectado.

        Args:
            product_repository: Implementacion del contrato IProductRepository.
        """
        self.product_repository = product_repository

    def get_all_products(self) -> List[ProductDTO]:
        """Obtiene todos los productos y los transforma a DTOs.

        Retorna:
            Lista de productos en formato ProductDTO.
        """
        products = self.product_repository.get_all()
        return [self._entity_to_dto(product) for product in products]

    def get_product_by_id(self, product_id: int) -> ProductDTO:
        """Obtiene un producto por su identificador.

        Args:
            product_id: Identificador numerico del producto.

        Retorna:
            Producto encontrado en formato ProductDTO.

        Lanza:
            ProductNotFoundError: Si no existe un producto para el id indicado.
        """
        product = self.product_repository.get_by_id(str(product_id))
        if product is None:
            raise ProductNotFoundError(
                f"No existe un producto con id '{product_id}'."
            )
        return self._entity_to_dto(product)

    def get_products_by_brand(self, brand: str) -> List[ProductDTO]:
        """Filtra productos por marca y retorna DTOs.

        Args:
            brand: Marca por la cual se filtraran productos.

        Retorna:
            Lista de productos de la marca solicitada.
        """
        products = self.product_repository.get_by_brand(brand)
        return [self._entity_to_dto(product) for product in products]

    def get_products_by_category(self, category: str) -> List[ProductDTO]:
        """Filtra productos por categoria y retorna DTOs.

        Args:
            category: Categoria de productos a consultar.

        Retorna:
            Lista de productos de la categoria solicitada.
        """
        products = self.product_repository.get_by_category(category)
        return [self._entity_to_dto(product) for product in products]

    def create_product(self, dto: CreateProductDTO) -> ProductDTO:
        """Crea un nuevo producto a partir de un DTO de entrada.

        Args:
            dto: Datos necesarios para crear el producto.

        Retorna:
            Producto creado en formato ProductDTO.

        Lanza:
            InvalidPriceError: Si el precio no cumple las reglas del dominio.
        """
        if dto.price <= 0:
            raise InvalidPriceError("El precio del producto debe ser mayor a 0.")

        new_product = Product(
            id=self._generate_product_id(),
            name=dto.name,
            brand=dto.brand,
            category=dto.category,
            size=dto.size,
            color=dto.color,
            price=dto.price,
            stock=dto.stock,
        )
        saved_product = self.product_repository.save(new_product)
        return self._entity_to_dto(saved_product)

    def _entity_to_dto(self, product: Product) -> ProductDTO:
        """Convierte una entidad Product del dominio a ProductDTO.

        Args:
            product: Entidad de dominio a convertir.

        Retorna:
            DTO listo para exponer en capa de entrada.
        """
        return ProductDTO(
            id=product.id,
            name=product.name,
            brand=product.brand,
            category=product.category,
            size=product.size,
            color=product.color,
            price=product.price,
            stock=product.stock,
        )

    @staticmethod
    def _generate_product_id() -> str:
        """Genera un identificador estable para nuevos productos.

        Retorna:
            Identificador con prefijo 'prod_'.
        """
        return f"prod_{uuid4().hex[:12]}"

"""Implementación de repositorio de productos con SQLite y SQLAlchemy."""
from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.entities.product import Product
from app.domain.repositories import IProductRepository
from app.infrastructure.database.models import ProductModel


class ProductRepository(IProductRepository):
    """Implementación de IProductRepository usando SQLite.

    Proporciona operaciones CRUD y consultas especializadas para
    productos en la base de datos usando SQLAlchemy ORM.
    """

    def __init__(self, session: Session) -> None:
        """Inicializa el repositorio con una sesión de base de datos.

        Parámetros:
            session: Sesión de SQLAlchemy para ejecutar operaciones de BD.
        """
        self.session = session

    def _model_to_entity(self, model: ProductModel) -> Product:
        """Convierte un modelo ORM ProductModel a una entidad Product.

        Parámetros:
            model: Instancia de ProductModel de la base de datos.

        Retorna:
            Product: Entidad de dominio equivalente.
        """
        return Product(
            id=str(model.id),
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
        )

    def _entity_to_model(self, product: Product) -> ProductModel:
        """Convierte una entidad Product a un modelo ORM ProductModel.

        Parámetros:
            product: Entidad de dominio a convertir.

        Retorna:
            ProductModel: Modelo ORM listo para persistir.
        """
        product_id = int(product.id) if product.id else None
        return ProductModel(
            id=product_id,
            name=product.name,
            brand=product.brand,
            category=product.category,
            size=product.size,
            color=product.color,
            price=product.price,
            stock=product.stock,
        )

    def get_all(self) -> List[Product]:
        """Obtiene todos los productos disponibles en la base de datos.

        Retorna:
            Lista de entidades Product. Retorna lista vacía si no hay productos.
        """
        models = self.session.query(ProductModel).all()
        return [self._model_to_entity(model) for model in models]

    def get_by_id(self, product_id: str) -> Optional[Product]:
        """Obtiene un producto específico por su identificador único.

        Parámetros:
            product_id: Identificador del producto a buscar.

        Retorna:
            Entidad Product si existe, None si no se encuentra.
        """
        try:
            product_id_int = int(product_id)
        except (ValueError, TypeError):
            return None

        model = (
            self.session.query(ProductModel)
            .filter(ProductModel.id == product_id_int)
            .first()
        )
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str) -> List[Product]:
        """Filtra todos los productos que pertenecen a una marca específica.

        Parámetros:
            brand: Marca por la que filtrar (búsqueda exacta).

        Retorna:
            Lista de entidades Product que coinciden con la marca.
        """
        models = (
            self.session.query(ProductModel)
            .filter(ProductModel.brand == brand)
            .all()
        )
        return [self._model_to_entity(model) for model in models]

    def get_by_category(self, category: str) -> List[Product]:
        """Filtra todos los productos de una categoría específica.

        Parámetros:
            category: Categoría por la que filtrar (búsqueda exacta).

        Retorna:
            Lista de entidades Product que pertenecen a la categoría.
        """
        models = (
            self.session.query(ProductModel)
            .filter(ProductModel.category == category)
            .all()
        )
        return [self._model_to_entity(model) for model in models]

    def save(self, product: Product) -> Product:
        """Guarda o actualiza un producto en la base de datos.

        Si el producto tiene un ID existente, actualiza el registro.
        Si el producto no tiene ID, crea un nuevo registro.

        Parámetros:
            product: Entidad Product a persistir.

        Retorna:
            Entidad Product actualizada con el ID asignado por la BD.
        """
        model = self._entity_to_model(product)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._model_to_entity(model)

"""Rutas de API para gestión de productos."""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.application import ProductService, ProductDTO, CreateProductDTO

router = APIRouter(prefix="/products", tags=["Products"])


def get_product_service(session=None) -> ProductService:
    """Inyecta ProductService con dependencias.

    Parámetros:
        session: Sesión de base de datos inyectada.

    Retorna:
        ProductService: Instancia del servicio configurada.
    """
    if session is None:
        from app.infrastructure.database import SessionLocal
        session = SessionLocal()
    
    from app.infrastructure.repositories import ProductRepository
    repo = ProductRepository(session)
    return ProductService(repo)


@router.get("", response_model=List[ProductDTO], status_code=status.HTTP_200_OK)
async def get_all_products(
    service: ProductService = Depends(get_product_service),
) -> List[ProductDTO]:
    """Obtiene todos los productos disponibles.

    Retorna la lista completa de productos registrados en el catálogo
    del e-commerce de zapatos.

    Parámetros:
        service: ProductService inyectado mediante dependencias.

    Retorna:
        List[ProductDTO]: Lista de DTOs de productos disponibles.

    Códigos HTTP:
        200: Operación exitosa, lista de productos retornada.
    """
    return service.get_all_products()


@router.get("/{product_id}", response_model=ProductDTO, status_code=status.HTTP_200_OK)
async def get_product_by_id(
    product_id: int,
    service: ProductService = Depends(get_product_service),
) -> ProductDTO:
    """Obtiene un producto específico por su identificador único.

    Busca y retorna los detalles de un producto individual basado en su ID.
    Si el producto no existe, retorna un error 404.

    Parámetros:
        product_id: Identificador único del producto a consultar.
        service: ProductService inyectado mediante dependencias.

    Retorna:
        ProductDTO: Datos completos del producto solicitado.

    Excepciones:
        HTTPException: Si el producto no existe (código 404).

    Códigos HTTP:
        200: Producto encontrado y retornado.
        404: El producto con el ID especificado no existe.
    """
    product = service.get_product_by_id(str(product_id))
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )
    return product


@router.get(
    "/brand/{brand}", response_model=List[ProductDTO], status_code=status.HTTP_200_OK
)
async def get_products_by_brand(
    brand: str,
    service: ProductService = Depends(get_product_service),
) -> List[ProductDTO]:
    """Filtra productos por marca.

    Retorna todos los productos que pertenecen a la marca especificada.
    Si no hay productos de esa marca, retorna una lista vacía.

    Parámetros:
        brand: Nombre de la marca por la que filtrar.
        service: ProductService inyectado mediante dependencias.

    Retorna:
        List[ProductDTO]: Lista de productos que coinciden con la marca.

    Códigos HTTP:
        200: Operación exitosa, lista retornada (puede estar vacía).
    """
    return service.get_products_by_brand(brand)


@router.get(
    "/category/{category}",
    response_model=List[ProductDTO],
    status_code=status.HTTP_200_OK,
)
async def get_products_by_category(
    category: str,
    service: ProductService = Depends(get_product_service),
) -> List[ProductDTO]:
    """Filtra productos por categoría.

    Retorna todos los productos que pertenecen a la categoría especificada.
    Si no hay productos en esa categoría, retorna una lista vacía.

    Parámetros:
        category: Nombre de la categoría por la que filtrar.
        service: ProductService inyectado mediante dependencias.

    Retorna:
        List[ProductDTO]: Lista de productos de la categoría.

    Códigos HTTP:
        200: Operación exitosa, lista retornada (puede estar vacía).
    """
    return service.get_products_by_category(category)


@router.post("", response_model=ProductDTO, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: CreateProductDTO,
    service: ProductService = Depends(get_product_service),
) -> ProductDTO:
    """Crea un nuevo producto en el catálogo.

    Crea un registro de producto con los datos proporcionados.
    Los datos se validan automáticamente con Pydantic antes de procesar.
    El precio debe ser positivo y el stock no negativo.

    Parámetros:
        product_data: CreateProductDTO con los datos del nuevo producto.
        service: ProductService inyectado mediante dependencias.

    Retorna:
        ProductDTO: El producto creado con su ID asignado.

    Códigos HTTP:
        201: Producto creado exitosamente.
        422: Datos de entrada inválidos (validación fallida).
    """
    return service.create_product(product_data)

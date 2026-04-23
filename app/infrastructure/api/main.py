"""Aplicación FastAPI principal - Configuración y setup de la API REST."""
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Crear instancia de FastAPI
app = FastAPI(
    title="E-commerce de Zapatos con Chat IA",
    description="API REST con asistente inteligente basado en Google Gemini para recomendación de productos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Incluir routers de rutas (lazy loading)
def _include_routers():
    """Incluye los routers de la API (llamado en startup)."""
    from app.infrastructure.api.routes import products_router, chat_router
    app.include_router(products_router)
    app.include_router(chat_router)

@app.on_event("startup")
async def startup_event():
    """Evento de startup para inicializar la aplicación."""
    _include_routers()


@app.get("/", tags=["Root"])
async def root() -> dict:
    """Endpoint raíz de bienvenida a la API.

    Retorna información general sobre la aplicación y enlaces
    a la documentación interactiva.

    Retorna:
        dict: Mensaje de bienvenida con enlaces a documentación.

    Códigos HTTP:
        200: OK
    """
    return {
        "message": "Bienvenido al E-commerce de Zapatos con Chat IA",
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "endpoints": {
            "products": "/products",
            "chat": "/chat",
            "health": "/health",
        },
    }


@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    """Verifica el estado de la aplicación (health check).

    Endpoint para monitoreo que indica si la API está operacional
    y todas sus dependencias están disponibles.

    Retorna:
        dict: Status de la aplicación.

    Códigos HTTP:
        200: OK - API funcionando correctamente
    """
    return {
        "status": "ok",
        "message": "API está funcionando correctamente",
        "service": "E-commerce Zapatos Chat IA",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.infrastructure.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )

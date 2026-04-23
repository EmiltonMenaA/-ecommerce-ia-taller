"""Punto de entrada de la aplicación.

Para ejecutar:
    python main.py
    
O con uvicorn directamente:
    uvicorn main:app --reload
"""
from app.infrastructure.api.main import app

if __name__ == "__main__":
    import uvicorn
    import os
    from dotenv import load_dotenv

    load_dotenv()

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))

    print("Iniciando E-commerce de Zapatos con Chat IA")
    print(f"Servidor en: http://{host}:{port}")
    print(f"Documentacion en: http://{host}:{port}/docs")

    uvicorn.run(
        "app.infrastructure.api.main:app",
        host=host,
        port=port,
        reload=False,
    )

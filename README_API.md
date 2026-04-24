"""
# E-commerce de Zapatos con Chat IA - Guía de Inicio

##  Requisitos

- Python 3.10+
- Virtualenv configurado
- Google Gemini API Key

##  Iniciando la Aplicación

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Crear el archivo .env

Copia `.env.example` a `.env` y configura tu Google Gemini API Key:

```bash
cp .env.example .env
```

Luego edita `.env`:

```
GEMINI_API_KEY=your_actual_api_key_here
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=sqlite:///./ecommerce.db
```

### 3. Inicializar la Base de Datos

```bash
python -m app.infrastructure.database.init
```

Esto creará las tablas: `products` y `chat_messages`.

### 4. Ejecutar la Aplicación

```bash
python main.py
```

O con uvicorn:

```bash
uvicorn app.infrastructure.api.main:app --reload
```

La API estará disponible en:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

##  API Endpoints

### Productos

- `GET /products` - Obtiene todos los productos
- `GET /products/{product_id}` - Obtiene un producto por ID
- `GET /products/brand/{brand}` - Filtra productos por marca
- `GET /products/category/{category}` - Filtra productos por categoría  
- `POST /products` - Crea un nuevo producto

### Chat con IA

- `POST /chat` - Envía un mensaje y obtiene respuesta de Gemini
- `GET /chat/history/{session_id}` - Obtiene historial de chat
- `DELETE /chat/history/{session_id}` - Elimina historial de chat

### Health & Root

- `GET /` - Información general de la API
- `GET /health` - Health check

##  Ejemplo de Uso

### 1. Crear un Producto

```bash
curl -X POST http://localhost:8000/products \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Nike Air Max",
    "brand": "Nike",
    "category": "running",
    "size": "42",
    "color": "Negro",
    "price": 150.00,
    "stock": 10
  }'
```

### 2. Obtener Todos los Productos

```bash
curl http://localhost:8000/products
```

### 3. Chat con IA

```bash
curl -X POST http://localhost:8000/chat \\
  -H "Content-Type: application/json" \\
  -d '{
    "session_id": "user_123",
    "message": "¿Qué zapatos para correr recomiendas?"
  }'
```

##  Estructura de Carpetas

```
app/
├── domain/                  # Lógica de negocio (entidades, excepciones)
├── application/            # Casos de uso (servicios, DTOs)
├── infrastructure/         # Implementación técnica
│   ├── api/               # Endpoints HTTP con FastAPI
│   ├── database/          # Configuración BD y modelos ORM
│   ├── repositories/      # Implementación de repositorios
│   └── external/          # Servicios externos (Gemini)
└── tests/                 # Tests automáticos
```

##  Tecnologías

- **Framework**: FastAPI
- **BD**: SQLite + SQLAlchemy
- **IA**: Google Generative AI (Gemini)
- **Validación**: Pydantic
- **Servidor**: Uvicorn

##  Notas

- La base de datos SQLite se crea automáticamente en `ecommerce.db`
- Los mensajes de chat se guardan en `chat_messages` tabla
- Los productos se guardan en `products` tabla
- La API está documentada con Swagger en `/docs`

##  Troubleshooting

### Error: "ModuleNotFoundError: No module named 'sqlalchemy'"

Ejecuta: `pip install -r requirements.txt`

### Error: "GEMINI_API_KEY no configurada"

Asegúrate de:
1. Crear archivo `.env` basado en `.env.example`
2. Configurar tu API Key de Gemini
3. Ejecutar nuevamente

### Puerto 8000 en uso

Cambia el puerto en `.env`:
```
API_PORT=8001
```

---

**Última actualización**: Abril 2026
"""

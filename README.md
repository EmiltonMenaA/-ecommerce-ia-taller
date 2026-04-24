Aquí tienes un **README.md completo, formal y listo para entregar** para tu proyecto de E-commerce con IA usando FastAPI y Clean Architecture:

---

# 🛒 E-commerce con Chat IA - FastAPI

##  Descripción

Este proyecto consiste en el desarrollo de una API REST para un sistema de **E-commerce con integración de Chat IA**, implementado con **FastAPI** y siguiendo estrictamente los principios de **Clean Architecture**.

El sistema permite gestionar productos mediante un CRUD completo y cuenta con un módulo de chat preparado para integrarse con servicios de inteligencia artificial como OpenAI o Gemini.

---

##  Arquitectura

El proyecto está estructurado bajo el enfoque de **Clean Architecture**, separando responsabilidades en tres capas principales:

```
app/
│
├── domain/            # Entidades y contratos
│   ├── entities.py
│   ├── repositories.py
│   └── exceptions.py
│
├── application/       # Lógica de negocio
│   ├── dtos.py
│   └── services/
│       ├── product_service.py
│       └── chat_service.py
│
├── infrastructure/    # Implementaciones externas
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   │
│   ├── repositories/
│   │   ├── product_repository.py
│   │   └── chat_repository.py
│   │
│   └── api/
│       ├── routes/
│       │   ├── products.py
│       │   └── chat_simple.py
│       └── main.py
│
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .dockerignore
```

---

## ⚙️ Tecnologías utilizadas

*  FastAPI
*  Python 3.10+
*  SQLite
*  SQLAlchemy
*  Pydantic
*  Docker & Docker Compose

---

##  Funcionalidades

###  CRUD de Productos

* `GET /products` → Obtener todos los productos
* `GET /products/{id}` → Obtener producto por ID
* `POST /products` → Crear producto
* `PUT /products/{id}` → Actualizar producto
* `DELETE /products/{id}` → Eliminar producto

---

### Chat IA

* `GET /chat/test` → Endpoint de prueba
* `POST /chat` → Preparado para integración con IA

---

## Principios aplicados

* Separación de capas (Domain, Application, Infrastructure)
* Inversión de dependencias
* Uso de interfaces (repositorios)
* Inyección de dependencias con FastAPI
* DTOs para comunicación entre capas
* Independencia del framework en la lógica de negocio

---

## Base de datos

* Motor: **SQLite**
* ORM: **SQLAlchemy**
* Configuración centralizada en:

```
app/infrastructure/database/connection.py
```

---

# Ejecución con Docker

### 1. Construir y levantar el proyecto

```bash
docker-compose up --build
```

### 2. Acceder a la API

```
http://localhost:8000/docs
```

---

## Ejecución local (sin Docker)

### 1. Crear entorno virtual

```bash
python -m venv venv
```

### 2. Activar entorno

```bash
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar servidor

```bash
uvicorn main:app --reload
```

---

## 📡 Documentación automática

FastAPI genera documentación automática en:

* Swagger UI:

  ```
  http://localhost:8000/docs
  ```

* ReDoc:

  ```
  http://localhost:8000/redoc
  ```

---

## 📌 Buenas prácticas implementadas

*  Uso de DTOs (evita exponer modelos de base de datos)
*  Manejo de errores con excepciones personalizadas
*  Tipado estático (type hints)
*  Código documentado (docstrings en español)
*  Sin dependencias incorrectas entre capas
*  Arquitectura escalable y mantenible

---

##  Futuras mejoras

* Integración real con OpenAI / Gemini
* Autenticación con JWT
* Carrito de compras
* Órdenes y pagos
* Panel administrativo

---

##  Autor

Proyecto desarrollado como parte de un ejercicio académico de ingeniería de software, aplicando buenas prácticas profesionales en desarrollo backend, hecho por EMILTON MENA ACEVEDO

---


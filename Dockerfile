# Usar Python 3.11 slim como imagen base
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . .

# Crear directorio para la base de datos
RUN mkdir -p /app/data

# Exponer puerto 8000
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "app.infrastructure.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
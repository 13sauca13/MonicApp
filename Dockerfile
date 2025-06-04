# Usar una imagen base de Python 3.12 slim para mantener la imagen ligera
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar requirements.txt primero para aprovechar el cacheo de capas
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos del proyecto
COPY . .

# No definimos un puerto estático; Render lo asigna dinámicamente
# Exponer un puerto genérico para documentación (Render lo ignorará si es dinámico)
EXPOSE 8080

# Configurar gunicorn para usar la variable de entorno PORT proporcionada por Render
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]
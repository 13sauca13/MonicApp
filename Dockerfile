# Usar una imagen base ligera de Python
FROM python:3.9.21-alpine3.20

# Establecer el directorio de trabajo dentro de /app/nereo
WORKDIR /app

# Copiar solo el archivo de requisitos primero para aprovechar el caché de Docker
COPY app/requirements.txt .

# Instalar dependencias
RUN apk add --no-cache bash && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY app/ .

# Exponer el puerto (Render asignará dinámicamente, pero lo especificamos)
EXPOSE 3000

# Configurar la variable de entorno para Flask
ENV FLASK_ENV=production

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "run:app"]
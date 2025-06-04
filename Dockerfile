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

# Exponer el puerto que usará Render (por defecto 10000)
EXPOSE 10000

# Configurar la variable de entorno para el puerto
ENV PORT=10000

# Comando para ejecutar la aplicación con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]
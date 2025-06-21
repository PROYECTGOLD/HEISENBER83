# Imagen base ligera de Python 3.10
FROM python:3.10-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos ffmpeg para moviepy y librerías del sistema necesarias
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copiamos el archivo con las dependencias Python
COPY requirements.txt .

# Instalamos las dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código fuente al contenedor
COPY . .

# Exponemos el puerto 10000 (el que usas en Render)
EXPOSE 10000

# Comando para iniciar la app con Gunicorn y 1 worker
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:10000", "app:app"]

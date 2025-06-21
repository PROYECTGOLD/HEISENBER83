# Usamos una imagen oficial de Python 3.10 slim (más liviana)
FROM python:3.10-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias
COPY requirements.txt .

# Instalamos las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código fuente al contenedor
COPY . .

# Puerto en el que la app va a escuchar (Render usa 10000 según tu config)
EXPOSE 10000

# Comando para arrancar la app con gunicorn (1 worker)
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:10000", "app:app"]

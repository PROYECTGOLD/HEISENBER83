FROM python:3.10-slim

WORKDIR /app

# Instalar ffmpeg y dependencias
RUN apt-get update && apt-get install -y ffmpeg curl && apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:10000", "app:app"]

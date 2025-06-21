# Heisenber83 Video Generator

## Descripción
Este proyecto genera videos a partir de imágenes e ideas usando Flask, MoviePy, y sube el resultado a Google Drive.

## Archivos

- `app.py`: API REST en Flask para generar videos.
- `Dockerfile`: Imagen Docker con dependencias.
- `requirements.txt`: Dependencias de Python.
- `generate_images.py`: Script para generar imágenes simuladas.
- `tts.py`: Genera audio TTS local con pyttsx3.
- `video_creator.py`: Crea videos con imágenes y audio.
- `main.py`: FastAPI para batch de prompts (opcional).
- `prompts.txt`: Prompts para batch.

## Uso

1. Construye la imagen Docker:

```bash
docker build -t heisenber83 .
```

2. Ejecuta el contenedor:

```bash
docker run -p 10000:10000 -v /ruta/a/credenciales:/etc/secrets heisenber83
```

3. Llama al endpoint POST `/generar_video` enviando JSON con:

```json
{
  "idea": "Texto para el video",
  "imagenes": ["url_de_la_imagen"]
}
```

## Notas
- Monta el archivo JSON de credenciales de Google en `/etc/secrets/heisenberg-credentials.json`.
- Requiere ffmpeg instalado (incluido en Dockerfile).

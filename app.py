from flask import Flask, request, jsonify
from moviepy.editor import ImageClip, concatenate_videoclips
import os
import tempfile
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

app = Flask(__name__)

# Ruta al archivo de credenciales en Render
CREDENTIALS_PATH = "/etc/secrets/heisenberg-credentials.json"
# ID de carpeta de destino en tu Google Drive
FOLDER_ID = "1952GPiJ002KyA8hYkEnt7nvSSGAHweoN"

def descargar_imagen(url):
    response = requests.get(url)
    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
            f.write(response.content)
            return f.name
    else:
        raise Exception(f"Error al descargar imagen: {response.status_code}")

def subir_a_drive(ruta_video, nombre_video):
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    service = build("drive", "v3", credentials=creds)
    file_metadata = {"name": nombre_video, "parents": [FOLDER_ID]}
    media = MediaFileUpload(ruta_video, mimetype="video/mp4")
    archivo = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    video_id = archivo.get("id")
    return f"https://drive.google.com/file/d/{video_id}/view"

@app.route("/generar_video", methods=["POST"])
def generar_video():
    try:
        data = request.get_json()
        idea = data.get("idea")
        imagen_url = data.get("imagenes", [])[0]  # Solo la primera imagen

        if not idea or not imagen_url:
            return jsonify({"error": "Faltan datos: 'idea' o 'imagenes'"}), 400

        # Descargar imagen desde URL
        imagen_local = descargar_imagen(imagen_url)

        # Crear clip de 12s con la imagen redimensionada (vertical 1080x1920)
        clip = ImageClip(imagen_local).set_duration(12).resize(height=1920).set_position("center")
        video = concatenate_videoclips([clip], method="compose")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as f:
            ruta_video = f.name
            video.write_videofile(ruta_video, fps=24, codec="libx264")

        nombre_video = f"{idea[:50].replace(' ', '_')}.mp4"
        video_url = subir_a_drive(ruta_video, nombre_video)

        # Limpiar archivos temporales
        os.remove(ruta_video)
        os.remove(imagen_local)

        return jsonify({"video_url": video_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

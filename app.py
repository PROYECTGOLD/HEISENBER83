from flask import Flask, request, jsonify
from moviepy.editor import ImageClip, concatenate_videoclips
import os
import tempfile
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

app = Flask(__name__)

FOLDER_ID = "1952GPiJ002KyA8hYkEnt7nvSSGAHweoN"
CREDENTIALS_PATH = "/etc/secrets/heisenberg-credentials.json"

def subir_a_drive(ruta_video, nombre_video):
    creds = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
    service = build("drive", "v3", credentials=creds)
    file_metadata = {"name": nombre_video, "parents": [FOLDER_ID]}
    media = MediaFileUpload(ruta_video, mimetype="video/mp4")
    archivo = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return f"https://drive.google.com/file/d/{archivo['id']}/view"

@app.route("/generar_video", methods=["POST"])
def generar_video():
    data = request.get_json()
    idea = data.get("idea")
    imagenes = data.get("imagenes", [])

    if not idea or not imagenes or not imagenes[0]:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        clip = ImageClip(imagenes[0]).set_duration(12).resize(height=1920).set_position("center")
        video = concatenate_videoclips([clip], method="compose")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as f:
            ruta_video = f.name
            video.write_videofile(ruta_video, fps=24, codec="libx264", audio=False)

        nombre_video = f"{idea[:50].replace(' ', '_')}.mp4"
        video_url = subir_a_drive(ruta_video, nombre_video)
        os.remove(ruta_video)

        return jsonify({"video_url": video_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

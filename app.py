from flask import Flask, request, jsonify
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

app = Flask(__name__)

# Carga de credenciales de Google
SERVICE_ACCOUNT_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)

@app.route("/generate", methods=["POST"])
def generate_video():
    try:
        data = request.json
        image_path = data["image_path"]
        audio_path = data["audio_path"]
        duration = data.get("duration", 5)
        output_path = "output_video.mp4"

        clip = ImageClip(image_path, duration=duration).set_audio(AudioFileClip(audio_path))
        clip = clip.set_duration(duration)
        clip.write_videofile(output_path, fps=24)

        # Subir a Google Drive
        file_metadata = {"name": output_path}
        media = MediaFileUpload(output_path, mimetype="video/mp4")
        file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

        return jsonify({"status": "success", "video_id": file.get("id")})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Flask Render Video Service is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
INSTRUCCIONES:

1. Sube este ZIP a GitHub o directamente a Render.
2. En Render, crea un nuevo Web Service:
   - Runtime: Python 3
   - Start command: ./start.sh
   - Añade tu archivo client_secrets.json como archivo secreto en la pestaña de Environment.
3. Envía un POST a /generate con:
   {
     "image_path": "ruta/a/la/imagen.jpg",
     "audio_path": "ruta/a/la/audio.mp3",
     "duration": 5
   }
4. El servicio generará un video y lo subirá a tu Google Drive.
import pyttsx3
import os

def generate_audio(prompt, index=0):
    audio_path = f"static/audio_{index}.mp3"
    engine = pyttsx3.init()
    engine.save_to_file(prompt, audio_path)
    engine.runAndWait()
    return audio_path

from moviepy.editor import *
import os

def create_video(image_paths, audio_path, index=0):
    clips = [ImageClip(m).set_duration(2).resize(height=1080) for m in image_paths]
    video = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(audio_path)
    final = video.set_audio(audio)
    out_path = f"static/final_video_{index}.mp4"
    final.write_videofile(out_path, fps=24)
    return os.path.basename(out_path)

from fastapi import FastAPI
from generate_images import generate_images_from_prompt
from video_creator import create_video
from tts import generate_audio
import os

app = FastAPI()

@app.post("/render_next")
def render_next():
    with open("prompts.txt", "r") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines):
        if not line.startswith("#done"):
            prompt = line.strip()
            break
    else:
        return {"status": "No more prompts"}

    img_paths = generate_images_from_prompt(prompt, index=idx)
    audio_path = generate_audio(prompt, idx)
    video_path = create_video(img_paths, audio_path, idx)

    lines[idx] = f"#done {prompt}\n"
    with open("prompts.txt", "w") as f:
        f.writelines(lines)

    return {"video_url": f"/static/{video_path}"}

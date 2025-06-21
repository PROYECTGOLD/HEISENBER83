from PIL import Image, ImageDraw
import os

def generate_images_from_prompt(prompt, index=0):
    os.makedirs("static/frames", exist_ok=True)
    img_paths = []
    for i in range(5):
        img = Image.new("RGB", (512, 768), color=(30, 30, 30))
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), prompt, fill=(255, 255, 255))
        path = f"static/frames/prompt_{index}_img_{i}.png"
        img.save(path)
        img_paths.append(path)
    return img_paths

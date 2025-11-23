# src/generate_pseudoword_stimuli.py
import os
from PIL import Image, ImageDraw, ImageFont

COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 128, 0),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "brown": (139, 69, 19),
    "pink": (255, 192, 203),
    "gray": (128, 128, 128),
    "black": (0, 0, 0),
}

# Reviewer için tek bir pseudoword yeterli → ZARP
PSEUDOWORD = "zarp"

def generate(output_dir="data/pseudoword_stimuli"):
    os.makedirs(output_dir, exist_ok=True)

    font_size = 80
    img_w, img_h = 384, 256

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    for color_name, rgb in COLORS.items():
        # Congruent
        img = Image.new("RGB", (img_w, img_h), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((img_w//4, img_h//3), PSEUDOWORD.upper(), fill=rgb, font=font)
        img.save(f"{output_dir}/{PSEUDOWORD}_congruent_{color_name}.png")

        # Incongruent: all other colors
        for alt_name, alt_rgb in COLORS.items():
            if alt_name == color_name:
                continue
            img = Image.new("RGB", (img_w, img_h), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.text((img_w//4, img_h//3), PSEUDOWORD.upper(), fill=alt_rgb, font=font)
            img.save(f"{output_dir}/{PSEUDOWORD}_incongruent_{color_name}_{alt_name}.png")

    print(f"Generated pseudoword stimuli → {output_dir}/")


if __name__ == "__main__":
    generate()

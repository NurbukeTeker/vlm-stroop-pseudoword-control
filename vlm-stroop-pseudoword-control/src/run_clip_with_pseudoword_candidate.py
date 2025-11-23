# src/run_clip_with_pseudoword_candidate.py
import os
import torch
import pandas as pd
from PIL import Image
from tqdm import tqdm
from transformers import CLIPProcessor, CLIPModel

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Real colors
COLORS = [
    "red", "blue", "green", "yellow", "orange",
    "purple", "brown", "pink", "gray", "black"
]

# Pseudoword under test
PSEUDOWORD = "zarp"

# Candidate set (this is the FIX!)
CANDIDATES = COLORS + [PSEUDOWORD]

def run(
    input_dir="data/pseudoword_stimuli",
    output_dir="outputs/clip_predictions"
):
    os.makedirs(output_dir, exist_ok=True)

    # Load CLIP
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(DEVICE)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    model.eval()

    # Prompts = single-word labels ONLY (CRITICAL FIX)
    prompts = CANDIDATES

    results = []
    for fname in tqdm(os.listdir(input_dir)):
        if not fname.endswith(".png"):
            continue

        img = Image.open(os.path.join(input_dir, fname)).convert("RGB")

        # Prepare inputs
        inputs = processor(
            text=prompts,
            images=img,
            return_tensors="pt",
            padding=True
        ).to(DEVICE)

        with torch.no_grad():
            logits = model(**inputs).logits_per_image
            probs = logits.softmax(dim=1)[0]
            pred_idx = probs.argmax().item()
            pred_color = CANDIDATES[pred_idx]

        results.append({
            "image": fname,
            "prediction": pred_color
        })

    df = pd.DataFrame(results)
    df.to_csv(f"{output_dir}/clip_predictions.csv", index=False)
    print(f"Saved predictions → {output_dir}/clip_predictions.csv")


if __name__ == "__main__":
    run()

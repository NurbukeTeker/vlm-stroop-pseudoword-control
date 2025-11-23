# src/analyze_predictions.py
import os
import pandas as pd

PSEUDOWORD = "zarp"

def analyze(
    pred_file="outputs/clip_predictions/clip_predictions.csv",
    output_file="outputs/clip_predictions/clip_analysis.csv"
):
    df = pd.read_csv(pred_file)

    summary = {
        "total": len(df),
        "ink_correct": 0,
        "zarp_chosen": 0,
        "random_incorrect": 0,
    }

    for _, row in df.iterrows():
        img = row["image"]
        pred = row["prediction"]

        parts = img.replace(".png", "").split("_")

        # format: zarp_congruent_red.png
        # or: zarp_incongruent_red_blue.png
        if "congruent" in img:
            ink_color = parts[-1]
        else:
            ink_color = parts[-1]  # the last color is the ink

        # Count metrics
        if pred == ink_color:
            summary["ink_correct"] += 1
        elif pred == PSEUDOWORD:
            summary["zarp_chosen"] += 1
        else:
            summary["random_incorrect"] += 1

    pd.DataFrame([summary]).to_csv(output_file, index=False)
    print(f"Saved analysis → {output_file}")


if __name__ == "__main__":
    analyze()

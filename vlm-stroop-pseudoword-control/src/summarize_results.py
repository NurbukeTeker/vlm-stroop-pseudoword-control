# src/summarize_results.py
import pandas as pd

def summarize(
    file="outputs/clip_predictions/clip_analysis.csv",
    output_file="results/pseudoword_summary.csv"
):
    df = pd.read_csv(file)

    total = df["total"][0]
    summary = {
        "Model": "CLIP ViT-B/32",
        "Ink Accuracy (%)": df["ink_correct"][0] * 100 / total,
        "ZARP chosen (%)": df["zarp_chosen"][0] * 100 / total,
        "Random incorrect (%)": df["random_incorrect"][0] * 100 / total
    }

    out = pd.DataFrame([summary])
    out.to_csv(output_file, index=False)
    print(f"Final summary → {output_file}")


if __name__ == "__main__":
    summarize()

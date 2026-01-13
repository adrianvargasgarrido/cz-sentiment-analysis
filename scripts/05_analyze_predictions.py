"""
Analyze prediction results.
Generates distribution charts, confidence stats, and example predictions.
"""
import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.utils import find_project_root, load_latest_predictions

PROJECT_ROOT = find_project_root()
SENTIMENTS = ["Negative", "Neutral", "Positive"]
COLORS = ["#e74c3c", "#3498db", "#27ae60"]


def save_class_distribution(df: pd.DataFrame, output_dir: Path):
    """Save sentiment distribution chart and CSV."""
    dist = (df["predicted_sentiment"]
            .value_counts()
            .reindex(SENTIMENTS, fill_value=0)
            .rename_axis("sentiment")
            .reset_index(name="count"))
    
    dist["percentage"] = dist["count"] / len(df) * 100
    dist.to_csv(output_dir / "class_distribution.csv", index=False)

    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    sns.barplot(data=dist, x="sentiment", y="count", palette=COLORS, ax=ax1)
    ax1.set_title("Sentiment Distribution (Counts)", fontweight="bold")
    ax1.set_xlabel("")
    ax1.bar_label(ax1.containers[0])

    sns.barplot(data=dist, x="sentiment", y="percentage", palette=COLORS, ax=ax2)
    ax2.set_title("Sentiment Distribution (%)", fontweight="bold")
    ax2.set_xlabel("")
    ax2.bar_label(ax2.containers[0], fmt="%.1f%%")

    plt.tight_layout()
    fig.savefig(output_dir / "distribution.png", dpi=150)
    plt.close()

    return dist


def save_confidence_summary(df: pd.DataFrame, output_dir: Path):
    """Save confidence statistics for each sentiment."""
    conf_cols = ["confidence_negative", "confidence_neutral", "confidence_positive"]
    
    rows = []
    for sentiment, col in zip(SENTIMENTS, conf_cols):
        subset = df[df["predicted_sentiment"] == sentiment]
        if subset.empty:
            continue
        rows.append({
            "sentiment": sentiment,
            "mean": subset[col].mean(),
            "median": subset[col].median(),
            "min": subset[col].min(),
            "max": subset[col].max()
        })
    
    summary = pd.DataFrame(rows)
    summary.to_csv(output_dir / "confidence_summary.csv", index=False)
    return summary


def save_text_length_stats(df: pd.DataFrame, output_dir: Path):
    """Save text length statistics."""
    lengths = df["text"].str.len()
    stats = pd.DataFrame({
        "metric": ["mean", "median", "min", "max"],
        "characters": [lengths.mean(), lengths.median(), lengths.min(), lengths.max()]
    })
    stats.to_csv(output_dir / "text_length_stats.csv", index=False)
    return stats


def save_representative_examples(df: pd.DataFrame, output_dir: Path, top_n: int = 5):
    """Save markdown with high/low confidence examples per sentiment."""
    df = df.copy()
    df["max_conf"] = df[["confidence_negative", "confidence_neutral", "confidence_positive"]].max(axis=1)

    with (output_dir / "representative_examples.md").open("w") as f:
        f.write("# Representative Predictions\n\n")
        
        for sentiment in SENTIMENTS:
            subset = df[df["predicted_sentiment"] == sentiment]
            f.write(f"## {sentiment.upper()}\n\n")
            if subset.empty:
                f.write("No predictions.\n\n")
                continue

            high = subset.nlargest(top_n, "max_conf")
            low = subset.nsmallest(top_n, "max_conf")

            f.write(f"### High confidence ({len(high)})\n")
            for _, row in high.iterrows():
                f.write(f"- **{row['max_conf']:.2f}**: {row['text']}\n")
            f.write("\n")

            f.write(f"### Low confidence ({len(low)})\n")
            for _, row in low.iterrows():
                f.write(f"- **{row['max_conf']:.2f}**: {row['text']}\n")
            f.write("\n")


def save_most_uncertain(df: pd.DataFrame, output_dir: Path, limit: int = 50):
    """Save CSV of predictions with lowest confidence."""
    df = df.copy()
    df["max_conf"] = df[["confidence_negative", "confidence_neutral", "confidence_positive"]].max(axis=1)
    uncertain = df.nsmallest(limit, "max_conf")
    uncertain.to_csv(output_dir / "most_uncertain_predictions.csv", index=False)


def main():
    print("Analyzing predictions...")
    
    df, run_dir = load_latest_predictions(PROJECT_ROOT)
    analysis_dir = run_dir / "analysis"
    analysis_dir.mkdir(exist_ok=True)
    print(f"Loaded {len(df)} predictions")
    
    dist = save_class_distribution(df, analysis_dir)
    conf = save_confidence_summary(df, analysis_dir)
    stats = save_text_length_stats(df, analysis_dir)
    save_representative_examples(df, analysis_dir)
    save_most_uncertain(df, analysis_dir)
    
    print("\nDistribution:")
    print(dist.to_string(index=False))
    print("\nConfidence:")
    print(conf.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
    print("\nText length:")
    print(stats.to_string(index=False, float_format=lambda x: f"{x:.1f}"))
    print(f"\nSaved to {analysis_dir.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

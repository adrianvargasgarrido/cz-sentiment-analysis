"""
Flag sustained negative sentiment patterns.
Alerts when negative comments exceed threshold in rolling window.
"""
import argparse
import sys
import json
from pathlib import Path

import pandas as pd
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.utils import find_project_root, load_latest_predictions

PROJECT_ROOT = find_project_root()
CONFIG_PATH = PROJECT_ROOT / "config.yaml"


def compute_alert_windows(df, window_size, ratio_threshold, min_confidence, require_full_window):
    
    df = df.copy()
    df["row_number"] = df.index + 1

    # Mark negative comments
    is_neg = df["predicted_sentiment"].str.lower() == "negative"
    if min_confidence is not None:
        is_neg &= df["confidence_negative"] >= min_confidence
    df["is_negative"] = is_neg.astype(int)

    # Rolling window calculations
    min_periods = window_size if require_full_window else 1
    df["window_size"] = df["is_negative"].rolling(window=window_size, min_periods=1).count()
    df["neg_count"] = df["is_negative"].rolling(window=window_size, min_periods=min_periods).sum()

    if require_full_window:
        df["neg_ratio"] = df["neg_count"] / window_size
    else:
        df["neg_ratio"] = df["neg_count"] / df["window_size"].replace(0, pd.NA)
    
    df["neg_ratio"] = df["neg_ratio"].fillna(0.0)
    df["neg_count"] = df["neg_count"].fillna(0).astype(int)
    df["window_size"] = df["window_size"].fillna(0).astype(int)

    # Find windows that exceed threshold
    flagged = []
    for idx, ratio in df["neg_ratio"].items():
        if ratio < ratio_threshold:
            continue
        win_size = int(df.at[idx, "window_size"])
        if win_size == 0:
            continue
        start_idx = max(0, idx - win_size + 1)
        flagged.append({
            "window_end_row": int(df.at[idx, "row_number"]),
            "window_start_row": int(df.at[start_idx, "row_number"]),
            "window_size": win_size,
            "negative_count": int(df.at[idx, "neg_count"]),
            "negative_ratio": float(ratio),
        })

    flagged_windows = pd.DataFrame(flagged)

    # Get latest window stats
    if df.empty:
        latest_ratio = 0.0
        latest_size = 0
        latest_count = 0
    else:
        latest_ratio = float(df["neg_ratio"].iloc[-1])
        latest_size = int(df["window_size"].iloc[-1])
        latest_count = int(df["neg_count"].iloc[-1])

    window_ready = latest_size >= window_size if require_full_window else latest_size > 0
    alert_active = window_ready and latest_ratio >= ratio_threshold

    status = {
        "window_size": window_size,
        "ratio_threshold": ratio_threshold,
        "min_confidence": min_confidence,
        "require_full_window": require_full_window,
        "latest_window_size": latest_size,
        "latest_negative_count": latest_count,
        "latest_negative_ratio": latest_ratio,
        "alert_active": alert_active,
        "total_flagged": len(flagged_windows),
    }

    return df, flagged_windows, status


def save_reports(df, flagged_windows, alert_dir, status):
    """Save alert status and flagged windows."""
    with open(alert_dir / "alert_status.json", "w") as f:
        json.dump(status, f, indent=2)

    flagged_windows.to_csv(alert_dir / "flagged_windows.csv", index=False)

    # Save recent window details
    recent_size = min(status["window_size"], len(df))
    if recent_size > 0:
        recent = df.tail(recent_size).copy()
        cols = ["row_number", "predicted_sentiment", "confidence_negative", "is_negative", "neg_ratio"]
        if "text" in recent.columns:
            cols.insert(1, "text")
        recent[cols].to_csv(alert_dir / "recent_window.csv", index=False)

    # Generate markdown summary
    with open(alert_dir / "summary.md", "w") as f:
        f.write("# Negative Sentiment Alert\n\n")
        f.write(f"**Window size:** {status['window_size']}\n")
        f.write(f"**Threshold:** {status['ratio_threshold']:.2f}\n")
        if status['min_confidence']:
            f.write(f"**Min confidence:** {status['min_confidence']:.2f}\n")
        f.write(f"**Latest ratio:** {status['latest_negative_ratio']:.2%}\n")
        f.write(f"**Flagged windows:** {status['total_flagged']}\n\n")

        if status["alert_active"]:
            f.write("⚠️ Alert active\n\n")
        else:
            f.write("✅ No alert\n\n")

        if not flagged_windows.empty:
            f.write("## Flagged Windows\n\n")
            for _, row in flagged_windows.tail(5).iterrows():
                f.write(f"- Rows {row['window_start_row']}-{row['window_end_row']}: "
                       f"{row['negative_count']}/{row['window_size']} "
                       f"({row['negative_ratio']:.1%})\n")

        # Show sample negative comments
        recent = df.tail(status['window_size'])
        neg_comments = recent[recent["is_negative"] == 1]
        if not neg_comments.empty:
            f.write("\n## Recent Negative Comments\n\n")
            for _, row in neg_comments.head(5).iterrows():
                text = str(row.get("text", "")).replace("\n", " ").strip()
                if len(text) > 150:
                    text = text[:147] + "..."
                f.write(f"- Row {int(row['row_number'])}: {text}\n")


def parse_args():
    parser = argparse.ArgumentParser(description="Flag negative sentiment patterns")
    parser.add_argument("--window-size", type=int, help="Rolling window size")
    parser.add_argument("--threshold", type=float, help="Negative ratio threshold (0-1)")
    parser.add_argument("--min-confidence", type=float, help="Min confidence to count as negative")
    parser.add_argument("--require-full-window", action="store_true", help="Wait for full window")
    return parser.parse_args()


def main():
    print("Flagging negative sentiment patterns...\n")

    args = parse_args()

    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    alerts_cfg = config.get("prediction_alerts", {})

    # Get parameters from config or CLI
    window_size = args.window_size or alerts_cfg.get("window_size", 100)
    threshold = args.threshold or alerts_cfg.get("negative_ratio_threshold", 0.3)
    min_confidence = args.min_confidence or alerts_cfg.get("min_negative_confidence")
    require_full = args.require_full_window or alerts_cfg.get("require_full_window", False)

    print(f"Window: {window_size}, Threshold: {threshold:.2f}, "
          f"Min confidence: {min_confidence or 'None'}, Full window: {require_full}\n")

    df, run_dir = load_latest_predictions(PROJECT_ROOT)
    
    # Validate columns
    required = {"predicted_sentiment", "confidence_negative"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(missing)}")
    
    df["predicted_sentiment"] = df["predicted_sentiment"].astype(str)
    
    alert_dir = run_dir / "alerts"
    alert_dir.mkdir(parents=True, exist_ok=True)
    
    df, flagged, status = compute_alert_windows(df, window_size, threshold, min_confidence, require_full)

    save_reports(df, flagged, alert_dir, status)

    if status["alert_active"]:
        print(f"⚠️  Alert: {status['latest_negative_ratio']:.1%} negative in latest window "
              f"(threshold: {threshold:.1%})")
    else:
        print(f"✅ No alert: {status['latest_negative_ratio']:.1%} negative in latest window")

    print(f"\nReports saved to {alert_dir}")


if __name__ == "__main__":
    main()

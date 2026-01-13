"""Shared utility functions for the sentiment analysis project."""

from pathlib import Path
import pandas as pd


def find_project_root(markers=("pyproject.toml", "src", "config.yaml")):
    """Find project root by looking for marker files."""
    current_path = Path.cwd()
    for parent in [current_path] + list(current_path.parents):
        if any((parent / marker).exists() for marker in markers):
            return parent
    return current_path


def find_latest_run_dir(runs_base_dir):
    """Return the most recent run directory, if any."""
    if not runs_base_dir.exists():
        return None
    run_dirs = [p for p in runs_base_dir.iterdir() if p.is_dir()]
    if not run_dirs:
        return None
    return max(run_dirs, key=lambda p: p.name)


def load_latest_predictions(project_root):
    """Load predictions from latest run in results folder.
    
    Returns:
        tuple: (predictions_df, run_dir)
    """
    results_root = project_root / "results"
    if not results_root.exists():
        raise FileNotFoundError("No results folder. Run 04_predict.py first.")
    
    run_dirs = sorted([d for d in results_root.iterdir() if d.is_dir()], reverse=True)
    if not run_dirs:
        raise FileNotFoundError(f"No runs found in {results_root}")
    
    latest_run = run_dirs[0]
    predictions_path = latest_run / "predictions" / "predictions.csv"
    
    if not predictions_path.exists():
        raise FileNotFoundError("Predictions not found. Run 04_predict.py first.")
    
    df = pd.read_csv(predictions_path)
    return df, latest_run
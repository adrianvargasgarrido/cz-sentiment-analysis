"""CLI entry point to orchestrate the sentiment analysis pipeline."""

import argparse
import subprocess
import sys
from pathlib import Path

# --- Project Setup ---
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.utils import find_project_root

PROJECT_ROOT = find_project_root()
SCRIPT_DIR = PROJECT_ROOT / "scripts"


def run_script(name: str, script_path: Path, extra_args=None):
    if extra_args is None:
        extra_args = []
    cmd = [sys.executable, str(script_path)] + extra_args
    print(f"\n=== Running step: {name} ===")
    print("Command:", " ".join(cmd))
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Step '{name}' failed with exit code {result.returncode}.")
    print(f"=== Step '{name}' completed successfully ===\n")

def main():
    parser = argparse.ArgumentParser(description="Run the sentiment analysis pipeline.")
    parser.add_argument(
        "step",
        choices=["prepare", "train", "evaluate", "predict", "all"],
        help="The pipeline step to run."
    )
    parser.add_argument(
        '--epochs', type=int, help='Number of training epochs for the train step.'
    )
    parser.add_argument(
        '--lr', type=float, help='Learning rate for the train step.'
    )
    parser.add_argument(
        '--class-weighting',
        type=str,
        choices=['none', 'balanced', 'extreme', 'custom'],
        help='Class weighting strategy for the train step.'
    )
    parser.add_argument(
        '--extreme-weight',
        type=float,
        help="Weight multiplier for 'extreme' strategy."
    )
    parser.add_argument(
        '--monitor-metric',
        type=str,
        choices=['accuracy', 'macro_f1', 'weighted_f1'],
        help='Metric to monitor for saving the best model.'
    )

    args, remaining_argv = parser.parse_known_args()
    
    prepare_script = SCRIPT_DIR / "01_prepare_data.py"
    train_script = SCRIPT_DIR / "02_train_model.py"
    evaluate_script = SCRIPT_DIR / "03_evaluate_model.py"
    predict_script = SCRIPT_DIR / "04_predict.py"

    if args.step in {"prepare", "all"}:
        run_script("prepare", prepare_script)
    
    if args.step in {"train", "all"}:
        train_args = []
        if args.epochs is not None:
            train_args += ['--epochs', str(args.epochs)]
        if args.lr is not None:
            train_args += ['--lr', str(args.lr)]
        if args.class_weighting is not None:
            train_args += ['--class-weighting', args.class_weighting]
        if args.extreme_weight is not None:
            train_args += ['--extreme-weight', str(args.extreme_weight)]
        if args.monitor_metric is not None:
            train_args += ['--monitor-metric', args.monitor_metric]
        train_args += remaining_argv
        run_script("train", train_script, train_args)

    if args.step in {"evaluate", "all"}:
        run_script("evaluate", evaluate_script)

    if args.step in {"predict", "all"}:
        run_script("predict", predict_script)

if __name__ == "__main__":
    main()

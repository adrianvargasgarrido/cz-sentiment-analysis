"""
Train sentiment analysis model.
Fine-tunes ELECTRA on processed data using config.yaml settings.
Supports CLI overrides for hyperparameters.
"""
import sys
import argparse
from pathlib import Path
from datetime import datetime
import shutil
import yaml
import warnings

warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+.*LibreSSL")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.utils import find_project_root
from src.train import main as run_training

PROJECT_ROOT = find_project_root()

def main():
    """Run training with config from YAML and optional CLI overrides."""
    print("Starting model training...\n")

    # --- Load Config from YAML ---
    config_path = PROJECT_ROOT / "config.yaml"
    print(f"Loading config from {config_path}")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    train_config = config.get('training', {})
    data_config = config.get('data', {})
    model_config = config.get('model', {})
    
    parser = argparse.ArgumentParser(description="Train sentiment model with config overrides")
    parser.add_argument("--train-data", type=str, default=str(PROJECT_ROOT / data_config.get('train_data')))
    parser.add_argument("--val-data", type=str, default=str(PROJECT_ROOT / data_config.get('val_data')))
    parser.add_argument("--model-dir", type=str, default=str(PROJECT_ROOT / model_config.get('base_model_dir')))
    parser.add_argument("--output-dir", type=str, default=str(PROJECT_ROOT / model_config.get('output_dir')))
    parser.add_argument("--epochs", type=int, default=train_config.get('epochs'))
    parser.add_argument("--batch-size", type=int, default=train_config.get('batch_size'))
    parser.add_argument("--lr", type=float, default=train_config.get('lr'))
    parser.add_argument("--warmup-ratio", type=float, default=train_config.get('warmup_ratio'))
    parser.add_argument("--num-workers", type=int, default=train_config.get('num_workers'))
    parser.add_argument("--seed", type=int, default=config.get('seed'))
    parser.add_argument("--monitor-metric", type=str, default=train_config.get('monitor_metric'))
    parser.add_argument("--class-weighting", type=str, default=train_config.get('class_weighting'))
    parser.add_argument("--class-weights", nargs='+', type=float, default=train_config.get('class_weights'))
    parser.add_argument("--loss-function", type=str, default=train_config.get('loss_function', 'cross_entropy'))
    parser.add_argument("--focal-loss-gamma", type=float, default=train_config.get('focal_loss_gamma', 2.0))
    parser.add_argument(
        "--use-weighted-sampler",
        action=argparse.BooleanOptionalAction,
        default=train_config.get('use_weighted_sampler', False)
    )
    
    args = parser.parse_args()

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    base_output_dir = Path(args.output_dir)
    base_output_dir.mkdir(parents=True, exist_ok=True)
    run_dir = base_output_dir / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    # Save a snapshot of the configuration for reproducibility
    config_snapshot_path = run_dir / "config.yaml"
    shutil.copy2(config_path, config_snapshot_path)

    print(f"Run ID: {run_id}")
    print(f"Output: {run_dir}\n")

    cmd_args = [
        "--train-data", args.train_data,
        "--val-data", args.val_data,
        "--model-dir", args.model_dir,
        "--output-dir", str(run_dir),
        "--epochs", str(args.epochs),
        "--batch-size", str(args.batch_size),
        "--lr", str(args.lr),
        "--warmup-ratio", str(args.warmup_ratio),
        "--num-workers", str(args.num_workers),
        "--seed", str(args.seed),
        "--monitor-metric", args.monitor_metric,
        "--class-weighting", args.class_weighting,
        "--loss-function", args.loss_function,
        "--focal-loss-gamma", str(args.focal_loss_gamma),
    ]
    if args.class_weighting == 'custom' and args.class_weights:
        cmd_args.append("--class-weights")
        cmd_args.extend([str(w) for w in args.class_weights])
    if args.use_weighted_sampler:
        cmd_args.append("--use-weighted-sampler")

    original_argv = sys.argv
    sys.argv = [original_argv[0]] + cmd_args
    
    print("Starting training with configuration:")
    print(" ".join(sys.argv[1:]))
    print()

    run_training()
    
    sys.argv = original_argv

    print(f"\nArtifacts saved in: {run_dir}")
    print("Training complete!")

if __name__ == "__main__":
    main()

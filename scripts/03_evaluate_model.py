"""
Evaluate trained sentiment model on test set.
Generates classification reports, confusion matrices, and error analysis.
"""
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import torch
from torch.utils.data import DataLoader
from transformers import ElectraTokenizerFast, ElectraForSequenceClassification
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm.auto import tqdm
import yaml
import warnings

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+.*LibreSSL")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.utils import find_project_root, find_latest_run_dir
from src.model import SentimentDataset

PROJECT_ROOT = find_project_root()

CONFIG_PATH = PROJECT_ROOT / "config.yaml"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
CLASS_NAMES = ['Negative', 'Neutral', 'Positive']
MODEL_SUBDIR = "trained_sentiment_electra"



def resolve_model_path(
    model_path_setting: str,
    runs_base_dir: Path,
    project_root: Path,
) -> tuple[Path, Path]:
    """Return (run_dir, model_path) based on config setting.

    model_path_setting can be:
    - "latest" (handled outside this function)
    - a relative/absolute path to the model directory
    - a run name under runs_base_dir
    """
    candidate_path = Path(model_path_setting)
    if not candidate_path.is_absolute():
        candidate_path = project_root / candidate_path

    if candidate_path.exists():
        model_path = candidate_path
        run_dir = model_path.parent if model_path.name == MODEL_SUBDIR else candidate_path
        return run_dir, model_path

    run_dir = runs_base_dir / model_path_setting
    if run_dir.exists():
        return run_dir, run_dir / MODEL_SUBDIR

    raise FileNotFoundError(f"Model path not found: {model_path_setting}")


def get_predictions(model, loader):
    """Get model predictions and per-class probabilities for a dataset."""
    model.eval()
    all_predictions = []
    all_labels = []
    all_probs = []
    with torch.no_grad():
        for batch in tqdm(loader, desc="Evaluating"):
            input_ids = batch['input_ids'].to(DEVICE)
            attention_mask = batch['attention_mask'].to(DEVICE)
            labels = batch['labels'].to(DEVICE)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            probs = torch.softmax(outputs.logits, dim=-1)
            predictions = torch.argmax(probs, dim=-1)

            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
    return np.array(all_labels), np.array(all_predictions), np.array(all_probs)


def build_classification_report(y_true: np.ndarray, y_pred: np.ndarray) -> pd.DataFrame:
    """Return sklearn classification report as a DataFrame."""
    report = classification_report(
        y_true,
        y_pred,
        target_names=CLASS_NAMES,
        digits=4,
        output_dict=True,
    )
    return pd.DataFrame(report).transpose()


def _confidence_interval(prob_row: np.ndarray) -> tuple[float, float]:
    """Return (runner_up_prob, top_prob) to describe confidence spread."""
    if prob_row.size <= 1:
        return prob_row[0], prob_row[0]
    top_two = np.partition(prob_row, -2)[-2:]
    low, high = np.sort(top_two)
    return float(low), float(high)


def build_incorrect_examples(
    df: pd.DataFrame,
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_probs: np.ndarray,
) -> pd.DataFrame:
    """Return a DataFrame with metadata for misclassified samples."""
    incorrect_mask = y_true != y_pred
    if not np.any(incorrect_mask):
        return pd.DataFrame()

    subset = df.loc[incorrect_mask].copy().reset_index(drop=True)
    true_labels = y_true[incorrect_mask]
    pred_labels = y_pred[incorrect_mask]
    probs_subset = y_probs[incorrect_mask]

    pred_conf = probs_subset[np.arange(len(probs_subset)), pred_labels]
    true_conf = probs_subset[np.arange(len(probs_subset)), true_labels]
    intervals = np.array([_confidence_interval(row) for row in probs_subset])

    subset['true_label'] = true_labels
    subset['predicted_label'] = pred_labels
    subset['true_label_name'] = [CLASS_NAMES[idx] for idx in true_labels]
    subset['predicted_label_name'] = [CLASS_NAMES[idx] for idx in pred_labels]
    subset['predicted_confidence'] = np.round(pred_conf, 4)
    subset['true_label_confidence'] = np.round(true_conf, 4)
    subset['confidence_interval_low'] = np.round(intervals[:, 0], 4)
    subset['confidence_interval_high'] = np.round(intervals[:, 1], 4)

    return subset


def save_incorrect_predictions(incorrect_df: pd.DataFrame, filepath: Path):
    """Save misclassified samples to CSV with confidence metadata."""
    if incorrect_df.empty:
        print("No incorrect predictions.")
        return

    filepath.parent.mkdir(parents=True, exist_ok=True)
    incorrect_df.to_csv(filepath, index=False)
    print(f"Saved {len(incorrect_df)} misclassified samples")

def save_classification_report(report_df: pd.DataFrame, filepath: Path):
    """Persist classification report DataFrame to CSV."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    report_df.to_csv(filepath)
    print("Saved classification report")

def save_visual_classification_report(report_df: pd.DataFrame, filepath: Path):
    """Generate visual classification report using a precomputed DataFrame."""
    plot_df = report_df.loc[
        ['Negative', 'Neutral', 'Positive', 'macro avg', 'weighted avg'],
        ['precision', 'recall', 'f1-score'],
    ].round(4)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.axis('off')
    
    table = ax.table(
        cellText=plot_df.values,
        colLabels=plot_df.columns,
        rowLabels=plot_df.index,
        loc='center',
        cellLoc='center',
        colWidths=[0.15] * 3
    )

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)

    for (i, j), cell in table.get_celld().items():
        if i == 0 or j == -1:
            cell.set_text_props(weight='bold')
        if i > 0 and j > -1:
            val = float(cell.get_text().get_text())
            cell.set_facecolor('#d4edda' if val >= 0.8 else '#fff3cd' if val >= 0.6 else '#f8d7da')

    ax.set_title('Classification Report', fontweight='bold', fontsize=16, pad=20)
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved visual classification report")
def save_detailed_misclassifications(
    incorrect_df: pd.DataFrame,
    filepath: Path,
    num_examples: int = 50,
):
    """Save markdown report of misclassified examples with confidence bands."""
    if incorrect_df.empty:
        print("No incorrect predictions!")
        return

    error_counts = (
        incorrect_df
        .groupby(['true_label_name', 'predicted_label_name'])
        .size()
        .sort_values(ascending=False)
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("# Misclassification Report\n\n")
        f.write("## Most Frequent Errors\n\n")
        f.write("| True Label | Predicted Label | Count |\n")
        f.write("|------------|-----------------|-------|\n")
        for (true, pred), count in error_counts.head(5).items():
            f.write(f"| {true} | {pred} | {count} |\n")

        sample_size = min(num_examples, len(incorrect_df))
        f.write(f"\n## Sample Misclassified Comments ({sample_size})\n\n")

        sample_idx = np.random.default_rng(42).choice(len(incorrect_df), size=sample_size, replace=False)
        for i, idx in enumerate(sample_idx, 1):
            row = incorrect_df.iloc[idx]
            f.write(f"### Example {i}\n")
            f.write(
                f"**True:** `{row.true_label_name}` ({row.true_label_confidence*100:.1f}%) | "
                f"**Predicted:** `{row.predicted_label_name}` ({row.predicted_confidence*100:.1f}%)\n\n"
            )
            f.write(
                f"Confidence interval (top-2 probs): "
                f"[{row.confidence_interval_low*100:.1f}%, {row.confidence_interval_high*100:.1f}%] "
                f"| Gap: {(row.confidence_interval_high-row.confidence_interval_low)*100:.1f}%\n\n"
            )
            f.write(f"````\n{row.text}\n````\n\n")

    print("Saved misclassification analysis")


def save_confusion_matrix(y_true, y_pred, filepath):
    """Generate confusion matrix with counts and percentages."""
    cm = confusion_matrix(y_true, y_pred)
    cm_pct = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis] * 100
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax1,
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, cbar_kws={'label': 'Count'})
    ax1.set_ylabel('True Label', fontweight='bold')
    ax1.set_xlabel('Predicted Label', fontweight='bold')
    ax1.set_title('Counts', fontweight='bold')
    
    sns.heatmap(cm_pct, annot=True, fmt='.1f', cmap='Blues', ax=ax2,
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, cbar_kws={'label': '%'})
    ax2.set_ylabel('True Label', fontweight='bold')
    ax2.set_xlabel('Predicted Label', fontweight='bold')
    ax2.set_title('Percentages', fontweight='bold')
    
    filepath.parent.mkdir(parents=True, exist_ok=True)
    plt.suptitle('Confusion Matrix', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"Saved confusion matrix")

def main():
    """Evaluate model on test set."""
    print("Starting model evaluation...\n")

    print(f"Loading config from {CONFIG_PATH}")
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    
    eval_config = config['evaluation']

    test_data_path = PROJECT_ROOT / eval_config['test_data_path']
    runs_base_dir = PROJECT_ROOT / eval_config.get('runs_base_dir', 'models/runs')
    model_path_setting = eval_config.get('model_path', 'latest')

    if model_path_setting == 'latest':
        run_dir = find_latest_run_dir(runs_base_dir)
        if run_dir is None:
            print(f"Error: No runs found in {runs_base_dir}")
            print("Run training first (02_train_model.py)")
            sys.exit(1)
        model_path = run_dir / MODEL_SUBDIR
    else:
        try:
            run_dir, model_path = resolve_model_path(
                model_path_setting=model_path_setting,
                runs_base_dir=runs_base_dir,
                project_root=PROJECT_ROOT,
            )
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)

    if not model_path.exists():
        print(f"Error: Model not found at {model_path}")
        sys.exit(1)

    try:
        relative_run_dir = run_dir.relative_to(PROJECT_ROOT)
    except ValueError:
        relative_run_dir = run_dir

    print(f"Using run: {relative_run_dir}\n")

    # Save all evaluation artifacts under PROJECT_ROOT / "results" by default,
    # or under a custom subfolder inside "results" if configured.
    results_root = PROJECT_ROOT / "results"
    output_dir_setting = eval_config.get('output_dir')
    if output_dir_setting:
        output_dir = results_root / output_dir_setting
    else:
        output_dir = results_root / relative_run_dir.name

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading model from {model_path}")
    tokenizer = ElectraTokenizerFast.from_pretrained(model_path)
    model = ElectraForSequenceClassification.from_pretrained(model_path)
    model.to(DEVICE)

    print(f"Loading test data from {test_data_path}")
    test_df = pd.read_csv(test_data_path)
    test_dataset = SentimentDataset(
        texts=test_df.text.to_numpy(),
        labels=test_df.label.to_numpy(),
        tokenizer=tokenizer,
        max_length=config['model'].get('max_length', 128)
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=eval_config['batch_size'],
        num_workers=config['training'].get('num_workers', 2),
        shuffle=False
    )

    print("Running predictions on test set...\n")
    y_true, y_pred, y_probs = get_predictions(model, test_loader)

    print(f"Saving results to {output_dir}\n")

    incorrect_df = build_incorrect_examples(test_df, y_true, y_pred, y_probs)
    save_incorrect_predictions(incorrect_df, output_dir / 'incorrect_predictions.csv')
    save_detailed_misclassifications(incorrect_df, output_dir / 'misclassified_examples.md')

    report_df = build_classification_report(y_true, y_pred)
    save_classification_report(report_df, output_dir / 'classification_report.csv')
    save_visual_classification_report(report_df, output_dir / 'classification_report.png')
    save_confusion_matrix(y_true, y_pred, output_dir / 'confusion_matrix.png')

    print("\nEvaluation complete!")

if __name__ == "__main__":
    main()

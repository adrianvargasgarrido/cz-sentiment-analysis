"""
Predict sentiment on new unlabeled comments.
Loads trained model and generates predictions with confidence scores.
"""
import sys
from pathlib import Path
from typing import Optional

import pandas as pd
import torch
from transformers import ElectraTokenizerFast, ElectraForSequenceClassification
from tqdm.auto import tqdm
import yaml
import warnings

warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+.*LibreSSL")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.utils import find_project_root, find_latest_run_dir
from src.data_utils import load_prediction_comments

PROJECT_ROOT = find_project_root()

CONFIG_PATH = PROJECT_ROOT / "config.yaml"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
ID_TO_LABEL = {0: "Negative", 1: "Neutral", 2: "Positive"}
MODEL_SUBDIR = "trained_sentiment_electra"



def predict_sentiment(texts, model, tokenizer, batch_size=16):
    """Predict sentiment for texts in batches."""
    model.eval()
    predictions = []
    confidences = []
    
    for i in tqdm(range(0, len(texts), batch_size), desc="Predicting"):
        batch_texts = texts[i:i+batch_size]
        inputs = tokenizer(
            batch_texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128
        ).to(DEVICE)
        
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)
            pred_ids = torch.argmax(probs, dim=-1)
        
        predictions.extend([ID_TO_LABEL[pid.item()] for pid in pred_ids])
        confidences.extend(probs.cpu().numpy())
        
    return predictions, confidences

def main():
    """Run predictions on new data."""
    print("Starting prediction...\n")

    print(f"Loading config from {CONFIG_PATH}")
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)
    
    pred_config = config['prediction']

    runs_base_dir = PROJECT_ROOT / pred_config.get('runs_base_dir', 'models/runs')
    model_path_setting = pred_config.get('model_path', 'latest')
    input_path = PROJECT_ROOT / pred_config['input_file']

    run_dir: Optional[Path] = None

    if model_path_setting == 'latest':
        run_dir = find_latest_run_dir(runs_base_dir)
        if run_dir is None:
            print(f"Error: No runs found in {runs_base_dir}")
            print("Run training first (02_train_model.py)")
            sys.exit(1)
        model_path = run_dir / MODEL_SUBDIR
    else:
        candidate_path = Path(model_path_setting)
        if not candidate_path.is_absolute():
            candidate_path = PROJECT_ROOT / candidate_path
        
        if candidate_path.exists():
            model_path = candidate_path
            run_dir = model_path.parent if model_path.name == MODEL_SUBDIR else candidate_path
        elif (runs_base_dir / model_path_setting).exists():
            run_dir = runs_base_dir / model_path_setting
            model_path = run_dir / MODEL_SUBDIR
        else:
            print(f"Error: Model path not found: {model_path_setting}")
            sys.exit(1)

    if not model_path.exists():
        print(f"Error: Model not found at {model_path}")
        sys.exit(1)

    try:
        relative_run_dir = run_dir.relative_to(PROJECT_ROOT)
    except ValueError:
        relative_run_dir = run_dir

    print(f"Using run: {relative_run_dir}\n")

    # Save all predictions to results/ folder
    results_root = PROJECT_ROOT / "results"
    output_dir = results_root / relative_run_dir.name / "predictions"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "predictions.csv"

    print(f"Loading model from {model_path}")
    tokenizer = ElectraTokenizerFast.from_pretrained(model_path)
    model = ElectraForSequenceClassification.from_pretrained(model_path)
    model.to(DEVICE)

    print(f"Loading comments from {input_path}")
    pred_df = load_prediction_comments(input_path)
    texts_to_predict = pred_df['text'].tolist()
    print(f"Loaded {len(texts_to_predict):,} comments\n")

    print("Running predictions...")
    sentiments, probs = predict_sentiment(
        texts_to_predict, model, tokenizer, batch_size=pred_config['batch_size']
    )

    print(f"\nSaving to {output_file}")
    results_df = pd.DataFrame({
        'text': texts_to_predict,
        'predicted_sentiment': sentiments,
        'confidence_negative': [p[0] for p in probs],
        'confidence_neutral': [p[1] for p in probs],
        'confidence_positive': [p[2] for p in probs],
    })
    
    results_df.to_csv(output_file, index=False)
    print("Prediction complete!")

if __name__ == "__main__":
    main()
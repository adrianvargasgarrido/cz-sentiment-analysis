"""
Prediction script for Czech sentiment analysis.

This script loads a trained sentiment model and predicts sentiment
for new unlabeled Czech comments.
"""

import sys
from pathlib import Path
from typing import List, Tuple, Optional
import argparse

import pandas as pd
import torch
from transformers import ElectraTokenizerFast, ElectraForSequenceClassification
from tqdm.auto import tqdm
import warnings

# Suppress urllib3 warning emitted on macOS system Python with LibreSSL
warnings.filterwarnings(
    "ignore",
    message="urllib3 v2 only supports OpenSSL 1.1.1+.*LibreSSL",
)

# Import data utilities
from .data_utils import load_prediction_comments

# Constants
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
ID_TO_LABEL = {0: "Negative", 1: "Neutral", 2: "Positive"}


def predict_sentiment(
    texts: List[str],
    model,
    tokenizer,
    batch_size: int = 16,
    max_length: int = 128,
    device: torch.device = DEVICE
) -> Tuple[List[str], List]:
    """
    Predict sentiment for a list of texts in batches.
    
    Args:
        texts: List of text strings to classify
        model: Trained sentiment classification model
        tokenizer: Tokenizer for the model
        batch_size: Number of texts to process at once
        max_length: Maximum sequence length
        device: Device to run predictions on
    
    Returns:
        tuple: (predictions, confidences) where predictions are sentiment labels
               and confidences are probability distributions
    """
    model.eval()
    predictions = []
    confidences = []
    
    for i in tqdm(range(0, len(texts), batch_size), desc="Predicting sentiment"):
        batch_texts = texts[i:i+batch_size]
        inputs = tokenizer(
            batch_texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length
        ).to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)
            pred_ids = torch.argmax(probs, dim=-1)
        
        predictions.extend([ID_TO_LABEL[pid.item()] for pid in pred_ids])
        confidences.extend(probs.cpu().numpy())
        
    return predictions, confidences


def find_latest_model(models_dir: Path) -> Optional[Path]:
    """
    Find the most recently trained model in the models directory.
    
    Args:
        models_dir: Base directory containing model runs
    
    Returns:
        Path to the most recent trained model, or None if not found
    """
    if not models_dir.exists():
        return None
    
    # Look for timestamped run directories
    run_dirs = [p for p in models_dir.iterdir() if p.is_dir() and p.name.startswith("run_")]
    if run_dirs:
        latest_run = max(run_dirs, key=lambda p: p.name)
        model_path = latest_run / "trained_sentiment_electra"
        if model_path.exists():
            return model_path
    
    # Look for direct model directory
    model_path = models_dir / "trained_sentiment_electra"
    if model_path.exists():
        return model_path
    
    return None


def main():
    """CLI interface for running predictions."""
    parser = argparse.ArgumentParser(description="Predict sentiment on new Czech comments")
    parser.add_argument("--input", type=str, required=True, help="Path to input file with comments")
    parser.add_argument("--model", type=str, help="Path to trained model (default: find latest)")
    parser.add_argument("--output", type=str, default="predictions.csv", help="Output CSV file")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size for prediction")
    parser.add_argument("--max-length", type=int, default=128, help="Max sequence length")
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: Input file not found: {input_path}")
        sys.exit(1)
    
    # Determine model path
    if args.model:
        model_path = Path(args.model)
    else:
        # Try to find latest model
        models_dir = Path("models")
        model_path = find_latest_model(models_dir)
        if model_path is None:
            print("❌ Error: No trained model found. Please specify --model or train a model first.")
            sys.exit(1)
        print(f"Using latest model: {model_path}")
    
    if not model_path.exists():
        print(f"❌ Error: Model not found at {model_path}")
        sys.exit(1)
    
    # Load model and tokenizer
    print(f"\n📥 Loading model from {model_path}...")
    tokenizer = ElectraTokenizerFast.from_pretrained(model_path)
    model = ElectraForSequenceClassification.from_pretrained(model_path)
    model.to(DEVICE)
    print(f"✅ Model loaded successfully (device: {DEVICE})")
    
    # Load input data
    print(f"\n📂 Loading comments from {input_path}...")
    pred_df = load_prediction_comments(input_path)
    texts_to_predict = pred_df['text'].tolist()
    print(f"✅ Loaded {len(texts_to_predict):,} comments")
    
    # Run predictions
    print(f"\n🔮 Running sentiment prediction...")
    sentiments, probs = predict_sentiment(
        texts_to_predict,
        model,
        tokenizer,
        batch_size=args.batch_size,
        max_length=args.max_length,
        device=DEVICE
    )
    
    # Prepare results
    results_df = pd.DataFrame({
        'text': texts_to_predict,
        'predicted_sentiment': sentiments,
        'confidence_negative': [p[0] for p in probs],
        'confidence_neutral': [p[1] for p in probs],
        'confidence_positive': [p[2] for p in probs],
    })
    
    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)
    
    # Print summary
    sentiment_counts = results_df['predicted_sentiment'].value_counts()
    print(f"\n{'='*70}")
    print(f"✨ Prediction Complete!")
    print(f"{'='*70}")
    print(f"Results saved to: {output_path}")
    print(f"\nSentiment distribution:")
    for sentiment, count in sentiment_counts.items():
        pct = (count / len(results_df)) * 100
        print(f"  {sentiment:>8}: {count:>5} ({pct:.1f}%)")
    
    # Calculate average confidence
    avg_conf = results_df[[f'confidence_{s.lower()}' for s in ['Negative', 'Neutral', 'Positive']]].max(axis=1).mean()
    print(f"\nAverage confidence: {avg_conf:.2%}")
    

if __name__ == "__main__":
    main()

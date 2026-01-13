"""
Data preparation script for sentiment analysis.
Loads raw labeled comments, normalizes text, and splits into train/val/test sets.
"""
import sys
import re
import emoji
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
import yaml

# --- Project Setup ---
# Add project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.data_utils import load_labeled_comments
from src.utils import find_project_root

PROJECT_ROOT = find_project_root()

# --- Constants ---
CONFIG_PATH = PROJECT_ROOT / "config.yaml"

def normalize_text(text: str) -> str:
    """Normalize text for model input."""
    # Convert emojis to text representations
    text = emoji.demojize(text, language='en')
    text = re.sub(r':([a-zA-Z0-9_]+):', r' <\1> ', text)

    # Apply regex patterns
    replacements = [
        (r"https?://\S+|www\.\S+", " <URL> "),
        (r"@\w+", " <USER> "),
        (r"([!?.]){2,}", r" \1 <repeat> "),
        (r"([,;:])", r" \1 "),
        (r"\s+", " "),
    ]
    
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    
    # Lowercase everything (including special tokens) for consistency
    return text.strip().lower()

def main():
    """Main function to prepare and split the data based on config.yaml."""
    print("=" * 70)
    print("Data Preparation")
    print("=" * 70)

    # Load config
    print(f"\nLoading config from {CONFIG_PATH}")
    try:
        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Config file not found at {CONFIG_PATH}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML - {e}")
        sys.exit(1)
    
    # Validate required config keys
    required_keys = ['data', 'prepare_data', 'seed']
    missing_keys = [k for k in required_keys if k not in config]
    if missing_keys:
        print(f"Error: Missing config keys: {missing_keys}")
        sys.exit(1)
    
    data_config = config['data']
    prep_config = config['prepare_data']
    seed = config['seed']
    
    raw_data_path = PROJECT_ROOT / data_config['raw_labeled_comments']
    processed_dir = PROJECT_ROOT / data_config['processed_dir']

    # Load data
    print(f"\nLoading comments from {raw_data_path}")
    try:
        df = load_labeled_comments(raw_data_path)
    except FileNotFoundError:
        print(f"Error: File not found at {raw_data_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)
    
    print(f"Loaded {len(df):,} comments")
    
    label_names = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
    print("\nClass distribution:")
    for label_id, count in df['label'].value_counts().sort_index().items():
        pct = (count / len(df)) * 100
        print(f"  {label_names[label_id]}: {count:>5} ({pct:.1f}%)")

    # Normalize text
    print("\nNormalizing text (emojis, URLs, mentions, lowercasing)...")
    df['text'] = df['text'].apply(normalize_text)

    # Remove duplicates
    print("Removing duplicates...")
    initial_count = len(df)
    df_clean = df.drop_duplicates(subset=['text', 'label']).reset_index(drop=True)
    duplicates_removed = initial_count - len(df_clean)
    
    if duplicates_removed > 0:
        print(f"Removed {duplicates_removed} duplicates")
    
    print(f"Clean dataset: {len(df_clean):,} samples")
    
    print("\nClass distribution after cleaning:")
    for label_id, count in df_clean['label'].value_counts().sort_index().items():
        pct = (count / len(df_clean)) * 100
        print(f"  {label_names[label_id]}: {count:>5} ({pct:.1f}%)")

    if len(df_clean) < 10:
        print(f"Error: Not enough data ({len(df_clean)} samples)")
        sys.exit(1)

    # Split data
    print("\nSplitting into train/val/test...")
    test_size = prep_config['test_size']
    val_size = prep_config['val_size']
    print(f"Strategy: {100 * (1 - test_size):.0f}% train, "
          f"{100 * test_size * (1 - val_size):.0f}% val, "
          f"{100 * test_size * val_size:.0f}% test")
    
    try:
        df_train, df_temp = train_test_split(
            df_clean,
            test_size=test_size,
            stratify=df_clean['label'],
            random_state=seed
        )
        df_val, df_test = train_test_split(
            df_temp,
            test_size=val_size,
            stratify=df_temp['label'],
            random_state=seed
        )
    except ValueError as e:
        print(f"Error during split: {e}")
        sys.exit(1)
    
    print(f"Train: {len(df_train):>5} ({len(df_train)/len(df_clean):>5.1%})")
    print(f"Val:   {len(df_val):>5} ({len(df_val)/len(df_clean):>5.1%})")
    print(f"Test:  {len(df_test):>5} ({len(df_test)/len(df_clean):>5.1%})")

    # Save splits
    print(f"\nSaving to {processed_dir}...")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    train_path = processed_dir / "train.csv"
    val_path = processed_dir / "val.csv"
    test_path = processed_dir / "test.csv"
    
    df_train[['text', 'label']].to_csv(train_path, index=False)
    df_val[['text', 'label']].to_csv(val_path, index=False)
    df_test[['text', 'label']].to_csv(test_path, index=False)
    
    print(f"Saved: {train_path.name}, {val_path.name}, {test_path.name}")
    print("\nDone!")
    print("=" * 70)

if __name__ == "__main__":
    main()

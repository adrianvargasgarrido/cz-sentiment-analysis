# src/data_utils.py
from pathlib import Path
from dataclasses import dataclass
from typing import Dict

import pandas as pd

# Adjust project root / paths if needed
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"

LABEL_MAP: Dict[str, int] = {"n": 0, "0": 1, "p": 2}
INV_LABEL_MAP: Dict[int, str] = {v: k for k, v in LABEL_MAP.items()}


@dataclass
class DatasetPaths:
    labeled: Path = DATA_RAW / "labeled_comments.txt"
    prediction: Path = DATA_RAW / "prediction_comments.txt"


def load_labeled_comments(file_path: Path = None) -> pd.DataFrame:
    """
    Returns a DataFrame with columns:
      - label_str: 'n' / '0' / 'p'
      - label:  0 / 1 / 2
      - text:      original Czech comment (stripped, not lowercased yet)
    
    Note: Text is NOT lowercased here to allow for flexible preprocessing.
          Apply lowercasing in your preprocessing pipeline as needed.
    """
    if file_path is None:
        file_path = DatasetPaths().labeled
        
    rows = []
    with file_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            label, text = line.split("\t", 1)
            rows.append(
                {
                    "label_str": label,
                    "label": LABEL_MAP[label],
                    "text": text.strip(),  # Keep original case
                }
            )

    df = pd.DataFrame(rows)
    return df


def load_prediction_comments(file_path: Path = None) -> pd.DataFrame:
    """
    Returns a DataFrame with columns:
      - text: comment text (stripped, not lowercased)
    
    Note: Text is NOT lowercased here to allow for flexible preprocessing.
          Apply lowercasing in your preprocessing pipeline as needed.
    """
    if file_path is None:
        file_path = DatasetPaths().prediction

    rows = []
    with file_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            # Some lines start with \t then text
            text = line.lstrip("\t").strip()  # Keep original case
            rows.append({"text": text})

    return pd.DataFrame(rows)
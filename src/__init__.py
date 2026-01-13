"""
Czech Sentiment Analysis Package

A sentiment classification system for Czech Facebook comments using ELECTRA.
"""

from .data_utils import load_labeled_comments, load_prediction_comments
from .model import FocalLoss, SentimentDataset
from .train import train_model
from .predict import predict_sentiment
from .utils import find_project_root

__all__ = [
    "load_labeled_comments",
    "load_prediction_comments",
    "FocalLoss",
    "SentimentDataset",
    "train_model",
    "predict_sentiment",
    "find_project_root",
]
__version__ = "0.1.0"
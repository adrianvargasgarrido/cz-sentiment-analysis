"""
Model definitions for Czech sentiment analysis.

Contains the custom loss function and dataset class used for training
the ELECTRA-based sentiment classifier.
"""

from typing import Optional
import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset


class FocalLoss(torch.nn.Module):
    """
    Implementation of Focal Loss for multi-class classification.
    
    Focal Loss helps with class imbalance by down-weighting easy examples
    and focusing on hard, misclassified examples.
    
    Args:
        alpha: Class weights (tensor of shape [num_classes])
        gamma: Focusing parameter (higher = more focus on hard examples)
        reduction: Reduction method ('mean', 'sum', or 'none')
    """

    def __init__(
        self, 
        alpha: Optional[torch.Tensor] = None, 
        gamma: float = 2.0, 
        reduction: str = "mean"
    ):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        """
        Compute focal loss.
        
        Args:
            inputs: Model logits [batch_size, num_classes]
            targets: Ground truth labels [batch_size]
            
        Returns:
            Computed focal loss
        """
        ce_loss = F.cross_entropy(inputs, targets, reduction="none")
        pt = torch.exp(-ce_loss)
        focal_loss = (1 - pt) ** self.gamma * ce_loss

        if self.alpha is not None:
            alpha_t = self.alpha[targets]
            focal_loss = alpha_t * focal_loss

        if self.reduction == "mean":
            return focal_loss.mean()
        if self.reduction == "sum":
            return focal_loss.sum()
        return focal_loss


class SentimentDataset(Dataset):
    """
    PyTorch dataset for Czech sentiment classification.
    
    Handles tokenization and encoding of text data for the ELECTRA model.
    
    Args:
        texts: Array of text strings
        labels: Array of integer labels (0=negative, 1=neutral, 2=positive)
        tokenizer: HuggingFace tokenizer instance
        max_length: Maximum sequence length for tokenization
    """
    
    def __init__(
        self, 
        texts: np.ndarray, 
        labels: np.ndarray, 
        tokenizer, 
        max_length: int = 128
    ):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        """
        Get a single tokenized example.
        
        Returns:
            Dictionary with 'input_ids', 'attention_mask', and 'labels'
        """
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        # Tokenize text
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

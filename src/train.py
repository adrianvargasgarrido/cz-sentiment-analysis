"""Training script for Czech sentiment analysis."""

import os
import time
import json
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, WeightedRandomSampler
from transformers import ElectraTokenizerFast, ElectraForSequenceClassification, get_linear_schedule_with_warmup
from torch.optim import AdamW
from tqdm.auto import tqdm
from sklearn.metrics import f1_score
from sklearn.utils.class_weight import compute_class_weight
from .model import FocalLoss, SentimentDataset

os.environ["TOKENIZERS_PARALLELISM"] = "false"

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def train_epoch(model, loader, optimizer, scheduler, device, criterion):
    """Train one epoch, return loss, accuracy, batch time, and F1."""
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    batch_times = []
    preds = []
    labels_list = []
    
    progress_bar = tqdm(loader, desc="Training")
    
    for batch in progress_bar:
        t0 = time.perf_counter()
        
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = criterion(outputs.logits, labels) if criterion else outputs.loss
        
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        
        total_loss += loss.item()
        batch_preds = torch.argmax(outputs.logits, dim=-1)
        correct += (batch_preds == labels).sum().item()
        total += labels.size(0)
        preds.extend(batch_preds.cpu().numpy())
        labels_list.extend(labels.cpu().numpy())
        
        batch_time = time.perf_counter() - t0
        batch_times.append(batch_time)
        
        progress_bar.set_postfix({
            'loss': f"{loss.item():.4f}",
            'acc': f"{100 * correct / total:.2f}%"
        })
    
    return (
        total_loss / len(loader),
        correct / total,
        sum(batch_times) / len(batch_times),
        f1_score(labels_list, preds, average='macro')
    )


def evaluate(model, loader, device, criterion=None):
    """Evaluate model, return loss, accuracy, F1 scores, predictions, and labels."""
    model.eval()
    total_loss = 0
    preds = []
    labels_list = []
    
    with torch.no_grad():
        for batch in tqdm(loader, desc="Evaluating"):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = criterion(outputs.logits, labels) if criterion else outputs.loss
            total_loss += loss.item()
            
            batch_preds = torch.argmax(outputs.logits, dim=-1)
            preds.extend(batch_preds.cpu().numpy())
            labels_list.extend(labels.cpu().numpy())
    
    preds = np.array(preds)
    labels_list = np.array(labels_list)
    
    return (
        total_loss / len(loader),
        np.mean(preds == labels_list),
        f1_score(labels_list, preds, average='macro'),
        f1_score(labels_list, preds, average='weighted'),
        preds.tolist(),
        labels_list.tolist()
    )


def train_model(
    train_df,
    val_df,
    model_dir,
    output_dir,
    epochs=3,
    batch_size=16,
    learning_rate=2e-5,
    warmup_ratio=0.1,
    max_length=128,
    num_workers=2,
    seed=42,
    class_weighting="none",
    custom_class_weights=None,
    extreme_weight=1.5,
    monitor_metric="accuracy",
    loss_function="cross_entropy",
    focal_loss_gamma=2.0,
    use_weighted_sampler=False
):
    """Train sentiment model with given configuration."""
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    
    if monitor_metric not in {"accuracy", "macro_f1", "weighted_f1"}:
        raise ValueError(f"Invalid monitor_metric: {monitor_metric}")
    if loss_function not in {"cross_entropy", "focal"}:
        raise ValueError(f"Invalid loss_function: {loss_function}")
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
    
    print(f"\nTraining Configuration")
    print(f"Device: {device_name}")
    print(f"Epochs: {epochs} | Batch size: {batch_size} | LR: {learning_rate}")
    print(f"Warmup: {warmup_ratio} | Max length: {max_length}")
    print(f"Loss: {loss_function}" + (f" (gamma={focal_loss_gamma})" if loss_function == "focal" else ""))
    print(f"Train: {len(train_df):,} | Val: {len(val_df):,}")
    print(f"Monitor: {monitor_metric}")
    print(f"Weighted sampler: {'on' if use_weighted_sampler else 'off'}")

    class_weights = None
    classes = np.array([0, 1, 2])
    if class_weighting != "none":
        labels = train_df['label'].values
        
        if class_weighting == "balanced":
            class_weights = compute_class_weight('balanced', classes=classes, y=labels)
        elif class_weighting == "extreme":
            class_weights = compute_class_weight('balanced', classes=classes, y=labels)
            class_weights[0] *= extreme_weight
            class_weights[2] *= extreme_weight
        elif class_weighting == "custom":
            if not custom_class_weights or len(custom_class_weights) != 3:
                raise ValueError("custom_class_weights must have 3 values")
            class_weights = np.array(custom_class_weights, dtype=np.float32)
        else:
            raise ValueError(f"Unknown class_weighting: {class_weighting}")
        
        print(f"\nClass weights: {np.round(class_weights, 3).tolist()}")
        counts = train_df['label'].value_counts().reindex(classes, fill_value=0)
        for i, cnt in counts.items():
            name = ['negative', 'neutral', 'positive'][i]
            print(f"  {name}: {cnt} ({cnt/len(train_df)*100:.1f}%)")
    
    print(f"\nLoading model from {model_dir}...")
    tokenizer = ElectraTokenizerFast.from_pretrained(model_dir)
    model = ElectraForSequenceClassification.from_pretrained(
        model_dir,
        num_labels=3,
        id2label={0: "negative", 1: "neutral", 2: "positive"},
        label2id={"negative": 0, "neutral": 1, "positive": 2}
    )
    model.to(device)
    
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Parameters: {total:,} (trainable: {trainable:,})")
    
    train_dataset = SentimentDataset(train_df['text'].values, train_df['label'].values, tokenizer, max_length)
    val_dataset = SentimentDataset(val_df['text'].values, val_df['label'].values, tokenizer, max_length)

    sampler = None
    if use_weighted_sampler:
        label_counts = train_df['label'].value_counts().reindex(classes, fill_value=0).astype(float)
        safe_counts = label_counts.replace(0.0, 1.0)
        class_sampling_weights = (1.0 / safe_counts).to_numpy()
        class_weight_lookup = dict(zip(classes, class_sampling_weights))
        per_example_weights = train_df['label'].map(class_weight_lookup).astype(float).values
        weights_tensor = torch.as_tensor(per_example_weights, dtype=torch.double)
        sampler = WeightedRandomSampler(weights=weights_tensor, num_samples=len(weights_tensor), replacement=True)
        print("\nWeightedRandomSampler enabled:")
        for cls, weight in zip(classes, class_sampling_weights):
            name = ['negative', 'neutral', 'positive'][cls]
            print(f"  {name}: sampling weight {weight:.3f}")

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=not use_weighted_sampler,
        sampler=sampler,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=torch.cuda.is_available()
    )

    weight_tensor = torch.tensor(class_weights, dtype=torch.float32, device=device) if class_weights is not None else None
    
    if loss_function == "focal":
        train_criterion = FocalLoss(alpha=weight_tensor, gamma=focal_loss_gamma, reduction="mean")
    else:
        train_criterion = torch.nn.CrossEntropyLoss(weight=weight_tensor)
    
    eval_criterion = torch.nn.CrossEntropyLoss(weight=weight_tensor)
    
    optimizer = AdamW(model.parameters(), lr=learning_rate)
    total_steps = len(train_loader) * epochs
    warmup_steps = int(total_steps * warmup_ratio)
    scheduler = get_linear_schedule_with_warmup(optimizer, warmup_steps, total_steps)
    
    print(f"Steps: {total_steps:,} (warmup: {warmup_steps:,})")
    print(f"Batches/epoch: {len(train_loader):,}")
    
    history = {
        'train_loss': [], 'train_acc': [], 'train_macro_f1': [],
        'val_loss': [], 'val_acc': [], 'val_macro_f1': [], 'val_weighted_f1': [],
        'epoch_times': [], 'avg_batch_times': [],
        'monitor_metric': monitor_metric,
        'loss_function': loss_function,
        'focal_loss_gamma': focal_loss_gamma if loss_function == "focal" else None,
        'class_weights': class_weights.tolist() if class_weights is not None else None,
        'run_output_dir': str(output_dir),
        'use_weighted_sampler': use_weighted_sampler
    }
    
    best_metric = -float("inf")
    best_epoch = 0
    best_model_path = output_dir / "best_sentiment_model.pt"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nStarting training...\n")
    t_start = time.perf_counter()
    
    for epoch in range(epochs):
        t_epoch = time.perf_counter()
        
        print(f"\nEpoch {epoch + 1}/{epochs}")
        
        train_loss, train_acc, batch_time, train_f1 = train_epoch(
            model, train_loader, optimizer, scheduler, device, train_criterion
        )
        
        val_loss, val_acc, val_f1, val_wf1, _, _ = evaluate(model, val_loader, device, eval_criterion)
        
        epoch_time = time.perf_counter() - t_epoch
        elapsed = time.perf_counter() - t_start
        
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['train_macro_f1'].append(train_f1)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        history['val_macro_f1'].append(val_f1)
        history['val_weighted_f1'].append(val_wf1)
        history['epoch_times'].append(epoch_time)
        history['avg_batch_times'].append(batch_time)
        
        print(f"Train - Loss: {train_loss:.4f} | Acc: {train_acc:.4f} | F1: {train_f1:.4f}")
        print(f"Val   - Loss: {val_loss:.4f} | Acc: {val_acc:.4f} | F1: {val_f1:.4f} | WF1: {val_wf1:.4f}")
        print(f"Time: {epoch_time/60:.2f}min | Total: {elapsed/60:.2f}min")
        
        current_metric = {"accuracy": val_acc, "macro_f1": val_f1, "weighted_f1": val_wf1}[monitor_metric]
        if current_metric > best_metric:
            best_metric = current_metric
            best_epoch = epoch + 1
            torch.save(model.state_dict(), best_model_path)
            print(f"New best {monitor_metric}: {current_metric:.4f}")
    
    total_time = time.perf_counter() - t_start
    best_acc = max(history['val_acc'])
    best_f1 = max(history['val_macro_f1'])
    best_wf1 = max(history['val_weighted_f1'])
    
    print(f"\nTraining complete!")
    print(f"Total time: {total_time/60:.2f}min ({total_time/epochs/60:.2f}min/epoch)")
    print(f"Best {monitor_metric}: {best_metric:.4f} (epoch {best_epoch})")
    print(f"Peak acc: {best_acc:.4f} | Peak F1: {best_f1:.4f} | Peak WF1: {best_wf1:.4f}")
    
    final_dir = output_dir / "trained_sentiment_electra"
    final_dir.mkdir(exist_ok=True)
    model.load_state_dict(torch.load(best_model_path))
    model.save_pretrained(final_dir)
    tokenizer.save_pretrained(final_dir)
    print(f"Model saved to: {final_dir}")
    
    history['best_metric_epoch'] = best_epoch
    history['best_metric_value'] = best_metric
    with open(output_dir / "training_history.json", 'w') as f:
        json.dump(history, f, indent=2)
    
    return history


def main():
    parser = argparse.ArgumentParser(description="Train sentiment model")
    parser.add_argument("--train-data", required=True)
    parser.add_argument("--val-data", required=True)
    parser.add_argument("--model-dir", required=True)
    parser.add_argument("--output-dir", default="models")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--lr", type=float, default=2e-5)
    parser.add_argument("--warmup-ratio", type=float, default=0.1)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--monitor-metric", choices=["accuracy", "macro_f1", "weighted_f1"], default="accuracy")
    parser.add_argument("--class-weighting", choices=["none", "balanced", "extreme", "custom"], default="none")
    parser.add_argument("--class-weights", type=float, nargs=3)
    parser.add_argument("--extreme-weight", type=float, default=1.5)
    parser.add_argument("--loss-function", choices=["cross_entropy", "focal"], default="cross_entropy")
    parser.add_argument("--focal-loss-gamma", type=float, default=2.0)
    parser.add_argument("--use-weighted-sampler", action=argparse.BooleanOptionalAction, default=False)
    
    args = parser.parse_args()
    
    if args.class_weights and args.class_weighting != "custom":
        parser.error("--class-weights requires --class-weighting custom")
    
    train_df = pd.read_csv(args.train_data)
    val_df = pd.read_csv(args.val_data)
    
    train_model(
        train_df=train_df,
        val_df=val_df,
        model_dir=Path(args.model_dir),
        output_dir=Path(args.output_dir),
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        warmup_ratio=args.warmup_ratio,
        max_length=args.max_length,
        num_workers=args.num_workers,
        seed=args.seed,
        class_weighting=args.class_weighting,
        custom_class_weights=args.class_weights,
        extreme_weight=args.extreme_weight,
        monitor_metric=args.monitor_metric,
        loss_function=args.loss_function,
        focal_loss_gamma=args.focal_loss_gamma,
        use_weighted_sampler=args.use_weighted_sampler
    )


if __name__ == "__main__":
    main()

"""Metrics used in strict temporal fraud-detection evaluation."""

from __future__ import annotations

import math

import numpy as np
from sklearn.metrics import average_precision_score, log_loss, roc_auc_score


def recall_at_fraction(labels: np.ndarray, scores: np.ndarray, fraction: float) -> float:
    """Recall among the highest-scoring fraction of observations."""
    labels = np.asarray(labels, dtype=np.int64)
    scores = np.asarray(scores, dtype=np.float64)
    if labels.shape != scores.shape or labels.ndim != 1:
        raise ValueError("labels and scores must be aligned one-dimensional arrays")
    if not 0.0 < fraction <= 1.0:
        raise ValueError("fraction must be in (0, 1]")
    positives = int(labels.sum())
    if positives == 0:
        return float("nan")
    count = max(1, math.ceil(len(labels) * fraction))
    selected = np.argsort(-scores, kind="stable")[:count]
    return float(labels[selected].sum() / positives)


def binary_classification_metrics(labels: np.ndarray, probabilities: np.ndarray) -> dict[str, float]:
    """Compute primary and operational metrics for a single temporal fold."""
    labels = np.asarray(labels, dtype=np.int64)
    probabilities = np.asarray(probabilities, dtype=np.float64)
    if labels.shape != probabilities.shape or labels.ndim != 1:
        raise ValueError("labels and probabilities must be aligned one-dimensional arrays")
    clipped = np.clip(probabilities, 1e-7, 1 - 1e-7)
    return {
        "auc_pr": float(average_precision_score(labels, probabilities)),
        "auc_roc": float(roc_auc_score(labels, probabilities)),
        "log_loss": float(log_loss(labels, clipped, labels=[0, 1])),
        "recall_at_5pct": recall_at_fraction(labels, probabilities, 0.05),
        "recall_at_10pct": recall_at_fraction(labels, probabilities, 0.10),
    }

import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score

def tune_threshold(y_true, y_proba):
    thresholds = np.arange(0.1, 0.9, 0.01)

    best_threshold = 0.5
    best_f1 = 0

    results = []

    for t in thresholds:
        y_pred = (y_proba >= t).astype(int) #It will be compare with threshold to determine the predicted class (0 or 1)

        f1 = f1_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)

        results.append((t, f1, precision, recall))

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = t

    print("\n=== Threshold Tuning Results ===")
    print(f"Best Threshold: {best_threshold:.2f}")
    print(f"Best F1 Score: {best_f1:.4f}")

    return best_threshold, results
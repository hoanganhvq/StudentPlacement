from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
import pandas as pd


def evaluate_classification_model(model, X_test, y_test, best_threshold):
    y_prob = model.predict_proba(X_test)[:, 1]

    # 👉 DÙNG threshold tuning
    y_pred = (y_prob >= best_threshold).astype(int)

    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("F1 Score:", f1_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred))
    print("Recall:", recall_score(y_test, y_pred))
    print("ROC AUC Score:", roc_auc_score(y_test, y_prob))

    return {
        "f1_score": f1_score(y_test, y_pred),
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "roc_auc_score": roc_auc_score(y_test, y_prob),
        "threshold": best_threshold
    }


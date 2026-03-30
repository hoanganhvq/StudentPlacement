import joblib
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, f1_score, precision_score, recall_score
from sklearn.model_selection import RandomizedSearchCV
from src.evaluation.evaluation_classtification import evaluate_classification_model
from src.models.optuna_tuning import ModelOptimizer, run_optuna_for_model
def train_knn(X_train, y_train):

    # Su dung Optuna để tìm hyperparameters tốt nhất cho KNN
    params_knn, best_f1 = run_optuna_for_model("KNN", X_train, y_train)
    
    model = KNeighborsClassifier(**params_knn)
    model.fit(X_train, y_train)

    print("Best Hyperparameters for KNN:", params_knn)
    print("Best F1 Score for KNN:", best_f1)

    joblib.dump(model, "models/classtification/knn_model.joblib")

    return model


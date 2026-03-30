import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import RandomizedSearchCV

from src.models.optuna_tuning import ModelOptimizer, run_optuna_for_model
def train_logistic_regression(X_train, y_train):
    
    param_lr, best_f1 = run_optuna_for_model("Logistic Regression", X_train, y_train)

    model = LogisticRegression(**param_lr)

    model.fit(X_train, y_train)


    print("Best Hyperparameters:", param_lr)
    print("Best F1 Score:", best_f1)

    joblib.dump(model, "models/classtification/logistic_regression_model.joblib")
    #Danh gia model tren test set

    return model


import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.models.optuna_tuning import ModelOptimizer, run_optuna_for_model

def train_random_forest(X_train, y_train):
    # Define the hyperparameters to search
    param_rf, best_f1 = run_optuna_for_model("Random Forest", X_train, y_train)

    model = RandomForestClassifier(**param_rf)

    model.fit(X_train, y_train)

    print("Best Hyperparameters:", param_rf)
    print("Best F1 Score:", best_f1)

    joblib.dump(model, "models/classtification/random_forest_model.joblib")

    return model


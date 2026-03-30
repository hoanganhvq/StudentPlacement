import joblib
import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import RandomizedSearchCV

from src.models.optuna_tuning import ModelOptimizer, run_optuna_for_model

def train_xgboost(X_train, y_train,):

    param_xgb, best_f1 = run_optuna_for_model("XGBoost", X_train, y_train)

    model = XGBClassifier(**param_xgb)

    model.fit(X_train, y_train)



    print("Best Hyperparameters:", param_xgb)
    print("Best F1 Score:", best_f1)

    joblib.dump(model, "models/classtification/xgboost_model.joblib")


    return model

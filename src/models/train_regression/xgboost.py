import joblib

from xgboost import XGBRegressor
from src.models.optuna_tuning import run_optuna_for_model

def train_xg_boost_reg(X_train, y_train):
    param, best_r2 = run_optuna_for_model("XGBoost Regression", X_train, y_train)

    model = XGBRegressor(**param)

    model.fit(X_train, y_train)

    print("Best Hyperparameters:", param)
    print("Best r2 Score:", best_r2)

    joblib.dump(model, "models/regression/xgboost_reg_model.joblib")

    return model
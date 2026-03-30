import joblib
from sklearn.ensemble import RandomForestRegressor
from src.models.optuna_tuning import run_optuna_for_model

def train_random_forest_reg(X_train, y_train):
    param, best_r2 = run_optuna_for_model("Random Forest Regression", X_train, y_train)

    model = RandomForestRegressor(**param)
    model.fit(X_train, y_train)

    print("Best Hyperparameter: ", param)
    print("Best r2 score: ", best_r2)

    joblib.dump(model, "models/regression/random_forest_reg_model.joblib")

    return model
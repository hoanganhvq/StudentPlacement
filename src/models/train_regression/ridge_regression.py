from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from src.models.optuna_tuning import run_optuna_for_model
import joblib
def train_ridge_regression(X_train, y_train):
    params, best_r2 = run_optuna_for_model("Ridge Regression", X_train, y_train)

    model = Ridge(**params)

    model.fit(X_train, y_train)

    print("Best hyperparameter: ", params)
    print("Best r2 ", best_r2)

    joblib.dump(model, "models/regression/ridge_regression.joblib")

    return model

import joblib
from xgboost import XGBRegressor
from sklearn.linear_model import Ridge, LinearRegression # Thêm LinearRegression
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from src.util.handle_params import load_best_params

def train_stacking_reg(X_train, y_train):
    # Load params từ JSON
    params_xgb_reg = load_best_params("XGBoost Regression")
    params_ridge_reg = load_best_params("Ridge Regression")
    params_rf_reg = load_best_params("Random Forest Regression")

    base_models = [
        ("xgb_reg", XGBRegressor(**params_xgb_reg)),
        ("ridge_reg", Ridge(**params_ridge_reg)),
        ("rf_reg", RandomForestRegressor(**params_rf_reg))
    ]

    meta_model = Ridge() 

    stack_model = StackingRegressor(
        estimators=base_models,
        final_estimator=meta_model,
        cv=5,
        n_jobs=-1,
        passthrough=False
    )

    print(" Training Stacking Regression...")
    stack_model.fit(X_train, y_train)
    
    joblib.dump(stack_model, "models/regression/stacking_reg_model.joblib")
    return stack_model
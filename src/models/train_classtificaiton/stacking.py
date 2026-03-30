import joblib
from src.models.optuna_tuning import run_optuna_for_model

from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from src.util.handle_params import load_best_params
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score

def train_stacking(X_train, y_train):
    # params_rf, _ = run_optuna_for_model("Random Forest", X_train, y_train)
    # params_xgb, _ = run_optuna_for_model("XGBoost", X_train, y_train)
    # params_knn, _ = run_optuna_for_model("KNN", X_train, y_train)
    # params_lr, _ = run_optuna_for_model("Logistic Regression", X_train, y_train)

    params_rf = load_best_params("Random Forest")
    params_xgb = load_best_params("XGBoost")
    params_knn = load_best_params("KNN")
    params_lr = load_best_params("Logistic Regression")

    #Model tang 1 (base models)
    base_models = [
        ("rf", RandomForestClassifier(**params_rf)),
        ("xgb", XGBClassifier(**params_xgb)),
        ("knn", KNeighborsClassifier(**params_knn)),
        ("lr", LogisticRegression(**params_lr))
    
    ]
    #Model tang 2 (meta model)
    meta_model = LogisticRegression()

    stack_model = StackingClassifier (
        estimators=base_models,
        final_estimator=meta_model,
        cv=5,
        n_jobs=-1,
        passthrough=False
    )
    print("Training Stacking Classifier...")
    stack_model.fit(X_train, y_train)
    joblib.dump(stack_model, "models/classtification/stacking_model.joblib")
    return stack_model
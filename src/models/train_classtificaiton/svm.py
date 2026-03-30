import joblib
import pandas as pd
from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import RandomizedSearchCV
from src.evaluation.evaluation_classtification import evaluate_classification_model

def train_svm(X_train, y_train, X_test, y_test):


    model = svm.SVC(random_state=42)
    params = {
        "C": [0.1, 1, 10, 100],
        "kernel": ["linear", "rbf"],
        "gamma": ["scale"]
    }

    random_search = RandomizedSearchCV(
        model,
        param_distributions=params,
        n_iter=10, #Test 10 different combinations of hyperparameters
        cv=5, #5-fold cross-validation
        random_state=42,
        n_jobs=-1,
        scoring="f1"
    )

    random_search.fit(X_train, y_train)
    print("Best Hyperparameters:", random_search.best_params_)
    print("Best F1 Score:", random_search.best_score_)
    best_model = random_search.best_estimator_
    
    joblib.dump(best_model, "src/models/svm_model.joblib")


    return best_model


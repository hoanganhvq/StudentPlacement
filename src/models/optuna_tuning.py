import optuna
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier, XGBRegressor
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
from src.util.handle_params import save_best_params
import numpy as np

class ModelOptimizer:
    def __init__(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train
    
    def objective_xgb(self, trial):
    #Search space cho XGBoost
        param = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.001, 0.1, log=True),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
            'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
            'gamma': trial.suggest_float('gamma', 0, 5),
            'random_state': 42,
            'use_label_encoder': False,
            'eval_metric': 'logloss'
        }

        model = XGBClassifier(**param)
        
        score = cross_val_score(model, self.X_train, self.y_train, cv=5, scoring='f1', n_jobs=-1)
        f1 = score.mean()

        return f1

    def objective_rf(self, trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 500),
            'max_depth': trial.suggest_int('max_depth', 5, 30),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
            'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2']),
            'random_state': 42
        }
        model = RandomForestClassifier(**params)
        
        score = cross_val_score(model, self.X_train, self.y_train, cv=5, scoring='f1', n_jobs=-1)
        f1 = score.mean()

        return f1
    
    def objective_lr(self, trial):
        params = {
            'C': trial.suggest_float('C', 0.001, 100, log=True),
            'solver': trial.suggest_categorical('solver', ['saga']),
            'l1_ratio': trial.suggest_float('l1_ratio', 0, 1) if trial.suggest_categorical('solver', ['saga']) == 'saga' else None,
            'max_iter': 1000,
            'random_state': 42
        }
        model = LogisticRegression(**params)
        
        score = cross_val_score(model, self.X_train, self.y_train, cv=5, scoring='f1', n_jobs=-1)
        f1 = score.mean()

        return f1

    def objective_knn(self, trial):
        params = {
            'n_neighbors': trial.suggest_int('n_neighbors', 3, 15),
            'weights': trial.suggest_categorical('weights', ['uniform', 'distance']),
            'metric': trial.suggest_categorical('metric', ['euclidean', 'manhattan']),
        }
        
        model = KNeighborsClassifier(**params)
        score = cross_val_score(model, self.X_train, self.y_train, cv=5, scoring='f1', n_jobs=-1)

        f1 = score.mean()
        return f1

    def objective_ridge(self, trial):
        params = {
            'alpha': trial.suggest_float('alpha', 1e-3, 1e3, log=True),
            'solver': trial.suggest_categorical('solver', ['auto', 'svd', 'cholesky', 'lsqr']),
            'max_iter': 1000,
            'random_state': 42
        }

        model = Ridge(**params)
        score = cross_val_score(model, self.X_train, self.y_train, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
        rmse = np.sqrt(-score.mean())

        r2_score_val = cross_val_score(model, self.X_train, self.y_train, cv=5, scoring='r2', n_jobs=-1)

        return r2_score_val.mean()
    
    def objective_xgb_reg(self, trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.001, 0.1, log=True),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
            'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
            'gamma': trial.suggest_float('gamma', 0, 5),
            'random_state': 42,
            'use_label_encoder': False,
        }

        model =XGBRegressor(**params)

        r2_score_val = cross_val_score(model, self.X_train, self.y_train, cv=5, scoring='r2', n_jobs=-1)
        return r2_score_val.mean()
    
    def objective_rf_reg(self, trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 500),
            'max_depth': trial.suggest_int('max_depth', 5, 30),
            'min_samples_split': trial.suggest_int('min_samples_split', 2, 10),
            'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
            'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2']),
            'random_state': 42
        }

        model = RandomForestRegressor(**params)
        r2_score_val = cross_val_score(model, self.X_train, self.y_train, cv=5, scoring='r2', n_jobs=-1)
        return r2_score_val.mean()
    


def run_optuna_for_model(model_name, X_train, y_train):
    optimizer = ModelOptimizer(X_train, y_train)
    
    # Map tên model với hàm objective tương ứng
    mapping = {
        'XGBoost': optimizer.objective_xgb,
        'Random Forest': optimizer.objective_rf,
        'Logistic Regression': optimizer.objective_lr,
        'KNN': optimizer.objective_knn,

        'Ridge Regression': optimizer.objective_ridge,
        'XGBoost Regression': optimizer.objective_xgb_reg,
        'Random Forest Regression': optimizer.objective_rf_reg
    }



    if model_name not in mapping:
        print(f"Model {model_name} không có trong danh sách hỗ trợ!")
        return None

    print(f"--- Đang tối ưu hóa {model_name} ---")
    study = optuna.create_study(direction='maximize')
    study.optimize(mapping[model_name], n_trials=50) # Chạy 50 lần dò

    print(f"\n✅ Kết quả tốt nhất cho {model_name}:")
    print(f"F1 Score: {study.best_value:.4f}")
    print(f"Best Params: {study.best_params}")
    save_best_params(model_name, study.best_params)

    return study.best_params, study.best_value
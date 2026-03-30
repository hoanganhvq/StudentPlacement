import joblib
import pandas as pd

from src.models.train_regression.xgboost import train_xg_boost_reg
from src.models.train_regression.ridge_regression import train_ridge_regression
from src.models.train_regression.random_forest import train_random_forest_reg
from src.models.train_regression.stacking_reg import train_stacking_reg
from src.evaluation.evaluation_regression import evaluate_regression
from src.data.preprocess_regression import preprocess_data_reg
from src.explainability.shap_analysis_reg import SalaryShapeExplainer
(X_train, X_val, X_test, y_train, y_val, y_test) = preprocess_data_reg("data/raw/global_placement.csv")

models = {
    "Ridge Regression": train_ridge_regression,
    "XGBoost Regression": train_xg_boost_reg,
    "Random Forest Regression": train_random_forest_reg,
    "Stacking": train_stacking_reg
}

results = []

for model_name, model_func in models.items():
    print(f"Evaluating  {model_name}....")

    model = model_func(X_train, y_train)

    metrics = evaluate_regression(model, X_test, y_test)
    results.append({
        "Model":model_name,
        **metrics,
        "model_obj": model
    })

# 3. Tổng hợp kết quả
df_results = pd.DataFrame(results)
df_results = df_results.sort_values(by="r2_score", ascending=False)

print("\n" + "="*50)
print("📊 BẢNG SO SÁNH KẾT QUẢ REGRESSION")
print(df_results[["Model", "r2_score", "mean_absolute_error"]].to_string(index=False))
print("="*50)

# 4. Lấy model tốt nhất và lưu
best_row = df_results.iloc[0]
best_model_name = best_row["Model"].replace(" ", "_").lower()
best_model = best_row["model_obj"]

save_path = f"models/regression/best_model_{best_model_name}.joblib"
joblib.dump(best_model, save_path)

print(f"Đã lưu model tốt nhất tại: {save_path}")


#SHAP analysis
print("\n" + "="*50)
print(f"🧠 ĐANG CHẠY SHAP ANALYSIS CHO {best_row['Model'].upper()}...")
print("="*50)

shap_explainer = SalaryShapeExplainer(best_model, X_train)

summary_path = f"src/evaluation/shap_summary_{best_model_name}.png"
shap_explainer.save_global_explanation(X_test)

sample_student = X_test.iloc[[0]] 
waterfall_path = f"src/evaluation/shap_waterfall_{best_model_name}_sample.png"
shap_explainer.save_student_waterfall(sample_student)


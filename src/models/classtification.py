import pandas as pd

import joblib
from src.models.train_classtificaiton.knn import train_knn
from src.models.train_classtificaiton.logistic_regression import train_logistic_regression
from src.models.train_classtificaiton.random_forest import train_random_forest
from src.models.train_classtificaiton.svm import train_svm
from src.models.train_classtificaiton.xg_boost import train_xgboost
from src.models.train_classtificaiton.stacking import train_stacking
from src.evaluation.evaluation_classtification import evaluate_classification_model
from src.data.preprocess_classtification import preprocess_data_cls
from src.models.threshold_tuning import tune_threshold

from src.evaluation.fairness import CareerFairnessAnalyzer
from src.explainability.shap_analysis_cls import CareerShapeExplainer



# 1. Load data
(X_train, X_val, X_test, y_train, y_val, y_test)= preprocess_data_cls("data/raw/global_placement.csv")
# 2. Load models đã train

models = {
    "KNN": train_knn,
    "Logistic Regression": train_logistic_regression,
    "Random Forest": train_random_forest,
    # "SVM": train_svm,
    "XGBoost": train_xgboost,
    "Stacking": train_stacking
}

# 3. Train and evaluate models, tune threshold trên validation, rồi đánh giá lại trên test với threshold mới
results = []

for model_name, model_func in models.items():
    print(f"\nEvaluating {model_name}...")

    # Train
    model = model_func(X_train, y_train)

    #   Tune threshold (VALIDATION)
    y_proba_val = model.predict_proba(X_val)[:, 1]
    best_threshold, _ = tune_threshold(y_val, y_proba_val)

    # Evaluate TEST với threshold mới
    metrics = evaluate_classification_model(model, X_test, y_test, best_threshold)

    results.append({
        "Model": model_name,
        **metrics,
        "threshold": best_threshold,
        "model_obj": model  
    })

#5. Hien thi ket qua
df_results = pd.DataFrame(results)
    
# Sắp xếp theo F1-Score giảm dần
df_results = df_results.sort_values(by="f1_score", ascending=False)

    # Lấy model tốt nhất
best_row = df_results.iloc[0]

best_model_name = best_row["Model"]
best_model = best_row["model_obj"]
best_threshold = best_row["threshold"]

joblib.dump(best_model, f"models/classtification/best_model_{best_model_name}.joblib")

with open(f"models/classtification/best_threshold_{best_model_name}.txt", "w") as f:
    f.write(str(best_threshold))

    # Chỉ lấy các cột cần thiết (bỏ model_obj cho đỡ rối)
df_display = df_results[[
    "Model", "f1_score", "accuracy", "precision", "recall", "roc_auc_score", "threshold"
]].copy()

df_display = df_display.round(3)
df_display = df_display.reset_index(drop=True)

print("\n" + "="*60)
print("📊 BẢNG SO SÁNH MODEL CLASSTIFITION")
print("="*60)
print(df_display.to_string(index=False))

#SHAP analysis
print("\n" + "="*50)
print(f"🧠 ĐANG CHẠY SHAP ANALYSIS ")
print("="*50)

shap_explainer = CareerShapeExplainer(best_model, X_train)

summary_path = f"src/evaluation/shap_summary_{best_model_name}.png"
shap_explainer.save_global_explanation(X_test)

sample_student = X_test.iloc[[0]] 
waterfall_path = f"src/evaluation/shap_waterfall_{best_model_name}_sample.png"
shap_explainer.save_student_waterfall(sample_student)

# 6. Fairness Analysis with best model
# print("\n" + "="*60)
# print(f"⚖️ ĐÁNH GIÁ ĐẠO ĐỨC & CÔNG BẰNG CHO MODEL: {best_model_name}")
# print("="*60)

# # Khởi tạo công cụ đo lường với model tốt nhất vừa tìm được
# fairness_tool = CareerFairnessAnalyzer(best_model)

# try:
#     # SỬ DỤNG 'college_tier' LÀM ĐẶC TRƯNG ĐỂ KIỂM TRA SỰ THIÊN VỊ
#     df_raw = pd.read_csv("data/raw/global_placement.csv")
#     sensitive_col_raw = df_raw.loc[y_test.index, 'college_tier']    
#     # Chạy phân tích và xuất ảnh
#     fairness_tool.evaluate_and_plot_fairness(
#         X_test=X_test, 
#         y_true=y_test, 
#         sensitive_feature=sensitive_col_raw, 
#         feature_name="Hạng Trường (College Tier)",
#         output_image=f"src/evaluatiton/Fairness_Report_{best_model_name}_cls.png"
#     )
#     print("Thanh cong fairness !")
# except KeyError:
#     print("LỖI: Không tìm thấy cột 'college_tier' trong X_test.")

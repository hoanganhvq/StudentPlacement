import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shap
class SalaryShapeExplainer:
    def __init__(self, model, X_train):
        self.model = model
        self.X_train = X_train

        self.explainer = shap.TreeExplainer(self.model)

    def save_global_explanation(self, X_test, output_path="models/regression/shap_salary_summary.png"):
        shap_values = self.explainer(X_test)
        plt.figure(figsize=(10, 6))
        # Dùng beeswarm hoặc summary_plot đều đẹp
        shap.plots.beeswarm(shap_values, show=False)
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Đã lưu biểu đồ tổng quan Tác động Lương tại: {output_path}")

    def save_student_waterfall(self, student_features, output_path="models/regression/student_salary_waterfall.png"):
        shap_values = self.explainer(student_features)
        
        plt.figure(figsize=(8, 6))
        shap.plots.waterfall(shap_values[0], show=False)
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Đã lưu biểu đồ giải thích Lương cho sinh viên tại: {output_path}")

    def get_chatbot_advice_data(self, student_features):
        shap_values = self.explainer(student_features)

        # Regression chỉ trả về 1 mảng giá trị (Không bị 3 chiều như Classification)
        values = shap_values.values[0]
        feature_names = student_features.columns.tolist()

        impact_dict = dict(zip(feature_names, values))
        
        # Điểm mạnh (Yếu tố kéo mức lương LÊN)
        strengths = {k: v for k, v in impact_dict.items() if v > 0}
        # Điểm yếu (Yếu tố kéo mức lương XUỐNG)
        weaknesses = {k: v for k, v in impact_dict.items() if v < 0}
        
        top_strength = sorted(strengths.items(), key=lambda x: x[1], reverse=True)
        top_weakness = sorted(weaknesses.items(), key=lambda x: x[1]) 

        return {
            "base_value_log": shap_values.base_values[0], # Lương nền tảng (hệ log)
            "top_positive": top_strength[0] if top_strength else None,
            "top_negative": top_weakness[0] if top_weakness else None,
            "all_impacts": impact_dict
        }
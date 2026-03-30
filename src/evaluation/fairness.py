import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import matplotlib.pyplot as plt

from fairlearn.metrics import (
    MetricFrame, 
    demographic_parity_difference, 
    equal_opportunity_difference,
    equalized_odds_difference,
    selection_rate,
    true_positive_rate
)

class CareerFairnessAnalyzer:
    def __init__(self, model):
        self.model = model

    def evaluate_and_plot_fairness(self, X_test, y_true, sensitive_feature, feature_name, output_image="models/fairness_report.png"):
        y_pred = self.model.predict(X_test)

        dp_diff = demographic_parity_difference(y_true, y_pred, sensitive_features=sensitive_feature)
        eo_diff = equal_opportunity_difference(y_true, y_pred, sensitive_features=sensitive_feature)

        metric_frame = {
            "Demographic Parity": selection_rate,
            "Equal Opportunity": true_positive_rate,
            "Accuracy": accuracy_score
        }

        metric_frame = MetricFrame(
            metrics = metric_frame,
            y_true = y_true,
            y_pred = y_pred,
            sensitive_features = sensitive_feature
        )

        # === IN BÁO CÁO RA CONSOLE ===
        print(f"\n{'='*60}")
        print(f"BÁO CÁO CÔNG BẰNG AI THEO: {feature_name.upper()}")
        print(f"{'='*60}")
        
        print("\n[1] CHỈ SỐ CHÊNH LỆCH (Difference):")
        print(f"  - Lệch Demographic Parity : {dp_diff:.4f} (Phản ánh định kiến tổng thể của dữ liệu)")
        print(f"  - Lệch Equal Opportunity  : {eo_diff:.4f} (Chỉ số quyết định mô hình có đạo đức không)")
        
        print("\n[2] PHÂN TÍCH CHI TIẾT TỪNG NHÓM:")
        print(metric_frame.by_group.to_string())

        print("\n[3] KẾT LUẬN HỆ THỐNG:")
        if eo_diff > 0.1:
            print("  ⚠️ CẢNH BÁO: Vi phạm Equal Opportunity (Lệch > 10%). Cần áp dụng Bias Mitigation.")
        else:
            print("  ✅ ĐẠT: Mô hình đảm bảo công bằng về cơ hội cho các nhóm.")

        self._plot_fairness_chart(metric_frame, feature_name, output_image)
        
        return metric_frame, dp_diff, eo_diff
    
    def _plot_fairness_chart(self, metric_frame, feature_name, output_image):
        df_plot = metric_frame.by_group[['Demographic Parity', 'Equal Opportunity']]
        
        df_plot = df_plot.fillna(0)
        
        ax = df_plot.plot(kind='bar', figsize=(10, 6), color=['#1f77b4', '#ff7f0e'], width=0.6)
        
        plt.title(f"So sánh các Chỉ số Công bằng theo {feature_name}", fontsize=14, fontweight='bold')
        plt.ylabel("Tỷ lệ (Từ 0 đến 1)", fontsize=12)
        plt.xlabel(feature_name, fontsize=12)
        
        for p in ax.patches:
            height = p.get_height()
            if height > 0: # Tránh in số 0.00
                ax.annotate(f"{height:.2f}", 
                            (p.get_x() + p.get_width() / 2., height), 
                            ha='center', va='bottom', fontsize=10, color='black')

        plt.xticks(rotation=0)
        plt.ylim(0, 1.15)
        plt.legend(loc='lower right')
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        
        # Lưu ảnh biểu đồ
        plt.savefig(output_image.replace('.png', '_chart.png'), bbox_inches='tight', dpi=300)
        plt.close()
        print(f"📸 Đã lưu ảnh Biểu đồ cột tại: {output_image.replace('.png', '_chart.png')}")

        # IF have a time, i can do more like country, 
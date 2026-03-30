import shap
import matplotlib.pyplot as plt
import pandas as pd

class CareerShapeExplainer:
    def __init__(self, model, X_train):
        self.model = model
        self.X_train = X_train
        masker = shap.maskers.Independent(data=self.X_train)
        
        try:
            self.explainer = shap.Explainer(self.model, masker=masker)
            print(f"🚀 Khởi tạo Explainer vạn năng cho {type(model).__name__}")
        except Exception as e:
            print(f"⚠️ Chuyển sang KernelExplainer do lỗi: {e}")
            self.explainer = shap.KernelExplainer(self.model.predict_proba, shap.sample(self.X_train, 50))

    def save_global_explanation(self, X_test, output_path="models/classtification/shap_global_summary.png"):
        shap_values = self.explainer(X_test)
        plt.figure(figsize=(10, 6))
        shap.plots.beeswarm(shap_values, show=False)
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Đã lưu biểu đồ tổng quan tại: {output_path}")
    
    def save_student_waterfall(self, student_features, output_path="models/classtification/student_waterfall.png"):
        shap_values = self.explainer(student_features)
        plt.figure(figsize=(8, 6))
        # shap_values[0] đại diện cho 1 dòng dữ liệu truyền vào
        shap.plots.waterfall(shap_values[0], show=False)
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"✅ Đã lưu biểu đồ Waterfall tại: {output_path}")
    def get_chatbot_adivce_data(self, student_features):

        #Tinh shap values cho 1 sinh viên cụ thể
        shape_values = self.explainer(student_features)

        values = shape_values.values[0]
        feature_names = student_features.columns.tolist()

        # Tạo dictionary map giữa tên cột và mức độ tác động
        impact_dict = dict(zip(feature_names, values))
        
        # Phân loại điểm mạnh (tác động dương) và điểm yếu (tác động âm)
        strengths = {k: v for k, v in impact_dict.items() if v > 0}
        weaknesses = {k: v for k, v in impact_dict.items() if v < 0}
        
        # Sắp xếp để lấy ra yếu tố ảnh hưởng mạnh nhất
        top_strength = sorted(strengths.items(), key=lambda x: x[1], reverse=True)
        top_weakness = sorted(weaknesses.items(), key=lambda x: x[1]) 

        # print("Top Strengths:", top_strength)
        # print("Top Weaknesses:", top_weakness)
        # # Trả về data thô để Chatbot tự sinh câu văn
        return {
            "top_positive": top_strength[0] if top_strength else None,
            "top_negative": top_weakness[0] if top_weakness else None,
            "all_impacts": impact_dict
        }
    
    def save_student_waterfall(self, student_features, output_path="models/classtification/student_waterfall.png"):
      
        shap_values = self.explainer(student_features)
    

        plt.figure(figsize=(8, 6))
        # shap_values[0] lấy sinh viên đầu tiên (và duy nhất) trong DataFrame đầu vào
        shap.plots.waterfall(shap_values[0], show=False)
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Đã lưu biểu đồ Waterfall cho sinh viên tại: {output_path}")

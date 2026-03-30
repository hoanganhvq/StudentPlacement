import joblib
import os
import pandas as pd
import numpy as np
from app.schema import CareerInputPredict, PredictionResponse
from fastapi.encoders import jsonable_encoder

from src.explainability.shap_analysis_cls import CareerShapeExplainer
from src.explainability.shap_analysis_reg import SalaryShapeExplainer
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models"))

class ModelService:
    def __init__(self):
        self.scaler_cls = joblib.load(os.path.join(MODEL_DIR, "scaler_cls.joblib"))
        self.encoder_cls = joblib.load(os.path.join(MODEL_DIR, "encoder_cls.joblib"))
        self.model_cls = joblib.load(os.path.join(MODEL_DIR, "classtification/best_model_Logistic Regression.joblib"))

        self.encoder_reg = joblib.load(os.path.join(MODEL_DIR, "encoder_reg.joblib"))
        self.scaler_reg = joblib.load(os.path.join(MODEL_DIR, "scaler_reg.joblib"))
        self.model_reg = joblib.load(os.path.join(MODEL_DIR, "regression/best_model_xgboost_regression.joblib"))

        #SHAP
        X_train_cls = pd.read_csv("data/processed/X_train_cls.csv")
        X_train_reg = pd.read_csv("data/processed/X_train_reg.csv")

        self.career_explainer = CareerShapeExplainer(self.model_cls, X_train_cls)
        self.salary_explainer = SalaryShapeExplainer(self.model_reg, X_train_reg)

        self.optimal_threshold = 0.45999999999999985

    def _feature_engineering(self, df, mode="cls"):
        df = df.copy()

        tier_mapping = {"Tier 1": 3, "Tier 2": 2, "Tier 3": 1}
        rank_mapping = {'Top 100': 3, '100-300': 2, '300+': 1}
        
        df['college_tier'] = df['college_tier'].map(tier_mapping)
        df['university_ranking_band'] = df['university_ranking_band'].map(rank_mapping)
        
        df['total_internship_value'] = df['internship_quality_score'] * df['internship_count']
        df['academic_power'] = df['cgpa'] * df['university_ranking_band']
        if(mode =="cls"):
            df['risk_index'] = df['backlogs'] * (df['cgpa'] + 0.1)
        else:
            df['pedigree_score'] = df['college_tier'] * df['university_ranking_band']
            df['weighted_gpa'] = df['cgpa'] * df['college_tier']
            df['soft_tech_synergy'] = df['aptitude_score'] * df['communication_score']
            df['risk_adjusted_gpa'] = df['cgpa'] / (df['backlogs'] + 1)

            top_countries = ['USA', 'UK', 'Canada']
            df['is_top_market'] = df['country'].apply(lambda x: 1 if x in top_countries else 0)
        return df

    def handle_data_cls(self, input_data:CareerInputPredict):
        data_dict = input_data.dict()
        #1 Xu ly du lieu input de dua vao chay, feature engineering
        df_cls = pd.DataFrame([data_dict])
        df_cls = self._feature_engineering(df_cls, mode="cls")
        
        #2. onehot encoded truoc khi dua vao chay 
        categorical_cols = ['country', 'specialization', 'industry']
        encoded_cls = self.encoder_cls.transform(df_cls[categorical_cols])
        encoded_df_cls = pd.DataFrame(encoded_cls, columns=self.encoder_cls.get_feature_names_out(categorical_cols))
        
        X_cls = pd.concat([df_cls.drop(columns=categorical_cols), encoded_df_cls], axis=1)
        #3. Scaler du lieu 
        num_features_cls = ['cgpa', 'aptitude_score', 'communication_score', 
                            'internship_quality_score', 'internship_count',
                            'total_internship_value', 'academic_power', 'risk_index']
        X_cls[num_features_cls] = self.scaler_cls.transform(X_cls[num_features_cls])
        
        return X_cls
    
    def handle_data_reg (self, input_data:CareerInputPredict):
        data_dict = input_data.dict()

        df_reg = pd.DataFrame([data_dict])
        df_reg = self._feature_engineering(df_reg, mode="reg")
        
        #1. Encoded du lie 
        categorical_cols = ['country', 'specialization', 'industry']
        encoded_reg = self.encoder_reg.transform(df_reg[categorical_cols])
        encoded_df_reg = pd.DataFrame(encoded_reg, columns=self.encoder_reg.get_feature_names_out(categorical_cols))
        X_reg = pd.concat([df_reg.drop(columns=categorical_cols), encoded_df_reg], axis=1)
            #Scaler du lieu 
        num_features_reg = [
                'cgpa', 'aptitude_score', 'communication_score', 'internship_count', 
                'internship_quality_score', 'total_internship_value', 'academic_power', 
                'pedigree_score', 'weighted_gpa', 'soft_tech_synergy', 'risk_adjusted_gpa',
                'college_tier', 'university_ranking_band'
            ]
        X_reg[num_features_reg] = self.scaler_reg.transform(X_reg[num_features_reg])
        return X_reg

    def to_json_safe(self, advice):
        if advice is None: return None
        # advice thường là: ("tên_feature", np.float32(0.88))
        # Ta biến nó thành: ["tên_feature", 0.88]
        return [str(advice[0]), float(advice[1])]
    
    def generate_natural_insights_cls(self, advice_data):
        all_impacts = advice_data.get("all_impacts", {})
        if not all_impacts:
            return ["Hồ sơ của bạn đang ở mức trung bình của thị trường."]

        contributions = []
        for feature, weight in all_impacts.items():
            contributions.append({"name": feature, "weight": weight})
        
        sorted_contribs = sorted(contributions, key=lambda x: abs(x['weight']), reverse=True)

        friendly_name = {
                "cgpa": "Điểm trung bình tích lũy",
                "backlogs": "Số môn nợ",
                "college_tier": "Hạng trường",
                "country": "Quốc gia",
                "university_ranking_band": "Bảng xếp hạng trường",
                "internship_count": "Số lượng kỳ thực tập",
                "aptitude_score": "Điểm tư duy logic",
                "communication_score": "Kỹ năng giao tiếp",
                "specialization": "Chuyên ngành đào tạo",
                "industry": "Ngành nghề mong muốn",
                "internship_quality_score": "Chất lượng kỳ thực tập",
            }
        
        insights = []

        for item in sorted_contribs[:3]:
            name = friendly_name.get(item['name'], item['name'])
            weight = item['weight']
            if (weight > 0.05):
                msg = f"Yếu tố  {name} có ảnh hưởng tích cực mạnh mẽ đến khả năng được tuyển dụng."
            elif weight < -0.05:
                msg = f"Yếu tố  {name} có ảnh hưởng tiêu cực đến khả năng được tuyển dụng."
            insights.append(msg)

        return insights
    
    def generate_natural_insights_reg(self, advice_data):
        all_impacts = advice_data.get("all_impacts", {})
        if not all_impacts:
            return ["Hồ sơ của bạn đang ở mức trung bình của thị trường."]

        contributions = []
        for feature, weight in all_impacts.items():
            contributions.append({"name": feature, "weight": weight})
        sorted_contribs = sorted(contributions, key=lambda x: abs(x['weight']), reverse=True)

        friendly_name = {
                "cgpa": "Điểm trung bình tích lũy",
                "backlogs": "Số môn nợ",
                "college_tier": "Hạng trường",
                "country": "Quốc gia",
                "university_ranking_band": "Bảng xếp hạng trường",
                "internship_count": "Số lượng kỳ thực tập",
                "aptitude_score": "Điểm tư duy logic",
                "communication_score": "Kỹ năng giao tiếp",
                "specialization": "Chuyên ngành đào tạo",
                "industry": "Ngành nghề mong muốn",
                "internship_quality_score": "Chất lượng kỳ thực tập",
            }

        insights = []

        for item in sorted_contribs[:3]:
            name = friendly_name.get(item['name'], item['name'])
            weight = item['weight']
            if (weight > 0.05):
                msg = f"Yếu tố  {name} có ảnh hưởng tích cực mạnh mẽ đến mức lương dự kiến."
            elif weight < -0.05:
                msg = f"Yếu tố  {name} có ảnh hưởng tiêu cực đến mức lương dự kiến."
            insights.append(msg)

        return insights

    def predict(self, input_data: CareerInputPredict):
        X_cls = self.handle_data_cls(input_data)
        #1. clastification
        probs = self.model_cls.predict_proba(X_cls)[0]
        proba_placed = float(probs[1])


        is_placed = 1 if proba_placed > self.optimal_threshold else 0
        estimated_salary = 0.0

        cls_advice = self.career_explainer.get_chatbot_adivce_data(X_cls)
        ai_insights_cls = self.generate_natural_insights_cls(cls_advice)
        # print("CLS Advice:", cls_advice)
        reg_advice = None
        if is_placed == 1:
            X_reg = self.handle_data_reg(input_data)

            # Predict & Inverse Log Transform
            log_salary = self.model_reg.predict(X_reg)[0]
            estimated_salary = float(np.expm1(log_salary))

            #1. Regression Advice
            reg_advice = self.salary_explainer.get_chatbot_advice_data(X_reg)
            ai_insights_reg = self.generate_natural_insights_reg(reg_advice) if is_placed == 1 else []


        
        result = {
        "status": "Placed" if is_placed == 1 else "Not Placed",
        "probability": round(float(proba_placed), 4),
        "ai_insights_placement": ai_insights_cls,
        "ai_insights_salary": ai_insights_reg,
        "estimated_salary": round(float(estimated_salary), 2),
        "explanations": {
            "placement": {
                "top_strength": self.to_json_safe(cls_advice.get("top_positive")),
                "top_weakness": self.to_json_safe(cls_advice.get("top_negative")),
                "all_features": [
                   {"name": k, "value": float(v)} 
                    for k, v in cls_advice.get("all_impacts", {}).items()
                ] 
            },
            "salary": {
                "top_strength": self.to_json_safe(reg_advice.get("top_positive")) if reg_advice else None,
                "top_weakness": self.to_json_safe(reg_advice.get("top_negative")) if reg_advice else None,
                "all_features": [
                    {"name": k, "value": float(v)} 
                    for k, v in reg_advice.get("all_impacts", {}).items()
                ] if reg_advice else []
                }
            }
        }
        return jsonable_encoder(result);
    
    

model_service = ModelService()
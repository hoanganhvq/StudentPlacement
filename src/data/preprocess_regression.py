import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling  import SMOTE #Smote handle class imbalance
import numpy as np

def preprocess_data_reg(file_path):
  # 1. Load the dataset
    df = pd.read_csv(file_path)

    #2. Just for regression, we only care about placed students
    df_reg = df[df['placement_status'] == 'Placed'].copy()

    # 3. Ordinal Encoding
    tier_mapping = {"Tier 1": 3, "Tier 2": 2, "Tier 3": 1}
    rank_mapping = {'Top 100': 3, '100-300': 2, '300+': 1}
    
    df_reg['college_tier'] = df_reg['college_tier'].map(tier_mapping)
    df_reg['university_ranking_band'] = df_reg['university_ranking_band'].map(rank_mapping)

    # 4. Feature Engineering 
    df_reg['total_internship_value'] = df_reg['internship_quality_score'] * df_reg['internship_count']
    df_reg['academic_power'] = df_reg['cgpa'] * df_reg['university_ranking_band']
    df_reg['pedigree_score'] = df_reg['college_tier'] * df_reg['university_ranking_band']
    df_reg['weighted_gpa'] = df_reg['cgpa'] * df_reg['college_tier']
    df_reg['soft_tech_synergy'] = df_reg['aptitude_score'] * df_reg['communication_score']
    df_reg['risk_adjusted_gpa'] = df_reg['cgpa'] / (df_reg['backlogs'] + 1)
    
    top_countries = ['USA', 'UK', 'Canada']
    df_reg['is_top_market'] = df_reg['country'].apply(lambda x: 1 if x in top_countries else 0)

    # 5. Danh sách các cột cần Scale
    numerical_features = [
        'cgpa', 'aptitude_score', 'communication_score', 'internship_count', 
        'internship_quality_score', 'total_internship_value', 'academic_power', 
        'pedigree_score', 'weighted_gpa', 'soft_tech_synergy', 'risk_adjusted_gpa',
        'college_tier', 'university_ranking_band' # Scale luôn 2 biến này để Ridge học tốt hơn
    ]

    
    
     #6 One-Hot Encoding
    categorical_cols = ['country', 'specialization', 'industry']
    ohe_reg = OneHotEncoder(handle_unknown="ignore", sparse_output=False) #It will be 0 if another input 
    
    encoded_cols = ohe_reg.fit_transform(df_reg[categorical_cols])
    encoded_df = pd.DataFrame(encoded_cols, columns=ohe_reg.get_feature_names_out(categorical_cols))

    df_final = pd.concat([df_reg.drop(columns=categorical_cols + ['placement_status', 'salary']).reset_index(drop=True), 
                          encoded_df.reset_index(drop=True)], axis=1)
  
    X_reg = df_final
    #5 Handle target - Log-transform salary để giảm độ lệch
    #Thu hep khoảng cách giữa các mức lương cao và thấp, giúp mô hình học tốt hơn
    y_reg = np.log1p(df_reg['salary'])

    #7 Split data into train/val/test
    X_train_reg, X_temp_reg, y_train_reg, y_temp_reg = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
    X_val_reg, X_test_reg, y_val_reg, y_test_reg = train_test_split(X_temp_reg, y_temp_reg, test_size=0.5, random_state=42)

    #8 Scale features
    scaler_reg = StandardScaler()
    X_train_reg[numerical_features] = scaler_reg.fit_transform(X_train_reg[numerical_features])
    X_test_reg[numerical_features] = scaler_reg.transform(X_test_reg[numerical_features])
    X_val_reg[numerical_features] = scaler_reg.transform(X_val_reg[numerical_features])

    #Check
    X_train_reg.to_csv("data/processed/X_train_reg.csv", index=False)

    joblib.dump(ohe_reg, "models/encoder_reg.joblib")
    joblib.dump(scaler_reg, "models/scaler_reg.joblib")

    print("Preprocessing regression data completed. Scalers saved.")

    return (X_train_reg, X_val_reg, X_test_reg, y_train_reg, y_val_reg, y_test_reg)
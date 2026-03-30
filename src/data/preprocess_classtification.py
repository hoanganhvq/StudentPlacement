import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling  import SMOTE #Smote handle class imbalance


def preprocess_data_cls(file_path):
  # 1. Load the dataset
    df = pd.read_csv(file_path)

    # 2. Ordinal Encoding (Sửa lỗi khoảng trắng)
    tier_mapping = {"Tier 1": 3, "Tier 2": 2, "Tier 3": 1}
    df['college_tier'] = df['college_tier'].map(tier_mapping)

    ranking_mapping = {'Top 100': 3, '100-300': 2, '300+': 1}
    df['university_ranking_band'] = df['university_ranking_band'].map(ranking_mapping)


    # 3 Feature Engineering 
    df['total_internship_value'] = df['internship_quality_score'] * df['internship_count']
    df['academic_power'] = df['cgpa'] * df['university_ranking_band']
    df['risk_index'] = df['backlogs'] * (df['cgpa'] + 0.1)



    numerical_features = ['cgpa', 'aptitude_score', 'communication_score', 
                      'internship_quality_score', 'internship_count',
                      'total_internship_value', 'academic_power', 'risk_index']


    # 4. Encode target
    df['placement_status_num'] = df['placement_status'].map({'Placed': 1, 'Not Placed': 0})
    
     #5 One-Hot Encoding
    categorical_cols = ['country', 'specialization', 'industry']

    onehot_encode_cls = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    
    encoded_cols = onehot_encode_cls.fit_transform(df[categorical_cols])
    
    encoded_df = pd.DataFrame(encoded_cols, columns=onehot_encode_cls.get_feature_names_out(categorical_cols))

    df_final = pd.concat([df.drop(columns=categorical_cols + ['placement_status', 'placement_status_num', 'salary']), 
                          encoded_df], axis=1)
    
    X_cls = df_final
    y_cls = df['placement_status_num']
    
    # 6. Chia dữ liệu thành train/test
    X_train_cls, X_temp_cls, y_train_cls, y_temp_cls = train_test_split(X_cls, y_cls, test_size=0.2, random_state=42)
    X_val_cls, X_test_cls, y_val_cls, y_test_cls = train_test_split(X_temp_cls, y_temp_cls, test_size=0.5, random_state=42)

      #7 Scale features
    scaler_cls = StandardScaler()
    X_train_cls[numerical_features] = scaler_cls.fit_transform(X_train_cls[numerical_features])
    X_test_cls[numerical_features] = scaler_cls.transform(X_test_cls[numerical_features])
    X_val_cls[numerical_features] = scaler_cls.transform(X_val_cls[numerical_features])


    #Check 
    X_train_cls.to_csv("data/processed/X_train_cls.csv", index=False)

    joblib.dump(scaler_cls, "models/scaler_cls.joblib")
    joblib.dump(onehot_encode_cls, "models/encoder_cls.joblib")

    
    print("Preprocessing completed. Scalers saved.")

    return (X_train_cls, X_val_cls, X_test_cls, y_train_cls, y_val_cls, y_test_cls)
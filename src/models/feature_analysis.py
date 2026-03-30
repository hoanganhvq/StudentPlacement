import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

def save_correlation_plots(df, output_dir="models"):
    """Tự động tính toán và lưu biểu đồ Heatmap ra file ảnh"""
    os.makedirs(output_dir, exist_ok=True)
    
    # --- 1. Phân tích cho Classification ---
    plt.figure(figsize=(10, 8))
    df_cls = df.copy()
    df_cls['placement_status_num'] = df_cls['placement_status'].map({'Placed': 1, 'Not Placed': 0})
    
    corr_cls = df_cls.select_dtypes(include=[np.number]).corr()
    sns.heatmap(corr_cls[['placement_status_num']].sort_values(by='placement_status_num', ascending=False), 
                annot=True, cmap='Blues', fmt=".2f")
    plt.title("Correlation - Placement Status")
    plt.savefig(f"{output_dir}/correlation_classification.png") # Lưu ảnh
    plt.close()

    # --- 2. Phân tích cho Regression ---
    plt.figure(figsize=(10, 8))
    df_reg = df[df['placement_status'] == 'Placed'].copy()
    df_reg['salary_log'] = np.log1p(df_reg['salary'])
    
    corr_reg = df_reg.select_dtypes(include=[np.number]).corr()
    sns.heatmap(corr_reg[['salary_log']].sort_values(by='salary_log', ascending=False), 
                annot=True, cmap='Oranges', fmt=".2f")
    plt.title("Correlation - Salary (Log)")
    plt.savefig(f"{output_dir}/correlation_regression.png") # Lưu ảnh
    plt.close()
    
    print(f"✅ Đã xuất biểu đồ vào thư mục: {output_dir}")

if __name__ == "__main__":
    # Chạy thử nghiệm
    raw_df = pd.read_csv("data/raw/global_placement.csv")

    tier_mapping = {"Tier 1": 3, "Tier 2": 2, "Tier 3": 1}
    raw_df['college_tier'] = raw_df['college_tier'].map(tier_mapping)

    ranking_mapping = {'Top 100': 3, '100-300': 2, '300+': 1}
    raw_df['university_ranking_band'] = raw_df['university_ranking_band'].map(ranking_mapping)


    # 4 Feature Engineering 
    raw_df['total_internship_value'] = raw_df['internship_quality_score'] * raw_df['internship_count']
    raw_df['academic_power'] = raw_df['cgpa'] * raw_df['university_ranking_band']
    raw_df['risk_index'] = raw_df['backlogs'] * (raw_df['cgpa'] + 0.1)


    raw_df['pedigree_score'] = raw_df['college_tier'] * raw_df['university_ranking_band']
    raw_df['weighted_gpa'] = raw_df['cgpa'] * raw_df['college_tier']
    
    # 2. Nhóm Kỹ năng
    raw_df['soft_tech_synergy'] = raw_df['aptitude_score'] * raw_df['communication_score']
    raw_df['practical_index'] = raw_df['internship_quality_score'] * raw_df['internship_count']
    
    # 3. Nhóm Rủi ro
    raw_df['risk_adjusted_gpa'] = raw_df['cgpa'] / (raw_df['backlogs'] + 1)
    
    # 4. Nhóm Địa lý (Ví dụ)
    top_countries = ['USA', 'UK', 'Canada']
    raw_df['is_top_market'] = raw_df['country'].apply(lambda x: 1 if x in top_countries else 0)
    save_correlation_plots(raw_df)
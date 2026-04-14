# 🚀 Hệ thống Tư vấn Sự nghiệp Thông minh (Smart Career Advisory System)

### Kết hợp Chatbot tương tác, Dự báo đa mục tiêu và Phân tích công bằng

Dự án này là một hệ thống toàn diện hỗ trợ sinh viên trong việc định hướng nghề nghiệp dựa trên dữ liệu. Hệ thống tích hợp các mô hình Machine Learning mạnh mẽ để dự báo khả năng có việc làm và mức lương, kết hợp với Chatbot AI để tư vấn trực tiếp từ hồ sơ (CV/PDF).

---

## 📌 Tính năng chính

- **Dự báo đa mục tiêu (Multi-target Prediction):**  
  Dự báo khả năng trúng tuyển (Classification) và mức lương kỳ vọng (Regression).

- **Chatbot AI tương tác:**  
  Hỗ trợ đọc file CV (PDF), tư vấn lộ trình học tập thông qua Google Gemini API.

- **Giải thích mô hình (Explainability):**  
  Sử dụng **SHAP** để giải thích lý do mô hình đưa ra kết quả, giúp tăng tính minh bạch.

- **Phân tích công bằng (Fairness Analysis):**  
  Đánh giá và đảm bảo mô hình không bị thiên kiến đối với các nhóm đối tượng khác nhau.

- **Tối ưu hóa mô hình:**  
  Sử dụng **Optuna** để Threshold Tuning và tìm bộ tham số tốt nhất.

---

## 🛠 Công nghệ sử dụng

- **Backend:** FastAPI (Python 3.13)  
- **Frontend:** Streamlit  
- **Machine Learning:** Scikit-learn, XGBoost, Optuna, SHAP  
- **Algorithms:** KNN, Random Forest, XGBoost, Stacking Ensemble, Ridge Regression  
- **AI Integration:** Google Gemini API (LangChain)  
- **Containerization:** Docker & Docker Compose  

---

## 📂 Cấu trúc dự án

```text
.
├── app/                  # Backend FastAPI
│   ├── langchain_logic/  # Xử lý RAG và Chatbot với Gemini
│   ├── services/         # Logic nghiệp vụ và load model
│   └── main.py           # Entry point của server
├── frontend/             # Giao diện Streamlit
│   └── frontend_streamlit.py
├── models/               # Chứa các model (.joblib) và bộ mã hóa (Scaler/Encoder)
├── notebooks/            # Quá trình EDA và thực nghiệm mô hình (Jupyter Notebook)
├── src/                  # Mã nguồn core (Huấn luyện, đánh giá, SHAP, Fairness)
├── data/                 # Dữ liệu CSV (Raw & Processed)
├── Dockerfile            # Dockerfile cho Backend
├── Dockerfile.frontend   # Dockerfile cho Frontend
└── docker-compose.yml    # Cấu hình triển khai hệ thống


Hướng dẫn cài đặt
1. Chuẩn bị môi trường
python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate      # Windows

pip install -r requirements.txt
2. Cấu hình biến môi trường

Tạo file .env tại thư mục gốc:

GEMINI_API_KEY="..."
3. Chạy ứng dụng
▶️ Backend (FastAPI)
python -m app.main
🎨 Frontend (Streamlit)
streamlit run frontend/frontend_streamlit.py
4. Triển khai với Docker
docker-compose up --build
📊 Phương pháp tiếp cận Machine Learning
Tiền xử lý:
Xử lý dữ liệu thô, encoding các biến phân loại và scaling dữ liệu.
Huấn luyện:
Thực nghiệm với KNN, Random Forest, XGBoost và kết hợp mô hình qua Stacking.
Tối ưu:
Sử dụng Optuna để tìm ngưỡng (threshold) tối ưu nhằm cân bằng giữa Precision và Recall.
Giải thích & Công bằng:
Triển khai SHAP value để trực quan hóa mức độ ảnh hưởng của đặc trưng và kiểm tra tính công bằng của dự báo.



🚀 Hướng dẫn cài đặt
1. Chuẩn bị môi trường
python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate      # Windows

pip install -r requirements.txt
2. Cấu hình biến môi trường

Tạo file .env tại thư mục gốc:

GEMINI_API_KEY="..."
3. Chạy ứng dụng
▶️ Backend (FastAPI)
python -m app.main
🎨 Frontend (Streamlit)
streamlit run frontend/frontend_streamlit.py
4. Triển khai với Docker
docker-compose up --build

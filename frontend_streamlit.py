import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Career AI | Tư vấn sự nghiệp", layout="wide", page_icon="🚀")

# Inject Custom CSS để làm giao diện mềm mại hơn
st.markdown("""
    <style>
    /* Gradient Background cho Header */
    .main-header {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }
    /* Card style cho các chỉ số */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #eee;
    }
    /* Custom button style */
    .stButton>button {
        border-radius: 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

BASE_URL = "http://localhost:8000"

# --- INITIALIZATION ---
if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "👋 Chào bạn! Tớ là trợ lý ảo Career AI. Tớ sẽ giúp bạn dự báo khả năng có việc làm và mức lương dựa trên profile của bạn."}]

if "career_data" not in st.session_state:
    st.session_state["career_data"] = {
        "cgpa": None, "backlogs": None, "college_tier": None, "country": None,
        "university_ranking_band": None, "internship_count": None, "aptitude_score": None,
        "communication_score": None, "specialization": None, "industry": None, "internship_quality_score": None,
    }

if "mode" not in st.session_state:
    st.session_state["mode"] = None

# --- HEADER ---
st.markdown('<div class="main-header"><h1>🤖 Career Advisory Hybrid System</h1><p>Phân tích CV & Dự báo lộ trình nghề nghiệp bằng AI</p></div>', unsafe_allow_html=True)

# --- MODE SELECTION ---
if st.session_state["mode"] is None:
    st.subheader("Bắt đầu bằng cách nào?")
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.info("### 📄 Tải lên CV\nAI sẽ tự động đọc thông tin từ file PDF của bạn.")
            if st.button("Sử dụng CV có sẵn", use_container_width=True):
                st.session_state["mode"] = "CV"
                st.session_state["message"].append({"role": "assistant", "content": "Tuyệt! Hãy tải file CV của bạn ở thanh bên trái (Sidebar) nhé."})
                st.rerun()
    with col2:
        with st.container():
            st.success("### 💬 Chat trực tiếp\nCung cấp thông tin qua việc trò chuyện cùng AI.")
            if st.button("Bắt đầu Chat ngay", use_container_width=True):
                st.session_state["mode"] = "chat"
                welcome_content = "💡 **Hãy chia sẻ một chút về học vấn của bạn:**\n* Bạn học trường nào?\n* Chuyên ngành của bạn là gì?"
                st.session_state["message"].append({"role": "assistant", "content": welcome_content})
                st.rerun()

# --- SIDEBAR & DATA PROGRESS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("Hồ sơ của bạn")
    
    # Progress Bar theo dõi tiến độ điền form
    filled_fields = sum(1 for v in st.session_state["career_data"].values() if v is not None)
    progress = filled_fields / len(st.session_state["career_data"])
    st.write(f"Độ hoàn thiện: {int(progress*100)}%")
    st.progress(progress)
    
    if st.session_state["mode"] == "CV":
        st.divider()
        st.header("📤 Tải CV tại đây")
        uploaded_file = st.file_uploader("Định dạng hỗ trợ: PDF", type=["pdf"])
        if uploaded_file and st.session_state["career_data"]["cgpa"] is None:
            with st.spinner("Đang 'đọc' CV của bạn..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                try:
                    response = requests.post(f"{BASE_URL}/api/chat/extract", files=files)
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state["career_data"].update(result)
                        st.success("Trích xuất dữ liệu thành công!")
                        if result.get("next_question"):
                            st.session_state["message"].append({"role": "assistant", "content": result.get("next_question")})
                        st.rerun()
                except:
                    st.error("Không thể kết nối đến Server.")


# --- MAIN CHAT INTERFACE ---
chat_container = st.container(height=450 if "prediction_result" not in st.session_state else 250)

with chat_container:
    for msg in st.session_state["message"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Slot Filling Logic
missing_fields = [k for k, v in st.session_state["career_data"].items() if v is None]
print("Missing field:", missing_fields)

if prompt := st.chat_input("Nhập thông tin hoặc câu hỏi của bạn..."):
    st.session_state["message"].append({"role": "user", "content": prompt})
    
    with st.spinner("Đang xử lý..."):
        payload = {"message": prompt, "missing_field": missing_fields}
        response = requests.post(f"{BASE_URL}/api/handle_chat", json=payload)
        
        if response.status_code == 200:
            result = response.json()  # Giả sử result là 1 dict
            
            for field, value in result.items():
                if field in st.session_state["career_data"] and value is not None:
                    st.session_state["career_data"][field] = value
                    print(f"✅ Đã gán {field}: {value}")
                    print("Du lieu hien taij: ", st.session_state["career_data"])

            if result.get("next_question"):
                st.session_state["message"].append({
                    "role": "assistant", 
                    "content": result.get("next_question")
                })
            
            if result.get("is_complete"):
                st.session_state["message"].append({
                    "role": "assistant", 
                    "content": "🎉 Tuyệt vời! Tớ đã có đủ thông tin để phân tích rồi."
                })
            
            # 3. Cuối cùng mới rerun để cập nhật UI
            st.rerun()
            
        else:
            st.error("Đã có lỗi xảy ra khi xử lý thông tin.")
        print("Current career data: ", st.session_state["career_data"])

# --- PREDICTION RESULTS ---
if st.session_state["mode"] and not missing_fields:
    if "prediction_result" not in st.session_state:
        st.balloons()
        st.info("🚀 Tất cả dữ liệu đã sẵn sàng!")
        if st.button("PHÂN TÍCH SỰ NGHIỆP NGAY", use_container_width=True, type="primary"):
            with st.spinner("Hệ thống AI đang tính toán xác suất..."):
                res = requests.post(f"{BASE_URL}/api/predict", json=st.session_state["career_data"])
                if res.status_code == 200:
                    st.session_state["prediction_result"] = res.json()
                    st.rerun()

if "prediction_result" in st.session_state:
    res = st.session_state["prediction_result"]
    st.divider()
    
    # Dashboard hiển thị kết quả
    st.subheader("📊 Kết quả dự báo chuyên sâu")
    m_col1, m_col2, m_col3 = st.columns(3)
    
    with m_col1:
        st.markdown(f"""<div class='metric-card'><p style='color:gray;'>Tỉ lệ trúng tuyển</p><h2>{res['probability']*100:.1f}%</h2></div>""", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""<div class='metric-card'><p style='color:gray;'>Lương khởi điểm kỳ vọng</p><h2>${res['estimated_salary']:,}</h2></div>""", unsafe_allow_html=True)
    with m_col3:
        status = "Rất khả quan" if res['probability'] > 0.7 else "Cần nỗ lực thêm"
        st.markdown(f"""<div class='metric-card'><p style='color:gray;'>Đánh giá chung</p><h2>{status}</h2></div>""", unsafe_allow_html=True)

    # Visualization
    st.write("")
    col_graph, col_advice = st.columns([2, 1])
    
    with col_graph:
        target_features = ["cgpa", "backlogs", "college_tier", "internship_count", "aptitude_score", "communication_score", "internship_quality_score"]
        df_all = pd.DataFrame(res['explanations']['placement']['all_features'])
        df_plot = df_all[df_all['name'].isin(target_features)].copy()
        
        fig = go.Figure(go.Waterfall(
            orientation = "h",
            measure = ["relative"] * len(df_plot),
            y = df_plot['name'],
            x = df_plot['value'],
            text = [f"{v:+.2f}" for v in df_plot['value']],
            increasing = {"marker":{"color":"#2ecc71"}},
            decreasing = {"marker":{"color":"#e74c3c"}}
        ))
        fig.update_layout(title="Yếu tố ảnh hưởng (SHAP)", height=400, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_advice:
        st.markdown("### 💡 Lời khuyên cho bạn")
        if res['probability'] < 0.6:
            st.warning("- Hãy cải thiện điểm Aptitude Test.\n- Tìm kiếm thêm ít nhất 1 kỳ thực tập chuyên ngành.")
        else:
            st.success("- Hồ sơ của bạn rất mạnh!\n- Tập trung vào kỹ năng thương lượng lương.")
        
        if st.button("🔄 Làm lại từ đầu", use_container_width=True):
            st.session_state.clear()
            st.rerun()
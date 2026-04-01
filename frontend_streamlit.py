import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Student Placement Dashboard", layout="wide")

# 1. Khởi tạo bộ nhớ
if "message" not in st.session_state:
    st.session_state["message"] = [{"role": "assistant", "content": "Chào Phan! Tớ là trợ lý tư vấn sự nghiệp.Chúng ta sẽ chat để lấy thông tin nhaaaa?"}]

if "career_data" not in st.session_state:
    st.session_state["career_data"] = {
        "cgpa": None, "backlogs": None, "college_tier": None, "country": None,
        "university_ranking_band": None, "internship_count": None, "aptitude_score": None,
        "communication_score": None, "specialization": None, "industry": None, "internship_quality_score": None,
    }

if "mode" not in st.session_state:
    st.session_state["mode"] = None

print("Chay lai tu dau")

st.title("🤖 Career Advisory Hybrid System")

# Chọn chế độ
if st.session_state["mode"] is None:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📁 Tôi có sẵn CV", use_container_width=True):
            st.session_state["mode"] = "CV"
            st.session_state["message"].append({"role": "assistant", "content": "Tuyệt! Hãy tải file CV của bạn ở thanh bên trái (Sidebar) nhé."})
            st.rerun()
    with col2:
        if st.button("💬 Tôi muốn chat", use_container_width=True):
            st.session_state["mode"] = "chat"
            st.session_state["message"].append({"role": "assistant", "content": "Oki! Đầu tiên, Ban hay gioi thieu ve ban than va muc tieu nghe nghiep nha!"})            
            st.rerun()

# 2. Sidebar xử lý PDF
with st.sidebar:
    if st.session_state["mode"] == "CV":
        st.header("Upload CV")
        uploaded_file = st.file_uploader("Chọn file CV (PDF)", type=["pdf"])
        # Chỉ gọi API extract nếu chưa có dữ liệu nào (cgpa là trường đại diện)
        if uploaded_file and st.session_state["career_data"]["cgpa"] is None:
            with st.spinner("Đang phân tích CV..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                response = requests.post(f"{BASE_URL}/api/chat/extract", files=files)
                if response.status_code == 200:
                    st.session_state["career_data"].update(response.json())
                    st.success("Phân tích CV thành công!")
                    st.rerun()

# 3. Hiển thị Chat
for msg in st.session_state["message"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Logic Gôm thông tin (Slot Filling)
missing_fields = [k for k, v in st.session_state["career_data"].items() if v is None]


# 5. Ô nhập liệu (Luôn hiện để User chat bất cứ lúc nào)
if prompt := st.chat_input("Nhập thông tin tại đây..."):
    st.session_state["message"].append({"role": "user", "content": prompt})
    with st.spinner("Đang xử lý thông tin..."):
       
        payload = {"message": prompt,
                   "current_data": st.session_state["career_data"]} # Gửi cả dữ liệu đã có để LLM biết đang thiếu gì
        
        print("Sending to API: ", payload)

        response = requests.post(f"{BASE_URL}/api/handle_chat", json=payload)
        
        print("API response content: ", response.json())

        if response.status_code == 200:
            result = response.json()
            #Neu hoi ngoai le thi phan hoi lai va khong update du lieu
            if result.get("next_question"):
                print("Next question from API: ", result.get("next_question"))
                st.session_state["message"].append({""
                "role": "assistant", "content": result.get("next_question", "")})
                st.rerun()
            if result.get("is_off_topic"):
                st.session_state["message"].append({
                    "role": "assistant", 
                    "content": result.get("analysis_feedback", "Hãy tập trung vào câu hỏi nhé!")
                })
                st.rerun()
            else:
                for field, value in result.items():
                    if field in st.session_state["career_data"] and value is not None:
                        print(f"Updating field {field} with value {value}")
                        st.session_state["career_data"][field] = value
                        
           
                #Cập nhật câu hỏi tiếp theo nếu còn thiếu thông tin
            

        else:
            st.error("Đã có lỗi xảy ra khi xử lý thông tin. Vui lòng thử lại sau.")
    print("Current career data: ", st.session_state["career_data"])

    st.rerun()


# 6. Khi ĐÃ GÔM ĐỦ -> Hiện nút Dự báo
if st.session_state["mode"] and not missing_fields:
    if "prediction_result" not in st.session_state:
        st.info("🎉 Tớ đã có đủ thông tin! Nhấn nút bên dưới để xem dự báo.")
        if st.button("🚀 XEM DỰ BÁO NGAY", use_container_width=True):
            with st.spinner("Đang chạy mô hình Stacking ML..."):
                res = requests.post(f"{BASE_URL}/api/predict", json=st.session_state["career_data"])
                if res.status_code == 200:
                    st.session_state["prediction_result"] = res.json()
                    st.rerun()

# 7. Hiển thị Kết quả & Biểu đồ Waterfall
if "prediction_result" in st.session_state:
    res = st.session_state["prediction_result"]
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Xác suất có việc", f"{res['probability']*100:.2f}%")
    with col2:
        st.metric("Lương dự kiến", f"${res['estimated_salary']:,}/tháng")
    
    # Biểu đồ Waterfall SHAP
    st.subheader("📊 Giải thích các yếu tố ảnh hưởng (SHAP)")
    features = res['explanations']['placement']['all_features']
    df_plot = pd.DataFrame(features)
    
    fig = go.Figure(go.Waterfall(
        name = "SHAP Impact", orientation = "v",
        measure = ["relative"] * len(df_plot),
        x = df_plot['name'],
        y = df_plot['value'],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))
    st.plotly_chart(fig, use_container_width=True)

    if st.button("🔄 Làm mới dữ liệu & Chat lại"):
        st.session_state.clear()
        st.rerun()
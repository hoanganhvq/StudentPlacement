import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="CareerAI — Dự báo sự nghiệp",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root variables ── */
:root {
    --bg-deep:     #0b0f1a;
    --bg-card:     #111827;
    --bg-card2:    #1a2235;
    --border:      rgba(99,179,237,0.15);
    --accent:      #63b3ed;
    --accent-soft: rgba(99,179,237,0.12);
    --gold:        #f6c90e;
    --green:       #48bb78;
    --red:         #fc8181;
    --text-main:   #e2e8f0;
    --text-muted:  #718096;
    --radius:      14px;
    --font-body:   'DM Sans', sans-serif;
    --font-serif:  'DM Serif Display', serif;
    --font-mono:   'JetBrains Mono', monospace;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    color: var(--text-main) !important;
}

.stApp {
    background: var(--bg-deep) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg-deep); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--text-main) !important; }

.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0 24px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}
.sidebar-logo .icon { font-size: 28px; }
.sidebar-logo .brand { font-family: var(--font-serif); font-size: 22px; line-height: 1.1; }
.sidebar-logo .brand span { color: var(--accent); }

.sidebar-section {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px;
    margin-bottom: 16px;
}
.sidebar-section h4 {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
    margin: 0 0 12px 0;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: var(--bg-deep) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: var(--radius) !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}

/* ── Hero header ── */
.hero {
    background: linear-gradient(135deg, var(--bg-card2) 0%, var(--bg-card) 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 32px 36px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,179,237,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: var(--font-serif) !important;
    font-size: 2.1rem;
    line-height: 1.15;
    margin: 0 0 8px 0;
    color: var(--text-main) !important;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    color: var(--text-muted) !important;
    font-size: 0.95rem;
    margin: 0;
}

/* ── Mode buttons ── */
.stButton > button {
    background: var(--bg-card2) !important;
    border: 1.5px solid var(--border) !important;
    color: var(--text-main) !important;
    border-radius: var(--radius) !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    padding: 14px 20px !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
.stButton > button:hover {
    background: var(--accent-soft) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(99,179,237,0.15) !important;
}

/* Primary button */
.stButton > button[kind="primary"],
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #2b6cb0, #2c5282) !important;
    border-color: var(--accent) !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 4px 0 !important;
}

/* Assistant bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown,
[data-testid="stChatMessage"][data-role="assistant"] .stMarkdown {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px 16px 16px 16px !important;
    padding: 14px 18px !important;
    margin-left: 0;
    max-width: 82%;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}

/* User bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown,
[data-testid="stChatMessage"][data-role="user"] .stMarkdown {
    background: linear-gradient(135deg, #1a365d, #1e3a5f) !important;
    border: 1px solid rgba(99,179,237,0.3) !important;
    border-radius: 16px 4px 16px 16px !important;
    padding: 14px 18px !important;
    margin-left: auto;
    max-width: 78%;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}

/* Avatar icons */
[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, var(--accent), #4299e1) !important;
    border-radius: 50% !important;
}
[data-testid="chatAvatarIcon-user"] {
    background: linear-gradient(135deg, #553c9a, #6b46c1) !important;
    border-radius: 50% !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: var(--bg-card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 4px 8px !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.1) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text-main) !important;
    font-family: var(--font-body) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 20px 24px !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-serif) !important;
    font-size: 2rem !important;
    color: var(--accent) !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border) !important;
    margin: 28px 0 !important;
}

/* ── Info / success / error boxes ── */
[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    background: var(--bg-card2) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--accent) !important; }

/* ── Data fill progress ── */
.progress-bar-wrap {
    background: var(--bg-deep);
    border-radius: 99px;
    height: 6px;
    margin-top: 6px;
    overflow: hidden;
}
.progress-bar-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), #4299e1);
    transition: width 0.4s ease;
}
.field-chip {
    display: inline-block;
    background: var(--accent-soft);
    border: 1px solid var(--border);
    color: var(--accent) !important;
    font-size: 11px;
    font-family: var(--font-mono);
    padding: 3px 9px;
    border-radius: 99px;
    margin: 3px 3px 0 0;
}
.field-chip.missing {
    background: rgba(252,129,129,0.1);
    border-color: rgba(252,129,129,0.3);
    color: var(--red) !important;
}

/* ── Mode badge ── */
.mode-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.mode-badge.chat { background: rgba(72,187,120,0.15); color: #68d391; border: 1px solid rgba(72,187,120,0.3); }
.mode-badge.cv   { background: rgba(246,201,14,0.15);  color: #f6e05e; border: 1px solid rgba(246,201,14,0.3); }
</style>
""", unsafe_allow_html=True)


# ─── STATE INIT ──────────────────────────────────────────────────────────────
if "message" not in st.session_state:
    st.session_state["message"] = [
        {"role": "assistant", "content": "Xin chào! 👋 Tôi là **CareerAI** — trợ lý tư vấn sự nghiệp thông minh.\n\nHãy chọn phương thức bên dưới để bắt đầu phân tích lộ trình của bạn nhé!"}
    ]
if "career_data" not in st.session_state:
    st.session_state["career_data"] = {
        "cgpa": None, "backlogs": None, "college_tier": None, "country": None,
        "university_ranking_band": None, "internship_count": None, "aptitude_score": None,
        "communication_score": None, "specialization": None, "industry": None,
        "internship_quality_score": None,
    }
if "mode" not in st.session_state:
    st.session_state["mode"] = None


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="icon">🤖</span>
        <div class="brand">Career<span>AI</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Data status panel
    total_fields = len(st.session_state["career_data"])
    filled_fields = sum(1 for v in st.session_state["career_data"].values() if v is not None)
    pct = int(filled_fields / total_fields * 100) if total_fields else 0

    st.markdown(f"""
    <div class="sidebar-section">
        <h4>📊 Tiến độ thu thập dữ liệu</h4>
        <div style="display:flex; justify-content:space-between; font-size:13px; margin-bottom:6px;">
            <span style="color:var(--text-muted);">{filled_fields}/{total_fields} trường</span>
            <span style="color:var(--accent); font-weight:600;">{pct}%</span>
        </div>
        <div class="progress-bar-wrap">
            <div class="progress-bar-fill" style="width:{pct}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Field chips
    chip_html = '<div class="sidebar-section"><h4>🗂️ Trạng thái trường dữ liệu</h4>'
    label_map = {
        "cgpa": "GPA", "backlogs": "Backlogs", "college_tier": "Tier",
        "country": "Quốc gia", "university_ranking_band": "Xếp hạng ĐH",
        "internship_count": "Số thực tập", "aptitude_score": "Aptitude",
        "communication_score": "Giao tiếp", "specialization": "Chuyên ngành",
        "industry": "Ngành", "internship_quality_score": "Chất lượng TT",
    }
    for k, v in st.session_state["career_data"].items():
        cls = "" if v is not None else "missing"
        icon = "✓" if v is not None else "○"
        chip_html += f'<span class="field-chip {cls}">{icon} {label_map.get(k, k)}</span>'
    chip_html += "</div>"
    st.markdown(chip_html, unsafe_allow_html=True)

    # CV upload
    if st.session_state["mode"] == "CV":
        st.markdown('<div class="sidebar-section"><h4>📄 Tải lên CV</h4>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Chọn file PDF", type=["pdf"], label_visibility="collapsed")
        if uploaded_file and st.session_state["career_data"]["cgpa"] is None:
            with st.spinner("Đang trích xuất CV..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                try:
                    response = requests.post(f"{BASE_URL}/api/chat/extract", files=files)
                    if response.status_code == 200:
                        st.session_state["career_data"].update(response.json())
                        st.success("✅ Phân tích CV thành công!")
                        st.rerun()
                    else:
                        st.error("Lỗi khi phân tích CV.")
                except Exception as e:
                    st.error(f"Không thể kết nối server: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # Reset
    st.markdown("---")
    if st.button("🔄 Làm mới & Chat lại", use_container_width=True):
        st.session_state.clear()
        st.rerun()


# ─── MAIN CONTENT ────────────────────────────────────────────────────────────
# Hero header
mode_badge = ""
if st.session_state["mode"] == "chat":
    mode_badge = '<span class="mode-badge chat">● Chế độ Chat</span>'
elif st.session_state["mode"] == "CV":
    mode_badge = '<span class="mode-badge cv">● Chế độ CV</span>'

st.markdown(f"""
<div class="hero">
    <p class="hero-title">Khám phá lộ trình<br><span>sự nghiệp của bạn</span></p>
    <p class="hero-sub">Hệ thống AI dự báo khả năng có việc & mức lương dựa trên Stacking ML + SHAP</p>
    {f'<br>{mode_badge}' if mode_badge else ''}
</div>
""", unsafe_allow_html=True)


# ─── MODE SELECTION ───────────────────────────────────────────────────────────
if st.session_state["mode"] is None:
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("### 📁 Đã có CV sẵn")
        st.markdown('<p style="color:var(--text-muted); font-size:0.9rem;">Tải file PDF lên, AI sẽ tự động đọc và phân tích thông tin của bạn.</p>', unsafe_allow_html=True)
        if st.button("📂  Dùng CV của tôi", use_container_width=True, key="btn_cv"):
            st.session_state["mode"] = "CV"
            st.session_state["message"].append({
                "role": "assistant",
                "content": "📂 Tuyệt vời! Hãy tải file **CV (PDF)** của bạn lên ở thanh bên trái nhé.\n\nSau khi phân tích xong, tôi sẽ hỏi thêm những thông tin còn thiếu."
            })
            st.rerun()
    with col2:
        st.markdown("### 💬 Muốn chat trực tiếp")
        st.markdown('<p style="color:var(--text-muted); font-size:0.9rem;">Trả lời một vài câu hỏi ngắn, AI sẽ thu thập đủ thông tin để phân tích.</p>', unsafe_allow_html=True)
        if st.button("🗨️  Bắt đầu chat", use_container_width=True, key="btn_chat"):
            st.session_state["mode"] = "chat"
            st.session_state["message"].append({
                "role": "assistant",
                "content": """👋 **Chào bạn! Rất vui được đồng hành cùng bạn giải mã lộ trình sự nghiệp.**

Để phân tích chính xác nhất, bạn hãy chia sẻ:
* 🎓 **Trường đại học** bạn đang theo học?
* 💻 **Chuyên ngành** cụ thể?
* 📈 **Điểm GPA** hiện tại (thang 4 hoặc thang 10)?

Tôi đang đợi tin từ bạn!"""
            })
            st.rerun()

    st.stop()


# ─── CHAT DISPLAY ─────────────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    for msg in st.session_state["message"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


# ─── CHAT INPUT ───────────────────────────────────────────────────────────────
missing_fields = [k for k, v in st.session_state["career_data"].items() if v is None]

if "prediction_result" not in st.session_state:
    if prompt := st.chat_input("Nhập câu trả lời hoặc câu hỏi của bạn..."):
        st.session_state["message"].append({"role": "user", "content": prompt})
        with st.spinner("Đang xử lý..."):
            payload = {
                "message": prompt,
                "current_data": st.session_state["career_data"]
            }
            try:
                response = requests.post(f"{BASE_URL}/api/handle_chat", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    for field, value in result.items():
                        if field in st.session_state["career_data"] and value is not None:
                            st.session_state["career_data"][field] = value
                    if result.get("next_question"):
                        st.session_state["message"].append({
                            "role": "assistant",
                            "content": result.get("next_question", "")
                        })
                    if result.get("is_complete"):
                        st.session_state["message"].append({
                            "role": "assistant",
                            "content": "🎉 **Cảm ơn bạn đã cung cấp đầy đủ thông tin!**\n\nNhấn nút **Xem dự báo ngay** bên dưới để tôi chạy mô hình Stacking ML và phân tích kết quả cho bạn."
                        })
                else:
                    st.error("Lỗi kết nối server. Vui lòng thử lại.")
            except Exception as e:
                st.session_state["message"].append({
                    "role": "assistant",
                    "content": f"⚠️ Không thể kết nối đến server: `{e}`"
                })
        st.rerun()


# ─── PREDICT BUTTON ───────────────────────────────────────────────────────────
if st.session_state["mode"] and not missing_fields and "prediction_result" not in st.session_state:
    st.markdown("---")
    st.info("🎉 Đã thu thập đủ thông tin! Nhấn nút bên dưới để xem dự báo sự nghiệp.")
    if st.button("🚀  XEM DỰ BÁO NGAY", use_container_width=True):
        with st.spinner("Đang chạy mô hình Stacking ML..."):
            try:
                res = requests.post(f"{BASE_URL}/api/predict", json=st.session_state["career_data"])
                if res.status_code == 200:
                    st.session_state["prediction_result"] = res.json()
                    st.rerun()
                else:
                    st.error("Lỗi khi chạy mô hình dự báo.")
            except Exception as e:
                st.error(f"Không thể kết nối server: {e}")


# ─── RESULTS ─────────────────────────────────────────────────────────────────
if "prediction_result" in st.session_state:
    res = st.session_state["prediction_result"]
    st.markdown("---")

    # Metrics
    col1, col2, col3 = st.columns(3)
    prob = res.get("probability", 0)
    salary = res.get("estimated_salary", 0)
    verdict = "Cao" if prob >= 0.7 else ("Trung bình" if prob >= 0.4 else "Thấp")
    with col1:
        st.metric("🎯 Xác suất có việc", f"{prob*100:.1f}%")
    with col2:
        st.metric("💰 Lương dự kiến", f"${salary:,}/tháng")
    with col3:
        st.metric("📊 Mức đánh giá", verdict)

    # SHAP Waterfall chart
    st.markdown("### 🔍 Phân tích yếu tố ảnh hưởng (SHAP)")

    target_features = [
        "cgpa", "backlogs", "college_tier", "country",
        "university_ranking_band", "internship_count", "aptitude_score",
        "communication_score", "specialization", "industry", "internship_quality_score"
    ]
    label_map_chart = {
        "cgpa": "GPA", "backlogs": "Backlogs", "college_tier": "Tier trường",
        "country": "Quốc gia", "university_ranking_band": "Xếp hạng ĐH",
        "internship_count": "Số lần TT", "aptitude_score": "Aptitude",
        "communication_score": "Giao tiếp", "specialization": "Chuyên ngành",
        "industry": "Ngành nghề", "internship_quality_score": "Chất lượng TT",
    }

    features = res.get("explanations", {}).get("placement", {}).get("all_features", [])
    if features:
        df_all = pd.DataFrame(features)
        df_plot = df_all[df_all["name"].isin(target_features)].copy()
        df_plot["abs_value"] = df_plot["value"].abs()
        df_plot = df_plot.sort_values("abs_value", ascending=True)
        df_plot["label"] = df_plot["name"].map(label_map_chart).fillna(df_plot["name"])

        colors = ["#48bb78" if v >= 0 else "#fc8181" for v in df_plot["value"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_plot["value"],
            y=df_plot["label"],
            orientation="h",
            marker=dict(
                color=colors,
                line=dict(color="rgba(255,255,255,0.08)", width=1)
            ),
            text=[f"{v:+.3f}" for v in df_plot["value"]],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=11, color="#a0aec0"),
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#a0aec0"),
            height=420,
            margin=dict(l=20, r=80, t=20, b=20),
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(99,179,237,0.08)",
                zeroline=True,
                zerolinecolor="rgba(99,179,237,0.3)",
                zerolinewidth=1.5,
                tickfont=dict(family="JetBrains Mono", size=10),
            ),
            yaxis=dict(
                showgrid=False,
                tickfont=dict(size=12),
            ),
            bargap=0.35,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Legend
        st.markdown("""
        <div style="display:flex; gap:20px; font-size:12px; color:var(--text-muted); margin-top:-8px; padding-left:4px;">
            <span><span style="color:#48bb78;">■</span> Tác động tích cực (tăng xác suất)</span>
            <span><span style="color:#fc8181;">■</span> Tác động tiêu cực (giảm xác suất)</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Không có dữ liệu SHAP để hiển thị.")
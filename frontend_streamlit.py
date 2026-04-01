import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

BASE_URL = "http://localhost:8000"

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Career Advisor AI",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,300;12..96,400;12..96,500;12..96,600;12..96,700&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"] {
    background: #080810 !important;
    font-family: 'Bricolage Grotesque', sans-serif !important;
    color: #c8c8e0 !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: -20vh; left: 50%; transform: translateX(-50%);
    width: 900px; height: 500px;
    background: radial-gradient(ellipse at 30% 50%, rgba(91,77,224,0.1) 0%, transparent 60%),
                radial-gradient(ellipse at 70% 50%, rgba(56,189,248,0.06) 0%, transparent 60%);
    pointer-events: none; z-index: 0;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
.stDeployButton { display: none !important; }

[data-testid="stAppViewContainer"] > .main > .block-container {
    max-width: 760px !important;
    padding: 2rem 1.75rem 7rem !important;
    margin: 0 auto;
    position: relative; z-index: 1;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0c0c18 !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem !important; }
[data-testid="stSidebarNav"] { display: none !important; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 2px 0 !important;
    gap: 12px !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown p,
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown li {
    color: #cccce8 !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) .stMarkdown {
    background: rgba(255,255,255,0.035) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 2px 18px 18px 18px !important;
    padding: 13px 17px !important;
    font-size: 14px !important;
    line-height: 1.75 !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.06) !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown p {
    color: #fff !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown {
    background: linear-gradient(135deg, #5b4de0 0%, #7c6af5 50%, #9d8fff 100%) !important;
    border-radius: 18px 2px 18px 18px !important;
    padding: 13px 17px !important;
    font-size: 14px !important;
    line-height: 1.75 !important;
    border: none !important;
    box-shadow: 0 6px 28px rgba(91,77,224,0.45), inset 0 1px 0 rgba(255,255,255,0.15) !important;
}
[data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #5b4de0, #38bdf8) !important;
    border-radius: 10px !important;
    box-shadow: 0 0 0 1px rgba(91,77,224,0.4), 0 4px 12px rgba(91,77,224,0.3) !important;
    border: none !important;
}
[data-testid="chatAvatarIcon-user"] {
    background: #1a1a2e !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* ── Chat input ── */
[data-testid="stChatInputContainer"] {
    background: rgba(8,8,16,0.95) !important;
    backdrop-filter: blur(20px) !important;
    border-top: 1px solid rgba(255,255,255,0.06) !important;
    padding: 14px 20px 16px !important;
    position: fixed !important; bottom: 0 !important;
    left: 50% !important; transform: translateX(-50%) !important;
    width: 100% !important; max-width: 760px !important;
    z-index: 999 !important;
}
[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 14px !important;
    color: #e8e8f8 !important;
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 14px !important;
    caret-color: #7c6af5 !important;
    transition: border-color .2s, box-shadow .2s !important;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: rgba(124,106,245,0.5) !important;
    box-shadow: 0 0 0 3px rgba(91,77,224,0.12) !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #44445a !important; }
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #5b4de0, #7c6af5) !important;
    border-radius: 11px !important; border: none !important;
    box-shadow: 0 4px 14px rgba(91,77,224,0.5) !important;
    transition: box-shadow .2s, transform .15s !important;
}
[data-testid="stChatInput"] button:hover {
    box-shadow: 0 6px 20px rgba(91,77,224,0.65) !important;
    transform: scale(1.04) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important;
    color: #c8c8e0 !important;
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 13.5px !important; font-weight: 500 !important;
    padding: 10px 22px !important; letter-spacing: 0.01em !important;
    transition: all .25s cubic-bezier(.4,0,.2,1) !important;
}
.stButton > button:hover {
    border-color: rgba(124,106,245,0.4) !important;
    color: #e8e4ff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3), 0 0 0 1px rgba(91,77,224,0.15) !important;
    background: rgba(91,77,224,0.1) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] section {
    background: rgba(255,255,255,0.02) !important;
    border: 1.5px dashed rgba(124,106,245,0.22) !important;
    border-radius: 16px !important;
    transition: border-color .2s, background .2s !important;
}
[data-testid="stFileUploader"] section:hover {
    background: rgba(91,77,224,0.05) !important;
    border-color: rgba(124,106,245,0.42) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] div span {
    color: #444460 !important; font-size: 13px !important;
}
[data-testid="stFileUploader"] label { display: none !important; }

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.025) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 16px !important;
    padding: 20px 22px !important;
    position: relative !important; overflow: hidden !important;
    transition: border-color .2s !important;
}
[data-testid="stMetric"]:hover { border-color: rgba(124,106,245,0.3) !important; }
[data-testid="stMetric"]::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(circle at top left, rgba(91,77,224,0.07), transparent 70%);
    pointer-events: none;
}
[data-testid="stMetricLabel"] p {
    color: #555570 !important; font-size: 11.5px !important;
    text-transform: uppercase !important; letter-spacing: .08em !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    font-size: 32px !important; font-weight: 700 !important;
    background: linear-gradient(135deg, #a59bff, #e8e4ff) !important;
    -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
    font-family: 'Bricolage Grotesque', sans-serif !important;
}

/* ── Progress ── */
[data-testid="stProgressBar"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 99px !important; height: 4px !important;
}
[data-testid="stProgressBar"] > div {
    background: linear-gradient(90deg, #5b4de0, #38bdf8) !important;
    border-radius: 99px !important;
    box-shadow: 0 0 8px rgba(91,77,224,0.5) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
}
[data-testid="stExpander"] summary {
    color: #666688 !important; font-size: 13px !important;
    font-family: 'Bricolage Grotesque', sans-serif !important;
    padding: 14px 18px !important;
}
[data-testid="stExpander"] summary:hover { color: #b0b0d0 !important; }

/* ── Alerts ── */
[data-testid="stAlert"] {
    background: rgba(91,77,224,0.08) !important;
    border: 1px solid rgba(91,77,224,0.2) !important;
    border-radius: 12px !important;
    color: #b8b0ff !important; font-size: 13px !important;
}

/* ── Typography ── */
p, li { color: #9898b8 !important; font-size: 14px !important; line-height: 1.75 !important; }
strong, b { color: #c8c0ff !important; font-weight: 600 !important; }
h1 { font-size: 28px !important; font-weight: 700 !important; color: #eeeeff !important;
     letter-spacing: -.02em !important; }
h2 { font-size: 20px !important; font-weight: 600 !important; color: #d8d8f0 !important; }
h3 { font-size: 16px !important; font-weight: 600 !important; color: #c8c8e8 !important; }
hr { border-color: rgba(255,255,255,0.05) !important; margin: 2rem 0 !important; }
code, pre { font-family: 'DM Mono', monospace !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(124,106,245,0.22); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(124,106,245,0.4); }

[data-testid="stHorizontalBlock"] { gap: 14px !important; }
[data-testid="stSpinner"] svg { color: #7c6af5 !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
def _init():
    defaults = {
        "messages": [],
        "career_data": {
            "cgpa": None, "backlogs": None, "college_tier": None, "country": None,
            "university_ranking_band": None, "internship_count": None,
            "aptitude_score": None, "communication_score": None,
            "specialization": None, "industry": None, "internship_quality_score": None,
        },
        "mode": None,
        "prediction_result": None,
        "cv_processed": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
_init()

FIELD_META = {
    "cgpa":                    ("GPA",             "📈"),
    "backlogs":                ("Môn nợ",          "📋"),
    "college_tier":            ("Hạng trường",     "🏛"),
    "country":                 ("Quốc gia",        "🌏"),
    "university_ranking_band": ("Xếp hạng ĐH",    "🏆"),
    "internship_count":        ("Số thực tập",     "💼"),
    "aptitude_score":          ("Điểm tư duy",     "🧠"),
    "communication_score":     ("Giao tiếp",       "🗣"),
    "specialization":          ("Chuyên ngành",    "🎓"),
    "industry":                ("Ngành nghề",      "🏭"),
    "internship_quality_score":("Chất lượng TT",  "⭐"),
}

def missing_fields():
    return [k for k, v in st.session_state.career_data.items() if v is None]

def filled_count():
    return sum(1 for v in st.session_state.career_data.values() if v is not None)

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})


# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;padding:0 4px 20px;
                border-bottom:1px solid rgba(255,255,255,0.05);margin-bottom:20px;">
        <div style="width:34px;height:34px;border-radius:10px;flex-shrink:0;
                    background:linear-gradient(135deg,#5b4de0,#38bdf8);
                    display:flex;align-items:center;justify-content:center;
                    font-size:16px;box-shadow:0 0 0 1px rgba(91,77,224,0.35),
                    0 4px 12px rgba(91,77,224,0.28);">✦</div>
        <div>
            <div style="font-size:13px;font-weight:700;color:#e8e8f8;
                        font-family:'Bricolage Grotesque',sans-serif;line-height:1.1;">
                Career Advisor
            </div>
            <div style="font-size:10px;color:#5b4de0;font-family:'DM Mono',monospace;
                        letter-spacing:.04em;margin-top:1px;">AI · v2.0</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    count = filled_count()
    pct = count / 11
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <span style="font-size:10.5px;font-weight:600;color:#444460;text-transform:uppercase;
                     letter-spacing:.08em;font-family:'Bricolage Grotesque',sans-serif;">
            Hồ sơ
        </span>
        <span style="font-size:11px;color:{'#a59bff' if pct > 0 else '#333350'};
                     font-family:'DM Mono',monospace;font-weight:500;">
            {count}/11
        </span>
    </div>
    """, unsafe_allow_html=True)
    st.progress(pct)
    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    for field, (label, icon) in FIELD_META.items():
        val = st.session_state.career_data[field]
        if val is not None:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:7px 10px;
                        background:rgba(91,77,224,0.08);
                        border:1px solid rgba(91,77,224,0.16);
                        border-radius:10px;margin-bottom:5px;">
                <span style="font-size:12px;width:18px;text-align:center;">{icon}</span>
                <span style="font-size:12px;color:#7777a0;flex:1;
                             font-family:'Bricolage Grotesque',sans-serif;">{label}</span>
                <span style="font-size:11.5px;font-weight:600;color:#a59bff;
                             font-family:'DM Mono',monospace;">{val}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding:7px 10px;
                        background:rgba(255,255,255,0.012);
                        border:1px solid rgba(255,255,255,0.04);
                        border-radius:10px;margin-bottom:5px;">
                <span style="font-size:12px;width:18px;text-align:center;opacity:.2;">{icon}</span>
                <span style="font-size:12px;color:#2e2e48;flex:1;
                             font-family:'Bricolage Grotesque',sans-serif;">{label}</span>
                <span style="font-size:10px;color:#252538;font-family:'DM Mono',monospace;">—</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    if st.button("↺  Bắt đầu lại", key="reset_btn", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    st.markdown("""
    <div style="margin-top:24px;padding:10px 12px;
                background:rgba(255,255,255,0.015);
                border:1px solid rgba(255,255,255,0.04);
                border-radius:10px;text-align:center;">
        <div style="font-size:9.5px;color:#252538;font-family:'DM Mono',monospace;
                    letter-spacing:.06em;text-transform:uppercase;">
            Powered by Stacking ML
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# WELCOME SCREEN
# ══════════════════════════════════════════════════════════
if st.session_state.mode is None:
    st.markdown("""
    <div style="text-align:center;padding:52px 0 44px;">
        <div style="display:inline-flex;align-items:center;justify-content:center;
                    width:68px;height:68px;border-radius:20px;
                    background:linear-gradient(135deg,#5b4de0 0%,#38bdf8 100%);
                    font-size:26px;margin-bottom:22px;
                    box-shadow:0 0 0 1px rgba(91,77,224,0.3),
                               0 0 48px rgba(91,77,224,0.2),
                               0 16px 40px rgba(0,0,0,0.5);">✦</div>

        <div style="font-size:10.5px;font-weight:600;color:#5b4de0;text-transform:uppercase;
                    letter-spacing:.16em;margin-bottom:14px;font-family:'DM Mono',monospace;">
            Career Intelligence Platform
        </div>

        <div style="font-size:30px;font-weight:700;color:#eeeeff;
                    letter-spacing:-.025em;margin:0 0 12px;line-height:1.2;
                    font-family:'Bricolage Grotesque',sans-serif;">
            Dự báo sự nghiệp<br>
            <span style="background:linear-gradient(90deg,#a59bff 0%,#38bdf8 100%);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                bằng AI
            </span>
        </div>

        <p style="font-size:13.5px;color:#444460;max-width:380px;margin:0 auto 44px;
                  line-height:1.75;font-family:'Bricolage Grotesque',sans-serif;">
            Phân tích hồ sơ sinh viên, dự báo xác suất có việc<br>
            và mức lương dựa trên mô hình Stacking ML
        </p>

        <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap;">
            <div style="background:rgba(255,255,255,0.025);
                        border:1px solid rgba(255,255,255,0.07);
                        border-radius:20px;padding:26px 30px;width:210px;text-align:left;
                        box-shadow:0 8px 32px rgba(0,0,0,0.3),inset 0 1px 0 rgba(255,255,255,0.05);">
                <div style="font-size:28px;margin-bottom:14px;">💬</div>
                <div style="font-size:14px;font-weight:600;color:#e0e0f8;margin-bottom:6px;
                            font-family:'Bricolage Grotesque',sans-serif;">Chat tư vấn</div>
                <div style="font-size:12px;color:#3a3a58;line-height:1.65;
                            font-family:'Bricolage Grotesque',sans-serif;">
                    AI hỏi từng bước,<br>bạn chỉ cần trả lời
                </div>
            </div>
            <div style="background:rgba(255,255,255,0.025);
                        border:1px solid rgba(255,255,255,0.07);
                        border-radius:20px;padding:26px 30px;width:210px;text-align:left;
                        box-shadow:0 8px 32px rgba(0,0,0,0.3),inset 0 1px 0 rgba(255,255,255,0.05);">
                <div style="font-size:28px;margin-bottom:14px;">📄</div>
                <div style="font-size:14px;font-weight:600;color:#e0e0f8;margin-bottom:6px;
                            font-family:'Bricolage Grotesque',sans-serif;">Upload CV</div>
                <div style="font-size:12px;color:#3a3a58;line-height:1.65;
                            font-family:'Bricolage Grotesque',sans-serif;">
                    Tải PDF lên, AI tự<br>trích xuất thông tin
                </div>
            </div>
        </div>
    </div>
    <div style="height:8px"></div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💬  Bắt đầu chat", key="btn_chat", use_container_width=True):
            st.session_state.mode = "chat"
            add_message("assistant",
                "👋 **Xin chào!** Rất vui được đồng hành cùng bạn.\n\n"
                "Để phân tích chính xác nhất, hãy chia sẻ:\n\n"
                "- 🎓 **Trường đại học** bạn đang theo học?\n"
                "- 💡 **Chuyên ngành** cụ thể?\n"
                "- 📊 **GPA** hiện tại (thang 4 hay 10 đều được)?"
            )
            st.rerun()
    with col2:
        if st.button("📄  Upload CV PDF", key="btn_cv", use_container_width=True):
            st.session_state.mode = "CV"
            add_message("assistant",
                "📎 **Tuyệt!** Hãy tải file CV (định dạng PDF) lên bên dưới.\n\n"
                "Tôi sẽ tự động đọc và trích xuất toàn bộ thông tin cần thiết."
            )
            st.rerun()
    st.stop()


# ══════════════════════════════════════════════════════════
# MODE BADGE
# ══════════════════════════════════════════════════════════
mode_label = "💬 Chế độ Chat" if st.session_state.mode == "chat" else "📄 Chế độ CV"
missing = missing_fields()
dot_color = "#22c55e" if not missing else "#5b4de0"
status_text = "✓ Đủ thông tin" if not missing else f"{len(missing)} trường còn trống"

st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:10px 16px;background:rgba(255,255,255,0.02);
            border:1px solid rgba(255,255,255,0.055);border-radius:12px;
            margin-bottom:22px;">
    <div style="display:flex;align-items:center;gap:8px;">
        <span style="font-size:12px;color:#555570;
                     font-family:'Bricolage Grotesque',sans-serif;">{mode_label}</span>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
        <span style="width:6px;height:6px;border-radius:50%;
                     background:{dot_color};display:inline-block;
                     box-shadow:0 0 6px {dot_color};"></span>
        <span style="font-size:11px;font-family:'DM Mono',monospace;color:{dot_color};">
            {status_text}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# CV UPLOAD
# ══════════════════════════════════════════════════════════
if st.session_state.mode == "CV" and not st.session_state.cv_processed:
    st.markdown("""
    <div style="margin-bottom:8px;">
        <span style="font-size:11px;font-weight:600;color:#444460;text-transform:uppercase;
                     letter-spacing:.09em;font-family:'Bricolage Grotesque',sans-serif;">
            Tải CV lên
        </span>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("cv_upload", type=["pdf"], label_visibility="collapsed")
    if uploaded_file:
        with st.spinner("Đang phân tích CV..."):
            try:
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                response = requests.post(f"{BASE_URL}/api/chat/extract", files=files)
                if response.status_code == 200:
                    st.session_state.career_data.update(response.json())
                    st.session_state.cv_processed = True
                    n = filled_count()
                    rem = 11 - n
                    add_message("assistant",
                        f"✅ **CV đã được phân tích!** Trích xuất **{n}/11** thông tin.\n\n"
                        + (f"Còn **{rem} trường** cần bổ sung — nhập tiếp vào chat nhé."
                           if rem > 0 else "🎉 Đã đủ dữ liệu! Nhấn nút dự báo bên dưới.")
                    )
                    st.rerun()
                else:
                    st.error("Lỗi khi đọc CV. Vui lòng thử lại.")
            except Exception as e:
                st.error(f"Không kết nối được server: {e}")
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# CHAT HISTORY
# ══════════════════════════════════════════════════════════
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ══════════════════════════════════════════════════════════
# PREDICT CTA
# ══════════════════════════════════════════════════════════
if st.session_state.mode and not missing_fields() and st.session_state.prediction_result is None:
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(91,77,224,0.1) 0%,rgba(56,189,248,0.05) 100%);
                border:1px solid rgba(91,77,224,0.2);border-radius:18px;
                padding:20px 22px;margin:20px 0;
                box-shadow:inset 0 1px 0 rgba(255,255,255,0.05),0 8px 32px rgba(0,0,0,0.25);">
        <div style="display:flex;align-items:center;gap:14px;">
            <div style="width:44px;height:44px;border-radius:13px;flex-shrink:0;
                        background:linear-gradient(135deg,#5b4de0,#38bdf8);
                        display:flex;align-items:center;justify-content:center;
                        font-size:20px;box-shadow:0 4px 16px rgba(91,77,224,0.45);">🎯</div>
            <div>
                <div style="font-size:14px;font-weight:600;color:#e8e8f8;
                            font-family:'Bricolage Grotesque',sans-serif;margin-bottom:3px;">
                    Đã sẵn sàng phân tích!
                </div>
                <div style="font-size:12px;color:#444460;font-family:'Bricolage Grotesque',sans-serif;">
                    11/11 thông tin đã được thu thập đầy đủ
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("⚡  Chạy mô hình & Xem dự báo", key="predict_btn", use_container_width=True):
        with st.spinner("Đang chạy Stacking ML model..."):
            try:
                res = requests.post(f"{BASE_URL}/api/predict", json=st.session_state.career_data)
                if res.status_code == 200:
                    st.session_state.prediction_result = res.json()
                    add_message("assistant", "✅ **Mô hình hoàn tất!** Kết quả hiển thị bên dưới.")
                    st.rerun()
                else:
                    st.error("Lỗi từ server dự báo.")
            except Exception as e:
                st.error(f"Không thể kết nối: {e}")


# ══════════════════════════════════════════════════════════
# PREDICTION RESULTS
# ══════════════════════════════════════════════════════════
if st.session_state.prediction_result:
    res = st.session_state.prediction_result
    prob = res.get("probability", 0)
    salary = res.get("estimated_salary", 0)

    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin:28px 0 18px;">
        <div style="flex:1;height:1px;background:rgba(255,255,255,0.05);"></div>
        <span style="font-size:10px;font-weight:600;color:#2a2a42;text-transform:uppercase;
                     letter-spacing:.14em;font-family:'DM Mono',monospace;">Kết quả dự báo</span>
        <div style="flex:1;height:1px;background:rgba(255,255,255,0.05);"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🎯 Xác suất có việc", f"{prob * 100:.1f}%")
    with col2:
        st.metric("💰 Lương dự kiến", f"${salary:,.0f} /tháng")

    # SHAP Chart
    TARGET = [
        "cgpa","backlogs","college_tier","country","university_ranking_band",
        "internship_count","aptitude_score","communication_score",
        "specialization","industry","internship_quality_score"
    ]
    LABEL = {k: v[0] for k, v in FIELD_META.items()}

    features = res.get("explanations", {}).get("placement", {}).get("all_features", [])
    if features:
        df = pd.DataFrame(features)
        df = df[df["name"].isin(TARGET)].copy()
        df["abs"] = df["value"].abs()
        df = df.sort_values("abs", ascending=False)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[LABEL.get(n, n) for n in df["name"]],
            y=df["value"],
            marker=dict(
                color=["#7c6af5" if v >= 0 else "#f87171" for v in df["value"]],
                opacity=0.85,
                line=dict(width=0),
            ),
            text=[f"{v:+.2f}" for v in df["value"]],
            textposition="outside",
            textfont=dict(family="DM Mono", size=10, color="#444460"),
        ))

        fig.update_layout(
            title=dict(
                text="Mức độ ảnh hưởng của từng yếu tố (SHAP values)",
                font=dict(family="Bricolage Grotesque", size=12.5, color="#555570"),
                x=0, pad=dict(b=12)
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Bricolage Grotesque", color="#555570", size=11),
            height=320,
            showlegend=False,
            margin=dict(t=48, b=12, l=0, r=0),
            xaxis=dict(
                gridcolor="rgba(255,255,255,0.03)",
                tickfont=dict(size=10.5, color="#444460"),
                showline=False, zeroline=False,
            ),
            yaxis=dict(
                gridcolor="rgba(255,255,255,0.03)",
                tickfont=dict(size=9.5, color="#333350", family="DM Mono"),
                showline=False,
                zeroline=True, zerolinecolor="rgba(255,255,255,0.07)", zerolinewidth=1,
            ),
            bargap=0.38,
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Advice cards
    with st.expander("💡  Gợi ý cải thiện hồ sơ"):
        cd = st.session_state.career_data
        items = []
        if cd.get("cgpa") and float(cd["cgpa"]) < 3.0:
            items.append(("📚", "Cải thiện GPA",
                "GPA hiện còn thấp. Hãy tập trung vào các môn còn lại để nâng điểm tích lũy."))
        if cd.get("backlogs") and int(cd["backlogs"]) > 0:
            items.append(("⚠️", "Xử lý môn nợ",
                "Hoàn thành các môn nợ trước khi apply — nhiều nhà tuyển dụng yêu cầu tốt nghiệp đúng hạn."))
        if cd.get("internship_count") and int(cd["internship_count"]) < 2:
            items.append(("🏢", "Tăng kinh nghiệm thực tập",
                "Mục tiêu ít nhất 2–3 kỳ thực tập ở các công ty liên quan đến ngành bạn theo học."))
        if cd.get("communication_score") and float(cd["communication_score"]) < 7:
            items.append(("🗣", "Rèn kỹ năng giao tiếp",
                "Tham gia câu lạc bộ, thuyết trình hoặc khóa học soft skills để cải thiện điểm này."))
        if not items:
            items.append(("🌟", "Hồ sơ rất tốt!",
                "Bạn đang ở vị thế rất tốt. Hãy polish CV và chuẩn bị kỹ cho vòng phỏng vấn."))

        for icon, title, desc in items:
            st.markdown(f"""
            <div style="display:flex;gap:14px;padding:14px 16px;
                        background:rgba(255,255,255,0.018);
                        border:1px solid rgba(255,255,255,0.05);
                        border-radius:12px;margin-bottom:8px;
                        transition:border-color .2s;">
                <div style="font-size:18px;flex-shrink:0;padding-top:1px;">{icon}</div>
                <div>
                    <div style="font-size:13px;font-weight:600;color:#c0b8ff;
                                margin-bottom:4px;font-family:'Bricolage Grotesque',sans-serif;">
                        {title}
                    </div>
                    <div style="font-size:12px;color:#444460;line-height:1.65;
                                font-family:'Bricolage Grotesque',sans-serif;">
                        {desc}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
# CHAT INPUT
# ══════════════════════════════════════════════════════════
placeholder = (
    "Nhập câu trả lời của bạn..."
    if st.session_state.mode == "chat"
    else "Hỏi thêm hoặc bổ sung thông tin..."
)

if prompt := st.chat_input(placeholder):
    add_message("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner(""):
        payload = {"message": prompt, "current_data": st.session_state.career_data}
        try:
            response = requests.post(f"{BASE_URL}/api/handle_chat", json=payload)
            if response.status_code == 200:
                result = response.json()
                for field, value in result.items():
                    if field in st.session_state.career_data and value is not None:
                        st.session_state.career_data[field] = value

                reply = result.get("next_question", "")
                if result.get("is_complete"):
                    suffix = "\n\n🎉 **Đã đủ thông tin!** Cuộn xuống và nhấn **⚡ Xem dự báo** nhé."
                    reply = reply + suffix if reply else suffix.strip()

                if reply:
                    add_message("assistant", reply)
                    with st.chat_message("assistant"):
                        st.markdown(reply)
            else:
                err = "❌ Đã có lỗi. Vui lòng thử lại."
                add_message("assistant", err)
                with st.chat_message("assistant"):
                    st.markdown(err)
        except Exception as e:
            err = f"❌ Không thể kết nối server: `{e}`"
            add_message("assistant", err)
            with st.chat_message("assistant"):
                st.markdown(err)
    st.rerun()
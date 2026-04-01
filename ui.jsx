import { useState, useRef, useEffect } from "react";

const BASE_URL = "http://localhost:8000";

const INITIAL_MESSAGES = [
  {
    role: "assistant",
    content: "Chào bạn! Tôi là **trợ lý tư vấn sự nghiệp AI**. Tôi sẽ giúp bạn dự báo cơ hội việc làm và mức lương dựa trên hồ sơ của bạn.\n\nBạn muốn bắt đầu bằng cách nào?",
    type: "welcome",
  },
];

const FIELDS_LABEL = {
  cgpa: "GPA",
  backlogs: "Số môn nợ",
  college_tier: "Hạng trường",
  country: "Quốc gia",
  university_ranking_band: "Xếp hạng ĐH",
  internship_count: "Số thực tập",
  aptitude_score: "Điểm tư duy",
  communication_score: "Điểm giao tiếp",
  specialization: "Chuyên ngành",
  industry: "Ngành nghề",
  internship_quality_score: "Chất lượng thực tập",
};

function Avatar({ role }) {
  if (role === "assistant") {
    return (
      <div style={{
        width: 32, height: 32, borderRadius: "50%",
        background: "linear-gradient(135deg, #6C63FF, #3ECFCF)",
        display: "flex", alignItems: "center", justifyContent: "center",
        flexShrink: 0, fontSize: 14, fontWeight: 700, color: "#fff",
        boxShadow: "0 2px 8px rgba(108,99,255,0.4)"
      }}>AI</div>
    );
  }
  return (
    <div style={{
      width: 32, height: 32, borderRadius: "50%",
      background: "#2d2d3a", border: "1.5px solid #3d3d50",
      display: "flex", alignItems: "center", justifyContent: "center",
      flexShrink: 0, fontSize: 13, color: "#aaa"
    }}>U</div>
  );
}

function MessageBubble({ msg }) {
  const isAI = msg.role === "assistant";

  const renderContent = (text) => {
    if (!text) return null;
    return text.split(/\*\*(.*?)\*\*/g).map((part, i) =>
      i % 2 === 1
        ? <strong key={i} style={{ color: isAI ? "#a78bfa" : "#fff" }}>{part}</strong>
        : part
    );
  };

  return (
    <div style={{
      display: "flex", gap: 10,
      flexDirection: isAI ? "row" : "row-reverse",
      marginBottom: 16, alignItems: "flex-start"
    }}>
      <Avatar role={msg.role} />
      <div style={{
        maxWidth: "72%",
        background: isAI
          ? "rgba(255,255,255,0.04)"
          : "linear-gradient(135deg, #6C63FF, #8B83FF)",
        borderRadius: isAI ? "4px 16px 16px 16px" : "16px 4px 16px 16px",
        padding: "10px 14px",
        fontSize: 14, lineHeight: 1.65,
        color: isAI ? "#d4d4e8" : "#fff",
        border: isAI ? "1px solid rgba(255,255,255,0.07)" : "none",
        boxShadow: isAI ? "none" : "0 4px 16px rgba(108,99,255,0.3)",
      }}>
        {renderContent(msg.content)}
      </div>
    </div>
  );
}

function TypingIndicator() {
  return (
    <div style={{ display: "flex", gap: 10, alignItems: "flex-start", marginBottom: 16 }}>
      <Avatar role="assistant" />
      <div style={{
        background: "rgba(255,255,255,0.04)", borderRadius: "4px 16px 16px 16px",
        padding: "12px 16px", border: "1px solid rgba(255,255,255,0.07)",
        display: "flex", gap: 5, alignItems: "center"
      }}>
        {[0, 1, 2].map(i => (
          <span key={i} style={{
            width: 7, height: 7, borderRadius: "50%",
            background: "#6C63FF", opacity: 0.7,
            animation: `bounce 1.2s ease-in-out ${i * 0.2}s infinite`,
          }} />
        ))}
      </div>
    </div>
  );
}

function DataCard({ data }) {
  const filled = Object.entries(data).filter(([, v]) => v !== null);
  if (filled.length === 0) return null;
  return (
    <div style={{
      background: "rgba(255,255,255,0.03)", borderRadius: 12,
      border: "1px solid rgba(255,255,255,0.08)", padding: "12px 14px",
      marginBottom: 12
    }}>
      <p style={{ fontSize: 11, color: "#7c7c9e", margin: "0 0 8px", letterSpacing: "0.08em", textTransform: "uppercase" }}>
        Dữ liệu đã thu thập
      </p>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px 12px" }}>
        {filled.map(([k, v]) => (
          <div key={k} style={{ display: "flex", gap: 6, alignItems: "baseline" }}>
            <span style={{ fontSize: 11, color: "#7c7c9e", flexShrink: 0 }}>{FIELDS_LABEL[k] || k}:</span>
            <span style={{ fontSize: 12, color: "#a78bfa", fontWeight: 500, truncate: true }}>{String(v)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function PredictionResult({ result }) {
  if (!result) return null;
  const pct = (result.probability * 100).toFixed(1);
  const salary = result.estimated_salary?.toLocaleString() || "N/A";
  const features = result.explanations?.placement?.all_features || [];

  const TARGET = ["cgpa","backlogs","college_tier","country","university_ranking_band","internship_count","aptitude_score","communication_score","specialization","industry","internship_quality_score"];
  const filtered = features.filter(f => TARGET.includes(f.name)).sort((a, b) => Math.abs(b.value) - Math.abs(a.value)).slice(0, 8);
  const maxAbs = Math.max(...filtered.map(f => Math.abs(f.value)), 0.01);

  return (
    <div style={{
      background: "rgba(108,99,255,0.08)", borderRadius: 16,
      border: "1px solid rgba(108,99,255,0.2)", padding: "16px",
      marginTop: 8
    }}>
      <p style={{ fontSize: 12, color: "#7c7c9e", margin: "0 0 12px", textTransform: "uppercase", letterSpacing: "0.08em" }}>Kết quả dự báo</p>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 16 }}>
        <div style={{ background: "rgba(108,99,255,0.12)", borderRadius: 10, padding: "12px 14px", textAlign: "center" }}>
          <p style={{ fontSize: 11, color: "#9d9db8", margin: "0 0 4px" }}>Xác suất có việc</p>
          <p style={{ fontSize: 28, fontWeight: 700, color: "#a78bfa", margin: 0 }}>{pct}%</p>
        </div>
        <div style={{ background: "rgba(62,207,207,0.1)", borderRadius: 10, padding: "12px 14px", textAlign: "center" }}>
          <p style={{ fontSize: 11, color: "#9d9db8", margin: "0 0 4px" }}>Lương dự kiến</p>
          <p style={{ fontSize: 22, fontWeight: 700, color: "#3ECFCF", margin: 0 }}>${salary}</p>
          <p style={{ fontSize: 10, color: "#7c7c9e", margin: "2px 0 0" }}>/tháng</p>
        </div>
      </div>
      {filtered.length > 0 && (
        <>
          <p style={{ fontSize: 11, color: "#7c7c9e", margin: "0 0 8px", textTransform: "uppercase", letterSpacing: "0.08em" }}>Yếu tố ảnh hưởng (SHAP)</p>
          {filtered.map(f => {
            const w = Math.abs(f.value) / maxAbs * 100;
            const pos = f.value >= 0;
            return (
              <div key={f.name} style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
                <span style={{ fontSize: 11, color: "#9d9db8", width: 110, flexShrink: 0, textAlign: "right" }}>{FIELDS_LABEL[f.name] || f.name}</span>
                <div style={{ flex: 1, background: "rgba(255,255,255,0.06)", borderRadius: 4, height: 8, overflow: "hidden" }}>
                  <div style={{
                    height: "100%", borderRadius: 4,
                    width: `${w}%`,
                    background: pos ? "#6C63FF" : "#e74c3c",
                    marginLeft: pos ? 0 : "auto"
                  }} />
                </div>
                <span style={{ fontSize: 11, color: pos ? "#a78bfa" : "#e87070", width: 44, textAlign: "right" }}>
                  {f.value > 0 ? "+" : ""}{f.value.toFixed(2)}
                </span>
              </div>
            );
          })}
        </>
      )}
    </div>
  );
}

export default function App() {
  const [messages, setMessages] = useState(INITIAL_MESSAGES);
  const [careerData, setCareerData] = useState({
    cgpa: null, backlogs: null, college_tier: null, country: null,
    university_ranking_band: null, internship_count: null, aptitude_score: null,
    communication_score: null, specialization: null, industry: null, internship_quality_score: null,
  });
  const [mode, setMode] = useState(null);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [predicting, setPredicting] = useState(false);
  const [predResult, setPredResult] = useState(null);
  const [showData, setShowData] = useState(false);
  const bottomRef = useRef(null);
  const fileRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const missingFields = Object.entries(careerData).filter(([, v]) => v === null);
  const isComplete = missingFields.length === 0;

  const addMsg = (role, content) =>
    setMessages(prev => [...prev, { role, content }]);

  const chooseMode = (m) => {
    setMode(m);
    if (m === "chat") {
      addMsg("assistant", "👋 **Bắt đầu nào!**\n\nBạn đang học trường nào, chuyên ngành gì, và GPA hiện tại là bao nhiêu?");
    } else {
      addMsg("assistant", "Tuyệt! Nhấn nút **📎 Đính kèm CV** bên dưới để tải file PDF của bạn lên nhé.");
    }
  };

  const handleFileUpload = async (file) => {
    if (!file) return;
    setPdfLoading(true);
    addMsg("user", `📄 Đã tải lên: ${file.name}`);
    addMsg("assistant", "Đang phân tích CV của bạn...");
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await fetch(`${BASE_URL}/api/chat/extract`, { method: "POST", body: formData });
      if (res.ok) {
        const data = await res.json();
        setCareerData(prev => ({ ...prev, ...data }));
        addMsg("assistant", "✅ **Phân tích CV thành công!** Tôi đã trích xuất được thông tin từ hồ sơ của bạn.\n\nNhấn **Xem dự báo** khi bạn sẵn sàng.");
      } else {
        addMsg("assistant", "❌ Có lỗi khi đọc CV. Vui lòng thử lại hoặc chuyển sang chế độ chat.");
      }
    } catch {
      addMsg("assistant", "❌ Không thể kết nối server. Vui lòng kiểm tra lại.");
    }
    setPdfLoading(false);
  };

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const text = input.trim();
    setInput("");
    addMsg("user", text);
    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/api/handle_chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, current_data: careerData }),
      });
      if (res.ok) {
        const result = await res.json();
        const updated = { ...careerData };
        Object.entries(result).forEach(([k, v]) => {
          if (k in updated && v !== null) updated[k] = v;
        });
        setCareerData(updated);
        if (result.next_question) addMsg("assistant", result.next_question);
        if (result.is_complete) addMsg("assistant", "🎉 **Tuyệt vời!** Tôi đã có đủ thông tin. Nhấn nút **Xem dự báo** bên dưới nhé!");
      } else {
        addMsg("assistant", "Có lỗi xảy ra. Vui lòng thử lại.");
      }
    } catch {
      addMsg("assistant", "Không thể kết nối server.");
    }
    setLoading(false);
  };

  const predict = async () => {
    setPredicting(true);
    addMsg("assistant", "⚡ Đang chạy mô hình Stacking ML...");
    try {
      const res = await fetch(`${BASE_URL}/api/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(careerData),
      });
      if (res.ok) {
        const data = await res.json();
        setPredResult(data);
        setMessages(prev => [...prev, { role: "assistant", content: "", type: "prediction", data }]);
      }
    } catch {
      addMsg("assistant", "Không thể kết nối đến server dự báo.");
    }
    setPredicting(false);
  };

  const reset = () => {
    setMessages(INITIAL_MESSAGES);
    setCareerData(Object.fromEntries(Object.keys(careerData).map(k => [k, null])));
    setMode(null);
    setPredResult(null);
    setShowData(false);
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #0d0d14; }
        @keyframes bounce {
          0%, 80%, 100% { transform: translateY(0); }
          40% { transform: translateY(-6px); }
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(8px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .msg-in { animation: fadeIn 0.3s ease; }
        textarea:focus { outline: none; }
        textarea { resize: none; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }
      `}</style>

      <div style={{
        fontFamily: "'Sora', sans-serif",
        background: "#0d0d14",
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "20px",
      }}>
        {/* Ambient glow */}
        <div style={{
          position: "fixed", top: "-30%", left: "50%", transform: "translateX(-50%)",
          width: 600, height: 400, borderRadius: "50%",
          background: "radial-gradient(ellipse, rgba(108,99,255,0.12) 0%, transparent 70%)",
          pointerEvents: "none", zIndex: 0
        }} />

        <div style={{
          width: "100%", maxWidth: 720,
          display: "flex", flexDirection: "column",
          height: "90vh", maxHeight: 820,
          position: "relative", zIndex: 1,
          background: "#12121e",
          borderRadius: 24,
          border: "1px solid rgba(255,255,255,0.08)",
          overflow: "hidden",
          boxShadow: "0 32px 64px rgba(0,0,0,0.5), 0 0 0 1px rgba(108,99,255,0.1)"
        }}>

          {/* Header */}
          <div style={{
            padding: "16px 20px",
            borderBottom: "1px solid rgba(255,255,255,0.06)",
            display: "flex", alignItems: "center", justifyContent: "space-between",
            background: "rgba(255,255,255,0.02)",
            flexShrink: 0
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <div style={{
                width: 36, height: 36, borderRadius: 10,
                background: "linear-gradient(135deg, #6C63FF, #3ECFCF)",
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 16, fontWeight: 700, color: "#fff",
                boxShadow: "0 4px 12px rgba(108,99,255,0.4)"
              }}>C</div>
              <div>
                <p style={{ fontSize: 14, fontWeight: 600, color: "#e4e4f0" }}>Career Advisor AI</p>
                <p style={{ fontSize: 11, color: "#6C63FF" }}>● Online</p>
              </div>
            </div>
            <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
              {Object.values(careerData).some(v => v !== null) && (
                <button onClick={() => setShowData(p => !p)} style={{
                  background: showData ? "rgba(108,99,255,0.2)" : "transparent",
                  border: "1px solid rgba(108,99,255,0.3)", borderRadius: 8,
                  color: "#a78bfa", fontSize: 11, padding: "5px 10px", cursor: "pointer"
                }}>
                  📊 Dữ liệu ({Object.values(careerData).filter(v => v !== null).length}/11)
                </button>
              )}
              <button onClick={reset} style={{
                background: "transparent", border: "1px solid rgba(255,255,255,0.1)",
                borderRadius: 8, color: "#666", fontSize: 11, padding: "5px 10px", cursor: "pointer"
              }}>Làm mới</button>
            </div>
          </div>

          {/* Data card panel */}
          {showData && (
            <div style={{ padding: "0 16px", flexShrink: 0 }}>
              <DataCard data={careerData} />
            </div>
          )}

          {/* Messages */}
          <div style={{ flex: 1, overflowY: "auto", padding: "16px 20px" }}>
            {messages.map((msg, i) => (
              <div key={i} className="msg-in">
                {msg.type === "prediction" ? (
                  <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
                    <Avatar role="assistant" />
                    <div style={{ flex: 1 }}>
                      <PredictionResult result={msg.data} />
                    </div>
                  </div>
                ) : msg.type === "welcome" && mode === null ? (
                  <div style={{ textAlign: "center", padding: "24px 0 16px" }}>
                    <div style={{
                      width: 56, height: 56, borderRadius: 16, margin: "0 auto 12px",
                      background: "linear-gradient(135deg, #6C63FF, #3ECFCF)",
                      display: "flex", alignItems: "center", justifyContent: "center",
                      fontSize: 24, boxShadow: "0 8px 24px rgba(108,99,255,0.4)"
                    }}>🤖</div>
                    <p style={{ fontSize: 16, fontWeight: 600, color: "#e4e4f0", marginBottom: 6 }}>Career Advisor AI</p>
                    <p style={{ fontSize: 13, color: "#7c7c9e", marginBottom: 24, lineHeight: 1.6 }}>
                      Hệ thống tư vấn sự nghiệp thông minh<br />dựa trên mô hình Machine Learning
                    </p>
                    <div style={{ display: "flex", gap: 10, justifyContent: "center" }}>
                      {[
                        { icon: "💬", label: "Chat tư vấn", sub: "Trả lời câu hỏi", val: "chat" },
                        { icon: "📄", label: "Upload CV", sub: "Phân tích tự động", val: "CV" }
                      ].map(opt => (
                        <button key={opt.val} onClick={() => chooseMode(opt.val)} style={{
                          background: "rgba(255,255,255,0.04)",
                          border: "1px solid rgba(255,255,255,0.1)",
                          borderRadius: 14, padding: "14px 20px",
                          cursor: "pointer", textAlign: "center",
                          transition: "all 0.2s", color: "#fff",
                          minWidth: 130
                        }}
                          onMouseEnter={e => { e.currentTarget.style.background = "rgba(108,99,255,0.15)"; e.currentTarget.style.borderColor = "rgba(108,99,255,0.4)"; }}
                          onMouseLeave={e => { e.currentTarget.style.background = "rgba(255,255,255,0.04)"; e.currentTarget.style.borderColor = "rgba(255,255,255,0.1)"; }}
                        >
                          <div style={{ fontSize: 24, marginBottom: 6 }}>{opt.icon}</div>
                          <div style={{ fontSize: 13, fontWeight: 600, color: "#e4e4f0", marginBottom: 2 }}>{opt.label}</div>
                          <div style={{ fontSize: 11, color: "#7c7c9e" }}>{opt.sub}</div>
                        </button>
                      ))}
                    </div>
                  </div>
                ) : (
                  <MessageBubble msg={msg} />
                )}
              </div>
            ))}
            {loading && <TypingIndicator />}
            <div ref={bottomRef} />
          </div>

          {/* Footer */}
          {mode !== null && (
            <div style={{
              padding: "12px 16px",
              borderTop: "1px solid rgba(255,255,255,0.06)",
              background: "rgba(255,255,255,0.01)",
              flexShrink: 0
            }}>
              {/* Predict button */}
              {isComplete && !predResult && (
                <button onClick={predict} disabled={predicting} style={{
                  width: "100%", padding: "10px",
                  background: "linear-gradient(135deg, #6C63FF, #3ECFCF)",
                  border: "none", borderRadius: 10, color: "#fff",
                  fontSize: 13, fontWeight: 600, cursor: "pointer",
                  marginBottom: 10, opacity: predicting ? 0.7 : 1
                }}>
                  {predicting ? "⚡ Đang dự báo..." : "🚀 Xem Dự Báo Sự Nghiệp"}
                </button>
              )}

              {/* Input area */}
              <div style={{
                display: "flex", gap: 8, alignItems: "flex-end",
                background: "rgba(255,255,255,0.04)",
                borderRadius: 14, border: "1px solid rgba(255,255,255,0.08)",
                padding: "8px 10px",
                transition: "border-color 0.2s"
              }}
                onFocus={e => e.currentTarget.style.borderColor = "rgba(108,99,255,0.4)"}
                onBlur={e => e.currentTarget.style.borderColor = "rgba(255,255,255,0.08)"}
              >
                {mode === "CV" && (
                  <>
                    <input
                      type="file" accept=".pdf" ref={fileRef} style={{ display: "none" }}
                      onChange={e => handleFileUpload(e.target.files[0])}
                    />
                    <button onClick={() => fileRef.current.click()} disabled={pdfLoading} style={{
                      background: "rgba(108,99,255,0.2)", border: "none",
                      borderRadius: 8, width: 32, height: 32,
                      color: "#a78bfa", cursor: "pointer", flexShrink: 0,
                      display: "flex", alignItems: "center", justifyContent: "center",
                      fontSize: 16
                    }} title="Upload PDF">📎</button>
                  </>
                )}
                <textarea
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); } }}
                  placeholder={mode === "CV" ? "Hỏi thêm hoặc nhập thông tin..." : "Nhập câu trả lời..."}
                  style={{
                    flex: 1, background: "transparent", border: "none",
                    color: "#e4e4f0", fontSize: 13, lineHeight: 1.5,
                    maxHeight: 100, minHeight: 20, fontFamily: "inherit"
                  }}
                  rows={1}
                />
                <button onClick={sendMessage} disabled={!input.trim() || loading} style={{
                  background: input.trim() ? "linear-gradient(135deg, #6C63FF, #8B83FF)" : "rgba(255,255,255,0.06)",
                  border: "none", borderRadius: 8,
                  width: 32, height: 32, cursor: input.trim() ? "pointer" : "default",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  flexShrink: 0, transition: "all 0.2s",
                  boxShadow: input.trim() ? "0 2px 8px rgba(108,99,255,0.4)" : "none"
                }}>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                    <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </button>
              </div>

              <p style={{ fontSize: 10, color: "#444", textAlign: "center", marginTop: 6 }}>
                {missingFields.length > 0
                  ? `Còn thiếu ${missingFields.length} thông tin`
                  : "✓ Đã đủ thông tin"}
              </p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
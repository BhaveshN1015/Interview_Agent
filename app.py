import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ARIA — AI Interview Trainer",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
.main-header {
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(135deg, #0f0f1a, #1a2a4a);
    border-radius: 12px;
    margin-bottom: 1.5rem;
}
.main-header h1 { color: #4f9eff; font-size: 2.5rem; margin: 0; }
.main-header p { color: #aaa; margin: 6px 0 0; }
.badge {
    background: #1a2a4a; color: #4f9eff;
    padding: 4px 14px; border-radius: 20px;
    font-size: 12px; display: inline-block; margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🎯 ARIA</h1>
    <p>AI Readiness Interview Agent</p>
    <span class="badge">Powered by IBM Granite via watsonx.ai | IBM SkillsBuild AICTE 2026</span>
</div>
""", unsafe_allow_html=True)

# ---------- Session State ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "started" not in st.session_state:
    st.session_state.started = False

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### 🎯 ARIA Controls")
    st.divider()

    if st.button("🚀 Start New Interview", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.started = True

        with st.spinner("Starting ARIA..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "message": "Hello, I want to start my mock interview preparation.",
                        "conversation_history": []
                    }
                )
                if response.status_code == 200:
                    reply = response.json()["reply"]
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": reply
                    })
                    st.rerun()
                else:
                    st.error("Failed to start. Is FastAPI running?")
            except Exception as e:
                st.error(f"Cannot connect: {str(e)}")

    if st.session_state.messages:
        st.divider()
        if st.button("🗑️ Reset Interview", use_container_width=True):
            st.session_state.messages = []
            st.session_state.started = False
            st.rerun()

    st.divider()
    st.markdown("### 📋 How ARIA Works")
    st.markdown("""
1. Click **Start New Interview**
2. Tell ARIA your name, role & skills
3. Rate your confidence (1-10)
4. **Technical Round** — 5 questions
5. **HR Round** — 3 questions
6. **Situational Round** — 2 questions
7. Get your **Final Report Card** 🎯
    """)
    st.divider()
    st.markdown("""
<p style='font-size:11px;color:#666;text-align:center'>
IBM SkillsBuild AICTE Internship 2026<br>
IBM Granite · watsonx.ai · FastAPI · Streamlit
</p>
""", unsafe_allow_html=True)

# ---------- Main Area ----------
if not st.session_state.started:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align:center;padding:4rem 0;color:#666'>
            <h2>👈 Click "Start New Interview"</h2>
            <p style='margin-top:1rem'>ARIA will conduct a personalized mock interview<br>
            based on your job role, experience, and target company</p>
        </div>
        """, unsafe_allow_html=True)
else:
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Type your answer here...")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("ARIA is thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={
                            "message": user_input,
                            "conversation_history": st.session_state.messages[:-1]
                        }
                    )
                    if response.status_code == 200:
                        reply = response.json()["reply"]
                        st.markdown(reply)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": reply
                        })
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Cannot connect to backend: {str(e)}")

# ---------- Footer ----------
st.divider()
st.markdown(
    "<p style='text-align:center;color:#666;font-size:12px'>ARIA — AI Readiness Interview Agent | IBM SkillsBuild AICTE Internship 2026</p>",
    unsafe_allow_html=True
)

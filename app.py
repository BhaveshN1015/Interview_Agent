import streamlit as st
import streamlit.components.v1 as components
import requests
import os

# Priority order:
#   1. Streamlit secrets   (production — share.streamlit.io → Settings → Secrets)
#   2. Environment variable (any host that sets API_URL)
#   3. localhost fallback  (local dev — always works with no config needed)
try:
    API_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://127.0.0.1:8000"))
except Exception:
    # No secrets.toml present locally — use localhost
    API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

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
    <span class="badge">Powered by Meta Llama 3.3 70B via IBM watsonx.ai | IBM SkillsBuild AICTE 2026</span>
</div>
""", unsafe_allow_html=True)

# ---------- Session State ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "started" not in st.session_state:
    st.session_state.started = False
# session_id is the ONLY state the frontend holds.
# All conversation history lives server-side in main.py's _SESSIONS dict.
if "session_id" not in st.session_state:
    st.session_state.session_id = None
# voice_transcript: populated by the JS voice component via query params
if "voice_transcript" not in st.session_state:
    st.session_state.voice_transcript = ""
# input_mode: "text" or "voice"
if "input_mode" not in st.session_state:
    st.session_state.input_mode = "text"
# resume_loaded: True once /resume/upload succeeds for current session
if "resume_loaded" not in st.session_state:
    st.session_state.resume_loaded = False
# resume_digest: the compact digest returned by the backend (for display only)
if "resume_digest" not in st.session_state:
    st.session_state.resume_digest = ""

# ---------- Pick up voice transcript from query params (set by JS component) ----------
# The voice widget writes ?voice_input=<transcript> into the URL, then
# Streamlit reruns and we read it here before rendering anything.
qp = st.query_params
if "voice_input" in qp:
    raw = qp["voice_input"].strip()
    if raw:
        st.session_state.voice_transcript = raw
    # Clear the param so a page refresh doesn't replay the same answer
    st.query_params.clear()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### 🎯 ARIA Controls")
    st.divider()

    if st.button("🚀 Start New Interview", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.session_state.started = True
        st.session_state.session_id = None
        st.session_state.voice_transcript = ""
        st.session_state.resume_loaded = False
        st.session_state.resume_digest = ""

        with st.spinner("Starting ARIA..."):
            try:
                # Step 1: create a fresh server-side session
                sess_resp = requests.post(f"{API_URL}/session/new")
                if sess_resp.status_code != 200:
                    st.error("Failed to create session. Is FastAPI running?")
                    st.stop()

                sid = sess_resp.json()["session_id"]
                st.session_state.session_id = sid

                # Step 2: send the greeting to kick ARIA off
                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "session_id": sid,
                        "message": "Hello, I want to start my mock interview preparation."
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
                    st.error(f"Failed to start. Error: {response.text}")
            except Exception as e:
                st.error(f"Cannot connect: {str(e)}")

    if st.session_state.messages:
        st.divider()
        if st.button("🗑️ Reset Interview", use_container_width=True):
            st.session_state.messages = []
            st.session_state.started = False
            st.session_state.session_id = None
            st.session_state.voice_transcript = ""
            st.session_state.resume_loaded = False
            st.session_state.resume_digest = ""
            st.rerun()

    # ---------- Resume Upload ----------
    st.divider()
    st.markdown("### 📄 Resume Upload *(optional)*")

    if not st.session_state.started:
        st.markdown(
            "<p style='font-size:11px;color:#888'>Start an interview first, then upload your resume.</p>",
            unsafe_allow_html=True
        )
    elif st.session_state.resume_loaded:
        st.success("✅ Resume loaded — ARIA will use it!")
        with st.expander("View Resume Digest", expanded=False):
            st.markdown(
                f"<pre style='font-size:11px;white-space:pre-wrap;color:#ccc'>"
                f"{st.session_state.resume_digest}</pre>",
                unsafe_allow_html=True
            )
    else:
        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=["pdf", "docx", "txt"],
            help="PDF, DOCX, or TXT — max ~5 pages. Used once to personalise your interview.",
            label_visibility="collapsed"
        )
        if uploaded_file is not None:
            with st.spinner("Reading resume & generating digest..."):
                try:
                    resp = requests.post(
                        f"{API_URL}/resume/upload",
                        data={"session_id": st.session_state.session_id},
                        files={"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.resume_loaded = True
                        st.session_state.resume_digest = data["digest"]
                        st.success(f"✅ Resume processed! ({data['word_count']} word digest)")
                        st.rerun()
                    else:
                        st.error(f"Upload failed: {resp.json().get('detail', resp.text)}")
                except Exception as e:
                    st.error(f"Cannot connect to backend: {str(e)}")

    st.divider()

    # ---------- Input Mode Toggle ----------
    st.markdown("### 🎙️ Input Mode")
    mode = st.radio(
        "Choose how to answer:",
        ["⌨️ Type (Text)", "🎙️ Speak (Voice)"],
        index=0 if st.session_state.input_mode == "text" else 1,
        label_visibility="collapsed"
    )
    st.session_state.input_mode = "text" if mode == "⌨️ Type (Text)" else "voice"

    if st.session_state.input_mode == "voice":
        st.markdown("""
<p style='font-size:11px;color:#888;margin-top:4px'>
🌐 Uses your browser's built-in speech recognition.<br>
Works best in <b>Chrome</b> or <b>Edge</b>.<br>
Click the mic button, speak clearly, then submit.
</p>
""", unsafe_allow_html=True)

    st.divider()
    st.markdown("### 📋 How ARIA Works")
    st.markdown("""
1. Click **Start New Interview**
2. *(Optional)* Upload your resume
3. Tell ARIA your name, role & skills
4. Rate your confidence (1-10)
5. **Technical Round** — 5 questions
6. **HR Round** — 3 questions
7. **Situational Round** — 2 questions
8. Get your **Final Report Card** 🎯
    """)
    st.divider()
    st.markdown("""
<p style='font-size:11px;color:#666;text-align:center'>
IBM SkillsBuild AICTE Internship 2026<br>
watsonx.ai · FastAPI · Streamlit
</p>
""", unsafe_allow_html=True)


# ---------- Helper: send message to ARIA ----------
def send_to_aria(user_input: str):
    """Appends user message, calls backend, appends ARIA reply."""
    user_input = user_input.strip()
    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("ARIA is thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "session_id": st.session_state.session_id,
                        "message": user_input
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


# ---------- Voice Component HTML ----------
# Uses the browser's Web Speech API (SpeechRecognition).
# When the user clicks Stop or speech ends, the transcript is appended to
# the URL as ?voice_input=<text>, which triggers a Streamlit rerun so we
# can read it from query_params above.
VOICE_COMPONENT_HTML = """
<style>
  body { margin: 0; font-family: -apple-system, "Segoe UI", sans-serif; }
  #voice-box {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 14px;
    background: #1a1a2e; border: 1px solid #2a3a5a;
    border-radius: 10px;
  }
  #mic-btn {
    width: 44px; height: 44px; border-radius: 50%; border: none;
    background: #4f9eff; color: white; font-size: 20px;
    cursor: pointer; flex-shrink: 0; transition: background 0.2s;
  }
  #mic-btn.listening { background: #ef4444; animation: pulse 1s infinite; }
  #mic-btn:disabled { background: #555; cursor: not-allowed; }
  @keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.5); }
    50%       { box-shadow: 0 0 0 8px rgba(239,68,68,0); }
  }
  #transcript {
    flex: 1; min-height: 38px; padding: 8px 10px;
    background: #0f0f1a; color: #eee; border: 1px solid #2a3a5a;
    border-radius: 6px; font-size: 13px; resize: none;
    font-family: inherit; outline: none;
  }
  #submit-btn {
    padding: 8px 16px; background: #22c55e; color: white;
    border: none; border-radius: 6px; font-size: 13px;
    cursor: pointer; flex-shrink: 0; font-weight: 600;
  }
  #submit-btn:disabled { background: #555; cursor: not-allowed; }
  #status { font-size: 11px; color: #888; min-width: 80px; text-align: center; }
</style>

<div id="voice-box">
  <button id="mic-btn" title="Click to speak">🎙️</button>
  <textarea id="transcript" placeholder="Click 🎙️ to speak, or type here..." rows="2"></textarea>
  <div style="display:flex;flex-direction:column;gap:6px;align-items:center">
    <button id="submit-btn">Send ↑</button>
    <span id="status">Ready</span>
  </div>
</div>

<script>
const micBtn      = document.getElementById('mic-btn');
const transcriptEl= document.getElementById('transcript');
const submitBtn   = document.getElementById('submit-btn');
const statusEl    = document.getElementById('status');

// ---- Web Speech API setup ----
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition = null;
let listening = false;

if (!SpeechRecognition) {
  statusEl.textContent = 'Not supported';
  statusEl.style.color = '#ef4444';
  micBtn.disabled = true;
  micBtn.title = 'Speech not supported in this browser. Use Chrome or Edge.';
} else {
  recognition = new SpeechRecognition();
  recognition.continuous = false;       // single utterance
  recognition.interimResults = true;    // show live partial results
  recognition.lang = 'en-US';

  recognition.onstart = () => {
    listening = true;
    micBtn.classList.add('listening');
    micBtn.textContent = '⏹️';
    micBtn.title = 'Click to stop';
    statusEl.textContent = 'Listening...';
    statusEl.style.color = '#ef4444';
  };

  recognition.onresult = (event) => {
    let interim = '';
    let final   = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const t = event.results[i][0].transcript;
      if (event.results[i].isFinal) final += t;
      else interim += t;
    }
    // Show live text; append final to whatever was already typed
    const existing = transcriptEl.value.trim();
    if (final) {
      transcriptEl.value = (existing ? existing + ' ' : '') + final;
    } else {
      transcriptEl.value = (existing ? existing + ' ' : '') + interim;
    }
  };

  recognition.onerror = (event) => {
    statusEl.textContent = event.error === 'no-speech' ? 'No speech' : 'Error';
    statusEl.style.color = '#f59e0b';
    stopListening();
  };

  recognition.onend = () => {
    stopListening();
  };
}

function stopListening() {
  listening = false;
  micBtn.classList.remove('listening');
  micBtn.textContent = '🎙️';
  micBtn.title = 'Click to speak';
  statusEl.textContent = transcriptEl.value.trim() ? 'Got it!' : 'Ready';
  statusEl.style.color = transcriptEl.value.trim() ? '#22c55e' : '#888';
}

micBtn.addEventListener('click', () => {
  if (!recognition) return;
  if (listening) {
    recognition.stop();
  } else {
    transcriptEl.value = '';
    statusEl.style.color = '#888';
    recognition.start();
  }
});

// Submit: write transcript into URL query param, Streamlit reads it on rerun
submitBtn.addEventListener('click', () => {
  const text = transcriptEl.value.trim();
  if (!text) return;
  submitBtn.disabled = true;
  statusEl.textContent = 'Sending...';
  statusEl.style.color = '#4f9eff';
  // Navigate parent frame URL to include voice_input param
  const url = new URL(window.parent.location.href);
  url.searchParams.set('voice_input', text);
  window.parent.location.href = url.toString();
});

// Also allow Enter key to submit (Shift+Enter for newline)
transcriptEl.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    submitBtn.click();
  }
});
</script>
"""


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
    # Display chat history (display-only — no token cost)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ---- If a voice transcript just arrived, send it now ----
    if st.session_state.voice_transcript:
        transcript = st.session_state.voice_transcript
        st.session_state.voice_transcript = ""   # consume it immediately
        send_to_aria(transcript)
        st.rerun()

    # ---- Input area depending on mode ----
    if st.session_state.input_mode == "text":
        # Standard Streamlit chat input
        user_input = st.chat_input("Type your answer here...")
        if user_input:
            send_to_aria(user_input)
            st.rerun()
    else:
        # Voice component (+ still allows typing in the same box)
        st.markdown(
            "<p style='font-size:12px;color:#888;margin-bottom:6px'>"
            "🎙️ Click the mic to speak — or type directly in the box — then click <b>Send</b></p>",
            unsafe_allow_html=True
        )
        components.html(VOICE_COMPONENT_HTML, height=90, scrolling=False)


# ---------- Footer ----------
st.divider()
st.markdown(
    "<p style='text-align:center;color:#666;font-size:12px'>ARIA — AI Readiness Interview Agent | IBM SkillsBuild AICTE Internship 2026</p>",
    unsafe_allow_html=True
)

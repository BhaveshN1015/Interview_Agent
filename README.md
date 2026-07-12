<div align="center">

# 🎯 ARIA — AI Readiness Interview Agent

### *Your Personal AI-Powered Mock Interview Coach*

[![IBM watsonx](https://img.shields.io/badge/IBM-watsonx.ai-0530AD?style=for-the-badge&logo=ibm&logoColor=white)](https://www.ibm.com/watsonx)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Meta Llama](https://img.shields.io/badge/Meta-Llama%203.3%2070B-0064E0?style=for-the-badge&logo=meta&logoColor=white)](https://ai.meta.com/llama/)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

**IBM SkillsBuild × AICTE Internship 2026 — Problem Statement #22**

---

> *"Don't just prepare for interviews — simulate them with AI."*

---

</div>

## 📌 Table of Contents
- [About ARIA](#-about-aria)
- [Demo](#-demo)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [AI Tools Used in Building ARIA](#-ai-tools-used-in-building-aria)
- [Installation](#-installation-local)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Token Optimisation](#-token-optimisation)
- [Resume Feature](#-resume-feature)

---

## 🤖 About ARIA

**ARIA (AI Readiness Interview Agent)** is an intelligent conversational agent that conducts full end-to-end mock interviews for job seekers targeting top IT companies like **TCS, Infosys, Wipro, Accenture, and Cognizant**.

Unlike generic Q&A tools, ARIA runs a **complete structured interview** across three rounds, scores every answer in real-time, adapts difficulty as you progress, and hands you a personalised **Final Report Card** with a 7-day study roadmap — all powered by **Meta Llama 3.3 70B Instruct** via **IBM watsonx.ai**.

Now with **Resume-Aware Interviews** — upload your PDF/DOCX resume once and ARIA will ask questions directly tied to your real projects, skills, and achievements.

---

## 🎬 Demo

<div align="center">

## 🎥 Demo Video

[![Watch Demo](https://img.youtube.com/vi/https://youtu.be/L8V0VZBCdbI/maxresdefault.jpg)](https://www.youtube.com/watch?v=https://youtu.be/L8V0VZBCdbI)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 **Role-Based Questions** | Tailored questions for any IT role and target company |
| 📄 **Resume-Aware Interviews** | Upload your PDF/DOCX/TXT resume — ARIA asks about your real projects, skills & achievements |
| 📊 **Real-Time Evaluation** | Score (X/10) + concise feedback after every answer |
| 💡 **Confidence Tracking** | Measures confidence growth from start to finish |
| 🔄 **Adaptive Difficulty** | Questions get progressively harder as you perform better |
| 🎙️ **Voice Input** | Speak your answers using your microphone (Chrome/Edge) |
| 📋 **Final Report Card** | Overall scores, top strengths, improvement areas + Resume Alignment score |
| 🗺️ **7-Day Study Roadmap** | Personalised preparation plan based on your performance |
| 💬 **Multi-Turn Chat** | Natural conversational interview flow — no forms or dropdowns |
| 🏢 **Multi-Company Support** | TCS, Infosys, Wipro, Accenture, Cognizant and more |
| ⚡ **Token-Optimised** | Server-side session store — flat token cost regardless of interview length |

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    User (Browser)                        │
│           Chrome / Edge  (voice input supported)         │
└─────────────────────────┬────────────────────────────────┘
                          │
┌─────────────────────────▼────────────────────────────────┐
│           Streamlit Frontend  (app.py · :8501)           │
│                                                          │
│  • Chat UI — displays messages                           │
│  • Voice widget — Web Speech API (browser-native STT)    │
│  • Resume uploader — PDF / DOCX / TXT (optional)         │
│  • Sends only: { session_id, message }                   │
│    ↳ NO conversation history in the HTTP body            │
└─────────────────────────┬────────────────────────────────┘
                          │  POST /chat        { session_id, message }
                          │  POST /session/new
                          │  POST /resume/upload { session_id, file }
┌─────────────────────────▼────────────────────────────────┐
│           FastAPI Backend  (main.py · :8000)             │
│                                                          │
│  • Server-side session store  (_SESSIONS dict)           │
│    ↳ { history: [...], resume_digest: str | None }       │
│  • Resume parser — PyMuPDF (PDF) + python-docx (DOCX)    │
│  • One-shot digest call → compact ~120-word summary      │
│  • History trimming + dynamic token budget               │
│  • ARIA system prompt engine (digest injected when set)  │
│  • Background model warmup at startup                    │
└─────────────────────────┬────────────────────────────────┘
                          │  ibm-watsonx-ai SDK
┌─────────────────────────▼────────────────────────────────┐
│           IBM watsonx.ai                                 │
│           Meta Llama 3.3 70B Instruct                    │
│           (Free Lite tier — Dallas region)               │
└──────────────────────────────────────────────────────────┘
```

**Key design decision — server-side sessions:** The frontend never sends conversation history. Only `session_id + message` travels over HTTP. The backend holds all history, trims it to a rolling window, and sends a fixed-size context to the LLM — keeping input token cost flat at every turn of the interview.

**Resume design decision — one-shot digest:** The raw resume is never stored or re-sent. One LLM call converts it to a ~120-word structured digest on upload. That digest (~130 tokens) is injected into the system prompt on every subsequent call — keeping the per-call overhead flat and the raw file off the wire entirely.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **LLM** | Meta Llama 3.3 70B Instruct | Interview agent brain — question generation, scoring, report card |
| **LLM Platform** | IBM watsonx.ai | Hosted inference, API access, token usage tracking |
| **Backend** | FastAPI + Uvicorn | REST API, session management, prompt engineering |
| **Frontend** | Streamlit | Chat UI, sidebar controls, real-time display |
| **Voice Input** | Browser Web Speech API | Microphone-to-text (zero external dependencies) |
| **Resume Parsing** | PyMuPDF + python-docx | Extract text from PDF and DOCX resumes |
| **SDK** | ibm-watsonx-ai | Official Python SDK for watsonx.ai model calls |
| **Language** | Python 3.10+ | Core language |
| **HTTP Client** | requests | Frontend → Backend API calls |

---

## 🤝 AI Tools Used in Building ARIA

ARIA was built using a combination of human engineering and AI-assisted development:

| Tool | Role in This Project |
|---|---|
| **IBM watsonx.ai** | Hosts Meta Llama 3.3 70B — the LLM that powers ARIA's interview agent at runtime |
| **IBM Bob (AI Software Engineer)** | Used throughout development to architect, debug, and optimise the entire codebase — from designing the server-side session store and token budget system, to fixing prompt behaviour bugs, implementing the voice input feature, and writing all deployment configuration |
| **Meta Llama 3.3 70B Instruct** | The foundation model ARIA uses to conduct interviews, score answers, and generate report cards |

> ARIA was designed and developed with IBM Bob as the primary engineering assistant — responsible for the full architecture, all code optimisations, the voice feature, and the token-reduction work that brought input cost from ~1,400 tokens/call down to ~505 tokens/call.

---

## ⚙️ Installation (Local)

### Prerequisites
- Python 3.10+
- IBM Cloud account — free at [cloud.ibm.com](https://cloud.ibm.com)
- IBM watsonx.ai project + API key
- Chrome or Edge browser (for voice input)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/interview-trainer.git
cd interview-trainer

# 2. Create virtual environment
python -m venv ml
ml\Scripts\activate        # Windows
source ml/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# If upgrading an existing install, add the two new resume packages:
pip install pymupdf==1.24.9 python-docx==1.1.2

# 4. Create .env from template
copy .env.example .env     # Windows
cp .env.example .env       # Mac/Linux
# Open .env and fill in your IBM credentials
```

### Environment Variables (`.env`)

```env
IBM_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_watsonx_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

Get your credentials at:
- **API Key** → [cloud.ibm.com/iam/apikeys](https://cloud.ibm.com/iam/apikeys)
- **Project ID** → watsonx.ai dashboard → your project → Manage tab

---

## 🚀 Running Locally

Open **two terminals** (both with `ml\Scripts\activate`):

**Terminal 1 — Backend:**
```bash
uvicorn main:app --reload
```
✅ Wait for: `Application startup complete.`

**Terminal 2 — Frontend:**
```bash
streamlit run app.py
```
✅ Opens at `http://localhost:8501`

Open in **Chrome or Edge** for voice input support.

---

## ☁️ Deployment

ARIA has two services — deploy them separately:

| Service | File | Recommended Platform |
|---|---|---|
| FastAPI backend | `main.py` | [Render](https://render.com) (free) |
| Streamlit frontend | `app.py` | [Streamlit Community Cloud](https://share.streamlit.io) (free) |

### Render (Backend)
1. New Web Service → connect GitHub repo
2. **Build:** `pip install -r requirements.txt`
3. **Start:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add env vars: `IBM_API_KEY`, `WATSONX_PROJECT_ID`, `WATSONX_URL`
5. Copy your service URL: `https://aria-api-xxxx.onrender.com`

### Streamlit Community Cloud (Frontend)
1. New app → select repo → main file: `app.py`
2. Settings → Secrets → add:
```toml
API_URL = "https://aria-api-xxxx.onrender.com"
```

---

## 📁 Project Structure

```
interview-trainer/
│
├── main.py                  # FastAPI backend — ARIA agent, session store, resume upload, LLM calls
├── app.py                   # Streamlit frontend — chat UI, voice input, resume uploader
├── watsonx_client.py        # Standalone IBM watsonx.ai smoke-test helper
├── prompt_templates.py      # Prompt builders — resume digest, interview questions, difficulty
├── sample_prompts.py        # Pre-written test conversations for 5 companies/roles
│
├── good_interview.gif       # Demo — high-scoring interview run
├── bad_interview.gif        # Demo — weak answers with ARIA's feedback
│
├── requirements.txt         # Python dependencies (pinned)
├── Procfile                 # Process file for Render / Railway / Heroku
├── .env.example             # Credentials template — safe to commit
├── .env                     # Your live credentials — NEVER commit this
├── .gitignore               # Excludes .env, ml/, videos, logs, uploaded resumes
└── README.md                # This file
```

---

## ⚡ Token Optimisation

ARIA was heavily optimised to stay within IBM watsonx.ai's free Lite tier limits.

| Metric | Before Optimisation | After Optimisation |
|---|---|---|
| Input tokens / call | ~1,400 | ~505 |
| History payload | Sent from browser (unbounded) | Held server-side (fixed window) |
| System prompt size | ~650 tokens | ~200 tokens |
| Truncation method | Character-count (inaccurate) | Word-count (token-accurate) |
| Output budget | 280 tokens (fixed) | 50 / 180 / 400 (dynamic per turn) |
| Full session cost | ~18,000 tokens | ~6,500 tokens |
| Sessions / month (free tier) | ~2–3 | ~7–8 |

Key changes: server-side session store, compressed system prompt, word-count truncation, dynamic output caps per interview phase, background model warmup at startup.

---

## 📄 Resume Feature

ARIA supports optional resume upload to personalise the interview with questions drawn from your actual experience.

| Step | What happens | Token cost |
|---|---|---|
| Upload PDF/DOCX/TXT | Text extracted server-side (PyMuPDF / python-docx) | 0 |
| Digest generation | ONE LLM call → ~120-word structured summary | ~650 input + ~150 output (once) |
| Per interview call | Digest injected into system prompt | +~130 tokens/call |
| Full session w/ resume | ~10,200 tokens total | ~4–5 sessions/month |

**How it works:**
1. Click **🚀 Start New Interview** — creates your session
2. Upload your resume in the **📄 Resume Upload** sidebar section
3. ARIA reads your Role, Experience, Skills, Projects, and Achievements from the digest
4. Questions are drawn from both general interview knowledge AND your specific resume
5. Final Report Card includes a **Resume Alignment** score — how well your answers matched your CV claims

**Supported formats:** PDF · DOCX · TXT (max ~5 pages recommended)

**Resume is never stored** — raw text is discarded after the digest is generated. Only the ~120-word summary is kept in memory for the session duration.

---

<div align="center">

**Built with ❤️ using Meta Llama 3.3 70B via IBM watsonx.ai**

[![IBM SkillsBuild](https://img.shields.io/badge/IBM-SkillsBuild%20AICTE%202026-0530AD?style=for-the-badge&logo=ibm&logoColor=white)](https://skillsbuild.org)
[![Built with Bob](https://img.shields.io/badge/Built%20with-IBM%20Bob%20AI-7c5cd8?style=for-the-badge)](https://www.ibm.com)

*IBM SkillsBuild × AICTE Internship 2026*

</div>

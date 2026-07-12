from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv
from prompt_templates import get_resume_digest_prompt
import os
import io
import time
import uuid
import threading

load_dotenv()

app = FastAPI(
    title="ARIA - AI Readiness Interview Agent",
    description="Powered by Meta Llama 3.3 70B via IBM watsonx.ai",
    version="5.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- ARIA System Prompt ----------
ARIA_SYSTEM_PROMPT = """You are ARIA, an AI interview coach for IT roles.

FLOW:
1) First turn: ask Name, Role, Experience, Skills, Target Company in ONE question. No Score line.
   If a Resume Digest is provided below, you already know their skills/role — greet them, confirm the details, and ask only for their Target Company and Name.
2) After they answer profile: ask ONLY "Confidence 1-10?" — nothing else. No Score line. This is onboarding, not an interview question.
3) After they give a number (their confidence): do NOT score it. Begin the interview immediately with Technical Q1.
4) Run 5 Technical + 3 HR(STAR) + 2 Situational questions, ONE at a time, increasing difficulty.
   When a Resume Digest is present, weave resume-specific questions naturally into the mix — ask about their actual projects, skills, and achievements listed there.
5) After EACH interview-question answer, reply in THIS EXACT FORMAT (blank line before Next Question):
Score: X/10
[1 line ONLY: strength | gap | ideal answer — max 20 words total]

Next Question: [single question]
6) After Q10, output the FINAL REPORT CARD:
Name/Role/Company | Scores: Technical/Comm/Confidence/ProblemSolving/Overall (X/10) | Start→End Confidence | Top 3 Strengths | Top 3 Improvement Areas | 7-Day Roadmap | 1-line motivation.
If a Resume Digest was present, add: Resume Alignment — how well answers matched the resume claims.

STRICT RULES:
- Never write the candidate's turn or invent their answer.
- No stage directions, parenthetical notes, or meta-commentary.
- NEVER emit a Score line for profile info or the confidence number.
- A Score line is ONLY valid after the candidate answers one of the 10 interview questions.
- Feedback line after Score MUST be 20 words or fewer — be concise and direct.
- Exactly ONE turn per response: one question, OR one eval+next question, OR the report card."""

# ---------- Model — module-level singleton ----------
_MODEL: Optional[ModelInference] = None
_MODEL_LOCK = threading.Lock()

def get_model() -> ModelInference:
    global _MODEL
    if _MODEL is None:
        with _MODEL_LOCK:
            # Double-checked locking — another thread may have initialised
            # it while we waited for the lock.
            if _MODEL is None:
                creds = Credentials(
                    url=os.getenv("WATSONX_URL"),
                    api_key=os.getenv("IBM_API_KEY")
                )
                _MODEL = ModelInference(
                    model_id="meta-llama/llama-3-3-70b-instruct",
                    credentials=creds,
                    project_id=os.getenv("WATSONX_PROJECT_ID"),
                )
    return _MODEL


def _warmup_model():
    """Pre-initialise the ModelInference object in a background thread at
    startup so the FIRST real user request doesn't pay the 3-6 s handshake
    cost. Runs once, silently — any error is ignored (lazy init still works)."""
    try:
        get_model()
    except Exception:
        pass   # credentials not set yet / network unavailable — safe to ignore


# ---------- Resume Text Extraction ----------
def _extract_text_from_pdf(data: bytes) -> str:
    """Extract plain text from a PDF file using PyMuPDF."""
    import fitz  # PyMuPDF
    text_parts = []
    with fitz.open(stream=data, filetype="pdf") as doc:
        for page in doc:
            text_parts.append(page.get_text())
    return "\n".join(text_parts).strip()


def _extract_text_from_docx(data: bytes) -> str:
    """Extract plain text from a DOCX file using python-docx."""
    from docx import Document
    doc = Document(io.BytesIO(data))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip()).strip()


def extract_resume_text(filename: str, data: bytes) -> str:
    """Route to the correct extractor based on file extension."""
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        return _extract_text_from_pdf(data)
    elif ext in ("docx", "doc"):
        return _extract_text_from_docx(data)
    elif ext == "txt":
        return data.decode("utf-8", errors="ignore").strip()
    else:
        raise ValueError(f"Unsupported file type: .{ext}")


# ---------- Server-side Session Store ----------
# history is stored on the server, NOT sent by the client on every request.
# The client sends only { "session_id": "...", "message": "..." }.
# Using a plain dict — fine for single-process uvicorn (dev + demo).
# For multi-worker production, swap with Redis or another shared store.
#
# Each session value is a dict:
#   { "history": [...], "resume_digest": str | None }
_SESSIONS: Dict[str, dict] = {}

MAX_HISTORY_TURNS = 2      # 2 recent user+assistant pairs kept (beyond pinned intro)
MAX_WORDS_PER_MSG = 45     # ~55–65 tokens per message — tighter now that we control history


def _truncate(text: str) -> str:
    """Word-count truncation — closer proxy to LLM token count than char limit."""
    words = text.strip().split()
    if len(words) <= MAX_WORDS_PER_MSG:
        return text.strip()
    return " ".join(words[:MAX_WORDS_PER_MSG]) + "..."


def build_messages(history: list, user_message: str, resume_digest: Optional[str] = None) -> list:
    """
    Build the LLM message list from server-side history.

    Strategy:
    - Always include system prompt (+ optional resume digest block).
    - Pin the FIRST assistant message (the profile question ARIA asked) — cheap
      anchor that tells the model who it is and what stage it was at.
    - Keep the last MAX_HISTORY_TURNS user+assistant pairs — just enough for
      ARIA to remember what question it just asked and the candidate's last answer.
    - Truncate every historical message by word count.
    - Append the current user message untruncated (it's always short).

    Token budget per call (approximate):
      system          ~210 tok  (constant — slightly larger with resume flow note)
      resume digest   ~130 tok  (when present — injected ONCE into system prompt)
      pinned          ~15 tok
      2 pairs         ~4 msgs × ~60 tok = ~240 tok
      user msg        ~50 tok
      ────────────────────────────────────────
      input w/resume  ~645 tok  (vs ~505 without resume)
    """
    # Build system prompt — append digest block if available
    if resume_digest:
        system_content = (
            ARIA_SYSTEM_PROMPT
            + f"\n\n--- Candidate Resume Digest ---\n{resume_digest}\n--- End Resume Digest ---"
        )
    else:
        system_content = ARIA_SYSTEM_PROMPT

    pinned = []
    rest = []
    pinned_used = False
    for msg in history:
        if not pinned_used and msg.get("role") == "assistant":
            pinned = [msg]
            pinned_used = True
        else:
            rest.append(msg)

    max_msgs = MAX_HISTORY_TURNS * 2
    trimmed = rest[-max_msgs:] if len(rest) > max_msgs else rest

    messages = [{"role": "system", "content": system_content}]
    for msg in pinned + trimmed:
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": _truncate(msg["content"])})
    messages.append({"role": "user", "content": user_message})
    return messages


def sanitize_reply(raw_reply: str) -> str:
    """
    Defense-in-depth guard: strips hallucinated stage directions,
    enforces one Score/Next-Question pair, deduplicates report card.
    """
    if not raw_reply:
        return raw_reply

    reply = raw_reply.strip()

    # Strip stray parenthetical stage-direction lines.
    lines = reply.split("\n")
    cleaned = [
        line for line in lines
        if not (line.strip().startswith("(") and line.strip().endswith(")"))
    ]
    reply = "\n".join(cleaned).strip()

    # Guarantee "Next Question:" starts on its own paragraph.
    if "Next Question:" in reply:
        idx = reply.find("Next Question:")
        before = reply[:idx].rstrip()
        after = reply[idx:]
        reply = f"{before}\n\n{after}" if before else after

    # Hard cap: only ONE Score/Next-Question pair per response.
    nq_idx = reply.find("Next Question:")
    if nq_idx != -1:
        second_score = reply.find("Score:", nq_idx + len("Next Question:"))
        if second_score != -1:
            reply = reply[:second_score].strip()

    # Deduplicate report card.
    marker = "FINAL REPORT CARD"
    first = reply.find(marker)
    if first != -1:
        second = reply.find(marker, first + len(marker))
        if second != -1:
            reply = reply[:second].strip()

    return reply


# ---------- Request / Response Models ----------
class NewSessionResponse(BaseModel):
    session_id: str

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    status: str
    reply: str
    session_id: str

class ResumeUploadResponse(BaseModel):
    status: str
    session_id: str
    digest: str          # the compressed digest (useful for debugging / display)
    word_count: int      # how many words the digest is


# ---------- Startup event — warm up model in background ----------
@app.on_event("startup")
def startup_event():
    """Fire-and-forget background thread that initialises the IBM watsonx
    ModelInference object while FastAPI is booting. By the time the first
    real user request arrives the object is already ready, so the user sees
    no cold-start delay."""
    t = threading.Thread(target=_warmup_model, daemon=True)
    t.start()


# ---------- Routes ----------
@app.get("/")
def root():
    return {
        "message": "ARIA is running!",
        "powered_by": "Meta Llama 3.3 70B via IBM watsonx.ai",
        "version": "5.0.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/session/new", response_model=NewSessionResponse)
def new_session():
    """Create a fresh interview session. Returns a session_id the frontend stores."""
    sid = str(uuid.uuid4())
    _SESSIONS[sid] = {"history": [], "resume_digest": None}
    return {"session_id": sid}


@app.post("/resume/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    session_id: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Accept a PDF / DOCX / TXT resume, extract its text, run ONE LLM call to
    produce a compact digest (~120 words), and store it in the session.

    Token cost: ~650 input + ~150 output — one-time per session.
    Every subsequent /chat call injects the digest (~130 tokens) instead of
    the raw text, keeping per-call cost flat.
    """
    if session_id not in _SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found. Call /session/new first.")

    # --- 1. Read & extract text ---
    data = await file.read()
    try:
        raw_text = extract_resume_text(file.filename, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not parse resume: {str(e)}")

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Resume appears to be empty or unreadable.")

    # --- 2. One LLM call → digest ---
    digest_prompt = get_resume_digest_prompt(raw_text)
    digest_messages = [
        {"role": "system", "content": "You are a resume summarizer. Follow the format exactly."},
        {"role": "user",   "content": digest_prompt}
    ]

    try:
        model = get_model()
        result = model.chat(
            messages=digest_messages,
            params={"temperature": 0.1, "max_tokens": 220, "top_p": 0.9}
        )
        digest = result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM digest failed: {str(e)}")

    # --- 3. Store digest in session ---
    _SESSIONS[session_id]["resume_digest"] = digest

    return {
        "status": "success",
        "session_id": session_id,
        "digest": digest,
        "word_count": len(digest.split())
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    sid = request.session_id
    if sid not in _SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found. Call /session/new first.")

    session   = _SESSIONS[sid]
    history   = session["history"]
    digest    = session["resume_digest"]   # None if no resume uploaded
    messages  = build_messages(history, request.message, resume_digest=digest)

    # Dynamic output cap:
    #   onboarding turns (history < 4 msgs) → short question only → 50 tokens
    #   interview turns                     → eval + next question → 180 tokens
    #   final report card (history >= 24)   → full report          → 400 tokens
    hist_len = len(history)
    if hist_len < 4:
        output_tokens = 50       # onboarding: just a short question
    elif hist_len >= 24:
        output_tokens = 400      # report card turn: needs more room
    else:
        output_tokens = 180      # interview turn: Score line + 1 feedback line + Next Question

    chat_params = {
        "temperature": 0.3,
        "max_tokens": output_tokens,
        "top_p": 0.85,
    }

    max_retries = 3
    last_error = None

    for attempt in range(max_retries):
        try:
            model = get_model()
            result = model.chat(messages=messages, params=chat_params)
            raw_reply = result["choices"][0]["message"]["content"]
            clean_reply = sanitize_reply(raw_reply.strip())

            # Append both turns to server-side history
            _SESSIONS[sid]["history"].append({"role": "user",      "content": request.message})
            _SESSIONS[sid]["history"].append({"role": "assistant", "content": clean_reply})

            return {"status": "success", "reply": clean_reply, "session_id": sid}

        except Exception as e:
            last_error = e
            error_str = str(e)
            if "429" in error_str or "consumption_limit_reached" in error_str:
                if attempt < max_retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise HTTPException(
                    status_code=429,
                    detail="ARIA is handling a lot of requests right now (IBM free-tier limit). "
                           "Please wait 30–60 seconds and try again."
                )
            raise HTTPException(status_code=500, detail=error_str)

    raise HTTPException(status_code=500, detail=str(last_error))

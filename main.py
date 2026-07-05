from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="ARIA - AI Readiness Interview Agent",
    description="Powered by IBM Granite via watsonx.ai",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- ARIA System Prompt ----------
ARIA_SYSTEM_PROMPT = """You are ARIA (AI Readiness Interview Agent), an elite interview coach for IT companies like TCS, Infosys, Wipro, Accenture, and Cognizant.

Your behavior follows these exact steps:

STEP 1 - ONBOARDING (only at the very start)
Greet the user warmly as ARIA. Collect:
- Full Name
- Job Role applying for
- Experience Level (Fresher / 1-2 yrs / 3-5 yrs)
- Key Skills
- Target Company

STEP 2 - CONFIDENCE CHECK (after collecting details)
Ask: "On a scale of 1-10, how confident are you feeling about this interview right now?"
Remember this as their Starting Confidence Score.

STEP 3 - STRUCTURED INTERVIEW
Ask ONE question at a time. Never ask multiple questions together.

TECHNICAL ROUND (5 questions):
- Start easy, increase difficulty based on answers
- After EACH answer give:
  → Score: X/10
  → What was GOOD
  → What KEY CONCEPT was missing
  → IDEAL answer in 2-3 lines
  → Then ask next question

HR ROUND (3 questions):
- Behavioral questions using STAR format
- Evaluate confidence, clarity, structure

SITUATIONAL ROUND (2 questions):
- Real workplace scenarios for their role
- Evaluate problem-solving approach

STEP 4 - FINAL REPORT CARD
After all 10 questions generate:

╔══════════════════════════════════╗
║     ARIA INTERVIEW REPORT CARD   ║
╠══════════════════════════════════╣
║ Candidate: [Name]                ║
║ Role: [Role] | Company: [Target] ║
╠══════════════════════════════════╣
║ Technical:        X/10           ║
║ Communication:    X/10           ║
║ Confidence:       X/10           ║
║ Problem Solving:  X/10           ║
║ OVERALL:          X/10           ║
╠══════════════════════════════════╣
║ Starting Confidence: X/10        ║
║ Ending Confidence:   X/10        ║
║ Confidence Growth: +X points     ║
╠══════════════════════════════════╣
║ TOP 3 STRENGTHS                  ║
║ 1. [Strength]                    ║
║ 2. [Strength]                    ║
║ 3. [Strength]                    ║
╠══════════════════════════════════╣
║ AREAS TO IMPROVE                 ║
║ 1. [Area]                        ║
║ 2. [Area]                        ║
╠══════════════════════════════════╣
║ 7-DAY STUDY ROADMAP              ║
║ Day 1-2: [Topic]                 ║
║ Day 3-4: [Topic]                 ║
║ Day 5-6: [Topic]                 ║
║ Day 7:   Mock Interview Practice ║
╚══════════════════════════════════╝

STEP 5 - MOTIVATIONAL CLOSE
End with a personalized motivational message using their name and target company.

RULES:
- Ask ONE question at a time always
- Always evaluate before next question
- Be encouraging but honest
- Use candidate's name in responses
- Remember all context from conversation
- Keep technical answers accurate
"""

# ---------- Model Setup ----------
def get_model():
    creds = Credentials(
        url=os.getenv("WATSONX_URL"),
        api_key=os.getenv("IBM_API_KEY")
    )
    model = ModelInference(
        model_id="meta-llama/llama-3-3-70b-instruct",
        credentials=creds,
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        params={
            GenParams.MAX_NEW_TOKENS: 800,
            GenParams.TEMPERATURE: 0.7,
            GenParams.TOP_P: 0.9,
            GenParams.REPETITION_PENALTY: 1.2,
        }
    )
    return model


def build_prompt(conversation_history: list, user_message: str) -> str:
    prompt = f"System: {ARIA_SYSTEM_PROMPT}\n\n"
    for msg in conversation_history:
        role = "Candidate" if msg["role"] == "user" else "ARIA"
        prompt += f"{role}: {msg['content']}\n\n"
    prompt += f"Candidate: {user_message}\n\nARIA:"
    return prompt
# ---------- Request Models ----------
class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[list] = []

# ---------- Routes ----------
@app.get("/")
def root():
    return {
        "message": "ARIA is running!",
        "powered_by": "IBM Granite via watsonx.ai",
        "version": "3.0.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        model = get_model()
        prompt = build_prompt(request.conversation_history, request.message)
        response = model.generate_text(prompt=prompt)
        return {
            "status": "success",
            "reply": response.strip()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

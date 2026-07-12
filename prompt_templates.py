# prompt_templates.py
# Standalone prompt builders — not used by main.py's ARIA agent directly,
# but available for future features (resume upload, difficulty check, etc.).
# All prompts are compressed to minimise input-token cost while retaining
# every instruction the model needs.


def get_resume_digest_prompt(resume_text: str) -> str:
    """
    One-shot call that turns a raw resume into a compact ~120-word digest.
    The digest is stored in the session and injected into every subsequent
    LLM call instead of the raw resume — keeps per-call token cost flat.

    Input cap: 500 words of resume text (~650 tokens).
    Expected output: ~120 words (~150 tokens) — one-time cost only.
    """
    words = resume_text.split()
    if len(words) > 500:
        resume_text = " ".join(words[:500]) + "..."

    return (
        "Summarize this resume into EXACTLY this format (be concise, max 120 words total):\n\n"
        "Role: <job title>\n"
        "Experience: <X years / fresher>\n"
        "Skills: <comma-separated top skills, max 10>\n"
        "Projects: <3 projects, 1 line each — name: what it did>\n"
        "Achievements: <3 achievements, 1 line each>\n"
        "Interview Topics: <5 specific topics an interviewer would probe from this resume>\n\n"
        f"Resume:\n{resume_text}\n\n"
        "Output only the structured digest above. No intro, no commentary."
    )


def get_interview_questions_prompt(job_role: str, experience: str, skills: str) -> str:
    return (
        f"You are an expert interview coach for top IT companies (TCS, Infosys, Wipro, Accenture).\n\n"
        f"Candidate: {job_role} | {experience} | Skills: {skills}\n\n"
        "Generate a structured interview prep guide:\n\n"
        "1. TECHNICAL QUESTIONS (5)\n"
        "   Each: Question / Model Answer / Key Points\n\n"
        "2. HR/BEHAVIORAL QUESTIONS (3)\n"
        "   Each: Question / STAR-format answer\n\n"
        "3. SITUATION-BASED QUESTIONS (2)\n"
        "   Each: Question / How to approach\n\n"
        "4. PREPARATION ROADMAP\n"
        "   Top 5 topics | Time estimate | Resources\n\n"
        "Be concise and practical."
    )


def get_followup_prompt(question: str, previous_context: str) -> str:
    return (
        f"You are an expert interview coach.\n\n"
        f"Context (summary): {previous_context}\n\n"
        f"Follow-up question: {question}\n\n"
        "Give a concise, practical answer to help the candidate prepare."
    )


def get_resume_based_prompt(job_role: str, experience: str, resume_text: str) -> str:
    # Cap resume_text to ~400 words to prevent runaway input tokens.
    words = resume_text.split()
    if len(words) > 400:
        resume_text = " ".join(words[:400]) + "..."

    return (
        f"You are an expert interview coach and resume analyzer.\n\n"
        f"Role: {job_role} | Experience: {experience}\n\n"
        f"Resume (excerpt):\n{resume_text}\n\n"
        "Based on the resume, generate:\n\n"
        "1. PERSONALIZED TECHNICAL QUESTIONS (5)\n"
        "   Each: Question / Model Answer / What interviewer is looking for\n\n"
        "2. RESUME-BASED HR QUESTIONS (3)\n"
        "   Each: Question / Strong Answer Template\n\n"
        "3. POTENTIAL WEAK AREAS (2)\n"
        "   Each: Gap identified / How to address it\n\n"
        "4. STRENGTHS TO HIGHLIGHT (3)\n"
        "   Based only on the resume content provided.\n\n"
        "Keep all answers tailored to the actual resume."
    )


def get_difficulty_rating_prompt(job_role: str, experience: str) -> str:
    return (
        f"You are an interview difficulty analyzer.\n\n"
        f"Candidate: {experience} applying for {job_role} at a top IT company.\n\n"
        "Provide:\n"
        "1. OVERALL DIFFICULTY: Easy / Medium / Hard\n"
        "2. ROUND-WISE DIFFICULTY: Technical X/10 | HR X/10 | Managerial X/10\n"
        "3. MOST CHALLENGING TOPICS for this role (3-4 bullet points)\n"
        "4. QUICK TIPS to crack this interview (3-5 bullet points)\n\n"
        "Be direct and honest."
    )

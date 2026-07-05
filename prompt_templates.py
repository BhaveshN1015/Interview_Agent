def get_interview_questions_prompt(job_role: str, experience: str, skills: str) -> str:
    return f"""You are an expert interview coach with 15 years of experience preparing candidates for top IT companies like TCS, Infosys, Wipro, and Accenture.

A candidate needs interview preparation for the following profile:
- Job Role: {job_role}
- Experience Level: {experience}
- Key Skills: {skills}

Generate a structured interview preparation guide with the following sections:

1. TECHNICAL QUESTIONS (5 questions)
For each question provide:
- Question
- Model Answer
- Key Points to Cover

2. HR/BEHAVIORAL QUESTIONS (3 questions)
For each question provide:
- Question
- Model Answer using STAR format (Situation, Task, Action, Result)

3. SITUATION-BASED QUESTIONS (2 questions)
For each question provide:
- Question
- How to approach the answer

4. PREPARATION ROADMAP
- Top 5 topics to study
- Estimated time for each topic
- Resources to refer

Keep answers clear, concise and practical. Format the output in a clean readable way."""


def get_followup_prompt(question: str, previous_context: str) -> str:
    return f"""You are an expert interview coach. 

Previous interview preparation context:
{previous_context}

The candidate is asking a follow-up question:
{question}

Provide a helpful, detailed response to assist the candidate in their interview preparation.
Keep the response practical and easy to understand."""


def get_resume_based_prompt(job_role: str, experience: str, resume_text: str) -> str:
    return f"""You are an expert interview coach and resume analyzer.

Analyze this candidate's resume and generate personalized interview questions:

Job Role Applied For: {job_role}
Experience Level: {experience}

Resume Content:
{resume_text}

Based on the resume above, generate:

1. PERSONALIZED TECHNICAL QUESTIONS (5 questions)
- Questions based specifically on the candidate's projects and skills mentioned in resume
- For each: Question + Model Answer + What interviewer is looking for

2. RESUME-BASED HR QUESTIONS (3 questions)
- Questions about their specific experience and achievements
- For each: Question + Strong Answer Template

3. POTENTIAL WEAK AREAS (2 points)
- Gaps or areas the interviewer might probe
- How to address them confidently

4. CANDIDATE STRENGTHS TO HIGHLIGHT (3 points)
- Based on the resume, what to emphasize in the interview

Keep all answers tailored to the actual resume content provided."""


def get_difficulty_rating_prompt(job_role: str, experience: str) -> str:
    return f"""You are an interview difficulty analyzer.

For a {experience} candidate applying for {job_role} position at a top IT company:

Provide:
1. OVERALL DIFFICULTY: (Easy / Medium / Hard)
2. ROUND-WISE DIFFICULTY:
   - Technical Round: X/10
   - HR Round: X/10  
   - Managerial Round: X/10
3. MOST CHALLENGING TOPICS for this role
4. QUICK TIPS to crack this interview in 3-5 bullet points

Be direct and honest in your assessment."""

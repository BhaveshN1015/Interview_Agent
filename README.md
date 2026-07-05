<div align="center">

# 🎯 ARIA — AI Readiness Interview Agent

### *Your Personal AI-Powered Interview Coach*

[![IBM watsonx](https://img.shields.io/badge/IBM-watsonx.ai-0530AD?style=for-the-badge&logo=ibm&logoColor=white)](https://www.ibm.com/watsonx)
[![IBM Orchestrate](https://img.shields.io/badge/IBM-watsonx%20Orchestrate-0530AD?style=for-the-badge&logo=ibm&logoColor=white)](https://www.ibm.com/products/watsonx-orchestrate)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**IBM SkillsBuild AICTE Internship 2026 | Problem Statement #22**

---

> *"Don't just prepare for interviews — simulate them with AI"*

---

</div>

## 📌 Table of Contents
- [About ARIA](#-about-aria)
- [Demo](#-demo)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Resume Impact](#-resume-impact)

---

## 🤖 About ARIA

**ARIA (AI Readiness Interview Agent)** is an intelligent conversational agent that conducts personalized mock interviews for job seekers targeting top IT companies like **TCS, Infosys, Wipro, Accenture, and Cognizant**.

Unlike generic interview prep tools, ARIA:
- Conducts **structured multi-round interviews** (Technical → HR → Situational)
- **Evaluates your answers** in real-time with scores and feedback
- **Adapts difficulty** based on your performance
- Tracks **Confidence Growth** from start to end (unique feature)
- Generates a **Final Report Card** with a 7-day study roadmap

Built using **IBM Granite LLM** via **IBM watsonx.ai** and deployed as an agent on **IBM watsonx Orchestrate**.

---

## 🎬 Demo

> 📺 **Watch the full demo on YouTube:**

[![ARIA Demo](https://img.shields.io/badge/▶%20Watch%20Demo-YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtube.com)

> *(Add your YouTube Studio link here after recording your demo)*

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎯 **Role-Based Questions** | Tailored questions for any IT role and company |
| 📊 **Real-Time Evaluation** | Score + feedback after every answer |
| 💡 **Confidence Tracking** | Measures confidence growth from start to end |
| 🔄 **Adaptive Difficulty** | Questions get harder as you improve |
| 📋 **Final Report Card** | Overall score, strengths, weak areas |
| 🗺️ **7-Day Study Roadmap** | Personalized preparation plan |
| 💬 **Multi-Turn Chat** | Natural conversational interview flow |
| 🏢 **Multi-Company Support** | TCS, Infosys, Wipro, Accenture, Cognizant |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           User (Browser)                    │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│         Streamlit Frontend (app.py)         │
│         localhost:8501                      │
└──────────────────┬──────────────────────────┘
                   │  HTTP POST /chat
┌──────────────────▼──────────────────────────┐
│         FastAPI Backend (main.py)           │
│         localhost:8000                      │
│         ARIA Behavior Prompt Engine         │
└──────────────────┬──────────────────────────┘
                   │  REST API
┌──────────────────▼──────────────────────────┐
│         IBM watsonx.ai                      │
│         Meta Llama 3.3 70B Instruct         │
│         (via ibm-watsonx-ai SDK)            │
└─────────────────────────────────────────────┘
         +
┌─────────────────────────────────────────────┐
│         IBM watsonx Orchestrate             │
│         ARIA Agent (Deployed)               │
│         RaAct reasoning + Memory            │
└─────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Meta Llama 3.3 70B via IBM watsonx.ai |
| **Agent Platform** | IBM watsonx Orchestrate |
| **Backend** | FastAPI + Uvicorn |
| **Frontend** | Streamlit |
| **SDK** | ibm-watsonx-ai |
| **Language** | Python 3.10+ |
| **Hosting** | IBM Cloud Lite (Free) |

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- IBM Cloud account (free at cloud.ibm.com)
- IBM watsonx.ai project + API key

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

# 4. Create .env file
cp .env.example .env
# Add your IBM credentials to .env
```

### Environment Variables

Create a `.env` file in the root folder:

```env
IBM_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_watsonx_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

---

## 🚀 Usage

Open **two terminals** with the virtual environment active:

**Terminal 1 — Start Backend:**
```bash
ml\Scripts\activate
uvicorn main:app --reload
```

**Terminal 2 — Start Frontend:**
```bash
ml\Scripts\activate
streamlit run app.py
```

Open your browser at `http://localhost:8501`

**Interview Flow:**
1. Click **"Start New Interview"**
2. Tell ARIA your name, role, skills, target company
3. Rate your confidence (1-10)
4. Complete Technical → HR → Situational rounds
5. Receive your **Final Report Card** 🎯

---

## 📁 Project Structure

```
interview-trainer/
│
├── main.py                  # FastAPI backend + ARIA behavior prompt
├── app.py                   # Streamlit frontend UI
├── watsonx_client.py        # IBM watsonx.ai connection
├── prompt_templates.py      # Prompt engineering templates
├── sample_prompts.py        # Sample interview conversations
├── requirements.txt         # Python dependencies
├── .env                     # API keys (never push to GitHub)
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

<div align="center">

**Built with ❤️ using IBM Granite & watsonx.ai**

[![IBM SkillsBuild](https://img.shields.io/badge/IBM-SkillsBuild%20AICTE%202026-0530AD?style=for-the-badge&logo=ibm&logoColor=white)](https://skillsbuild.org)

</div>

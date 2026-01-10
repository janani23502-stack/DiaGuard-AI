# Dia-Guard: AI Health Companion for Chronic Disease Management 🛡️

## 1. Project Overview
**Dia-Guard** is an AI-powered health agent designed to assist IT professionals and individuals in managing chronic conditions like **Hypertension (BP)** and **Diabetes**. 

Unlike simple tracking apps, Dia-Guard acts as an **intelligent agent** that perceives user data, reasons to create personalized plans, and acts by speaking advice and executing safety alerts.

## 2. Key Features (Agentic Capabilities)
### 🧠 Perception & Context Awareness
- **Vitals Logging**: Users input Blood Pressure and Glucose levels in the **Trends** tab.
- **Memory**: The Agent *remembers* these values across different tabs (Chat, Planner) to provide context-aware advice.

### 🛠️ Reasoning & Dynamic Planning
- **Dynamic Weekly Planner**: Instead of a static template, the AI generates a *unique* 7-day schedule (Diet, Exercise, Stress) based on the specific vitals logged.
- **Daily Tasks & Solutions**: Generates 5 specific daily tasks with actionable "Solutions" (e.g., "How to reduce sodium today") tailored to the user's condition.

### 🚨 Active Monitoring & Safety
- **Clinical Alerts**: Automatically detects dangerous values (e.g., BP > 180/120) and triggers a **Red Alert** + **Voice Warning**.
- **Safety Guidelines**: Strictly follows ADA (Diabetes) and AHA (Heart) guidelines.

### 🗣️ Autonomous Action
- **Voice Output**: The Agent automatically speaks its plans, advice, and alerts using Text-to-Speech (gTTS), making it an active companion interaction.

### 🛡️ Privacy & Security
- **Data Privacy**: Uses synthetic logs for demonstration; no real PHI is stored permanently.
- **Secure AI**: Powered by Llama 3 (via Groq) with secure API integration.

## 3. Technology Stack
- **Frontend**: Streamlit (Python) - *Pure Python UI*
- **AI Engine**: Llama 3 (via Groq API) - *High-performance reasoning*
- **Voice**: gTTS (Google Text-to-Speech) - *Audio feedback*
- **Data Handling**: Pandas & Session State - *Log management*

## 4. Project Structure
- `app.py`: Main application logic and UI.
- `utils.py`: Helper functions for AI connectivity and Voice generation.
- `prompts.py`: System Prompts defining the "Dia-Guard" persona and safety rules.
- `requirements.txt`: List of dependencies.
- `start.bat`: One-click startup script for Windows.

## 5. User Guide
1.  **Launch**: Double-click `start.bat`.
2.  **Tab 4 (Trends & Logs)**: Start here. Log your BP (e.g., 130/85) and Sugar (e.g., 110).
3.  **Tab 2 (Daily Tasks & Plan)**: Click "Generate Today's Tasks". The AI will read your logged vitals and create a custom plan.
4.  **Tab 1 (AI Doctor)**: Ask any question. The Agent knows your context.
5.  **Tab 3 (Funny Tasks)**: Get a stress-busting activity.

## 6. Clinical Thresholds (Reference)
- **Normal**: BP < 120/80, Sugar < 100
- **Elevated**: BP 120-129/<80
- **High (Stage 1)**: BP 130-139/80-89
- **Critical Alert**: BP > 180/120 or Sugar > 300 (Call Doctor)

---
*Created by [ℂ𝕣𝕖𝕒𝕥𝕖𝕕 𝕓𝕪 |𝕁𝔸𝕊|𝕊𝕀𝕍𝔸]*

import pandas as pd
import json

# Load synthetic patient data
data = pd.read_csv("sample_logs.csv")

# Guideline-based thresholds (simplified)
GLUCOSE_LIMIT = 150
BP_SYS_LIMIT = 140

# Analyze weekly trends
high_glucose_days = data[data["glucose"] > GLUCOSE_LIMIT].shape[0]
high_bp_days = data[data["bp_systolic"] > BP_SYS_LIMIT].shape[0]

insights = []
alerts = []

if high_glucose_days >= 3:
    insights.append("Glucose levels are frequently above recommended range.")
    alerts.append("Please consult a healthcare professional for glucose management.")

if high_bp_days >= 3:
    insights.append("Blood pressure frequently exceeds safe limits.")
    alerts.append("Medical consultation recommended for blood pressure control.")

# Updated care plan
updated_plan = {
    "daily_tasks": [
        "Check glucose twice daily",
        "Check blood pressure once daily",
        "30-minute physical activity",
        "Follow low sugar and low sodium diet"
    ]
}

# Multilingual motivational messages
def motivational_message(language="en"):
    messages = {
        "en": "Great job staying consistent! Small steps lead to better health.",
        "hi": "आप अच्छा कर रहे हैं! छोटे कदम बड़े स्वास्थ्य लाभ लाते हैं।",
        "ta": "நீங்கள் சிறப்பாக செய்கிறீர்கள்! சிறிய முயற்சிகள் பெரிய மாற்றங்களை உருவாக்கும்."
    }
    return messages.get(language, messages["en"])

# Structured output (agentic-style)
output = {
    "weekly_insights": insights,
    "alerts": alerts,
    "updated_plan": updated_plan,
    "motivation": motivational_message("en"),
    "safety_note": "This is not medical advice. Consult a healthcare professional."
}

print(json.dumps(output, indent=2))

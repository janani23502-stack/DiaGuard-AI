import streamlit as st
import utils
import prompts
import time

# Set Page Config
st.set_page_config(page_title="Dia-Guard AI", page_icon="🛡️", layout="wide")

# Custom CSS for aesthetic improvements
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .big-emoji {
        font-size: 4rem;
        text-align: center;
        display: block;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for API Key
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=100)
    st.title("Configuration")
    
    # Llama 3 Setup via Groq
    api_key = "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"
    
    if api_key:
        st.success("Llama 3 Connected")
        
    st.markdown("---")
    with st.expander("ℹ️ Project Goals"):
        st.markdown("""
        **Dia-Guard Mission:**
        - **Goal:** Help patients follow chronic care plans.
        - **Safety:** Not a medical diagnosis (ADA/AHA guidelines).
        - **Privacy:** Synthetic data logs.
        - **Agentic Features:**
            - 🧠 **Memory:** Remembers your Vitals across tabs.
            - 🛠️ **Planning:** Generates Weekly Plans dynamically.
            - 🚨 **Reasoning:** Detects trends and Alerts you.
            - 🗣️ **Action:** Speaks advice automatically.
        """)
        
    st.markdown("---")
    with st.expander("⚠️ Clinical Thresholds"):
        st.error("🚨 Call Doctor Immediately if:")
        st.write("- **Systolic BP** > 180 mmHg")
        st.write("- **Diastolic BP** > 120 mmHg")
        st.write("- **Blood Sugar** > 300 mg/dL")
        st.warning("⚠️ Consult Doctor if:")
        st.write("- **BP** > 140/90 consistently")
        st.write("- **Sugar** > 180 mg/dL (fasting)")


    st.markdown("---")

# Main Header
st.markdown('<h1 class="main-header">Dia-Guard 🛡️: Chronic Care AI</h1>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💬 AI Doctor", "📅 Daily Plan", "🤪 Funny Tasks", "📈 Trends & Logs"])

# --- Tab 1: AI Doctor Consultation ---
with tab1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Consultation Room")
    st.write("Ask about your symptoms, diet, or stress levels. I'll explain clearly with voice.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if user_input := st.chat_input("Type your health question here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_text = utils.get_ai_response(
                    api_key, 
                    user_input, 
                    system_instruction=prompts.DOCTOR_SYSTEM_PROMPT
                )
                st.markdown(response_text)
                
                # Voice Output (Auto-Play)
                if api_key and "Error" not in response_text:
                    audio_fp = utils.text_to_speech_audio(response_text)
                    if audio_fp:
                        st.audio(audio_fp, format='audio/mp3', start_time=0)
        
        st.session_state.messages.append({"role": "assistant", "content": response_text})
    st.markdown('</div>', unsafe_allow_html=True)

# --- Tab 2: Dynamic Weekly Planner ---
with tab2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📅 Personalized Weekly Care Plan")
    
    # Check if vitals exist in session state (Agent Memory)
    current_bp = st.session_state.get('last_bp', 'Not Logged')
    current_sugar = st.session_state.get('last_sugar', 'Not Logged')
    
    st.info(f"**Agent Context Awareness:** Planning based on BP: {current_bp} | Glucose: {current_sugar}")
    
    if st.button("✨ Generate Weekly Plan with Agent"):
        if api_key:
            with st.spinner("Agent is reasoning & planning..."):
                plan_prompt = f"""
                Create a 7-Day Care Plan for a user with BP {current_bp} and Glucose {current_sugar}.
                Include:
                1. Diet (Indian/Global options).
                2. Exercises (Provide YouTube Search Link format: [Exercise Name](https://www.youtube.com/results?search_query=Exercise+Name)).
                3. Warning Signs to watch.
                """
                plan_response = utils.get_ai_response(api_key, plan_prompt, system_instruction=prompts.DOCTOR_SYSTEM_PROMPT)
                st.markdown(plan_response)
                
                # Auto-Voice for Plan Summary
                summary_text = "I have generated your weekly plan based on your vitals. Please check the diet and exercise links below."
                audio_fp = utils.text_to_speech_audio(summary_text)
                if audio_fp:
                    st.audio(audio_fp, format='audio/mp3', start_time=0)
        else:
            st.warning("Please configure API Key.")
            
    st.markdown("---")
    st.subheader("✅ Daily Tasks Checklist")
    cols = st.columns(4)
    tasks = ["💊 Take Meds", "🥤 Hydrate (2L)", "🚶 Walk 30 Mins", "🩺 Check Vitals"]
    for i, task in enumerate(tasks):
        with cols[i]:
            if st.checkbox(task, key=f"daily_{i}"):
                st.caption("Done! 🎉")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Tab 3: Funny AI Tasks ---
with tab3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Stress Buster: The Funny Task Generator")
    st.write("Sitting too long? Let's get moving with something ridiculous!")
    
    if st.button("🎲 Generate Funny Task"):
        if api_key:
            with st.spinner("Cooking up something silly..."):
                task = utils.get_ai_response(api_key, "Give me one funny physical task.", system_instruction=prompts.FUNNY_TASK_PROMPT)
                st.markdown(f'<div class="big-emoji">🤪</div>', unsafe_allow_html=True)
                st.markdown(f"### {task}")
                
                # Speak the task
                audio_fp = utils.text_to_speech_audio(task)
                if audio_fp:
                    st.audio(audio_fp, format='audio/mp3', start_time=0)
        else:
            st.warning("Please enter your API Key first.")
    
    st.markdown("#### Why do this?")
    st.write("Laughter and movement lower blood pressure and reduce cortisol (stress hormone). Plus, your colleagues need a laugh!")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Tab 4: Trends & Logs ---
with tab4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Health Trends & Vitals Log")
    st.info("Visualizing your progress over time (Mock Data for Demonstration).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Input Today's Vitals")
        bp = st.text_input("Blood Pressure (e.g. 150/95)")
        sugar = st.number_input("Fasting Glucose (mg/dL)", value=100)
        
        if st.button("Log Vitals & Analyze"):
            # Save to Memory (Session State)
            st.session_state['last_bp'] = bp
            st.session_state['last_sugar'] = sugar
            
            # Alert Logic
            alert_msg = ""
            try:
                sys = int(bp.split('/')[0]) if '/' in bp else 0
                if sys > 140 or sugar > 180:
                    alert_msg = f"⚠️ CRITICAL ALERT: High Vitals Detected (BP {bp}, Sugar {sugar})! Consult Doctor Immediately."
                    st.error(alert_msg)
                else:
                    st.success(f"Logged: BP {bp}, Glucose {sugar} mg/dL (Normal Range)")
                    alert_msg = "Vitals Logged. Readings appear stable. Keep it up!"
            except:
                st.warning("Invalid BP format. Use 120/80.")
            
            # Voice Alert
            if alert_msg:
                audio_fp = utils.text_to_speech_audio(alert_msg)
                if audio_fp:
                    st.audio(audio_fp, format='audio/mp3', start_time=0)
            
    with col2:
        st.markdown("#### Weekly Trend Analysis")
        # Synthetic Data for demonstration
        import pandas as pd
        import numpy as np
        
        chart_data = pd.DataFrame(
            np.random.randint(90, 140, size=(7, 2)),
            columns=['Glucose', 'Systolic BP']
        )
        st.line_chart(chart_data)
        st.caption("Last 7 Days: Glucose vs BP Trends")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("### ⚠️ Medical Disclaimer")
st.caption("This AI Assistant provides information for educational and motivational purposes only. It does not replace professional medical advice, diagnosis, or treatment. Always consult your doctor.")

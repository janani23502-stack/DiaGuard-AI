# ================= IMPORTS =================
import streamlit as st
import pandas as pd
import datetime
import os
import hashlib
import pyttsx3

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Patient Health Monitoring System",
    page_icon="🩺",
    layout="wide"
)

# ================= VOICE SETUP =================
engine = pyttsx3.init()

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

# ================= SECURITY (PASSWORD HASH) =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ================= FILE STORAGE =================
USER_FILE = "users.csv"
DATA_FILE = "patient_data.csv"

if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["Username", "PasswordHash"]).to_csv(USER_FILE, index=False)

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=[
        "Username", "Date", "Age",
        "BP_Sys", "BP_Dia",
        "Glucose", "HeartRate", "Temperature"
    ]).to_csv(DATA_FILE, index=False)

users_df = pd.read_csv(USER_FILE)
data_df = pd.read_csv(DATA_FILE)

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# ================= ALERT SYSTEM =================
def show_alerts(bp_sys, bp_dia, glucose):
    alert = ""

    if bp_sys >= 140 or bp_dia >= 90:
        st.error("High Blood Pressure (Hypertension)")
        alert += "High blood pressure detected. "

    elif bp_sys < 90 or bp_dia < 60:
        st.warning("Low Blood Pressure")
        alert += "Low blood pressure detected. "

    if glucose >= 200:
        st.error("High Blood Sugar (Diabetes)")
        alert += "High blood sugar detected. "

    if alert == "":
        st.success("Vitals are normal")
        alert = "Vitals are normal."

    speak(alert)

# ================= LOGIN / SIGNUP =================
st.title("DiaGuard-AI")

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("Login")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            hashed = hash_password(p)
            match = users_df[
                (users_df["Username"] == u) &
                (users_df["PasswordHash"] == hashed)
            ]

            if not match.empty:
                st.session_state.logged_in = True
                st.session_state.username = u
                speak("Login successful")
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        st.subheader("Create Account")
        nu = st.text_input("New Username")
        np = st.text_input("New Password", type="password")

        if st.button("Register"):
            if nu in users_df["Username"].values:
                st.warning("Username already exists")
            else:
                users_df.loc[len(users_df)] = [nu, hash_password(np)]
                users_df.to_csv(USER_FILE, index=False)
                st.success("Account created successfully")
                speak("Account created successfully")

# ================= MAIN APP =================
else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # ================= INPUT VITALS =================
    st.header("Patient Vitals Entry")

    age = st.number_input("Age", 1, 120, 30)
    bp_sys = st.number_input("Systolic BP", 70, 200, 120)
    bp_dia = st.number_input("Diastolic BP", 40, 150, 80)
    glucose = st.number_input("Blood Glucose", 50, 400, 120)
    heart_rate = st.number_input("Heart Rate", 40, 200, 72)
    temperature = st.number_input("Temperature (C)", 30.0, 45.0, 37.0)

    if st.button("Save Vitals"):
        new_row = {
            "Username": st.session_state.username,
            "Date": datetime.date.today(),
            "Age": age,
            "BP_Sys": bp_sys,
            "BP_Dia": bp_dia,
            "Glucose": glucose,
            "HeartRate": heart_rate,
            "Temperature": temperature
        }

        data_df = pd.concat([data_df, pd.DataFrame([new_row])], ignore_index=True)
        data_df.to_csv(DATA_FILE, index=False)

        st.success("Vitals saved")
        show_alerts(bp_sys, bp_dia, glucose)

    # ================= FILTER & GRAPH =================
    st.header("Patient History")

    user_data = data_df[data_df["Username"] == st.session_state.username]
    user_data["Date"] = pd.to_datetime(user_data["Date"])

    if not user_data.empty:
        start = st.date_input("Start Date", user_data["Date"].min().date())
        end = st.date_input("End Date", user_data["Date"].max().date())

        filtered = user_data[
            (user_data["Date"] >= pd.to_datetime(start)) &
            (user_data["Date"] <= pd.to_datetime(end))
        ]

        st.dataframe(filtered)

        st.subheader("Systolic BP Trend")
        st.line_chart(filtered.set_index("Date")["BP_Sys"])

    # ================= EDUCATION =================
    st.header("Health Education")

    condition = st.selectbox(
        "Select Condition",
        ["Low Blood Pressure", "Hypertension", "Diabetes"]
    )

    if condition == "Low Blood Pressure":
        st.write("Symptoms: dizziness, fatigue, fainting")
        st.write("Exercises: walking, stretching")
        st.video("https://www.youtube.com/watch?v=QYFDhVN32lU")

    elif condition == "Hypertension":
        st.write("Symptoms: headache, chest pain")
        st.write("Exercises: walking, yoga")
        st.video("https://www.youtube.com/watch?v=4O2xCR2gFhg")

    else:
        st.write("Symptoms: thirst, fatigue")
        st.write("Exercises: walking, resistance training")
        st.video("https://www.youtube.com/watch?v=oC3L6mU4g1M")

# ================= FOOTER =================
st.markdown("""
---
ℂ𝕣𝕖𝕒𝕥𝕖𝕕 𝕓𝕪 | 𝕁𝔸𝕊|𝕊𝕀𝕍𝔸 |
""")

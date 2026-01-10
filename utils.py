from groq import Groq
import streamlit as st
from gtts import gTTS
import io

def get_ai_response(api_key, prompt, system_instruction=None):
    """
    Fetches a response from Groq (Llama 3).
    """
    if not api_key:
        return "Please enter your valid Groq API Key in the sidebar to proceed."
    
    try:
        client = Groq(api_key=api_key)
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})
        
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error communicating with Llama (Groq): {str(e)}"

def text_to_speech_audio(text):
    """
    Converts text to speech and returns the audio bytes.
    """
    if not text:
        return None
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp
    except Exception as e:
        st.error(f"Audio generation error: {e}")
        return None

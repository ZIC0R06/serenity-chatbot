
import streamlit as st
import ollama
import base64
from pathlib import Path

st.set_page_config(page_title="Serene Ai")



BACKGROUND_IMAGE = "hello.jpg"
if not Path(BACKGROUND_IMAGE).exists():
    st.error(f"Missing background image: {BACKGROUND_IMAGE}")
    st.stop()


# Background setup
def get_base64(background):
    with open(background, "rb") as f:
        return base64.b64encode(f.read()).decode()


bin_str = get_base64(BACKGROUND_IMAGE)
st.markdown(f"""
    <style>
        .main {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []


# Model configuration
MODEL_NAME = "llama3:8b"  

#fine tune the model
def handle_ollama_error(e):
    st.error(f"Error connecting to Ollama: {str(e)}")
    st.info("Please ensure Ollama is running and the model is installed")
    return "I'm having trouble connecting. Please try again later."

def generate_response(user_input):
    try:
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
       
        response = ollama.chat(
            model=MODEL_NAME,
            messages=st.session_state.conversation_history
        )
       
        ai_response = response['message']['content']
        st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})
        return ai_response
    except Exception as e:
        return handle_ollama_error(e)


def generate_affirmation():
    try:
        prompt = "Provide a positive affirmation to encourage someone feeling stressed or overwhelmed"
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return handle_ollama_error(e)


def generate_meditation_guide():
    try:
        prompt = "Provide a 5-minute guided meditation script to help relax and reduce stress"
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return handle_ollama_error(e)
    


# UI Components
st.title("Serene Ai")


# Display conversation history
for msg in st.session_state.conversation_history:
    role = "You" if msg['role'] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")


# User input
user_message = st.text_input("How can I help you today?", key="user_input")


# Handle main conversation
if user_message:
    with st.spinner("Thinking..."):
        ai_response = generate_response(user_message)
        st.markdown(f"**AI:** {ai_response}")


# Additional features
col1, col2 = st.columns(2)


with col1:
    if st.button("Give me a positive affirmation"):
        affirmation = generate_affirmation()
        st.session_state.conversation_history.extend([
            {"role": "user", "content": "Requested affirmation"},
            {"role": "assistant", "content": affirmation}
        ])
        st.markdown(f"**Affirmation:** {affirmation}")


with col2:
    if st.button("Give me a guided meditation"):
        meditation = generate_meditation_guide()
        st.session_state.conversation_history.extend([
            {"role": "user", "content": "Requested meditation"},
            {"role": "assistant", "content": meditation}
        ])
        st.markdown(f"**Guided Meditation:** {meditation}")



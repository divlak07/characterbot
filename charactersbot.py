import streamlit as st
import ollama
import random
import time

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Batman Chatbot 🦇", layout="wide")

# Gotham-style dark background + slide-in + hover effects
st.markdown("""
<style>
body {
    background-color: #0D0D0D;
    color: #FFFFFF;
    font-family: 'Arial', sans-serif;
}

.slide-in {
    animation: slide-in 0.5s ease-out;
}

@keyframes slide-in {
    from { transform: translateX(-100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.message:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #FFD700;
    transition: all 0.2s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#FFD700;'>🦇 Batman Chatbot</h1>", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    model = st.selectbox("Choose model", ["gemma3:latest"])
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
    if st.button("🧹 Clear chat"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Session Memory
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

batman_colors = ["#1C1C1C", "#2F4F4F", "#000000"]  # Gotham dark
batman_prefixes = [
    "Justice will prevail 🦇",
    "I am vengeance ⚡",
    "In the shadows… 🌃",
    "The night is my ally 🕶️"
]

# -----------------------------
# Render Messages with Effects
# -----------------------------
def render_message(role, content):
    if role == "user":
        color = "#4682B4"
        align = "right"
        emoji = "💬"
        font_family = "Arial"
        box_shadow = "0 0 5px #4682B4"
        extra_class = "message"
    else:
        color = random.choice(batman_colors)
        align = "left"
        emoji = "🦇"
        font_family = "'Courier New', monospace"
        box_shadow = "0 0 12px #FFD700"
        prefix = random.choice(batman_prefixes)
        content = f"{prefix}: {content}"
        extra_class = "slide-in message"

    st.markdown(f"""
    <div class="{extra_class}" style="
        background-color:{color};
        color:#FFFFFF;
        padding:14px 20px;
        border-radius:15px;
        margin:5px;
        text-align:{align};
        max-width:75%;
        font-weight:bold;
        font-family:{font_family};
        font-size:16px;
        box-shadow:{box_shadow};
    ">
        {emoji} {content}
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"])

# -----------------------------
# Chat Input with Typing Indicator
# -----------------------------
user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    render_message("user", user_input)

    with st.spinner("Batman is thinking... 🦇"):
        time.sleep(1)

    batman_prompt = [
        {"role": "system", "content": (
            "You are Batman. Speak as a serious, mysterious, and heroic detective. "
            "Use suspense, wisdom, and Gotham style. Add dramatic tone and emojis 🦇⚡🌃🕶️."
        )}
    ] + st.session_state.messages

    response = ollama.chat(model=model, messages=batman_prompt, options={"temperature": temperature})
    reply = response["message"]["content"]

    st.session_state.messages.append({"role": "assistant", "content": reply})
    render_message("assistant", reply)


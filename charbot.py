import streamlit as st
import ollama

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Steve Harrington AI", layout="wide", page_icon="🕶️")

# -----------------------------
# Advanced Retro-Synthwave CSS
# -----------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bungee&family=Inter:wght@400;700&family=Permanent+Marker&display=swap');

    /* Global Background */
    .stApp {
        background: radial-gradient(circle at top, #1a1a2e 0%, #0f0f1b 100%);
        color: #ffffff;
    }

    /* Scoops Ahoy Banner Effect */
    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0);
    }

    /* Title Styling - Neon Pink/Cyan */
    .title-text {
        font-family: 'Bungee', cursive;
        font-size: 4rem !important;
        text-align: center;
        color: #ff2e9f;
        text-shadow: 3px 3px 0px #00d4ff, 6px 6px 15px rgba(255, 46, 159, 0.7);
        margin-bottom: 0px;
    }

    .subtitle-text {
        font-family: 'Permanent Marker', cursive;
        font-size: 1.5rem;
        text-align: center;
        color: #00d4ff;
        margin-top: -10px;
        letter-spacing: 2px;
    }

    /* Chat Container Glassmorphism */
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    /* Custom Avatar Glow */
    [data-testid="stChatMessage"] img {
        border: 2px solid #ff2e9f;
        box-shadow: 0px 0px 10px #ff2e9f;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 2px solid #ff2e9f;
    }

    /* Input Field */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    
    /* Decorative Grid Floor (Synthwave Style) */
    .grid-bg {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 100px;
        background-image: 
            linear-gradient(rgba(0, 212, 255, 0.3) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 212, 255, 0.3) 1px, transparent 1px);
        background-size: 40px 40px;
        transform: perspective(100px) rotateX(60deg);
        z-index: -1;
    }
</style>
<div class="grid-bg"></div>
""", unsafe_allow_html=True)

# -----------------------------
# Visual Assets
# -----------------------------
# Icons for the chat
STEVE_AVATAR = "https://img.icons8.com/color/96/ice-cream-cone.png" # Scoops Ahoy Vibe
USER_AVATAR = "https://img.icons8.com/fluency/96/walkman.png" # 80s Walkman Vibe

# -----------------------------
# Sidebar & Controls
# -----------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/6/6f/Steve_Harrington_Stranger_Things.jpg", use_container_width=True)
    st.markdown("### 🍦 Scoops Ahoy Employee of the Month")
    st.info("Don't ask about the hair. It's Fabergé Organics. Use the hairspray, kid.")
    
    model = st.selectbox("Choose Model", ["gemma3:latest", "llama3:latest"], index=0)
    temp = st.slider("Sarcasm Level", 0.0, 1.5, 0.9)
    
    if st.button("🧹 Wipe Hawkins Memory"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Main UI
# -----------------------------
st.markdown('<p class="title-text">KING STEVE</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">"Always the goddamn babysitter."</p>', unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
        You are Steve Harrington from Stranger Things (Season 3/4 personality). 
        - You are the protective "Mom" of the group.
        - You use 80s slang like 'totally', 'gnarly', 'tubular'.
        - You are slightly protective and very sarcastic.
        - You give unsolicited advice about hair and dating.
        - Call the user 'Kid', 'Henderson', or 'Newbie'.
        - Mention your nail-bat if things get dangerous.
        - If the user asks for help, complain about being a babysitter but then help them anyway.
        """}
    ]

# Display Messages
for msg in st.session_state.messages:
    if msg["role"] == "system": continue
    avatar = STEVE_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask Steve for some dating advice... or monster fighting tips."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=STEVE_AVATAR):
        with st.spinner("Styling the hair..."):
            response = ollama.chat(
                model=model,
                messages=st.session_state.messages,
                options={"temperature": temp}
            )
            reply = response["message"]["content"]
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
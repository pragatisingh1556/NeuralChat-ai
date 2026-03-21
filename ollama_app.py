# NeuralChat - local AI chatbot using Ollama
# runs completely offline, no API keys needed
# i used streamlit because its the easiest way to build a quick UI in python

import streamlit as st
import requests

# page setup
st.set_page_config(
    page_title="NeuralChat",
    page_icon="",
    layout="wide"
)

# --- custom CSS for the dark theme ---
# using google fonts - Orbitron for headings, Rajdhani for body
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');

    * { font-family: 'Rajdhani', sans-serif; }

    /* main background - dark gradient */
    .stApp {
        background: linear-gradient(160deg, #000000 0%, #0a0010 50%, #000a10 100%);
    }

    /* header section with neon borders */
    .header {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, rgba(0,255,255,0.05), rgba(255,0,255,0.05));
        border-radius: 5px;
        border-top: 3px solid #00ffff;
        border-bottom: 3px solid #ff00ff;
        margin-bottom: 30px;
    }

    .header h1 {
        font-family: 'Orbitron', monospace;
        color: #00ffff;
        font-size: 3.5em;
        font-weight: 900;
        letter-spacing: 5px;
        text-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff;
        margin: 0;
    }

    .header p {
        color: #ff00ff;
        font-size: 1.1em;
        letter-spacing: 3px;
        text-shadow: 0 0 10px #ff00ff;
        margin-top: 10px;
    }

    /* chat message styling */
    .stChatMessage {
        background: rgba(0,255,255,0.03) !important;
        border: 1px solid rgba(0,255,255,0.15);
        border-left: 3px solid #00ffff;
        padding: 5px;
        margin: 8px 0;
    }

    /* sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000000, #0a0010);
        border-right: 2px solid #00ffff;
        box-shadow: 5px 0 15px rgba(0,255,255,0.1);
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    .sidebar-logo {
        text-align: center;
        padding: 20px 0;
        font-family: 'Orbitron', monospace;
        font-size: 1.4em;
        font-weight: 900;
        color: #00ffff !important;
        letter-spacing: 3px;
        text-shadow: 0 0 10px #00ffff;
        border-bottom: 1px solid rgba(0,255,255,0.3);
        margin-bottom: 20px;
    }

    /* stats cards in the sidebar */
    .stat-card {
        background: rgba(0,255,255,0.05);
        border: 1px solid rgba(0,255,255,0.2);
        border-left: 3px solid #00ffff;
        padding: 10px 15px;
        margin: 8px 0;
        display: flex;
        justify-content: space-between;
        letter-spacing: 1px;
    }

    .stat-value {
        color: #ff00ff !important;
        font-weight: 600;
        text-shadow: 0 0 5px #ff00ff;
    }

    .stat-label { color: #ffffff !important; }

    .feature-item {
        padding: 8px 0;
        color: #ffffff !important;
        font-size: 0.9em;
        border-bottom: 1px solid rgba(0,255,255,0.1);
        letter-spacing: 1px;
    }

    /* button styling - neon cyan border with glow */
    .stButton button {
        background: transparent !important;
        color: #00ffff !important;
        border: 2px solid #00ffff !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        letter-spacing: 2px !important;
        padding: 10px !important;
        text-shadow: 0 0 10px #00ffff !important;
        box-shadow: 0 0 10px rgba(0,255,255,0.2) !important;
    }

    /* chat input box */
    .stChatInput input {
        background: rgba(0,255,255,0.05) !important;
        border: 1px solid rgba(0,255,255,0.3) !important;
        color: #ffffff !important;
        letter-spacing: 1px !important;
    }

    /* section titles in sidebar */
    .section-title {
        color: #00ffff !important;
        font-size: 0.75em !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        font-weight: 700 !important;
        margin: 20px 0 10px 0 !important;
        font-family: 'Orbitron', monospace !important;
    }

    /* dropdown/selectbox styling */
    .stSelectbox > div > div {
        background-color: #0a0010 !important;
        border: 1px solid rgba(0,255,255,0.3) !important;
        color: #00ffff !important;
    }

    .stSelectbox > div > div > div {
        color: #00ffff !important;
    }

    .stSelectbox svg { fill: #00ffff !important; }

    div[data-baseweb="popover"] {
        background-color: #0a0010 !important;
    }
    div[data-baseweb="menu"] {
        background-color: #0a0010 !important;
    }
    li[role="option"] {
        background-color: #0a0010 !important;
        color: #00ffff !important;
    }
    li[role="option"]:hover {
        background-color: #00ffff !important;
        color: #000000 !important;
    }

    /* text colors */
    .stChatMessage p { color: #ffffff !important; }
    p, label, div { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)


# --- header section ---
st.markdown("""
    <div class="header">
        <h1>NEURALCHAT</h1>
        <p>LOCAL NEURAL NETWORK -- POWERED BY LLAMA 3.2</p>
    </div>
""", unsafe_allow_html=True)


# --- sidebar - model selection, stats, features ---
with st.sidebar:
    st.markdown('<div class="sidebar-logo">NEURAL</div>', unsafe_allow_html=True)

    # model dropdown - tinyllama is good for low RAM systems
    st.markdown('<p class="section-title">System Config</p>', unsafe_allow_html=True)
    model = st.selectbox("AI Core", ["tinyllama", "llama3.2", "gemma3:4b", "mistral"])

    # temperature = how random/creative the response is
    # low = factual, high = creative
    creativity = st.selectbox("Creativity Level", ["Low (0.3)", "Medium (0.7)", "High (1.0)"])
    if "Low" in creativity:
        temperature = 0.3
    elif "High" in creativity:
        temperature = 1.0
    else:
        temperature = 0.7

    # shows how many messages have been sent so far
    st.markdown('<p class="section-title">Live Metrics</p>', unsafe_allow_html=True)
    messages_count = len(st.session_state.get('messages', []))

    st.markdown(f"""
        <div class="stat-card">
            <span class="stat-label">SYSTEM</span>
            <span class="stat-value">ONLINE</span>
        </div>
        <div class="stat-card">
            <span class="stat-label">NETWORK</span>
            <span class="stat-value">OFFLINE</span>
        </div>
        <div class="stat-card">
            <span class="stat-label">QUERIES</span>
            <span class="stat-value">{messages_count}</span>
        </div>
        <div class="stat-card">
            <span class="stat-label">SECURITY</span>
            <span class="stat-value">MAX</span>
        </div>
    """, unsafe_allow_html=True)

    # just listing what the app can do
    st.markdown('<p class="section-title">Capabilities</p>', unsafe_allow_html=True)
    st.markdown("""
        <div class="feature-item">No internet required</div>
        <div class="feature-item">No API key needed</div>
        <div class="feature-item">Data never leaves device</div>
        <div class="feature-item">Powered by Ollama</div>
        <div class="feature-item">Free forever</div>
    """, unsafe_allow_html=True)

    # button to reset the conversation
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("CLEAR SYSTEM", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# --- chat section ---

# create empty list to store messages if first time loading
if "messages" not in st.session_state:
    st.session_state.messages = []

# show all old messages from the session
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# wait for user to type something
prompt = st.chat_input("Enter your query...")

if prompt:
    # show the user's message on screen
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # send the prompt to ollama running on localhost
    with st.chat_message("assistant"):
        with st.spinner("Processing query..."):
            try:
                # ollama runs on port 11434 by default
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": temperature}
                    },
                    timeout=120
                )
                data = response.json()

                # sometimes ollama gives an error if model is too big for RAM
                if "error" in data:
                    st.error("Ollama error: " + data["error"])
                else:
                    answer = data["response"]
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to Ollama. Make sure Ollama is running on your machine.")
            except requests.exceptions.Timeout:
                st.error("Request timed out. The model is taking too long. Try a shorter query.")
            except Exception as err:
                st.error("Something went wrong: " + str(err))

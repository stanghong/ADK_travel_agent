import streamlit as st
import requests
from google.adk.agents import Agent

API_URL = "http://localhost:8000"

st.title("🌍 Travel Assistant Chatbot")

if "session_id" not in st.session_state:
    st.session_state.session_id = None
    st.session_state.messages = []
if "pending_input" not in st.session_state:
    st.session_state.pending_input = ""

# Start session button
if st.button("Start New Travel Session"):
    resp = requests.post(f"{API_URL}/start_session", json={"user_id": "traveler"})
    if resp.status_code == 200:
        data = resp.json()
        st.session_state.session_id = data["session_id"]
        st.session_state.messages = []
        st.success(f"Travel session started: {data['session_id']}")
    else:
        st.error("Failed to start travel session.")

send_disabled = st.session_state.session_id is None

# Always show input box, send on Enter
def send_message():
    user_input = st.session_state.pending_input
    if user_input.strip() and not send_disabled:
        st.session_state.messages.append(("user", user_input))
        payload = {
            "session_id": st.session_state.session_id,
            "user_id": "traveler",
            "message": user_input,
        }
        with st.spinner("Travel Assistant is thinking..."):
            resp = requests.post(f"{API_URL}/send_message", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                agent_response = data["response"]
                st.session_state.messages.append(("agent", agent_response))
            else:
                st.session_state.messages.append(("agent", "[Error: Failed to get response]"))
        st.session_state.pending_input = ""  # Clear input

# The input box triggers send_message on change (Enter)
st.text_input(
    "Where would you like to travel or what do you want to know?",
    value=st.session_state.pending_input,
    key="pending_input",
    on_change=send_message,
    disabled=send_disabled,
)

if send_disabled:
    st.info("Please start a new travel session to begin.")

# --- Chat history with scroll and latest on top ---
chat_height = 400  # px

chat_css = """
<style>
.user-bubble {
    background: #d0e6ff;
    color: #003366;
    border-radius: 12px;
    padding: 0.7em 1em;
    margin: 0.5em 0 0.5em auto;
    max-width: 80%;
    text-align: right;
    font-weight: 500;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.agent-bubble {
    background: #e6ffe6;
    color: #145214;
    border-radius: 12px;
    padding: 0.7em 1em;
    margin: 0.5em auto 0.5em 0;
    max-width: 80%;
    text-align: left;
    font-weight: 500;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
</style>
"""
st.markdown(chat_css, unsafe_allow_html=True)

# Show chat messages, latest on top
for role, msg in reversed(st.session_state.messages):
    if role == "user":
        st.markdown(f'<div class="user-bubble"><b>You:</b> {msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="agent-bubble"><b>Travel Assistant:</b> {msg}</div>', unsafe_allow_html=True) 
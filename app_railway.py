import streamlit as st
import requests
import json
from datetime import datetime
import time
import logging
from typing import Tuple
import base64
import io
from PIL import Image
import os

# Configuration - Railway Backend
RAILWAY_URL = os.getenv('RAILWAY_BACKEND_URL', 'https://your-railway-app.railway.app')
API_URL = RAILWAY_URL  # Use Railway URL
USER_ID = "test_user"

# Page configuration
st.set_page_config(
    page_title="🌍 Travel Assistant (Railway)",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for chat layout
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-bottom: 20px;
    }
    
    /* Chat container styling */
    .chat-container {
        height: calc(100vh - 200px);
        overflow-y: auto;
        padding: 20px;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        background-color: #fafafa;
        margin-bottom: 20px;
    }
    
    /* Message styling */
    .message {
        margin-bottom: 15px;
        padding: 10px 15px;
        border-radius: 15px;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    .user-message {
        background-color: #007bff;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .assistant-message {
        background-color: #e9ecef;
        color: #333;
        margin-right: auto;
    }
    
    /* Enhanced chat messages styling */
    .chat-messages {
        height: 60vh;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        background-color: #fafafa;
        margin-bottom: 20px;
        scroll-behavior: smooth;
    }
    
    .message-bubble {
        margin-bottom: 15px;
        padding: 12px 16px;
        border-radius: 18px;
        max-width: 80%;
        word-wrap: break-word;
        clear: both;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white;
        float: right;
        margin-left: 20%;
        text-align: right;
    }
    
    .assistant-bubble {
        background: linear-gradient(135deg, #ffffff, #f8f9fa);
        color: #333;
        float: left;
        margin-right: 20%;
        border: 1px solid #e9ecef;
    }
    
    .clearfix::after {
        content: "";
        clear: both;
        display: table;
    }
    
    /* Welcome message styling */
    .welcome-message {
        text-align: center;
        padding: 40px 20px;
        color: #666;
    }
    
    .welcome-message h3 {
        color: #007bff;
        margin-bottom: 20px;
    }
    
    /* Status indicator */
    .status-indicator {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .status-online {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-offline {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "backend_status" not in st.session_state:
    st.session_state.backend_status = "unknown"

def check_backend_status():
    """Check if Railway backend is online"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            st.session_state.backend_status = "online"
            return True
        else:
            st.session_state.backend_status = "offline"
            return False
    except:
        st.session_state.backend_status = "offline"
        return False

def create_session():
    """Create a new session with Railway backend"""
    try:
        response = requests.post(
            f"{API_URL}/start_session",
            json={"user_id": USER_ID},
            timeout=10
        )
        if response.status_code == 200:
            result = response.json()
            st.session_state.session_id = result.get("session_id")
            return True
        else:
            st.error(f"Failed to create session: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"Error creating session: {str(e)}")
        return False

def send_message_to_railway(message: str, photo_data: str = None):
    """Send message to Railway backend"""
    if not st.session_state.session_id:
        if not create_session():
            return "Failed to create session"
    
    try:
        payload = {
            "message": message,
            "session_id": st.session_state.session_id,
            "user_id": USER_ID
        }
        
        if photo_data:
            payload["photo_data"] = photo_data
        
        response = requests.post(
            f"{API_URL}/send_message",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "No response received")
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Connection error: {str(e)}"

def encode_image_to_base64(image):
    """Encode PIL image to base64"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Main UI
st.title("🌍 Travel Assistant (Railway Backend)")
st.markdown("---")

# Check backend status
backend_online = check_backend_status()

# Display status
if backend_online:
    st.markdown(
        f'<div class="status-indicator status-online">✅ Railway Backend Online: {API_URL}</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f'<div class="status-indicator status-offline">❌ Railway Backend Offline: {API_URL}</div>',
        unsafe_allow_html=True
    )

# Sidebar
with st.sidebar:
    st.header("🔧 Configuration")
    st.info(f"**Backend URL:** {API_URL}")
    st.info(f"**User ID:** {USER_ID}")
    
    if st.session_state.session_id:
        st.success(f"**Session ID:** {st.session_state.session_id}")
    else:
        st.warning("No active session")
    
    if st.button("🔄 Refresh Session"):
        st.session_state.session_id = None
        if create_session():
            st.success("New session created!")
        else:
            st.error("Failed to create session")
    
    st.markdown("---")
    st.header("📝 Quick Actions")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("🧪 Test Connection"):
        if backend_online:
            st.success("✅ Backend is online!")
        else:
            st.error("❌ Backend is offline!")

# Main chat area
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-message">
        <h3>🌍 Welcome to Travel Assistant!</h3>
        <p>I'm your AI travel companion powered by Railway backend.</p>
        <p><strong>I can help you with:</strong></p>
        <ul style="text-align: left; display: inline-block;">
            <li>🌤️ Weather information for any city</li>
            <li>🗺️ Tourist attractions and landmarks</li>
            <li>🍽️ Restaurant recommendations</li>
            <li>🚶 Walking routes and directions</li>
            <li>📸 Photo analysis and travel stories</li>
            <li>🕐 Current time in different timezones</li>
            <li>📝 Travel blog writing</li>
        </ul>
        <p><em>Just start chatting or upload a photo to begin!</em></p>
    </div>
    """, unsafe_allow_html=True)

# Display chat messages
if st.session_state.messages:
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f'<div class="message-bubble user-bubble clearfix">{message["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="message-bubble assistant-bubble clearfix">{message["content"]}</div>',
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📸 Upload a photo (optional)", type=['png', 'jpg', 'jpeg'])

# Chat input
if prompt := st.chat_input("Ask me about travel..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Process photo if uploaded
    photo_data = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        photo_data = encode_image_to_base64(image)
        st.session_state.messages.append({
            "role": "user", 
            "content": f"📸 [Photo uploaded: {uploaded_file.name}]"
        })
    
    # Get assistant response
    with st.spinner("🤔 Thinking..."):
        if backend_online:
            response = send_message_to_railway(prompt, photo_data)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "❌ Sorry, I'm having trouble connecting to the backend. Please check if the Railway backend is running."
            })
    
    # Clear uploaded file
    uploaded_file = None
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: #666; font-size: 12px;'>"
    f"Powered by Railway Backend | Session: {st.session_state.session_id or 'None'}"
    f"</div>",
    unsafe_allow_html=True
) 
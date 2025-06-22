import streamlit as st
import requests
import json
import base64
from PIL import Image
import io
import os
from datetime import datetime

# Configuration
RAILWAY_BACKEND_URL = os.getenv("RAILWAY_BACKEND_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="Travel Assistant - Railway Combined",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-online {
        color: #28a745;
        font-weight: bold;
    }
    .status-offline {
        color: #dc3545;
        font-weight: bold;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .upload-section {
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_backend_health():
    """Check if the backend is healthy"""
    try:
        response = requests.get(f"{RAILWAY_BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        return False, None
    except Exception as e:
        return False, None

def start_session(user_id):
    """Start a new session"""
    try:
        response = requests.post(
            f"{RAILWAY_BACKEND_URL}/start_session",
            json={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to start session: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error starting session: {str(e)}")
        return None

def send_message(session_id, user_id, message, photo_data=None):
    """Send a message to the backend"""
    try:
        payload = {
            "message": message,
            "session_id": session_id,
            "user_id": user_id
        }
        
        if photo_data:
            payload["photo_data"] = photo_data
        
        response = requests.post(
            f"{RAILWAY_BACKEND_URL}/send_message",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to send message: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">✈️ Travel Assistant - Railway Combined</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Backend URL
        backend_url = st.text_input(
            "Backend URL",
            value=RAILWAY_BACKEND_URL,
            help="URL of the combined service backend"
        )
        
        # Health check
        st.subheader("🔍 Health Check")
        is_healthy, health_data = check_backend_health()
        
        if is_healthy:
            st.markdown('<p class="status-online">✅ Backend Online</p>', unsafe_allow_html=True)
            if health_data:
                st.json(health_data)
        else:
            st.markdown('<p class="status-offline">❌ Backend Offline</p>', unsafe_allow_html=True)
            st.error("Cannot connect to backend. Please check the URL and ensure the service is running.")
        
        # User ID
        user_id = st.text_input("User ID", value="railway_user", help="Unique identifier for the user")
        
        # Session management
        st.subheader("💬 Session Management")
        if st.button("🔄 Start New Session"):
            session_data = start_session(user_id)
            if session_data:
                st.session_state.session_id = session_data["session_id"]
                st.success(f"Session started: {session_data['session_id']}")
        
        if "session_id" in st.session_state:
            st.info(f"Active Session: {st.session_state.session_id}")
            if st.button("❌ Clear Session"):
                del st.session_state.session_id
                st.rerun()
    
    # Main content
    if not is_healthy:
        st.error("""
        ## Backend Connection Failed
        
        The backend service is not responding. Please:
        1. Check that the backend URL is correct
        2. Ensure the combined service is deployed and running
        3. Verify the service is accessible from this frontend
        
        **Backend URL:** `{backend_url}`
        """.format(backend_url=backend_url))
        return
    
    # Initialize session
    if "session_id" not in st.session_state:
        st.info("👈 Please start a session from the sidebar to begin chatting.")
        return
    
    # Chat interface
    st.header("💬 Chat with Travel Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "image" in message:
                st.image(message["image"], caption="Uploaded Image")
    
    # File upload
    uploaded_file = st.file_uploader(
        "📷 Upload a photo (optional)",
        type=['png', 'jpg', 'jpeg'],
        help="Upload an image to ask questions about it"
    )
    
    photo_data = None
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Convert to base64
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        photo_data = base64.b64encode(buffered.getvalue()).decode()
    
    # Chat input
    if prompt := st.chat_input("Ask me about travel destinations, weather, restaurants, or upload a photo to learn about it!"):
        # Add user message to chat history
        user_message = {"role": "user", "content": prompt}
        if uploaded_file:
            user_message["image"] = image
        st.session_state.messages.append(user_message)
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
            if uploaded_file:
                st.image(image, caption="Uploaded Image")
        
        # Send message to backend
        with st.spinner("🤔 Thinking..."):
            response_data = send_message(
                st.session_state.session_id,
                user_id,
                prompt,
                photo_data
            )
        
        if response_data and response_data.get("success"):
            assistant_response = response_data["response"]
            
            # Add assistant message to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_response
            })
            
            # Display assistant message
            with st.chat_message("assistant"):
                st.write(assistant_response)
        else:
            st.error("Failed to get response from assistant")
    
    # Clear chat button
    if st.session_state.messages and st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main() 
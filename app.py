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

# Configuration
API_URL = "http://localhost:8080"
USER_ID = "test_user"  # Use the same user_id as backend tests

# Page configuration
st.set_page_config(
    page_title="🌍 Travel Assistant",
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
    
    /* Input area styling */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: white;
        padding: 20px;
        border-top: 1px solid #e0e0e0;
        z-index: 1000;
    }
    
    /* Adjust sidebar for fixed input */
    .css-1d391kg {
        padding-bottom: 100px;
    }
    
    /* Hide Streamlit's default chat input */
    .stChatInput {
        position: relative !important;
        bottom: auto !important;
        margin-top: 20px;
    }
    
    /* Custom input styling */
    .custom-input {
        display: flex;
        gap: 10px;
        align-items: center;
    }
    
    .custom-input input {
        flex: 1;
        padding: 12px 15px;
        border: 2px solid #e0e0e0;
        border-radius: 25px;
        font-size: 16px;
        outline: none;
    }
    
    .custom-input input:focus {
        border-color: #007bff;
    }
    
    .custom-input button {
        padding: 12px 20px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 25px;
        cursor: pointer;
        font-size: 16px;
    }
    
    .custom-input button:hover {
        background-color: #0056b3;
    }
    
    /* Photo indicator */
    .photo-indicator {
        background-color: #28a745;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        margin-left: 10px;
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
    
    /* Auto-scroll to bottom */
    .chat-messages {
        scroll-behavior: smooth;
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
    
    .welcome-message ul {
        text-align: left;
        display: inline-block;
        margin-top: 15px;
    }
    
    .welcome-message li {
        margin-bottom: 8px;
        padding: 5px 0;
    }
    
    /* Input area improvements */
    .chat-input-section {
        background: white;
        padding: 20px;
        border-top: 1px solid #e0e0e0;
        border-radius: 10px 10px 0 0;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }
    
    /* Photo upload indicator */
    .photo-ready {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
        display: inline-block;
        margin-bottom: 10px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Make sure the input area is prominent */
    .stChatInput > div {
        border: 2px solid #e0e0e0;
        border-radius: 25px;
        padding: 10px;
        background: white;
    }
    
    .stChatInput input {
        font-size: 16px;
        padding: 12px 15px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_adk() -> Tuple[object, str, str]:
    """Initialize ADK Runner and Session. Cached to run once per session."""
    try:
        response = requests.post(f"{API_URL}/start_session", json={"user_id": USER_ID})
        if response.status_code != 200:
            raise Exception(f"Failed to start session: {response.status_code}")
        
        data = response.json()
        if not data.get("success"):
            raise Exception("Failed to initialize session")
            
        return None, data.get("session_id"), USER_ID  # Return user_id as well
    except Exception as e:
        raise Exception(f"Failed to initialize ADK: {str(e)}")

def run_adk_sync(_, session_id: str, user_id: str, message: str, photo_data: str = None) -> dict:
    """Run ADK agent turn synchronously through API."""
    try:
        payload = {
            "session_id": session_id,
            "user_id": user_id,
            "message": message
        }
        
        # Add photo data if provided
        if photo_data:
            payload["photo_data"] = photo_data
        
        response = requests.post(
            f"{API_URL}/send_message",
            json=payload
        )
        
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code}")
            
        data = response.json()
        if not data.get("success"):
            raise Exception("Failed to get response")
            
        return {
            "response": data.get("response", "No response received"),
            "image_links": data.get("image_links", None)
        }
    except Exception as e:
        raise Exception(f"Error running ADK: {str(e)}")

def encode_image_to_base64(image):
    """Convert PIL image to base64 string."""
    buffered = io.BytesIO()
    
    # Convert RGBA to RGB if necessary (JPEG doesn't support alpha channel)
    if image.mode == 'RGBA':
        # Create a white background
        rgb_image = Image.new('RGB', image.size, (255, 255, 255))
        # Paste the RGBA image onto the white background
        rgb_image.paste(image, mask=image.split()[-1])  # Use alpha channel as mask
        image = rgb_image
    elif image.mode != 'RGB':
        # Convert any other mode to RGB
        image = image.convert('RGB')
    
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Session state keys
SESSION_ID_KEY = "adk_session_id"
USER_ID_KEY = "adk_user_id"
MESSAGE_HISTORY_KEY = "travel_assistant_messages"
LAST_FILE_ID_KEY = "last_file_id"

# Sidebar: Reset Session button
with st.sidebar:
    st.markdown("## Session Controls")
    if st.button("🔄 Reset Session"):
        try:
            # Start a new backend session
            response = requests.post(f"{API_URL}/start_session", json={"user_id": USER_ID})
            if response.status_code == 200:
                data = response.json()
                # Clear all relevant session state keys
                for key in [SESSION_ID_KEY, USER_ID_KEY, MESSAGE_HISTORY_KEY, LAST_FILE_ID_KEY, "current_photo"]:
                    if key in st.session_state:
                        del st.session_state[key]

                # Re-initialize the session
                st.session_state[SESSION_ID_KEY] = data.get("session_id")
                st.session_state[USER_ID_KEY] = USER_ID
                st.session_state[MESSAGE_HISTORY_KEY] = []
                
                st.success(f"New session started: ...{data.get('session_id')[-12:]}")
                # Rerun to clear the chat window instantly
                st.rerun()
            else:
                st.error("Failed to reset session.")
        except Exception as e:
            st.error(f"Error resetting session: {e}")
    
    # Show current session info
    st.markdown(f"**Session ID:** ...{st.session_state.get(SESSION_ID_KEY, '')[-12:]}")
    st.markdown(f"**User ID:** {st.session_state.get(USER_ID_KEY, USER_ID)}")
    
    # Photo upload instructions
    st.markdown("---")
    st.markdown("## 📸 Photo Upload")
    st.markdown("""
    **How to upload photos:**
    1. Upload a photo below
    2. Type your question in the chat box
    3. Send your message - the photo will be included!
    
    **Example questions:**
    - "What landmark is this?"
    - "Tell me the history of this place"
    - "What's the story behind this building?"
    - "What are the best photo spots here?"
    """)
    
    # Photo upload widget
    uploaded_file = st.file_uploader(
        "Choose a photo...", 
        type=['png', 'jpg', 'jpeg'], 
        key="photo_uploader",
        help="Upload a photo to ask questions about landmarks, places, or get travel stories"
    )
    
    # Only process the file if it's a new upload.
    if uploaded_file is not None:
        current_file_id = uploaded_file.file_id
        # Check if this is a new file by comparing its ID to the last uploaded one.
        if st.session_state.get(LAST_FILE_ID_KEY) != current_file_id:
            # This is a new file, so process it.
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Photo", use_container_width=True)
            st.session_state["current_photo"] = image
            st.session_state[LAST_FILE_ID_KEY] = current_file_id
        
        # Add a button to manually clear the photo
        if st.button("🗑️ Clear Photo"):
            st.session_state["current_photo"] = None
            st.session_state[LAST_FILE_ID_KEY] = None
            st.rerun()

# Initialize ADK Runner and Session (if not already in session_state)
if SESSION_ID_KEY not in st.session_state or USER_ID_KEY not in st.session_state:
    try:
        adk_runner, current_session_id, current_user_id = initialize_adk()
        st.session_state[SESSION_ID_KEY] = current_session_id
        st.session_state[USER_ID_KEY] = current_user_id
        st.sidebar.success(f"ADK Initialized\nSession: ...{current_session_id[-12:]}\nUser: {current_user_id}", icon="✅")
    except Exception as e:
        st.error(f"**Fatal Error:** Could not initialize the ADK Runner or Session Service: {e}", icon="❌")
        st.error("Please check the terminal logs for more details and restart the application.")
        logging.exception("Critical ADK Initialization failed in Streamlit UI context.")
        st.stop()

# Initialize message history
if MESSAGE_HISTORY_KEY not in st.session_state:
    st.session_state[MESSAGE_HISTORY_KEY] = []

# Display chat messages from history
if not st.session_state.get(MESSAGE_HISTORY_KEY):
    st.markdown("""
    ### 👋 Welcome to the Travel Assistant!
    I can help you with:
    - 🌍 **Tourist spots and attractions**
    - 🌤️ **Weather information**
    - 🚶 **Walking routes and directions**
    - 🍽️ **Restaurant recommendations**
    - 📸 **Photo analysis and travel stories**
    
    Type your question below to get started!
    """)

for message in st.session_state[MESSAGE_HISTORY_KEY]:
    with st.chat_message(message["role"]):
        # Display photo if present in message
        if "photo" in message and message["photo"]:
            st.image(message["photo"], caption="Photo", use_container_width=True)
        
        # Display text content
        st.markdown(message["content"], unsafe_allow_html=False)
        
        # Display image links if present (for tourist spots)
        if "image_links" in message and message["image_links"]:
            st.markdown("### 📸 Tourist Attraction Images")
            
            # Create a grid layout for thumbnails
            cols = st.columns(3)
            for i, img_data in enumerate(message["image_links"]):
                col_idx = i % 3
                with cols[col_idx]:
                    try:
                        st.image(
                            img_data["thumbnail_url"], 
                            caption=f"{img_data['attraction']}, {img_data['location']}", 
                            use_container_width=True
                        )
                    except Exception as e:
                        st.error(f"Failed to load image: {e}")

# Show photo context if available
if st.session_state.get("current_photo") is not None:
    st.info("📸 Photo uploaded! Your next message will include this photo. Ask me anything about it!")

# Chat input is pinned to the bottom by default
if prompt := st.chat_input("Ask me about travel, weather, tourist spots, or anything else! 📎"):
    
    # Prepare message content
    message_content = prompt
    
    # Add photo context to message if available
    photo_data = None
    if "current_photo" in st.session_state and st.session_state["current_photo"] is not None:
        photo_data = encode_image_to_base64(st.session_state["current_photo"])
        message_content = f"[Photo attached] {prompt}"
    
    # Add and display user message
    message_data = {"role": "user", "content": message_content}
    if "current_photo" in st.session_state and st.session_state["current_photo"] is not None:
        message_data["photo"] = st.session_state["current_photo"]
    
    st.session_state[MESSAGE_HISTORY_KEY].append(message_data)
    
    # Immediately clear the photo from session state after it has been assigned to a message
    if "current_photo" in st.session_state:
        st.session_state["current_photo"] = None

    with st.chat_message("user"):
        # Display photo if present
        if message_data.get("photo"):
            st.image(message_data["photo"], caption="Photo", use_container_width=True)
        
        # Display text
        st.markdown(prompt, unsafe_allow_html=False)
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("🤔 Analyzing..." if photo_data else "🤔 Thinking..."):
            try:
                agent_response = run_adk_sync(
                    None,
                    st.session_state[SESSION_ID_KEY],
                    st.session_state[USER_ID_KEY],
                    prompt,
                    photo_data
                )
                message_placeholder.markdown(agent_response["response"], unsafe_allow_html=False)
                
                # Add to message history with image links if present
                message_data = {"role": "assistant", "content": agent_response["response"]}
                if agent_response.get("image_links"):
                    message_data["image_links"] = agent_response["image_links"]
                
                st.session_state[MESSAGE_HISTORY_KEY].append(message_data)
                
                # Rerun to update the chat display
                st.rerun()
                    
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state[MESSAGE_HISTORY_KEY].append({"role": "assistant", "content": error_msg})
                logging.exception("Error in chat processing")
                
                # Rerun to show the error message
                st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 14px;'>
    <p>Built with ❤️ using Google ADK, FastAPI, and Streamlit</p>
</div>
""", unsafe_allow_html=True)
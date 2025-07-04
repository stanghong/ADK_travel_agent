import asyncio
import uvicorn
import os
import logging
import json
from datetime import datetime
from typing import Dict, Optional, List
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from google.adk.cli.fast_api import get_fast_api_app
from orchestrator_agent.agent import root_agent
import base64
import httpx
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Disable OpenTelemetry if environment variable is set
if os.getenv('OTEL_PYTHON_DISABLED', 'false').lower() == 'true':
    os.environ['OTEL_PYTHON_DISABLED'] = 'true'
    logger.info("OpenTelemetry disabled via environment variable")

# Get the current directory as the agents directory
agents_dir = os.path.dirname(os.path.abspath(__file__))

# Create the main FastAPI app
app = FastAPI(
    title="Travel Assistant Combined Service",
    description="Combined ADK server with backend API endpoints",
    version="1.0.2"   # Updated version to trigger redeploy
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Add startup event to log deployment info
@app.on_event("startup")
async def startup_event():
    import platform
    logger.info("=" * 60)
    logger.info("🚀 Travel Assistant Combined Service Starting")
    logger.info(f"Version: 1.0.2")
    logger.info(f"Python: {platform.python_version()}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Working Directory: {os.getcwd()}")
    logger.info(f"Environment Variables:")
    for key, value in os.environ.items():
        if key in ['PORT', 'RAILWAY_DEPLOYMENT_VERSION', 'OTEL_PYTHON_DISABLED']:
            logger.info(f"  {key}: {value}")
    logger.info("=" * 60)

# Session storage (in production, use a proper database)
sessions: Dict[str, Dict] = {}

# Pydantic models
class SessionRequest(BaseModel):
    user_id: str

class MessageRequest(BaseModel):
    message: str
    session_id: str
    user_id: str
    photo_data: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    adk_server: str
    api_server: str

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="Healthy",
        adk_server="Integrated",
        api_server="Online"
    )

# Session management endpoint
@app.post("/start_session")
async def start_session(request: Request):
    """Create a new session"""
    # E-2-E-DEBUGGING
    logger.info(f"--- /start_session CALLED ---")
    logger.info(f"Request headers: {request.headers}")
    
    try:
        # We need to get the body and then parse it
        body = await request.json()
        user_id = body.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")

        session_id = f"session-{int(datetime.now().timestamp())}"
        # Use a plain dict for session storage
        sessions[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "messages": []
        }
        logger.info(f"Session created: {session_id} for user: {user_id}")
        return {
            "session_id": session_id,
            "success": True,
            "message": "Session started successfully",
            "user_id": user_id
        }
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")

# Message sending endpoint
@app.post("/send_message")
async def send_message(request: MessageRequest):
    """Send a message to the ADK server"""
    try:
        # Validate session
        if request.session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Prepare message parts
        message_parts = [{"text": request.message}]
        if request.photo_data:
            # The image and the text must be in separate parts
            message_parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": request.photo_data
                }
            })
        
        # Get session data
        session_data = sessions[request.session_id]
        user_id = session_data["user_id"]
        
        # Use the ADK app directly since it's integrated
        if adk_app is None:
            raise HTTPException(status_code=503, detail="ADK server not available")
        
        # Create a test client for the main app (not the mounted ADK app)
        from fastapi.testclient import TestClient
        test_client = TestClient(app)
        
        # First, create the session in ADK
        adk_session_url = f"/adk/apps/orchestrator_agent/users/{user_id}/sessions/{request.session_id}"
        try:
            session_response = test_client.post(adk_session_url)
            if session_response.status_code != 200:
                logger.warning(f"ADK session creation returned {session_response.status_code}")
        except Exception as e:
            logger.warning(f"Failed to create ADK session: {e}")
        
        # Send message to ADK
        adk_run_url = "/adk/run"
        
        payload = {
            "app_name": "orchestrator_agent",
            "user_id": user_id,
            "session_id": request.session_id,
            "new_message": {
                "role": "user",
                "parts": message_parts
            }
        }
        
        logger.info(f"Sending message to: {adk_run_url}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Send the request to the ADK endpoint
        response = test_client.post(adk_run_url, json=payload)
        
        if response.status_code == 200:
            adk_response = response.json()
            logger.info(f"ADK Response Events: {json.dumps(adk_response, indent=2)}")
            
            # Extract the final response text
            final_response = ""
            # Handle both dict (with "events") and list (direct events)
            if isinstance(adk_response, dict) and "events" in adk_response:
                events = adk_response["events"]
            elif isinstance(adk_response, list):
                events = adk_response
            else:
                events = []

            for event in events:
                if "content" in event and "parts" in event["content"]:
                    for part in event["content"]["parts"]:
                        if "text" in part:
                            final_response += part["text"]
            
            # Store message in session
            sessions[request.session_id]["messages"].append({
                "role": "user",
                "content": request.message,
                "timestamp": datetime.now().isoformat()
            })
            
            sessions[request.session_id]["messages"].append({
                "role": "assistant", 
                "content": final_response,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "success": True,
                "response": final_response,
                "session_id": request.session_id,
                "user_id": user_id
            }
        else:
            logger.error(f"ADK server error: {response.text}")
            raise HTTPException(
                status_code=503, 
                detail=f"ADK server error: {response.text}"
            )
            
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send message to ADK: {str(e)}")

# Create ADK web app for UI and direct access
try:
    # Create ADK app with proper agent registration
    adk_app = get_fast_api_app(
        agents_dir=agents_dir,
        web=True,
    )
    
    # Register the orchestrator agent properly
    adk_app.state.agents = {"orchestrator_agent": root_agent}
    
    # Also ensure the agent is available in the main app context
    app.state.orchestrator_agent = root_agent
    app.state.adk_app = adk_app
    
    logger.info("ADK web app created successfully")
    logger.info(f"Registered agents: {list(adk_app.state.agents.keys())}")
    
    # Mount ADK routes under /adk prefix - use the working ADK app directly
    app.mount("/adk", adk_app)
    
except Exception as e:
    logger.error(f"Failed to create ADK web app: {e}")
    adk_app = None

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Travel Assistant Combined Service",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "start_session": "/start_session",
            "send_message": "/send_message",
            "adk_ui": "/adk/dev-ui/",
            "adk_run": "/adk/run"
        }
    }

if __name__ == "__main__":
    logger.info("Starting Travel Assistant Combined Service...")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    ) 
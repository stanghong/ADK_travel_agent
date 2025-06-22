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
    version="1.0.0"
)

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
@app.post("/api/start_session")
async def start_session(request: SessionRequest):
    """Create a new session"""
    try:
        session_id = f"session-{int(datetime.now().timestamp())}"
        # Use a plain dict for session storage
        sessions[session_id] = {
            "user_id": request.user_id,
            "created_at": datetime.now().isoformat(),
            "messages": []
        }
        logger.info(f"Session created: {session_id} for user: {request.user_id}")
        return {
            "session_id": session_id,
            "success": True,
            "message": "Session started successfully",
            "user_id": request.user_id
        }
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")

# Message sending endpoint
@app.post("/api/send_message")
async def send_message(request: MessageRequest):
    """Send a message to the ADK server"""
    try:
        # Validate session
        if request.session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Prepare message parts
        message_parts = [{"text": request.message}]
        if request.photo_data:
            try:
                image_data = base64.b64decode(request.photo_data)
                message_parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": request.photo_data
                    }
                })
            except Exception as e:
                logger.warning(f"Failed to process photo data: {e}")
        
        # First, create the session in ADK if it doesn't exist
        session_data = sessions[request.session_id]
        user_id = session_data["user_id"]
        
        # Create session in ADK
        adk_session_url = f"http://localhost:8000/adk/apps/orchestrator_agent/users/{user_id}/sessions/{request.session_id}"
        async with httpx.AsyncClient() as client:
            try:
                session_response = await client.post(adk_session_url, timeout=10)
                if session_response.status_code != 200:
                    logger.warning(f"ADK session creation returned {session_response.status_code}")
            except Exception as e:
                logger.warning(f"Failed to create ADK session: {e}")
        
        # Send message to ADK
        adk_run_url = "http://localhost:8000/adk/run"
        
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
        
        async with httpx.AsyncClient() as client:
            response = await client.post(adk_run_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                adk_response = response.json()
                logger.info(f"ADK Response Events: {json.dumps(adk_response, indent=2)}")
                
                # Extract the final response text
                final_response = ""
                if "events" in adk_response:
                    for event in adk_response["events"]:
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
    adk_app = get_fast_api_app(
        agents_dir=agents_dir,
        web=True,
    )
    adk_app.state.agents = {"orchestrator_agent": root_agent}
    logger.info("ADK web app created successfully")
    
    # Mount ADK routes under /adk prefix
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
            "start_session": "/api/start_session",
            "send_message": "/api/send_message",
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
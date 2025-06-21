from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import asyncio
import requests
import json
import os
from typing import Optional
import time
import re
from urllib.parse import quote_plus

# Configuration using Pydantic Settings
class Settings(BaseSettings):
    ADK_BASE_URL: str = "http://localhost:8000"
    APP_NAME: str = "orchestrator_agent"
    USER_ID: str = "traveler"
    
    class Config:
        # Don't load from .env file to avoid validation errors
        env_file = None
        extra = "ignore"

settings = Settings()

app = FastAPI(title="Travel Assistant API", version="1.0.0")

# CORS configuration for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "https://your-streamlit-app.streamlit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class StartSessionRequest(BaseModel):
    user_id: str = settings.USER_ID

class StartSessionResponse(BaseModel):
    session_id: str
    success: bool
    message: str
    user_id: str

class MessageRequest(BaseModel):
    session_id: str
    message: str
    user_id: str = settings.USER_ID
    photo_data: Optional[str] = None  # Base64 encoded photo data

class MessageResponse(BaseModel):
    response: str
    success: bool
    session_id: str
    image_links: Optional[list] = None  # List of image data for tourist spots

class HealthResponse(BaseModel):
    status: str
    adk_server: str
    api_server: str

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check the health of both ADK and API servers."""
    try:
        adk_response = requests.get(f"{settings.ADK_BASE_URL}/", timeout=5)
        adk_status = "Online" if adk_response.status_code == 200 else "Error"
    except:
        adk_status = "Offline"
    
    return HealthResponse(
        status="Healthy",
        adk_server=adk_status,
        api_server="Online"
    )

# Start a new session
@app.post("/start_session", response_model=StartSessionResponse)
async def start_session(request: StartSessionRequest):
    """Start a new ADK session for the travel assistant."""
    try:
        # Create session with ADK using the correct endpoint pattern
        session_id = f"session-{int(time.time())}"
        session_url = f"{settings.ADK_BASE_URL}/apps/{settings.APP_NAME}/users/{request.user_id}/sessions/{session_id}"
        response = requests.post(
            session_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({})
        )
        
        if response.status_code != 200:
            print(f"ADK session creation failed: {response.status_code} - {response.text}")
            raise HTTPException(status_code=500, detail=f"Failed to create ADK session: {response.text}")
        
        return StartSessionResponse(
            session_id=session_id,
            success=True,
            message="Session started successfully",
            user_id=request.user_id
        )
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"ADK server error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Send message to agent
@app.post("/send_message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """Send a message to the travel assistant agent."""
    try:
        # Send message to ADK using the correct /run endpoint
        run_url = f"{settings.ADK_BASE_URL}/run"
        headers = {"Content-Type": "application/json"}
        
        # Prepare message parts
        message_parts = [{"text": request.message}]
        
        # Add photo data if provided
        if request.photo_data:
            message_parts.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": request.photo_data
                }
            })
        
        # Corrected payload structure based on working speaker_app.py example
        payload = {
            "app_name": settings.APP_NAME,
            "user_id": request.user_id,
            "session_id": request.session_id,
            "new_message": {
                "role": "user",
                "parts": message_parts
            }
        }
        
        print(f"Sending message to: {run_url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            run_url,
            json=payload,
            headers=headers,
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"ADK message sending failed: {response.status_code} - {response.text}")
            raise HTTPException(status_code=500, detail=f"Failed to send message to ADK: {response.text}")
        
        # Process response - ADK returns a list of events
        events = response.json()
        print(f"ADK Response Events: {json.dumps(events, indent=2)}")
        
        # Extract the agent's response from the events
        full_response = ""
        for event in events:
            # Look for the final text response from the model
            if (event.get("content", {}).get("role") == "model" and 
                "parts" in event.get("content", {}) and 
                len(event["content"]["parts"]) > 0 and
                "text" in event["content"]["parts"][0]):
                full_response = event["content"]["parts"][0]["text"]
                break  # Take the first model response we find
        
        # If no response found, try alternative parsing
        if not full_response:
            for event in events:
                if "content" in event and "parts" in event["content"]:
                    for part in event["content"]["parts"]:
                        if "text" in part:
                            full_response = part["text"]
                            break
                    if full_response:
                        break
        
        # Check if this is a tourist spots response and process accordingly
        image_links = None
        processed_response = full_response.strip() if full_response else "No response received"
        
        # Detect tourist spots queries (simple keyword matching)
        tourist_keywords = ["tourist", "attractions", "landmarks", "sights", "places to visit", "must see"]
        is_tourist_query = any(keyword in request.message.lower() for keyword in tourist_keywords)
        
        if is_tourist_query and "[IMAGE:" in processed_response:
            # Process tourist spots response
            processed_data = process_tourist_spots_response(processed_response)
            processed_response = processed_data["text"]
            image_links = processed_data["image_links"]
        
        return MessageResponse(
            response=processed_response,
            success=True,
            session_id=request.session_id,
            image_links=image_links
        )
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"ADK server error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Get session info
@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get information about a specific session."""
    try:
        session_url = f"{settings.ADK_BASE_URL}/apps/{settings.APP_NAME}/users/{settings.USER_ID}/sessions/{session_id}"
        response = requests.get(session_url)
        
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"ADK server error: {str(e)}")

def extract_image_links_from_response(response_text):
    """
    Extract image links from tourist spots agent response.
    Looks for [IMAGE: attraction_name, location_name] patterns.
    """
    image_links = []
    
    # Pattern to match [IMAGE: attraction_name, location_name]
    pattern = r'\[IMAGE:\s*([^,]+),\s*([^\]]+)\]'
    matches = re.findall(pattern, response_text)
    
    for attraction_name, location_name in matches:
        # Generate image URL using Unsplash
        image_url = f"https://source.unsplash.com/400x300/?{quote_plus(attraction_name.strip())} {quote_plus(location_name.strip())}"
        
        image_links.append({
            "attraction": attraction_name.strip(),
            "location": location_name.strip(),
            "image_url": image_url,
            "thumbnail_url": f"https://source.unsplash.com/150x150/?{quote_plus(attraction_name.strip())} {quote_plus(location_name.strip())}"
        })
    
    return image_links

def process_tourist_spots_response(response_text):
    """
    Process tourist spots response to extract image links and clean up the text.
    """
    # Extract image links
    image_links = extract_image_links_from_response(response_text)
    
    # Remove image markers from the text
    cleaned_text = re.sub(r'\[IMAGE:\s*[^,]+,\s*[^\]]+\]', '', response_text)
    
    return {
        "text": cleaned_text.strip(),
        "image_links": image_links
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 
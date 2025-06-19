from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from orchestrator_agent.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import add_user_query_to_history, call_agent_async

app = FastAPI()

# Allow CORS for local Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session service (non-persistent)
session_service = InMemorySessionService()

APP_NAME = "Customer Support"
USER_ID = "aiwithbrandon"

initial_state = {
    "user_name": "Brandon Hancock",
    "purchased_courses": [],
    "interaction_history": [],
}

# Create a runner with the main customer service agent
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

class StartSessionRequest(BaseModel):
    user_id: str = USER_ID

class StartSessionResponse(BaseModel):
    session_id: str
    state: dict

class MessageRequest(BaseModel):
    session_id: str
    user_id: str = USER_ID
    message: str

class MessageResponse(BaseModel):
    response: str
    state: dict

@app.post("/start_session", response_model=StartSessionResponse)
async def start_session(req: StartSessionRequest):
    new_session = session_service.create_session(
        app_name=APP_NAME,
        user_id=req.user_id,
        state=initial_state.copy(),
    )
    return StartSessionResponse(session_id=new_session.id, state=new_session.state)

@app.post("/send_message", response_model=MessageResponse)
async def send_message(req: MessageRequest):
    # Add user query to history
    add_user_query_to_history(
        session_service, APP_NAME, req.user_id, req.session_id, req.message
    )
    # Call the agent
    response = await call_agent_async(runner, req.user_id, req.session_id, req.message)
    # Get updated state
    session = session_service.get_session(
        app_name=APP_NAME, user_id=req.user_id, session_id=req.session_id
    )
    return MessageResponse(response=response, state=session.state) 
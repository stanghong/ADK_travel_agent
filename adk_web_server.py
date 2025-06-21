import asyncio
import uvicorn
import os
from google.adk.cli.fast_api import get_fast_api_app
from orchestrator_agent.agent import root_agent

# Get the current directory as the agents directory
agents_dir = os.path.dirname(os.path.abspath(__file__))

# Create web server using ADK's built-in FastAPI app
app = get_fast_api_app(
    agents_dir=agents_dir,
    web=True,
)

# Register our agent with the app
app.state.agents = {"orchestrator_agent": root_agent}

if __name__ == "__main__":
    print("Starting ADK Web Server on http://localhost:8000")
    print("Travel Assistant Agent is ready!")
    uvicorn.run(app, host="0.0.0.0", port=8000) 
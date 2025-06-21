#!/usr/bin/env python3

import asyncio
from google.adk.runners import Runner
from orchestrator_agent.sub_agents.walking_routes_agent.agent import walking_routes_agent
from google.adk.sessions import InMemorySessionService
from utils import call_agent_async

async def test_walking_routes():
    """Test the walking routes agent with map functionality."""
    
    # Create session service
    session_service = InMemorySessionService()
    
    # Create a runner
    runner = Runner(
        agent=walking_routes_agent,
        app_name="test_app",
        session_service=session_service
    )
    
    # Create a session
    user_id = "test_user"
    session = session_service.create_session(app_name="test_app", user_id=user_id, state={})
    session_id = session.id
    
    # Test message
    test_message = "Create a walking route between Eiffel Tower, Louvre Museum, and Notre Dame in Paris, and give me map links to follow"
    
    print("Testing Walking Routes Agent...")
    print(f"Message: {test_message}")
    print("-" * 50)
    
    # Run the agent using the utility
    response = await call_agent_async(runner, user_id, session_id, test_message)
    
    print("Response:")
    print(response)
    print("-" * 50)

if __name__ == "__main__":
    asyncio.run(test_walking_routes()) 
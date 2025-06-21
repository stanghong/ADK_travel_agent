#!/usr/bin/env python3
"""
Simple test script for the Orchestrator Agent with AgentTool.
"""

import asyncio
from google.adk.runners import Runner
from orchestrator_agent.agent import root_agent
from google.adk.sessions import InMemorySessionService
from utils import call_agent_async

async def test_orchestrator_agent():
    """Test the orchestrator agent directly."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="test_app",
        session_service=session_service
    )
    user_id = "test_user"
    session = await session_service.create_session(app_name="test_app", user_id=user_id, state={})
    session_id = session.id

    print("🎯 Testing Orchestrator Agent with AgentTool")
    print("=" * 50)

    # Test: Tourist spots in Paris
    query = "What are the top tourist spots in Paris?"
    print(f"\nTesting: {query}")
    response = await call_agent_async(runner, user_id, session_id, query)
    print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(test_orchestrator_agent()) 
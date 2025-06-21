#!/usr/bin/env python3

import asyncio
from google.adk.runners import Runner
from orchestrator_agent.sub_agents.weather_agent.agent import weather_agent
from google.adk.sessions import InMemorySessionService
from utils import call_agent_async

async def test_smart_weather() -> None:
    """Test the smart weather detection functionality."""
    
    # Create session service
    session_service = InMemorySessionService()
    
    # Create a runner
    runner = Runner(
        agent=weather_agent,
        app_name="test_app",
        session_service=session_service
    )
    
    # Create a session
    user_id = "test_user"
    session = session_service.create_session(app_name="test_app", user_id=user_id, state={})
    session_id = session.id
    
    print("🌤️ Testing Smart Weather Detection")
    print("=" * 50)
    
    # Test 1: Generic weather question (should show current time and ask for city)
    print("\n1️⃣ Testing generic weather question:")
    response1 = await call_agent_async(
        runner=runner,
        user_id=user_id,
        session_id=session_id,
        query="What's the weather?"
    )
    print(f"Response: {response1}")
    
    # Test 2: Specific city weather
    print("\n2️⃣ Testing specific city weather:")
    response2 = await call_agent_async(
        runner=runner,
        user_id=user_id,
        session_id=session_id,
        query="What's the weather in Paris?"
    )
    print(f"Response: {response2}")
    
    # Test 3: Current time request
    print("\n3️⃣ Testing current time request:")
    response3 = await call_agent_async(
        runner=runner,
        user_id=user_id,
        session_id=session_id,
        query="What's the current time in Tokyo?"
    )
    print(f"Response: {response3}")
    
    # Test 4: Follow-up weather question (should use context)
    print("\n4️⃣ Testing follow-up weather question:")
    response4 = await call_agent_async(
        runner=runner,
        user_id=user_id,
        session_id=session_id,
        query="How about the weather in London?"
    )
    print(f"Response: {response4}")
    
    # Test 5: Another generic weather question (should still ask for city)
    print("\n5️⃣ Testing another generic weather question:")
    response5 = await call_agent_async(
        runner=runner,
        user_id=user_id,
        session_id=session_id,
        query="Tell me about the weather"
    )
    print(f"Response: {response5}")
    
    print("\n✅ Smart weather testing completed!")

if __name__ == "__main__":
    asyncio.run(test_smart_weather()) 
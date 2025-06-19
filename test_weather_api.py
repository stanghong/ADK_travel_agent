#!/usr/bin/env python3

import asyncio
from agents.orchestrator_agent.sub_agents.weather_agent.agent import weather_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import call_agent_async

async def test_weather_api() -> None:
    """Test the weather API functionality."""
    
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
    
    print("🌤️ Testing Weather API Functionality")
    print("=" * 50)
    
    # Test 1: Weather for Paris
    print("\n1️⃣ Testing weather for Paris:")
    response1 = await call_agent_async(
        runner=runner,
        user_id=user_id,
        session_id=session_id,
        query="What's the weather like in Paris today?"
    )
    print(f"Response: {response1}")
    
    # Test 2: Weather for London
    print("\n2️⃣ Testing weather for London:")
    response2 = await call_agent_async(
        runner=runner,
        user_id=user_id,
        session_id=session_id,
        query="How's the weather in London?"
    )
    print(f"Response: {response2}")
    
    # Test 3: Weather for unknown location
    print("\n3️⃣ Testing weather for unknown location:")
    response3 = await call_agent_async(
        runner=runner,
        user_id=user_id,
        session_id=session_id,
        query="What's the weather in Sydney?"
    )
    print(f"Response: {response3}")
    
    # Test 4: Conversation memory with weather
    print("\n4️⃣ Testing conversation memory with weather:")
    response4 = await call_agent_async(
        runner=runner,
        user_id=user_id,
        session_id=session_id,
        query="Based on the weather we discussed earlier, what should I pack for my trip?"
    )
    print(f"Response: {response4}")
    
    print("\n✅ Weather API testing completed!")

if __name__ == "__main__":
    asyncio.run(test_weather_api()) 
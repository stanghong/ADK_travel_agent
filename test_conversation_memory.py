#!/usr/bin/env python3

import asyncio
from agents.orchestrator_agent.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import call_agent_async

async def test_conversation_memory():
    """Test the conversation memory functionality."""
    
    # Create session service
    session_service = InMemorySessionService()
    
    # Create a runner
    runner = Runner(
        agent=root_agent,
        app_name="test_app",
        session_service=session_service
    )
    
    # Create a session
    user_id = "test_user"
    session = session_service.create_session(app_name="test_app", user_id=user_id, state={})
    session_id = session.id
    
    print("🧠 Testing Conversation Memory Functionality")
    print("=" * 50)
    
    # Test 1: Ask about tourist spots in Paris
    print("\n📝 Test 1: Asking about tourist spots in Paris")
    print("-" * 40)
    response1 = await call_agent_async(runner, user_id, session_id, "What are the top tourist spots in Paris?")
    print(f"Response: {response1[:200]}..." if response1 and len(response1) > 200 else f"Response: {response1}")
    
    # Test 2: Ask for a walking route between "those places"
    print("\n📝 Test 2: Asking for walking route between 'those places'")
    print("-" * 40)
    response2 = await call_agent_async(runner, user_id, session_id, "Can you create a walking route between those places we just discussed and give me map links?")
    print(f"Response: {response2[:200]}..." if response2 and len(response2) > 200 else f"Response: {response2}")
    
    # Test 3: Ask about weather in Tokyo
    print("\n📝 Test 3: Asking about weather in Tokyo")
    print("-" * 40)
    response3 = await call_agent_async(runner, user_id, session_id, "What's the weather like in Tokyo?")
    print(f"Response: {response3[:200]}..." if response3 and len(response3) > 200 else f"Response: {response3}")
    
    # Test 4: Ask follow-up about packing based on previous weather
    print("\n📝 Test 4: Asking follow-up about packing")
    print("-" * 40)
    response4 = await call_agent_async(runner, user_id, session_id, "Based on that weather, what should I pack for my trip?")
    print(f"Response: {response4[:200]}..." if response4 and len(response4) > 200 else f"Response: {response4}")
    
    # Test 5: Ask about current time in a previously mentioned location
    print("\n📝 Test 5: Asking about current time in Paris")
    print("-" * 40)
    response5 = await call_agent_async(runner, user_id, session_id, "What's the current time in Paris?")
    print(f"Response: {response5[:200]}..." if response5 and len(response5) > 200 else f"Response: {response5}")
    
    print("\n" + "=" * 50)
    print("✅ Conversation Memory Test Complete!")
    print("The agent should have referenced previous conversations and maintained context throughout the session.")

if __name__ == "__main__":
    asyncio.run(test_conversation_memory()) 
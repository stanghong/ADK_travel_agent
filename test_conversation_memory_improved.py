#!/usr/bin/env python3

import asyncio
from agents.orchestrator_agent.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from utils import call_agent_async

async def test_conversation_memory_improved():
    """Test the improved conversation memory functionality."""
    
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
    
    print("🧠 Testing Improved Conversation Memory Functionality")
    print("=" * 60)
    
    # Test 1: Ask about tourist spots in Paris
    print("\n📝 Test 1: Asking about tourist spots in Paris")
    print("-" * 50)
    response1 = await call_agent_async(runner, user_id, session_id, "What are the top tourist spots in Paris?")
    print(f"Response: {response1[:300]}..." if response1 and len(response1) > 300 else f"Response: {response1}")
    
    # Test 2: Ask for a walking route between specific places mentioned
    print("\n📝 Test 2: Asking for walking route between Eiffel Tower and Louvre")
    print("-" * 50)
    response2 = await call_agent_async(runner, user_id, session_id, "Can you create a walking route between the Eiffel Tower and the Louvre Museum and give me map links?")
    print(f"Response: {response2[:300]}..." if response2 and len(response2) > 300 else f"Response: {response2}")
    
    # Test 3: Ask for weather in Paris (referencing the location we discussed)
    print("\n📝 Test 3: Asking about weather in Paris")
    print("-" * 50)
    response3 = await call_agent_async(runner, user_id, session_id, "What's the weather like in Paris right now?")
    print(f"Response: {response3[:300]}..." if response3 and len(response3) > 300 else f"Response: {response3}")
    
    # Test 4: Ask follow-up about the walking route we created
    print("\n📝 Test 4: Asking follow-up about the walking route")
    print("-" * 50)
    response4 = await call_agent_async(runner, user_id, session_id, "How long will that walking route take and what should I see along the way?")
    print(f"Response: {response4[:300]}..." if response4 and len(response4) > 300 else f"Response: {response4}")
    
    # Test 5: Ask about current time in Paris (should reference previous context)
    print("\n📝 Test 5: Asking about current time in Paris")
    print("-" * 50)
    response5 = await call_agent_async(runner, user_id, session_id, "What's the current time in Paris?")
    print(f"Response: {response5[:300]}..." if response5 and len(response5) > 300 else f"Response: {response5}")
    
    # Test 6: Ask for restaurant recommendations near the places we discussed
    print("\n📝 Test 6: Asking for restaurant recommendations")
    print("-" * 50)
    response6 = await call_agent_async(runner, user_id, session_id, "Can you recommend some restaurants near the Eiffel Tower and Louvre area?")
    print(f"Response: {response6[:300]}..." if response6 and len(response6) > 300 else f"Response: {response6}")
    
    print("\n" + "=" * 60)
    print("✅ Improved Conversation Memory Test Complete!")
    print("The agent should have maintained context and referenced previous conversations throughout the session.")

if __name__ == "__main__":
    asyncio.run(test_conversation_memory_improved()) 
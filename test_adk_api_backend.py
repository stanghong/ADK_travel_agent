#!/usr/bin/env python3
"""
Test script for the ADK API backend of the Travel Assistant.
This script tests the complete flow from API to ADK server.
"""

import requests
import json
import time
import sys
from typing import Dict, Any

# Configuration
API_URL = "http://localhost:8080"
ADK_URL = "http://localhost:8000"

def test_health_check() -> bool:
    """Test the health check endpoint."""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed:")
            print(f"   - API Server: {data['api_server']}")
            print(f"   - ADK Server: {data['adk_server']}")
            return data['adk_server'] == "Online"
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_session_creation() -> str:
    """Test session creation and return session ID."""
    print("\n🔍 Testing session creation...")
    try:
        response = requests.post(
            f"{API_URL}/start_session",
            json={"user_id": "test_user"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                session_id = data.get("session_id")
                print(f"✅ Session created successfully: {session_id}")
                return session_id
            else:
                print(f"❌ Session creation failed: {data.get('message')}")
                return None
        else:
            print(f"❌ Session creation failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Session creation error: {e}")
        return None

def test_message_sending(session_id: str, message: str) -> bool:
    """Test sending a message to the agent."""
    print(f"\n🔍 Testing message: '{message}'")
    try:
        response = requests.post(
            f"{API_URL}/send_message",
            json={
                "session_id": session_id,
                "user_id": "test_user",
                "message": message
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                agent_response = data.get("response", "")
                print(f"✅ Agent response received ({len(agent_response)} chars)")
                print(f"📝 Response preview: {agent_response[:200]}...")
                return True
            else:
                print(f"❌ Message sending failed: {data}")
                return False
        else:
            print(f"❌ Message sending failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Message sending error: {e}")
        return False

def test_session_info(session_id: str) -> bool:
    """Test getting session information."""
    print(f"\n🔍 Testing session info for: {session_id}")
    try:
        response = requests.get(f"{API_URL}/session/{session_id}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Session info retrieved: {len(data)} fields")
            return True
        else:
            print(f"❌ Session info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Session info error: {e}")
        return False

def test_conversation_flow(session_id: str) -> bool:
    """Test a complete conversation flow."""
    print(f"\n🔍 Testing conversation flow...")
    
    test_messages = [
        "What's the weather like in Paris today?",
        "What are the top tourist spots in Paris?",
        "Can you create a walking route between the Eiffel Tower and the Louvre?",
        "What restaurants would you recommend near the Eiffel Tower?",
        "What time is it in Tokyo right now?"
    ]
    
    success_count = 0
    for i, message in enumerate(test_messages, 1):
        print(f"\n--- Message {i}/{len(test_messages)} ---")
        if test_message_sending(session_id, message):
            success_count += 1
        time.sleep(1)  # Small delay between messages
    
    print(f"\n📊 Conversation flow results: {success_count}/{len(test_messages)} messages successful")
    return success_count == len(test_messages)

def main():
    """Main test function."""
    print("🌍 Travel Assistant - ADK API Backend Test")
    print("=" * 50)
    
    # Check if services are running
    print("🔍 Checking if services are running...")
    try:
        api_response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"✅ API server is running (status: {api_response.status_code})")
    except:
        print("❌ API server is not running. Please start the services first.")
        print("   Run: python start_services.py")
        return False
    
    try:
        adk_response = requests.get(f"{ADK_URL}/", timeout=5)
        print(f"✅ ADK server is running (status: {adk_response.status_code})")
    except:
        print("❌ ADK server is not running. Please start the services first.")
        print("   Run: python start_services.py")
        return False
    
    print("\n" + "=" * 50)
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Health check
    if test_health_check():
        tests_passed += 1
    
    # Test 2: Session creation
    session_id = test_session_creation()
    if session_id:
        tests_passed += 1
        
        # Test 3: Message sending
        if test_message_sending(session_id, "Hello! Can you help me plan a trip to Paris?"):
            tests_passed += 1
        
        # Test 4: Session info
        if test_session_info(session_id):
            tests_passed += 1
        
        # Bonus: Conversation flow
        print("\n" + "=" * 50)
        print("🎯 Testing complete conversation flow...")
        test_conversation_flow(session_id)
    
    # Results
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! The ADK API backend is working correctly.")
        print("\n🚀 You can now:")
        print("   • Use the Streamlit UI: http://localhost:8501")
        print("   • Make direct API calls to: http://localhost:8080")
        print("   • Access ADK server at: http://localhost:8000")
        return True
    else:
        print("❌ Some tests failed. Please check the logs and restart services if needed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
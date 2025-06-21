#!/usr/bin/env python3
"""
Test script to verify ADK server functionality in Docker
"""

import requests
import time
import json
import sys

def test_adk_server():
    """Test the ADK server endpoints"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing ADK Server in Docker...")
    print(f"📍 Testing against: {base_url}")
    
    # Test 1: Health check endpoint
    print("\n1️⃣ Testing health check endpoint...")
    try:
        response = requests.get(f"{base_url}/dev-ui/", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Create a session
    print("\n2️⃣ Testing session creation...")
    try:
        session_data = {
            "app_name": "orchestrator_agent",
            "user_id": "test_user",
            "session_id": f"session-{int(time.time())}"
        }
        response = requests.post(
            f"{base_url}/apps/orchestrator_agent/users/test_user/sessions/{session_data['session_id']}",
            timeout=10
        )
        if response.status_code == 200:
            print("✅ Session creation successful")
            session_id = session_data['session_id']
        else:
            print(f"❌ Session creation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Session creation error: {e}")
        return False
    
    # Test 3: Send a simple message
    print("\n3️⃣ Testing message sending...")
    try:
        message_data = {
            "app_name": "orchestrator_agent",
            "user_id": "test_user",
            "session_id": session_id,
            "new_message": {
                "role": "user",
                "parts": [
                    {
                        "text": "Hello, what can you help me with?"
                    }
                ]
            }
        }
        response = requests.post(
            f"{base_url}/run",
            json=message_data,
            timeout=30
        )
        if response.status_code == 200:
            print("✅ Message sending successful")
            result = response.json()
            print(f"📝 Response received: {len(result)} events")
        else:
            print(f"❌ Message sending failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Message sending error: {e}")
        return False
    
    # Test 4: Test weather functionality
    print("\n4️⃣ Testing weather functionality...")
    try:
        weather_data = {
            "app_name": "orchestrator_agent",
            "user_id": "test_user",
            "session_id": session_id,
            "new_message": {
                "role": "user",
                "parts": [
                    {
                        "text": "What's the weather in Paris?"
                    }
                ]
            }
        }
        response = requests.post(
            f"{base_url}/run",
            json=weather_data,
            timeout=30
        )
        if response.status_code == 200:
            print("✅ Weather functionality successful")
            result = response.json()
            print(f"📝 Weather response: {len(result)} events")
        else:
            print(f"❌ Weather functionality failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Weather functionality error: {e}")
        return False
    
    print("\n🎉 All tests passed! ADK server is working correctly in Docker.")
    return True

def main():
    """Main function"""
    print("🚀 ADK Docker Test Suite")
    print("=" * 50)
    
    # Wait a bit for the server to be ready
    print("⏳ Waiting for ADK server to be ready...")
    time.sleep(5)
    
    success = test_adk_server()
    
    if success:
        print("\n✅ ADK Docker test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ ADK Docker test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
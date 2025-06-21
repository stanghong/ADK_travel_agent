#!/usr/bin/env python3
"""
Simple test script to verify backend API functionality
"""

import requests
import time
import json

def test_backend():
    """Test backend API functionality"""
    
    base_url = "http://localhost:8080"
    
    print("🧪 Testing Backend API...")
    print(f"📍 Testing against: {base_url}")
    
    # Test 1: Health check
    print("\n1️⃣ Testing health check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health check passed: {result}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Create session
    print("\n2️⃣ Testing session creation...")
    try:
        session_data = {
            "user_id": "test_user"
        }
        response = requests.post(f"{base_url}/start_session", json=session_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            session_id = result.get("session_id")
            print(f"✅ Session creation successful: {session_id}")
        else:
            print(f"❌ Session creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Session creation error: {e}")
        return False
    
    # Test 3: Send message
    print("\n3️⃣ Testing message sending...")
    try:
        message_data = {
            "message": "What's the weather in Paris?",
            "session_id": session_id,
            "user_id": "test_user"
        }
        response = requests.post(f"{base_url}/send_message", json=message_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Message sending successful")
            print(f"Response: {result.get('response', 'No response')[:100]}...")
        else:
            print(f"❌ Message sending failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Message sending error: {e}")
        return False
    
    print("\n🎉 Backend API test completed successfully!")
    return True

if __name__ == "__main__":
    test_backend() 
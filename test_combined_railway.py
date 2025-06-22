#!/usr/bin/env python3
"""
Test script for the combined ADK server and API service.
Can be used to test both local and Railway deployments.
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

def test_combined_service(base_url="http://localhost:8000"):
    """Test the combined service endpoints"""
    
    print(f"🚀 Testing Combined Service at: {base_url}")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health Check PASSED")
            print(f"   Status: {health_data.get('status')}")
            print(f"   ADK Server: {health_data.get('adk_server')}")
            print(f"   API Server: {health_data.get('api_server')}")
        else:
            print(f"❌ Health Check FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check ERROR: {e}")
        return False
    
    # Test 2: Root Endpoint
    print("\n2️⃣ Testing Root Endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            root_data = response.json()
            print(f"✅ Root Endpoint PASSED")
            print(f"   Message: {root_data.get('message')}")
            print(f"   Version: {root_data.get('version')}")
        else:
            print(f"❌ Root Endpoint FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ Root Endpoint ERROR: {e}")
    
    # Test 3: Session Creation
    print("\n3️⃣ Testing Session Creation...")
    user_id = f"test_user_{int(time.time())}"
    session_id = None
    
    try:
        response = requests.post(
            f"{base_url}/api/start_session",
            json={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data.get("session_id")
            print(f"✅ Session Creation PASSED")
            print(f"   Session ID: {session_id}")
            print(f"   User ID: {session_data.get('user_id')}")
        else:
            print(f"❌ Session Creation FAILED: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Session Creation ERROR: {e}")
        return False
    
    # Test 4: Message Sending
    print("\n4️⃣ Testing Message Sending...")
    if not session_id:
        print("❌ Cannot test message sending without session ID")
        return False
    
    test_messages = [
        "Hello! Can you help me plan a trip to Paris?",
        "What's the weather like in Tokyo?",
        "Find me some good restaurants in Rome"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n   Testing message {i}: {message[:50]}...")
        try:
            response = requests.post(
                f"{base_url}/api/send_message",
                json={
                    "message": message,
                    "session_id": session_id,
                    "user_id": user_id
                },
                timeout=30
            )
            if response.status_code == 200:
                message_data = response.json()
                if message_data.get("success"):
                    print(f"   ✅ Message {i} PASSED")
                    response_text = message_data.get("response", "")[:100]
                    print(f"   Response: {response_text}...")
                else:
                    print(f"   ❌ Message {i} FAILED: {message_data}")
            else:
                print(f"   ❌ Message {i} FAILED: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ Message {i} ERROR: {e}")
    
    # Test 5: ADK UI Endpoint
    print("\n5️⃣ Testing ADK UI Endpoint...")
    try:
        response = requests.get(f"{base_url}/adk/dev-ui/", timeout=10)
        if response.status_code == 200:
            print(f"✅ ADK UI Endpoint PASSED")
        else:
            print(f"❌ ADK UI Endpoint FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ ADK UI Endpoint ERROR: {e}")
    
    # Test 6: Invalid Session
    print("\n6️⃣ Testing Invalid Session...")
    try:
        response = requests.post(
            f"{base_url}/api/send_message",
            json={
                "message": "This should fail",
                "session_id": "invalid_session_id",
                "user_id": user_id
            },
            timeout=10
        )
        if response.status_code == 404:
            print(f"✅ Invalid Session Test PASSED (correctly rejected)")
        else:
            print(f"❌ Invalid Session Test FAILED: Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"❌ Invalid Session Test ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Combined Service Testing Complete!")
    return True

def main():
    """Main function to run tests"""
    
    # Check if URL is provided as command line argument
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        # Default to localhost
        base_url = "http://localhost:8000"
    
    print(f"🔧 Testing URL: {base_url}")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    success = test_combined_service(base_url)
    
    if success:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
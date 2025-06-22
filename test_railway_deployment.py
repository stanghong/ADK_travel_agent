#!/usr/bin/env python3
"""
Test script specifically for Railway deployment testing.
"""

import requests
import json
import time
import sys
from datetime import datetime

def test_railway_deployment():
    """Test the Railway deployment"""
    
    railway_url = "https://adktravelagent-production.up.railway.app"
    
    print(f"🚀 Testing Railway Deployment at: {railway_url}")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{railway_url}/health", timeout=10)
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
        response = requests.get(f"{railway_url}/", timeout=10)
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
            f"{railway_url}/api/start_session",
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
                f"{railway_url}/api/send_message",
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
        response = requests.get(f"{railway_url}/adk/dev-ui/", timeout=10)
        if response.status_code == 200:
            print(f"✅ ADK UI Endpoint PASSED")
        else:
            print(f"❌ ADK UI Endpoint FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ ADK UI Endpoint ERROR: {e}")
    
    # Test 6: Direct ADK Run Test
    print("\n6️⃣ Testing Direct ADK Run...")
    try:
        # First create a session in ADK
        adk_session_url = f"{railway_url}/adk/apps/orchestrator_agent/users/{user_id}/sessions/{session_id}"
        session_response = requests.post(adk_session_url, timeout=10)
        print(f"   ADK Session Creation: {session_response.status_code}")
        
        # Then try to run a message
        adk_run_url = f"{railway_url}/adk/run"
        payload = {
            "app_name": "orchestrator_agent",
            "user_id": user_id,
            "session_id": session_id,
            "new_message": {
                "role": "user",
                "parts": [{"text": "Hello, this is a test message"}]
            }
        }
        
        run_response = requests.post(adk_run_url, json=payload, timeout=30)
        if run_response.status_code == 200:
            print(f"   ✅ Direct ADK Run PASSED")
            adk_data = run_response.json()
            if "events" in adk_data:
                print(f"   Events received: {len(adk_data['events'])}")
        else:
            print(f"   ❌ Direct ADK Run FAILED: {run_response.status_code} - {run_response.text}")
    except Exception as e:
        print(f"   ❌ Direct ADK Run ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Railway Deployment Testing Complete!")
    return True

def main():
    """Main function to run tests"""
    
    print(f"🔧 Testing Railway Deployment")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    success = test_railway_deployment()
    
    if success:
        print("\n✅ Railway deployment tests completed!")
        sys.exit(0)
    else:
        print("\n❌ Some Railway deployment tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
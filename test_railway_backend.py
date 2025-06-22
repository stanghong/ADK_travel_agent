#!/usr/bin/env python3
"""
Test script to verify Railway backend connection
"""

import requests
import time
import json
import os

def test_railway_backend():
    """Test Railway backend functionality"""
    
    # Get Railway URL from environment or use the production URL
    railway_url = os.getenv('RAILWAY_BACKEND_URL', 'https://adktravelagent-production.up.railway.app')
    
    print("🧪 Testing Railway Backend...")
    print(f"📍 Testing against: {railway_url}")
    
    # Test 1: Health check
    print("\n1️⃣ Testing health check...")
    try:
        response = requests.get(f"{railway_url}/health", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health check passed: {result}")
            
            # Check ADK server status
            adk_status = result.get("adk_server", "Unknown")
            if adk_status == "Online":
                print("✅ ADK server is online")
            else:
                print(f"⚠️ ADK server is {adk_status} - this may affect functionality")
                
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"Response: {response.text}")
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
        response = requests.post(f"{railway_url}/start_session", json=session_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            session_id = result.get("session_id")
            print(f"✅ Session creation successful: {session_id}")
        else:
            print(f"❌ Session creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            if response.status_code == 503:
                print("💡 This is expected if ADK server is offline in Railway")
            return False
    except Exception as e:
        print(f"❌ Session creation error: {e}")
        return False
    
    # Test 3: Send message (only if session was created)
    if 'session_id' in locals():
        print("\n3️⃣ Testing message sending...")
        try:
            message_data = {
                "message": "What's the weather in Paris?",
                "session_id": session_id,
                "user_id": "test_user"
            }
            response = requests.post(f"{railway_url}/send_message", json=message_data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                print("✅ Message sending successful")
                print(f"Response: {result.get('response', 'No response')[:100]}...")
            else:
                print(f"❌ Message sending failed: {response.status_code}")
                print(f"Response: {response.text}")
                if response.status_code == 503:
                    print("💡 This is expected if ADK server is offline in Railway")
                return False
        except Exception as e:
            print(f"❌ Message sending error: {e}")
            return False
    else:
        print("\n3️⃣ Skipping message test (no session created)")
    
    print("\n🎉 Railway backend test completed!")
    print("\n📋 Summary:")
    print(f"   Backend URL: {railway_url}")
    print(f"   Backend Status: ✅ Online")
    print(f"   ADK Server Status: {adk_status}")
    print(f"   Session Creation: {'✅ Working' if 'session_id' in locals() else '❌ Failed'}")
    
    return True

if __name__ == "__main__":
    # You can set the Railway URL as an environment variable
    # export RAILWAY_BACKEND_URL="https://adktravelagent-production.up.railway.app"
    
    print("🚀 Railway Backend Test Suite")
    print("=" * 50)
    print("Testing: adktravelagent-production.up.railway.app")
    print("=" * 50)
    
    test_railway_backend() 
#!/usr/bin/env python3
"""
Test script to verify combined ADK server with API endpoints
"""

import requests
import time
import json
import os

def test_combined_service():
    """Test combined ADK server with API endpoints"""
    
    # Get service URL from environment or use default
    service_url = os.getenv('COMBINED_SERVICE_URL', 'http://localhost:8000')
    
    print("🧪 Testing Combined ADK Server with API...")
    print(f"📍 Testing against: {service_url}")
    
    # Test 1: Root endpoint
    print("\n1️⃣ Testing root endpoint...")
    try:
        response = requests.get(f"{service_url}/", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Root endpoint: {result.get('message', 'Unknown')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
        return False
    
    # Test 2: Health check
    print("\n2️⃣ Testing health check...")
    try:
        response = requests.get(f"{service_url}/health", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Health check: {result}")
            
            # Check ADK server status
            adk_status = result.get("adk_server", "Unknown")
            if adk_status == "Online":
                print("✅ ADK server is online")
            else:
                print(f"⚠️ ADK server is {adk_status}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 3: ADK UI endpoint
    print("\n3️⃣ Testing ADK UI endpoint...")
    try:
        response = requests.get(f"{service_url}/dev-ui/", timeout=10)
        if response.status_code == 200:
            print("✅ ADK UI endpoint accessible")
        else:
            print(f"⚠️ ADK UI endpoint: {response.status_code}")
    except Exception as e:
        print(f"⚠️ ADK UI endpoint error: {e}")
    
    # Test 4: Create session
    print("\n4️⃣ Testing session creation...")
    try:
        session_data = {
            "user_id": "test_user"
        }
        response = requests.post(f"{service_url}/start_session", json=session_data, timeout=10)
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
    
    # Test 5: Send message
    print("\n5️⃣ Testing message sending...")
    try:
        message_data = {
            "message": "What's the weather in Paris?",
            "session_id": session_id,
            "user_id": "test_user"
        }
        response = requests.post(f"{service_url}/send_message", json=message_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Message sending successful")
            print(f"Response: {result.get('response', 'No response')[:100]}...")
        else:
            print(f"❌ Message sending failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Message sending error: {e}")
        return False
    
    print("\n🎉 Combined service test completed successfully!")
    print("\n📋 Summary:")
    print(f"   Service URL: {service_url}")
    print(f"   ADK Server Status: {adk_status}")
    print(f"   API Endpoints: ✅ Working")
    print(f"   Session Management: ✅ Working")
    print(f"   Message Processing: ✅ Working")
    
    return True

if __name__ == "__main__":
    print("🚀 Combined ADK Server with API Test Suite")
    print("=" * 60)
    print("Testing combined service with all endpoints")
    print("=" * 60)
    
    test_combined_service() 
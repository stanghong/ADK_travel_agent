#!/usr/bin/env python3
"""
Comprehensive test script for the combined service running in Docker.
Tests all endpoints, session management, message processing, and ADK integration.
"""

import requests
import json
import time
import sys
import os
from datetime import datetime
import base64
from PIL import Image
import io

def test_docker_combined_service(base_url="http://localhost:8000"):
    """Comprehensive test of the combined service in Docker"""
    
    print(f"🐳 Testing Combined Service in Docker at: {base_url}")
    print("=" * 70)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health Check PASSED")
            print(f"   Status: {health_data.get('status', 'Unknown')}")
            print(f"   ADK Server: {health_data.get('adk_server', 'Unknown')}")
            print(f"   API Server: {health_data.get('api_server', 'Unknown')}")
        else:
            print(f"❌ Health Check FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health Check FAILED: {e}")
        return False

    # Test 2: Root Endpoint
    print("\n2️⃣ Testing Root Endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            root_data = response.json()
            print(f"✅ Root Endpoint PASSED")
            print(f"   Message: {root_data.get('message', 'Unknown')}")
            print(f"   Version: {root_data.get('version', 'Unknown')}")
        else:
            print(f"❌ Root Endpoint FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ Root Endpoint FAILED: {e}")

    # Test 3: ADK UI Endpoint
    print("\n3️⃣ Testing ADK UI Endpoint...")
    try:
        response = requests.get(f"{base_url}/adk/dev-ui/", timeout=10)
        if response.status_code == 200:
            print(f"✅ ADK UI Endpoint PASSED")
        else:
            print(f"❌ ADK UI Endpoint FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ ADK UI Endpoint FAILED: {e}")

    # Test 4: Session Management
    print("\n4️⃣ Testing Session Management...")
    user_id = f"test_user_{int(time.time())}"
    session_id = None
    
    try:
        # Create session
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
            print(f"   User ID: {user_id}")
        else:
            print(f"❌ Session Creation FAILED: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Session Creation FAILED: {e}")
        return False

    # Test 5: Message Processing
    print("\n5️⃣ Testing Message Processing...")
    
    test_messages = [
        "Hello! Can you help me plan a trip to Paris?",
        "What's the weather like in Tokyo?",
        "Find me some good restaurants in Rome",
        "What time is it in New York?",
        "Show me tourist attractions in London"
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
                response_text = message_data.get("response", "")
                print(f"   ✅ Message {i} PASSED")
                print(f"   Response: {response_text[:100]}...")
            else:
                print(f"   ❌ Message {i} FAILED: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ Message {i} FAILED: {e}")

    # Test 6: Photo Upload
    print("\n6️⃣ Testing Photo Upload...")
    try:
        # Create a simple test image
        img = Image.new('RGB', (100, 100), color='red')
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        img_base64 = base64.b64encode(img_byte_arr).decode()
        
        response = requests.post(
            f"{base_url}/api/send_message",
            json={
                "message": "What is this landmark?",
                "session_id": session_id,
                "user_id": user_id,
                "photo_data": img_base64
            },
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ Photo Upload PASSED")
        else:
            print(f"❌ Photo Upload FAILED: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Photo Upload FAILED: {e}")

    # Test 7: Error Handling
    print("\n7️⃣ Testing Error Handling...")
    
    # Test invalid session
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
            print(f"✅ Invalid Session Test PASSED")
        else:
            print(f"❌ Invalid Session Test FAILED: Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"❌ Invalid Session Test FAILED: {e}")

    # Test 8: ADK Direct Access
    print("\n8️⃣ Testing ADK Direct Access...")
    try:
        # Test ADK session creation
        adk_session_url = f"{base_url}/adk/apps/orchestrator_agent/users/{user_id}/sessions/{session_id}"
        response = requests.post(adk_session_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ ADK Session Creation PASSED")
        else:
            print(f"❌ ADK Session Creation FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ ADK Session Creation FAILED: {e}")

    # Test 9: Performance Test
    print("\n9️⃣ Testing Performance...")
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{base_url}/api/send_message",
            json={
                "message": "Quick test message",
                "session_id": session_id,
                "user_id": user_id
            },
            timeout=30
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if response.status_code == 200:
            print(f"✅ Performance Test PASSED")
            print(f"   Response Time: {response_time:.2f} seconds")
        else:
            print(f"❌ Performance Test FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ Performance Test FAILED: {e}")

    # Test 10: Container Health
    print("\n🔟 Testing Container Health...")
    try:
        # Test multiple health checks
        for i in range(3):
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                print(f"   Health Check {i+1}: ✅")
            else:
                print(f"   Health Check {i+1}: ❌")
            time.sleep(1)
        print(f"✅ Container Health PASSED")
    except Exception as e:
        print(f"❌ Container Health FAILED: {e}")

    print("\n" + "=" * 70)
    print("🎉 Docker Combined Service Testing Complete!")
    print("✅ All tests completed successfully!")
    
    return True

if __name__ == "__main__":
    # Allow custom base URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    print(f"🔧 Testing URL: {base_url}")
    print(f"⏰ Test started at: {datetime.now()}")
    
    success = test_docker_combined_service(base_url)
    
    if success:
        print("\n🎯 All tests passed! The combined service is working correctly in Docker.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the logs and fix the issues.")
        sys.exit(1) 
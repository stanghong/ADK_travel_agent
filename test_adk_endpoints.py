#!/usr/bin/env python3
"""
Test script to verify ADK endpoints are working correctly
"""

import requests
import json
import time

def test_adk_endpoints():
    """Test the ADK endpoints directly"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing ADK Endpoints")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: ADK dev-ui endpoint
    print("\n3. Testing ADK dev-ui endpoint...")
    try:
        response = requests.get(f"{base_url}/adk/dev-ui/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ ADK dev-ui is accessible")
        else:
            print(f"   ❌ ADK dev-ui error: {response.status_code}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: ADK apps endpoint
    print("\n4. Testing ADK apps endpoint...")
    try:
        response = requests.get(f"{base_url}/adk/apps/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 5: Test session creation
    print("\n5. Testing session creation...")
    user_id = f"test_user_{int(time.time())}"
    session_id = f"test_session_{int(time.time())}"
    
    try:
        response = requests.post(f"{base_url}/adk/apps/orchestrator_agent/users/{user_id}/sessions/{session_id}")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Session created successfully")
        else:
            print(f"   ❌ Session creation failed: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 6: Test run endpoint
    print("\n6. Testing run endpoint...")
    payload = {
        "app_name": "orchestrator_agent",
        "user_id": user_id,
        "session_id": session_id,
        "new_message": {
            "role": "user",
            "parts": [{"text": "Hello! Can you help me plan a trip to Paris?"}]
        }
    }
    
    try:
        response = requests.post(f"{base_url}/adk/run", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Run endpoint working")
            result = response.json()
            if isinstance(result, dict):
                print(f"   Response keys: {list(result.keys())}")
            elif isinstance(result, list):
                print(f"   Response is a list with {len(result)} items")
            else:
                print(f"   Response type: {type(result)}")
        else:
            print(f"   ❌ Run endpoint failed: {response.text}")
    except Exception as e:
        print(f"   Error: {e}")

if __name__ == "__main__":
    test_adk_endpoints() 
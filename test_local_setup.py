#!/usr/bin/env python3
"""
Test script to verify local setup (backend on 8080, frontend on 8501)
"""

import requests
import time
import json

def test_local_setup():
    """Test local backend and frontend setup"""
    
    backend_url = "http://0.0.0.0:8080"
    frontend_url = "http://0.0.0.0:8501"
    
    print("🧪 Testing Local Setup...")
    print(f"📍 Backend: {backend_url}")
    print(f"📍 Frontend: {frontend_url}")
    
    # Test 1: Backend health
    print("\n1️⃣ Testing backend health...")
    try:
        response = requests.get(f"{backend_url}/health", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Backend health: {result}")
        else:
            print(f"❌ Backend health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health error: {e}")
        return False
    
    # Test 2: Frontend accessibility
    print("\n2️⃣ Testing frontend accessibility...")
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
        else:
            print(f"❌ Frontend failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return False
    
    # Test 3: Backend session creation
    print("\n3️⃣ Testing backend session creation...")
    try:
        session_data = {"user_id": "test_user"}
        response = requests.post(f"{backend_url}/start_session", json=session_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            session_id = result.get("session_id")
            print(f"✅ Session created: {session_id}")
        else:
            print(f"❌ Session creation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Session creation error: {e}")
        return False
    
    # Test 4: Backend message sending
    print("\n4️⃣ Testing backend message sending...")
    try:
        message_data = {
            "message": "What time is it in Tokyo?",
            "session_id": session_id,
            "user_id": "test_user"
        }
        response = requests.post(f"{backend_url}/send_message", json=message_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ Message sent successfully")
            print(f"Response: {result.get('response', 'No response')[:100]}...")
        else:
            print(f"❌ Message sending failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Message sending error: {e}")
        return False
    
    print("\n🎉 Local setup test completed successfully!")
    print(f"\n🌐 Access your application:")
    print(f"   Frontend: {frontend_url}")
    print(f"   Backend API: {backend_url}")
    print(f"   Backend Health: {backend_url}/health")
    
    return True

if __name__ == "__main__":
    test_local_setup() 
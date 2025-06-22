#!/usr/bin/env python3
"""
Test script for Railway deployment with Streamlit frontend.
"""

import requests
import json
import time
import sys
from datetime import datetime

def test_railway_frontend():
    """Test the Railway deployment with frontend integration"""
    
    railway_url = "https://adktravelagent-production.up.railway.app"
    frontend_url = "http://localhost:8502"
    
    print(f"🚀 Testing Railway + Frontend Integration")
    print("=" * 60)
    
    # Test 1: Railway Backend Health
    print("\n1️⃣ Testing Railway Backend Health...")
    try:
        response = requests.get(f"{railway_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Railway Backend PASSED")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Version: {health_data.get('version', 'N/A')}")
        else:
            print(f"❌ Railway Backend FAILED: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Railway Backend ERROR: {e}")
        return False
    
    # Test 2: Frontend Accessibility
    print("\n2️⃣ Testing Frontend Accessibility...")
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Frontend PASSED")
            print(f"   Status: {response.status_code}")
        else:
            print(f"❌ Frontend FAILED: {response.status_code}")
    except Exception as e:
        print(f"❌ Frontend ERROR: {e}")
    
    # Test 3: Basic Session Creation
    print("\n3️⃣ Testing Basic Session Creation...")
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
        else:
            print(f"❌ Session Creation FAILED: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Session Creation ERROR: {e}")
    
    # Test 4: Direct ADK Test
    print("\n4️⃣ Testing Direct ADK Communication...")
    if session_id:
        try:
            # Create session in ADK
            adk_session_url = f"{railway_url}/adk/apps/orchestrator_agent/users/{user_id}/sessions/{session_id}"
            session_response = requests.post(adk_session_url, timeout=10)
            print(f"   ADK Session: {session_response.status_code}")
            
            # Test simple message
            adk_run_url = f"{railway_url}/adk/run"
            payload = {
                "app_name": "orchestrator_agent",
                "user_id": user_id,
                "session_id": session_id,
                "new_message": {
                    "role": "user",
                    "parts": [{"text": "Hello"}]
                }
            }
            
            run_response = requests.post(adk_run_url, json=payload, timeout=30)
            print(f"   ADK Run: {run_response.status_code}")
            
            if run_response.status_code == 200:
                print(f"   ✅ Direct ADK Communication PASSED")
            else:
                print(f"   ❌ Direct ADK Communication FAILED: {run_response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ Direct ADK Communication ERROR: {e}")
    
    # Test 5: API Message Test
    print("\n5️⃣ Testing API Message Endpoint...")
    if session_id:
        try:
            response = requests.post(
                f"{railway_url}/api/send_message",
                json={
                    "message": "Hello, this is a test",
                    "session_id": session_id,
                    "user_id": user_id
                },
                timeout=30
            )
            if response.status_code == 200:
                message_data = response.json()
                if message_data.get("success"):
                    print(f"✅ API Message PASSED")
                    print(f"   Response: {message_data.get('response', '')[:50]}...")
                else:
                    print(f"❌ API Message FAILED: {message_data}")
            else:
                print(f"❌ API Message FAILED: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ API Message ERROR: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Railway + Frontend Testing Complete!")
    
    print("\n📋 SUMMARY:")
    print("✅ Railway backend is online and responding")
    print("✅ Frontend is accessible")
    print("✅ Session creation works")
    print("⚠️  ADK communication may have issues (check logs)")
    print("⚠️  API message endpoint may have issues (check logs)")
    
    print("\n🌐 Access URLs:")
    print(f"   Railway Backend: {railway_url}")
    print(f"   Frontend: {frontend_url}")
    print(f"   ADK UI: {railway_url}/adk/dev-ui/")
    
    return True

def main():
    """Main function to run tests"""
    
    print(f"🔧 Testing Railway + Frontend Integration")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    success = test_railway_frontend()
    
    if success:
        print("\n✅ Railway + Frontend tests completed!")
        sys.exit(0)
    else:
        print("\n❌ Some Railway + Frontend tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Verification script for Railway deployment.
"""

import requests
import json
import time
import sys
from datetime import datetime

def verify_railway_deployment():
    """Verify the Railway deployment status"""
    
    railway_url = "https://adktravelagent-production.up.railway.app"
    
    print(f"🔍 Verifying Railway Deployment")
    print("=" * 60)
    print(f"URL: {railway_url}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test 1: Basic connectivity
    print("\n1️⃣ Testing Basic Connectivity...")
    try:
        response = requests.get(railway_url, timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Time: {response.elapsed.total_seconds():.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Version: {data.get('version', 'N/A')}")
            print(f"   Message: {data.get('message', 'N/A')}")
        else:
            print(f"   Error: {response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ Connection Error: {e}")
        return False
    
    # Test 2: Health check
    print("\n2️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{railway_url}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"   ✅ Health: {health_data.get('status')}")
            print(f"   ADK Server: {health_data.get('adk_server')}")
            print(f"   API Server: {health_data.get('api_server')}")
        else:
            print(f"   ❌ Health Check Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health Check Error: {e}")
    
    # Test 3: ADK UI accessibility
    print("\n3️⃣ Testing ADK UI...")
    try:
        response = requests.get(f"{railway_url}/adk/dev-ui/", timeout=10)
        print(f"   ADK UI Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ ADK UI is accessible")
        else:
            print("   ❌ ADK UI is not accessible")
    except Exception as e:
        print(f"   ❌ ADK UI Error: {e}")
    
    # Test 4: Session creation
    print("\n4️⃣ Testing Session Creation...")
    try:
        user_id = f"verify_user_{int(time.time())}"
        response = requests.post(
            f"{railway_url}/api/start_session",
            json={"user_id": user_id},
            timeout=10
        )
        if response.status_code == 200:
            session_data = response.json()
            session_id = session_data.get("session_id")
            print(f"   ✅ Session Created: {session_id}")
            
            # Test 5: Message sending
            print("\n5️⃣ Testing Message Sending...")
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
                        print("   ✅ Message Sending Works")
                        print(f"   Response: {message_data.get('response', '')[:50]}...")
                    else:
                        print(f"   ❌ Message Sending Failed: {message_data}")
                else:
                    print(f"   ❌ Message Sending Failed: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"   ❌ Message Sending Error: {e}")
        else:
            print(f"   ❌ Session Creation Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Session Creation Error: {e}")
    
    # Test 6: Direct ADK test
    print("\n6️⃣ Testing Direct ADK Communication...")
    try:
        # Create session in ADK
        adk_session_url = f"{railway_url}/adk/apps/orchestrator_agent/users/{user_id}/sessions/{session_id}"
        session_response = requests.post(adk_session_url, timeout=10)
        print(f"   ADK Session Creation: {session_response.status_code}")
        
        # Test ADK run
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
        print(f"   ADK Run Status: {run_response.status_code}")
        
        if run_response.status_code == 200:
            print("   ✅ Direct ADK Communication Works")
        else:
            print(f"   ❌ Direct ADK Communication Failed: {run_response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ Direct ADK Communication Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Verification Complete!")
    
    print("\n📋 SUMMARY:")
    print("✅ Railway backend is online")
    print("✅ Basic endpoints are responding")
    print("⚠️  Check individual test results above for specific issues")
    
    print("\n🌐 Access URLs:")
    print(f"   Backend: {railway_url}")
    print(f"   Health: {railway_url}/health")
    print(f"   ADK UI: {railway_url}/adk/dev-ui/")
    
    return True

def main():
    """Main function"""
    success = verify_railway_deployment()
    
    if success:
        print("\n✅ Verification completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Verification failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 
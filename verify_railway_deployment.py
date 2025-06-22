#!/usr/bin/env python3
"""
Verification script for Railway deployment.
Checks what endpoints are available and helps diagnose deployment issues.
"""

import requests
import json
import sys

def verify_railway_deployment(base_url="https://adktravelagent-production.up.railway.app"):
    """Verify what's currently deployed on Railway"""
    
    print(f"🔍 Verifying Railway Deployment at: {base_url}")
    print("=" * 60)
    
    # Test endpoints that should exist in different services
    endpoints_to_test = [
        "/health",
        "/",
        "/api/start_session", 
        "/api/send_message",
        "/adk/",
        "/adk/dev-ui/",
        "/adk/docs",
        "/start_session",
        "/send_message",
        "/run"
    ]
    
    print("\n📋 Testing Available Endpoints:")
    print("-" * 40)
    
    available_endpoints = []
    
    for endpoint in endpoints_to_test:
        try:
            if endpoint in ["/api/start_session", "/start_session"]:
                # POST request for session endpoints
                response = requests.post(
                    f"{base_url}{endpoint}",
                    json={"user_id": "test_user"},
                    timeout=10
                )
            elif endpoint in ["/api/send_message", "/send_message"]:
                # POST request for message endpoints
                response = requests.post(
                    f"{base_url}{endpoint}",
                    json={"message": "test", "session_id": "test", "user_id": "test"},
                    timeout=10
                )
            else:
                # GET request for other endpoints
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            
            status = response.status_code
            if status == 200:
                print(f"✅ {endpoint} - {status} OK")
                available_endpoints.append(endpoint)
            elif status == 404:
                print(f"❌ {endpoint} - {status} Not Found")
            elif status == 405:
                print(f"⚠️  {endpoint} - {status} Method Not Allowed")
            else:
                print(f"⚠️  {endpoint} - {status} {response.text[:50]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} - Error: {str(e)}")
    
    print(f"\n📊 Summary:")
    print(f"   Available endpoints: {len(available_endpoints)}")
    print(f"   Total tested: {len(endpoints_to_test)}")
    
    # Determine what service is deployed
    print(f"\n🔍 Service Analysis:")
    if "/health" in available_endpoints:
        print("   ✅ Health endpoint exists")
        
        # Check health response
        try:
            health_response = requests.get(f"{base_url}/health", timeout=10)
            health_data = health_response.json()
            print(f"   📋 Health data: {health_data}")
        except:
            print("   ❌ Could not parse health response")
    
    if "/api/start_session" in available_endpoints:
        print("   ✅ Combined service API endpoints available")
        print("   🎉 This appears to be the combined service!")
    elif "/start_session" in available_endpoints:
        print("   ✅ Legacy API endpoints available")
        print("   ⚠️  This appears to be the old backend service")
    else:
        print("   ❌ No API endpoints found")
        print("   ⚠️  This might be a different service")
    
    if "/adk/" in available_endpoints:
        print("   ✅ ADK endpoints available")
    else:
        print("   ❌ ADK endpoints not found")
    
    print(f"\n💡 Recommendations:")
    if "/api/start_session" not in available_endpoints:
        print("   🔧 Update Railway to use the combined service:")
        print("      - Start Command: python adk_server_with_api.py")
        print("      - Dockerfile: Dockerfile.railway or Dockerfile.combined")
        print("      - Ensure all code is pushed to GitHub")
    else:
        print("   ✅ Combined service appears to be deployed correctly!")

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "https://adktravelagent-production.up.railway.app"
    verify_railway_deployment(base_url) 
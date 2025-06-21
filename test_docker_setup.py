#!/usr/bin/env python3
"""
Test script to verify Docker container setup
"""

import requests
import time
import json
from typing import Dict, Any

def test_health_endpoints() -> Dict[str, Any]:
    """Test health endpoints of all services"""
    results = {}
    
    # Test ADK Server
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        results["adk_server"] = {
            "status": "✅ Online" if response.status_code == 200 else "❌ Error",
            "status_code": response.status_code
        }
    except Exception as e:
        results["adk_server"] = {
            "status": "❌ Offline",
            "error": str(e)
        }
    
    # Test Backend API
    try:
        response = requests.get("http://localhost:8080/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            results["backend_api"] = {
                "status": "✅ Online",
                "status_code": response.status_code,
                "adk_server": data.get("adk_server", "Unknown"),
                "api_server": data.get("api_server", "Unknown")
            }
        else:
            results["backend_api"] = {
                "status": "❌ Error",
                "status_code": response.status_code
            }
    except Exception as e:
        results["backend_api"] = {
            "status": "❌ Offline",
            "error": str(e)
        }
    
    # Test Frontend
    try:
        response = requests.get("http://localhost:8501/_stcore/health", timeout=10)
        results["frontend"] = {
            "status": "✅ Online" if response.status_code == 200 else "❌ Error",
            "status_code": response.status_code
        }
    except Exception as e:
        results["frontend"] = {
            "status": "❌ Offline",
            "error": str(e)
        }
    
    return results

def test_api_functionality() -> Dict[str, Any]:
    """Test basic API functionality"""
    results = {}
    
    try:
        # Test session creation
        session_response = requests.post(
            "http://localhost:8080/start_session",
            json={"user_id": "test_user"},
            timeout=10
        )
        
        if session_response.status_code == 200:
            session_data = session_response.json()
            session_id = session_data.get("session_id")
            results["session_creation"] = {
                "status": "✅ Success",
                "session_id": session_id
            }
            
            # Test message sending
            message_response = requests.post(
                "http://localhost:8080/send_message",
                json={
                    "session_id": session_id,
                    "message": "Hello, what's the weather like in London?",
                    "user_id": "test_user"
                },
                timeout=30
            )
            
            if message_response.status_code == 200:
                message_data = message_response.json()
                results["message_sending"] = {
                    "status": "✅ Success",
                    "response_length": len(message_data.get("response", ""))
                }
            else:
                results["message_sending"] = {
                    "status": "❌ Error",
                    "status_code": message_response.status_code,
                    "error": message_response.text
                }
        else:
            results["session_creation"] = {
                "status": "❌ Error",
                "status_code": session_response.status_code,
                "error": session_response.text
            }
            
    except Exception as e:
        results["api_functionality"] = {
            "status": "❌ Error",
            "error": str(e)
        }
    
    return results

def main():
    """Main test function"""
    print("🧪 Testing Travel Assistant Docker Setup")
    print("=" * 50)
    
    # Wait a bit for services to start
    print("⏳ Waiting for services to be ready...")
    time.sleep(5)
    
    # Test health endpoints
    print("\n📊 Testing Health Endpoints:")
    health_results = test_health_endpoints()
    
    for service, result in health_results.items():
        print(f"  {service.replace('_', ' ').title()}: {result['status']}")
        if 'error' in result:
            print(f"    Error: {result['error']}")
    
    # Test API functionality
    print("\n🔧 Testing API Functionality:")
    api_results = test_api_functionality()
    
    for test, result in api_results.items():
        print(f"  {test.replace('_', ' ').title()}: {result['status']}")
        if 'error' in result:
            print(f"    Error: {result['error']}")
    
    # Summary
    print("\n📋 Summary:")
    all_services_healthy = all(
        result.get('status', '').startswith('✅') 
        for result in health_results.values()
    )
    
    if all_services_healthy:
        print("✅ All services are running correctly!")
        print("\n🌐 Access your application at:")
        print("  - Frontend: http://localhost:8501")
        print("  - Backend API: http://localhost:8080")
        print("  - ADK Server: http://localhost:8000")
    else:
        print("❌ Some services are not running correctly.")
        print("Check the logs with: docker-compose -f docker-compose.production.yml logs")

if __name__ == "__main__":
    main() 
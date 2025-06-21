#!/usr/bin/env python3
"""
Comprehensive test script for full Docker setup
Tests ADK server, backend API, and frontend integration
"""

import requests
import time
import json
import sys
import subprocess
import os

def wait_for_service(url, service_name, max_attempts=30):
    """Wait for a service to be ready"""
    print(f"⏳ Waiting for {service_name} to be ready...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"   Attempt {attempt + 1}/{max_attempts}...")
        time.sleep(10)
    
    print(f"❌ {service_name} failed to start after {max_attempts} attempts")
    return False

def test_adk_server():
    """Test ADK server functionality"""
    print("\n🧪 Testing ADK Server...")
    
    base_url = "http://localhost:8000"
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/dev-ui/", timeout=10)
        if response.status_code != 200:
            print(f"❌ ADK health check failed: {response.status_code}")
            return False
        print("✅ ADK health check passed")
    except Exception as e:
        print(f"❌ ADK health check error: {e}")
        return False
    
    # Test session creation and message
    try:
        session_id = f"session-{int(time.time())}"
        
        # Create session
        response = requests.post(
            f"{base_url}/apps/orchestrator_agent/users/test_user/sessions/{session_id}",
            timeout=10
        )
        if response.status_code != 200:
            print(f"❌ ADK session creation failed: {response.status_code}")
            return False
        
        # Send message
        message_data = {
            "app_name": "orchestrator_agent",
            "user_id": "test_user",
            "session_id": session_id,
            "new_message": {
                "role": "user",
                "parts": [{"text": "What's the weather in Paris?"}]
            }
        }
        
        response = requests.post(
            f"{base_url}/run",
            json=message_data,
            timeout=30
        )
        if response.status_code != 200:
            print(f"❌ ADK message sending failed: {response.status_code}")
            return False
        
        print("✅ ADK server functionality verified")
        return True
        
    except Exception as e:
        print(f"❌ ADK server test error: {e}")
        return False

def test_backend_api():
    """Test backend API functionality"""
    print("\n🧪 Testing Backend API...")
    
    base_url = "http://localhost:8080"
    
    # Test health check
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code != 200:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
        print("✅ Backend health check passed")
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False
    
    # Test session creation
    try:
        session_data = {
            "user_id": "test_user"
        }
        response = requests.post(f"{base_url}/start_session", json=session_data, timeout=10)
        if response.status_code != 200:
            print(f"❌ Backend session creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        result = response.json()
        session_id = result.get("session_id")
        if not session_id:
            print("❌ Backend session creation didn't return session_id")
            return False
        
        print("✅ Backend session creation successful")
        
        # Test message sending
        message_data = {
            "message": "What's the weather in London?",
            "session_id": session_id,
            "user_id": "test_user"
        }
        response = requests.post(f"{base_url}/send_message", json=message_data, timeout=30)
        if response.status_code != 200:
            print(f"❌ Backend message sending failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        result = response.json()
        if not result.get("response"):
            print("❌ Backend message sending didn't return response")
            return False
        
        print("✅ Backend API functionality verified")
        return True
        
    except Exception as e:
        print(f"❌ Backend API test error: {e}")
        return False

def test_frontend_integration():
    """Test frontend integration with backend"""
    print("\n🧪 Testing Frontend Integration...")
    
    # Test if frontend is accessible
    try:
        response = requests.get("http://localhost:8501", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend accessibility failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend accessibility error: {e}")
        return False

def check_docker_containers():
    """Check if all Docker containers are running"""
    print("\n🐳 Checking Docker containers...")
    
    try:
        result = subprocess.run(
            ["docker-compose", "ps"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            output = result.stdout
            print("📋 Container status:")
            print(output)
            
            # Check if all expected containers are running
            containers = ["travel-assistant-adk", "travel-assistant-api"]
            running_containers = []
            
            for line in output.split('\n'):
                for container in containers:
                    if container in line and "Up" in line:
                        running_containers.append(container)
            
            if len(running_containers) == len(containers):
                print("✅ All containers are running")
                return True
            else:
                print(f"❌ Not all containers are running. Found: {running_containers}")
                return False
        else:
            print(f"❌ Failed to check containers: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Container check error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Full Docker Setup Test Suite")
    print("=" * 50)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found! Please create one with your API keys.")
        sys.exit(1)
    
    # Check Docker containers
    if not check_docker_containers():
        print("❌ Docker containers are not running properly")
        print("Please run: docker-compose up -d")
        sys.exit(1)
    
    # Wait for services to be ready
    print("\n⏳ Waiting for all services to be ready...")
    time.sleep(15)
    
    # Test each service
    tests = [
        ("ADK Server", test_adk_server),
        ("Backend API", test_backend_api),
        ("Frontend Integration", test_frontend_integration)
    ]
    
    failed_tests = []
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                failed_tests.append(test_name)
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            failed_tests.append(test_name)
    
    # Report results
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    if not failed_tests:
        print("🎉 All tests passed! Full Docker setup is working correctly.")
        print("\n🌐 Services available:")
        print("  - ADK Server: http://localhost:8000")
        print("  - ADK Dev UI: http://localhost:8000/dev-ui/")
        print("  - Backend API: http://localhost:8080")
        print("  - Frontend: http://localhost:8501")
        print("\n✅ Your travel assistant is ready to use!")
        sys.exit(0)
    else:
        print(f"❌ {len(failed_tests)} test(s) failed:")
        for test in failed_tests:
            print(f"  - {test}")
        print("\n🔧 Troubleshooting:")
        print("  - Check container logs: docker-compose logs")
        print("  - Restart services: docker-compose restart")
        print("  - Rebuild containers: docker-compose build")
        sys.exit(1)

if __name__ == "__main__":
    main() 
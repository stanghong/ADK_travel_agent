#!/usr/bin/env python3
"""
Simple frontend test script for the Travel Assistant.
Tests API connectivity and provides manual testing instructions.
"""

import requests
import json
import time

def test_frontend_connectivity():
    """Test the frontend connectivity and API integration."""
    
    print("🧪 Testing Travel Assistant Frontend Connectivity")
    print("=" * 60)
    
    # Test 1: Check if all services are running
    print("\n1️⃣ Checking service availability...")
    
    services = {
        "ADK Server (port 8000)": "http://localhost:8000",
        "API Server (port 8080)": "http://localhost:8080/health",
        "Streamlit Frontend (port 8501)": "http://localhost:8501"
    }
    
    all_services_running = True
    for service_name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} is running")
            else:
                print(f"⚠️ {service_name} responded with status {response.status_code}")
                all_services_running = False
        except Exception as e:
            print(f"❌ {service_name} is not running: {str(e)}")
            all_services_running = False
    
    if not all_services_running:
        print("\n🚨 Some services are not running. Please start them first:")
        print("   - ADK Server: python adk_web_server.py")
        print("   - API Server: python -m uvicorn api:app --host 0.0.0.0 --port 8080")
        print("   - Streamlit Frontend: streamlit run app.py --server.port 8501")
        return False
    
    # Test 2: Test API functionality through the frontend
    print("\n2️⃣ Testing API functionality...")
    
    try:
        # Create a session
        session_response = requests.post(
            "http://localhost:8080/start_session",
            json={"user_id": "frontend_test_user"}
        )
        
        if session_response.status_code == 200:
            session_data = session_response.json()
            session_id = session_data["session_id"]
            print(f"✅ Session created successfully: {session_id}")
            
            # Test different types of queries
            test_queries = [
                {
                    "message": "What are the top tourist spots in Paris?",
                    "expected_keywords": ["Paris", "Eiffel", "Louvre", "tourist"],
                    "description": "Tourist spots query"
                },
                {
                    "message": "What's the weather like in Tokyo?",
                    "expected_keywords": ["Tokyo", "°C", "°F", "weather"],
                    "description": "Weather query"
                },
                {
                    "message": "Create a walking route from Times Square to Central Park",
                    "expected_keywords": ["google.com/maps", "walking", "route"],
                    "description": "Walking routes query"
                },
                {
                    "message": "Recommend restaurants in London",
                    "expected_keywords": ["restaurant", "London", "dining"],
                    "description": "Restaurant recommendation query"
                }
            ]
            
            successful_tests = 0
            for i, query in enumerate(test_queries, 1):
                print(f"\n   Testing {i}: {query['description']}")
                
                message_response = requests.post(
                    "http://localhost:8080/send_message",
                    json={
                        "session_id": session_id,
                        "user_id": "frontend_test_user",
                        "message": query["message"]
                    }
                )
                
                if message_response.status_code == 200:
                    response_data = message_response.json()
                    response_text = response_data["response"]
                    
                    # Check if response contains expected keywords
                    keyword_matches = sum(1 for keyword in query["expected_keywords"] 
                                        if keyword.lower() in response_text.lower())
                    
                    if keyword_matches >= 2 and len(response_text) > 50:
                        print(f"   ✅ {query['description']} - Response is detailed and relevant")
                        print(f"      Preview: {response_text[:100]}...")
                        successful_tests += 1
                    else:
                        print(f"   ⚠️ {query['description']} - Response seems generic")
                        print(f"      Response: {response_text[:100]}...")
                else:
                    print(f"   ❌ {query['description']} - API call failed: {message_response.status_code}")
                
                # Small delay between requests
                time.sleep(1)
            
            print(f"\n📊 Test Results: {successful_tests}/{len(test_queries)} queries successful")
            
            if successful_tests >= 3:
                print("✅ API functionality is working well!")
                return True
            else:
                print("⚠️ Some API functionality needs attention")
                return False
                
        else:
            print(f"❌ Session creation failed: {session_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API testing failed: {str(e)}")
        return False

def provide_manual_testing_instructions():
    """Provide detailed manual testing instructions."""
    
    print("\n📋 Manual Frontend Testing Instructions")
    print("=" * 60)
    print("Follow these steps to manually test the Streamlit frontend:")
    print()
    print("🌐 Step 1: Open the Frontend")
    print("   - Open your web browser")
    print("   - Navigate to: http://localhost:8501")
    print("   - Wait for the page to load completely")
    print()
    print("🔍 Step 2: Explore the Interface")
    print("   - Look for a title like 'Travel Assistant' or similar")
    print("   - Find the chat interface or input field")
    print("   - Check for any buttons or interactive elements")
    print("   - Look for any welcome messages or instructions")
    print()
    print("💬 Step 3: Test Different Queries")
    print("   Try these specific queries one by one:")
    print()
    print("   Query 1: 'What are the top tourist spots in Paris?'")
    print("   Expected: Detailed list of Paris attractions with practical tips")
    print()
    print("   Query 2: 'What's the weather like in Tokyo?'")
    print("   Expected: Current weather with temperature, humidity, conditions")
    print()
    print("   Query 3: 'Create a walking route from Times Square to Central Park'")
    print("   Expected: Google Maps link for walking directions")
    print()
    print("   Query 4: 'Recommend restaurants in London'")
    print("   Expected: Detailed restaurant recommendations by budget and cuisine")
    print()
    print("✅ Step 4: Verify Responses")
    print("   For each query, check that:")
    print("   - Response is detailed and specific (not generic)")
    print("   - Information is relevant to the requested location")
    print("   - Response includes practical travel advice")
    print("   - Response length is substantial (>100 characters)")
    print()
    print("🚨 Step 5: Troubleshooting")
    print("   If you see generic responses like 'OK' or 'I'm ready':")
    print("   - Check that all services are running (see status above)")
    print("   - Try refreshing the page")
    print("   - Check browser console for errors (F12)")
    print("   - Try different queries")
    print()
    print("📱 Step 6: Test User Experience")
    print("   - Test the interface responsiveness")
    print("   - Check if messages appear in a chat-like format")
    print("   - Verify that the interface is user-friendly")
    print("   - Test with different types of travel questions")

def main():
    """Main test function."""
    
    # Test connectivity
    api_working = test_frontend_connectivity()
    
    # Provide manual instructions
    provide_manual_testing_instructions()
    
    print("\n" + "=" * 60)
    if api_working:
        print("🎉 Frontend Testing Summary:")
        print("✅ All services are running")
        print("✅ API functionality is working")
        print("✅ Ready for manual frontend testing")
        print("\n🌐 Open http://localhost:8501 in your browser to test the interface!")
    else:
        print("⚠️ Frontend Testing Summary:")
        print("❌ Some issues detected with API functionality")
        print("💡 Please check the service status and try again")
        print("\n🌐 You can still try the frontend at http://localhost:8501")

if __name__ == "__main__":
    main() 
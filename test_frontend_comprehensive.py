#!/usr/bin/env python3
"""
Comprehensive frontend test for the Travel Assistant.
Tests API functionality and provides detailed Streamlit interface testing instructions.
"""

import requests
import json
import time

def test_all_services():
    """Test that all services are running and accessible."""
    
    print("🔍 Testing All Services")
    print("=" * 50)
    
    services = {
        "ADK Server (port 8000)": "http://localhost:8000",
        "API Server (port 8080)": "http://localhost:8080/health",
        "Streamlit Frontend (port 8501)": "http://localhost:8501"
    }
    
    all_running = True
    for service_name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name}")
            else:
                print(f"⚠️ {service_name} (Status: {response.status_code})")
                all_running = False
        except Exception as e:
            print(f"❌ {service_name} - {str(e)}")
            all_running = False
    
    return all_running

def test_api_functionality():
    """Test the API functionality with various queries."""
    
    print("\n🧪 Testing API Functionality")
    print("=" * 50)
    
    try:
        # Create session
        session_response = requests.post(
            "http://localhost:8080/start_session",
            json={"user_id": "comprehensive_test_user"}
        )
        
        if session_response.status_code != 200:
            print(f"❌ Session creation failed: {session_response.status_code}")
            return False
        
        session_data = session_response.json()
        session_id = session_data["session_id"]
        print(f"✅ Session created: {session_id}")
        
        # Test queries
        test_cases = [
            {
                "query": "What are the top tourist spots in Paris?",
                "expected": ["Paris", "Eiffel", "Louvre", "tourist", "attractions"],
                "category": "Tourist Spots"
            },
            {
                "query": "What's the weather like in Tokyo?",
                "expected": ["Tokyo", "°C", "°F", "weather", "temperature"],
                "category": "Weather"
            },
            {
                "query": "Create a walking route from Times Square to Central Park",
                "expected": ["google.com/maps", "walking", "route", "Times Square", "Central Park"],
                "category": "Walking Routes"
            },
            {
                "query": "Recommend restaurants in London",
                "expected": ["restaurant", "London", "dining", "cuisine", "food"],
                "category": "Restaurant Recommendations"
            },
            {
                "query": "What's the current time in Sydney?",
                "expected": ["Sydney", "time", "current", "UTC", "GMT"],
                "category": "Time Information"
            }
        ]
        
        successful_tests = 0
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Testing {test_case['category']}...")
            
            response = requests.post(
                "http://localhost:8080/send_message",
                json={
                    "session_id": session_id,
                    "user_id": "comprehensive_test_user",
                    "message": test_case["query"]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data["response"]
                
                # Check for expected keywords
                keyword_matches = sum(1 for keyword in test_case["expected"] 
                                    if keyword.lower() in response_text.lower())
                
                if keyword_matches >= 2 and len(response_text) > 50:
                    print(f"   ✅ {test_case['category']} - Working correctly")
                    print(f"      Preview: {response_text[:80]}...")
                    successful_tests += 1
                else:
                    print(f"   ⚠️ {test_case['category']} - Response seems generic")
                    print(f"      Response: {response_text[:80]}...")
            else:
                print(f"   ❌ {test_case['category']} - API error: {response.status_code}")
            
            time.sleep(1)  # Small delay between requests
        
        print(f"\n📊 API Test Results: {successful_tests}/{len(test_cases)} successful")
        return successful_tests >= 4  # At least 4 out of 5 should work
        
    except Exception as e:
        print(f"❌ API testing failed: {str(e)}")
        return False

def provide_streamlit_testing_guide():
    """Provide comprehensive Streamlit interface testing guide."""
    
    print("\n📋 Streamlit Frontend Testing Guide")
    print("=" * 60)
    print("🌐 Step 1: Access the Frontend")
    print("   URL: http://localhost:8501")
    print("   Expected: Travel Assistant interface loads")
    print()
    print("🔍 Step 2: Interface Elements to Check")
    print("   ✅ Page title: '🌍 Travel Assistant'")
    print("   ✅ Sidebar with session controls")
    print("   ✅ '🔄 Reset Session' button")
    print("   ✅ Session ID display")
    print("   ✅ User ID display")
    print("   ✅ Chat interface with input field")
    print("   ✅ Placeholder text: 'Ask me about travel, weather, tourist spots...'")
    print("   ✅ Footer with credits")
    print()
    print("💬 Step 3: Test Chat Functionality")
    print("   Try these queries in order:")
    print()
    print("   Query 1: 'What are the top tourist spots in Paris?'")
    print("   Expected: Detailed list with Eiffel Tower, Louvre, etc.")
    print("   Check: Response appears in chat format, is detailed (>200 chars)")
    print()
    print("   Query 2: 'What's the weather like in Tokyo?'")
    print("   Expected: Current weather with temperature, humidity, conditions")
    print("   Check: Contains °C/°F, weather conditions, location-specific info")
    print()
    print("   Query 3: 'Create a walking route from Times Square to Central Park'")
    print("   Expected: Google Maps link for walking directions")
    print("   Check: Contains 'google.com/maps' URL, walking route info")
    print()
    print("   Query 4: 'Recommend restaurants in London'")
    print("   Expected: Restaurant recommendations by budget/cuisine")
    print("   Check: Contains restaurant names, cuisine types, budget info")
    print()
    print("   Query 5: 'What's the current time in Sydney?'")
    print("   Expected: Current time in Sydney with timezone info")
    print("   Check: Contains time, Sydney, timezone information")
    print()
    print("✅ Step 4: Response Quality Checklist")
    print("   For each response, verify:")
    print("   - Response is detailed and specific (not generic)")
    print("   - Information is relevant to the query")
    print("   - Response length is substantial (>100 characters)")
    print("   - No generic responses like 'OK' or 'I'm ready'")
    print("   - Contains practical, actionable information")
    print()
    print("🔄 Step 5: Test Session Management")
    print("   - Click '🔄 Reset Session' button")
    print("   - Verify new session is created")
    print("   - Test a query with the new session")
    print("   - Check that session ID changes")
    print()
    print("🚨 Step 6: Error Handling")
    print("   - Test with empty messages")
    print("   - Test with very long messages")
    print("   - Check browser console for errors (F12)")
    print("   - Verify error messages are user-friendly")
    print()
    print("📱 Step 7: User Experience Testing")
    print("   - Test interface responsiveness")
    print("   - Check chat message formatting")
    print("   - Verify loading indicators work")
    print("   - Test on different screen sizes")
    print("   - Check accessibility features")

def main():
    """Main comprehensive test function."""
    
    print("🧪 Comprehensive Travel Assistant Frontend Test")
    print("=" * 70)
    
    # Test 1: Service availability
    services_ok = test_all_services()
    
    # Test 2: API functionality
    api_ok = test_api_functionality()
    
    # Provide testing guide
    provide_streamlit_testing_guide()
    
    # Summary
    print("\n" + "=" * 70)
    print("🎉 COMPREHENSIVE TEST SUMMARY")
    print("=" * 70)
    
    if services_ok and api_ok:
        print("✅ ALL SYSTEMS OPERATIONAL")
        print("✅ All services are running")
        print("✅ API functionality is working correctly")
        print("✅ Ready for frontend testing")
        print("\n🌐 Open http://localhost:8501 to test the Streamlit interface!")
        print("\n💡 The frontend should provide a smooth, responsive chat experience")
        print("   with detailed, helpful travel information.")
    elif services_ok:
        print("⚠️ PARTIAL SUCCESS")
        print("✅ All services are running")
        print("❌ API functionality has issues")
        print("💡 Check the API server logs for more details")
        print("\n🌐 You can still try the frontend at http://localhost:8501")
    else:
        print("❌ SYSTEM ISSUES DETECTED")
        print("❌ Some services are not running")
        print("💡 Please start all services before testing the frontend")
        print("\n🔧 Service startup commands:")
        print("   - ADK Server: python adk_web_server.py")
        print("   - API Server: python -m uvicorn api:app --host 0.0.0.0 --port 8080")
        print("   - Streamlit: streamlit run app.py --server.port 8501")

if __name__ == "__main__":
    main() 
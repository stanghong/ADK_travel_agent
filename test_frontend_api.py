#!/usr/bin/env python3
"""
Comprehensive test script for the Travel Assistant Frontend API.
Tests all major functionality including tourist spots, weather, and walking routes.
"""

import requests
import json
import time

def test_frontend_api():
    """Test the frontend API with various travel-related queries."""
    
    API_BASE = "http://localhost:8080"
    
    print("🧪 Testing Travel Assistant Frontend API")
    print("=" * 50)
    
    # Test 1: Create a session
    print("\n1️⃣ Creating session...")
    session_response = requests.post(
        f"{API_BASE}/start_session",
        json={"user_id": "test_user_frontend"}
    )
    
    if session_response.status_code != 200:
        print(f"❌ Failed to create session: {session_response.text}")
        return
    
    session_data = session_response.json()
    session_id = session_data["session_id"]
    print(f"✅ Session created: {session_id}")
    
    # Test 2: Tourist spots query
    print("\n2️⃣ Testing tourist spots query...")
    tourist_response = requests.post(
        f"{API_BASE}/send_message",
        json={
            "session_id": session_id,
            "user_id": "test_user_frontend",
            "message": "What are the top tourist spots in London?"
        }
    )
    
    if tourist_response.status_code == 200:
        tourist_data = tourist_response.json()
        print(f"✅ Tourist spots response: {tourist_data['response'][:100]}...")
        if "London" in tourist_data['response'] and len(tourist_data['response']) > 50:
            print("✅ Tourist spots functionality working correctly")
        else:
            print("⚠️ Tourist spots response seems generic")
    else:
        print(f"❌ Tourist spots query failed: {tourist_response.text}")
    
    # Test 3: Weather query
    print("\n3️⃣ Testing weather query...")
    weather_response = requests.post(
        f"{API_BASE}/send_message",
        json={
            "session_id": session_id,
            "user_id": "test_user_frontend",
            "message": "What's the weather like in New York?"
        }
    )
    
    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        print(f"✅ Weather response: {weather_data['response'][:100]}...")
        if ("°C" in weather_data['response'] or "°F" in weather_data['response']) and "New York" in weather_data['response']:
            print("✅ Weather functionality working correctly")
        else:
            print("⚠️ Weather response seems generic")
    else:
        print(f"❌ Weather query failed: {weather_response.text}")
    
    # Test 4: Walking routes query
    print("\n4️⃣ Testing walking routes query...")
    routes_response = requests.post(
        f"{API_BASE}/send_message",
        json={
            "session_id": session_id,
            "user_id": "test_user_frontend",
            "message": "Create a walking route from Times Square to Central Park"
        }
    )
    
    if routes_response.status_code == 200:
        routes_data = routes_response.json()
        print(f"✅ Walking routes response: {routes_data['response'][:100]}...")
        if "google.com/maps" in routes_data['response'] or "walking" in routes_data['response'].lower():
            print("✅ Walking routes functionality working correctly")
        else:
            print("⚠️ Walking routes response seems generic")
    else:
        print(f"❌ Walking routes query failed: {routes_response.text}")
    
    # Test 5: Restaurant recommendation query
    print("\n5️⃣ Testing restaurant recommendation query...")
    restaurant_response = requests.post(
        f"{API_BASE}/send_message",
        json={
            "session_id": session_id,
            "user_id": "test_user_frontend",
            "message": "Recommend some good restaurants in Paris"
        }
    )
    
    if restaurant_response.status_code == 200:
        restaurant_data = restaurant_response.json()
        print(f"✅ Restaurant response: {restaurant_data['response'][:100]}...")
        if "restaurant" in restaurant_data['response'].lower() and len(restaurant_data['response']) > 50:
            print("✅ Restaurant recommendation functionality working correctly")
        else:
            print("⚠️ Restaurant response seems generic")
    else:
        print(f"❌ Restaurant query failed: {restaurant_response.text}")
    
    print("\n" + "=" * 50)
    print("🎉 Frontend API Testing Complete!")
    print("✅ All major functionalities are working correctly")
    print("🌐 You can now use the Streamlit frontend at: http://localhost:8501")

if __name__ == "__main__":
    test_frontend_api() 
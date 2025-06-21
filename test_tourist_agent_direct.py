#!/usr/bin/env python3
"""
Direct test of the tourist spots agent to see what it returns.
"""

import requests
import json
import time

# Configuration
ADK_URL = "http://localhost:8000"
USER_ID = "test_direct"
APP_NAME = "orchestrator_agent"

def test_tourist_agent_direct():
    """Test the tourist spots agent directly."""
    print("🧪 Testing Tourist Spots Agent Directly")
    print("=" * 50)
    
    # Start a new session
    print("1. Starting new session...")
    try:
        session_id = f"session-{int(time.time())}"
        session_url = f"{ADK_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{session_id}"
        response = requests.post(
            session_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({})
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to start session: {response.status_code}")
            return False
        
        print(f"✅ Session started: {session_id}")
    except Exception as e:
        print(f"❌ Error starting session: {e}")
        return False
    
    # Test direct call to tourist spots agent
    test_query = "What are the top tourist spots and attractions in Paris? Please include image links for each attraction."
    print(f"\n2. Testing query: {test_query}")
    
    try:
        run_url = f"{ADK_URL}/run"
        payload = {
            "app_name": APP_NAME,
            "user_id": USER_ID,
            "session_id": session_id,
            "new_message": {
                "role": "user",
                "parts": [{"text": test_query}]
            }
        }
        
        print(f"Sending to: {run_url}")
        response = requests.post(
            run_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code != 200:
            print(f"❌ API error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        events = response.json()
        print(f"✅ Response received with {len(events)} events")
        
        # Extract the response text
        full_response = ""
        for event in events:
            if (event.get("content", {}).get("role") == "model" and 
                "parts" in event.get("content", {}) and 
                len(event["content"]["parts"]) > 0 and
                "text" in event["content"]["parts"][0]):
                full_response = event["content"]["parts"][0]["text"]
                break
        
        if not full_response:
            print("❌ No response text found")
            return False
        
        print(f"📝 Response length: {len(full_response)} characters")
        print(f"📝 Response preview: {full_response[:200]}...")
        
        # Check for image markers
        if "[IMAGE:" in full_response:
            print("✅ Image markers found in response!")
            # Count image markers
            image_count = full_response.count("[IMAGE:")
            print(f"📸 Found {image_count} image markers")
            
            # Show a few examples
            import re
            pattern = r'\[IMAGE:\s*([^,]+),\s*([^\]]+)\]'
            matches = re.findall(pattern, full_response)
            print(f"📸 Extracted {len(matches)} image references:")
            for i, (attraction, location) in enumerate(matches[:3]):
                print(f"   {i+1}. {attraction.strip()}, {location.strip()}")
        else:
            print("❌ No image markers found in response")
            print("🔍 Full response:")
            print(full_response)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Tourist Spots Agent Directly")
    print("=" * 60)
    
    success = test_tourist_agent_direct()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    print(f"Direct Tourist Agent Test: {'✅ PASSED' if success else '❌ FAILED'}")
    
    if success:
        print("\n🎉 Direct test completed! Check the output above for details.")
    else:
        print("\n⚠️ Test failed. Please check the logs above for details.") 
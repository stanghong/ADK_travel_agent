#!/usr/bin/env python3
"""
Detailed test for tourist spots with images functionality
"""

import requests
import json
import time
import re

def test_tourist_spots_detailed():
    print("🚀 Testing Tourist Spots with Images - Detailed Analysis")
    print("=" * 60)
    
    # Test data
    test_queries = [
        "What are the top tourist spots in Paris?",
        "Show me landmarks in Tokyo",
        "What attractions should I visit in New York?"
    ]
    
    # Create a session ID
    session_id = f"session-{int(time.time())}"
    print(f"1. Using session ID: {session_id}")
    
    print("\n🧪 Testing Tourist Spots Queries with Detailed Analysis")
    print("=" * 50)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n   Test {i}: {query}")
        print("   " + "-" * 40)
        
        # Send message directly to /run endpoint
        response = requests.post(
            "http://localhost:8000/run",
            json={
                "app_name": "orchestrator_agent",
                "user_id": "test_detailed",
                "session_id": session_id,
                "new_message": {
                    "role": "user",
                    "parts": [{"text": query}]
                }
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Response received ({len(str(data))} characters)")
            
            # Check if tourist_spots_agent was called
            events = data.get("events", [])
            tourist_agent_called = False
            image_tool_called = False
            
            for event in events:
                content = event.get("content", {})
                parts = content.get("parts", [])
                
                for part in parts:
                    # Check for tourist spots agent call
                    if "functionCall" in part:
                        func_call = part["functionCall"]
                        if func_call.get("name") == "tourist_spots_agent":
                            tourist_agent_called = True
                            print(f"   🎯 tourist_spots_agent called with: {func_call.get('args', {})}")
                    
                    # Check for image tool call
                    if "functionCall" in part:
                        func_call = part["functionCall"]
                        if func_call.get("name") == "get_attraction_image":
                            image_tool_called = True
                            print(f"   📸 get_attraction_image called with: {func_call.get('args', {})}")
                    
                    # Check for function response
                    if "functionResponse" in part:
                        func_response = part["functionResponse"]
                        if func_response.get("name") == "get_attraction_image":
                            result = func_response.get("response", {}).get("result", "")
                            print(f"   🖼️  Image tool returned: {result}")
            
            if not tourist_agent_called:
                print("   ⚠️  tourist_spots_agent was NOT called")
            if not image_tool_called:
                print("   ⚠️  get_attraction_image was NOT called")
            
            # Look for TripAdvisor URLs in the final response
            final_text = ""
            for event in events:
                content = event.get("content", {})
                parts = content.get("parts", [])
                for part in parts:
                    if "text" in part:
                        final_text += part["text"]
            
            tripadvisor_urls = re.findall(r'https://www\.tripadvisor\.com[^\s\)]+', final_text)
            if tripadvisor_urls:
                print(f"   🔗 TripAdvisor URLs found: {len(tripadvisor_urls)}")
                for url in tripadvisor_urls[:3]:  # Show first 3
                    print(f"      - {url}")
            else:
                print("   ❌ No TripAdvisor URLs found in response")
            
            # Show a snippet of the final response
            if final_text:
                snippet = final_text[:200] + "..." if len(final_text) > 200 else final_text
                print(f"   📝 Response snippet: {snippet}")
            
        else:
            print(f"   ❌ API error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error details: {error_data}")
            except:
                print(f"   Error text: {response.text}")
    
    print("\n" + "=" * 60)
    print("📊 Detailed Analysis Complete")
    print("=" * 60)

if __name__ == "__main__":
    test_tourist_spots_detailed() 
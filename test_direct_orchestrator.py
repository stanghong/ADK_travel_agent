#!/usr/bin/env python3
"""
Direct test of the orchestrator agent to see if it calls the image tool
"""

import requests
import json
import time

def test_direct_orchestrator():
    print("🧪 Direct Test of Orchestrator Agent")
    print("=" * 50)
    
    # Test query
    query = "What are the top tourist spots in Paris?"
    user_id = "test_direct"
    
    print(f"Query: {query}")
    print(f"User ID: {user_id}")
    print("-" * 40)
    
    # Start session first
    print("1. Starting session...")
    session_response = requests.post(
        "http://localhost:8080/start_session",
        json={"user_id": user_id}
    )
    
    if session_response.status_code != 200:
        print(f"❌ Failed to start session: {session_response.status_code}")
        return
    
    session_data = session_response.json()
    if not session_data.get("success"):
        print("❌ Failed to initialize session")
        return
    
    session_id = session_data.get("session_id")
    print(f"✅ Session started: {session_id}")
    
    # Send message to FastAPI server
    print("\n2. Sending message...")
    response = requests.post(
        "http://localhost:8080/send_message",
        json={
            "session_id": session_id,
            "user_id": user_id,
            "message": query
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Response received")
        print(f"Success: {data.get('success')}")
        print(f"Response length: {len(data.get('response', ''))}")
        print(f"Image links: {len(data.get('image_links', []))}")
        
        # Show response snippet
        response_text = data.get('response', '')
        if response_text:
            snippet = response_text[:300] + "..." if len(response_text) > 300 else response_text
            print(f"\nResponse snippet:\n{snippet}")
        
        # Show image links if any
        image_links = data.get('image_links', [])
        if image_links:
            print(f"\nImage links found:")
            for i, img in enumerate(image_links):
                print(f"  {i+1}. {img.get('attraction')} - {img.get('thumbnail_url')}")
        else:
            print(f"\n❌ No image links found")
            
    else:
        print(f"❌ API error: {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error details: {error_data}")
        except:
            print(f"Error text: {response.text}")

if __name__ == "__main__":
    test_direct_orchestrator() 
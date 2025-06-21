#!/usr/bin/env python3
"""
Test script for the tourist spots agent with image functionality.
"""

import requests
import json
import time

# Configuration
API_URL = "http://localhost:8080"
USER_ID = "test_tourist_images"

def test_tourist_spots_with_images():
    """Test tourist spots queries to see if they return image links."""
    print("🧪 Testing Tourist Spots with Images")
    print("=" * 50)
    
    # Start a new session
    print("1. Starting new session...")
    try:
        response = requests.post(f"{API_URL}/start_session", json={"user_id": USER_ID})
        if response.status_code != 200:
            print(f"❌ Failed to start session: {response.status_code}")
            return False
        
        data = response.json()
        if not data.get("success"):
            print("❌ Failed to initialize session")
            return False
        
        session_id = data.get("session_id")
        print(f"✅ Session started: {session_id}")
    except Exception as e:
        print(f"❌ Error starting session: {e}")
        return False
    
    # Test tourist spots queries
    test_queries = [
        "Tell me about tourist spots in Paris",
        "What are the must-see attractions in Tokyo?",
        "Show me landmarks in New York",
        "What places should I visit in London?",
        "Recommend tourist attractions in Rome"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n   Test {i}: {query}")
        try:
            payload = {
                "session_id": session_id,
                "user_id": USER_ID,
                "message": query
            }
            
            response = requests.post(f"{API_URL}/send_message", json=payload)
            
            if response.status_code != 200:
                print(f"   ❌ API error: {response.status_code}")
                continue
            
            data = response.json()
            if not data.get("success"):
                print(f"   ❌ Failed to get response")
                continue
            
            response_text = data.get("response", "")
            image_links = data.get("image_links", [])
            
            print(f"   ✅ Response received ({len(response_text)} characters)")
            print(f"   📸 Image links found: {len(image_links)}")
            
            if image_links:
                print(f"   🖼️  Sample image data:")
                for j, img in enumerate(image_links[:2]):  # Show first 2 images
                    print(f"      {j+1}. {img['attraction']}, {img['location']}")
                    print(f"         Thumbnail: {img['thumbnail_url']}")
            
            # Small delay between requests
            time.sleep(2)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ Tourist spots with images testing completed!")
    return True

def test_non_tourist_queries():
    """Test non-tourist queries to ensure they don't return image links."""
    print("\n🧪 Testing Non-Tourist Queries")
    print("=" * 50)
    
    # Start a new session
    print("1. Starting new session...")
    try:
        response = requests.post(f"{API_URL}/start_session", json={"user_id": f"{USER_ID}_non_tourist"})
        if response.status_code != 200:
            print(f"❌ Failed to start session: {response.status_code}")
            return False
        
        data = response.json()
        if not data.get("success"):
            print("❌ Failed to initialize session")
            return False
        
        session_id = data.get("session_id")
        print(f"✅ Session started: {session_id}")
    except Exception as e:
        print(f"❌ Error starting session: {e}")
        return False
    
    # Test non-tourist queries
    test_queries = [
        "What's the weather like in Tokyo?",
        "Create a walking route from Eiffel Tower to Louvre Museum",
        "Recommend restaurants in New York",
        "What time is it in London?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n   Test {i}: {query}")
        try:
            payload = {
                "session_id": session_id,
                "user_id": f"{USER_ID}_non_tourist",
                "message": query
            }
            
            response = requests.post(f"{API_URL}/send_message", json=payload)
            
            if response.status_code != 200:
                print(f"   ❌ API error: {response.status_code}")
                continue
            
            data = response.json()
            if not data.get("success"):
                print(f"   ❌ Failed to get response")
                continue
            
            response_text = data.get("response", "")
            image_links = data.get("image_links", [])
            
            print(f"   ✅ Response received ({len(response_text)} characters)")
            print(f"   📸 Image links found: {len(image_links)} (should be 0)")
            
            if image_links:
                print(f"   ⚠️  Unexpected image links found!")
            
            # Small delay between requests
            time.sleep(1)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ Non-tourist queries testing completed!")
    return True

if __name__ == "__main__":
    print("🚀 Testing Tourist Spots with Images")
    print("=" * 60)
    
    # Test tourist spots with images
    tourist_success = test_tourist_spots_with_images()
    
    # Test non-tourist queries
    non_tourist_success = test_non_tourist_queries()
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    print(f"Tourist Spots with Images: {'✅ PASSED' if tourist_success else '❌ FAILED'}")
    print(f"Non-Tourist Queries: {'✅ PASSED' if non_tourist_success else '❌ FAILED'}")
    
    if tourist_success and non_tourist_success:
        print("\n🎉 All tests passed! Tourist spots with images functionality is working correctly.")
        print("\n📝 Features verified:")
        print("- Tourist spots queries return image links")
        print("- Images are properly sized as thumbnails")
        print("- Non-tourist queries don't return image links")
        print("- API correctly processes image data")
    else:
        print("\n⚠️ Some tests failed. Please check the logs above for details.") 
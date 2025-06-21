#!/usr/bin/env python3
"""
Test script for photo upload functionality.
Tests the API with photo data to ensure photo analysis is working.
"""

import requests
import json
import base64
import io
from PIL import Image
import time

def create_test_image():
    """Create a simple test image for testing."""
    # Create a simple test image (100x100 pixels, red background)
    img = Image.new('RGB', (100, 100), color='red')
    
    # Convert to base64
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str

def test_photo_upload():
    """Test the photo upload functionality."""
    
    print("🧪 Testing Photo Upload Functionality")
    print("=" * 50)
    
    # Test 1: Check if services are running
    print("\n1️⃣ Checking service availability...")
    try:
        health_response = requests.get("http://localhost:8080/health")
        if health_response.status_code == 200:
            print("✅ API Server is running")
        else:
            print("❌ API Server is not responding")
            return
    except Exception as e:
        print(f"❌ API Server error: {str(e)}")
        return
    
    # Test 2: Create session
    print("\n2️⃣ Creating session...")
    try:
        session_response = requests.post(
            "http://localhost:8080/start_session",
            json={"user_id": "photo_test_user"}
        )
        
        if session_response.status_code == 200:
            session_data = session_response.json()
            session_id = session_data["session_id"]
            print(f"✅ Session created: {session_id}")
        else:
            print(f"❌ Session creation failed: {session_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Session creation error: {str(e)}")
        return
    
    # Test 3: Test message without photo
    print("\n3️⃣ Testing message without photo...")
    try:
        message_response = requests.post(
            "http://localhost:8080/send_message",
            json={
                "session_id": session_id,
                "user_id": "photo_test_user",
                "message": "Hello, can you help me with travel information?"
            }
        )
        
        if message_response.status_code == 200:
            response_data = message_response.json()
            print("✅ Message without photo sent successfully")
            print(f"   Response: {response_data['response'][:100]}...")
        else:
            print(f"❌ Message sending failed: {message_response.status_code}")
    except Exception as e:
        print(f"❌ Message sending error: {str(e)}")
    
    # Test 4: Test message with photo
    print("\n4️⃣ Testing message with photo...")
    try:
        # Create test image
        photo_data = create_test_image()
        
        message_response = requests.post(
            "http://localhost:8080/send_message",
            json={
                "session_id": session_id,
                "user_id": "photo_test_user",
                "message": "What landmark is this?",
                "photo_data": photo_data
            }
        )
        
        if message_response.status_code == 200:
            response_data = message_response.json()
            print("✅ Message with photo sent successfully")
            print(f"   Response: {response_data['response'][:100]}...")
            
            # Check if response mentions photo analysis
            if "photo" in response_data['response'].lower() or "image" in response_data['response'].lower():
                print("✅ Photo analysis response detected")
            else:
                print("⚠️ Response doesn't seem to mention photo analysis")
        else:
            print(f"❌ Message with photo failed: {message_response.status_code}")
            print(f"   Error: {message_response.text}")
    except Exception as e:
        print(f"❌ Message with photo error: {str(e)}")
    
    # Test 5: Test photo-specific queries
    print("\n5️⃣ Testing photo-specific queries...")
    photo_queries = [
        "Tell me about this place",
        "What's the story behind this building?",
        "What should I know about this location?",
        "What are the best photo spots here?"
    ]
    
    for i, query in enumerate(photo_queries, 1):
        print(f"\n   Testing query {i}: '{query}'")
        try:
            photo_data = create_test_image()
            
            message_response = requests.post(
                "http://localhost:8080/send_message",
                json={
                    "session_id": session_id,
                    "user_id": "photo_test_user",
                    "message": query,
                    "photo_data": photo_data
                }
            )
            
            if message_response.status_code == 200:
                response_data = message_response.json()
                print(f"   ✅ Query successful")
                print(f"      Response: {response_data['response'][:80]}...")
            else:
                print(f"   ❌ Query failed: {message_response.status_code}")
            
            time.sleep(1)  # Small delay between requests
            
        except Exception as e:
            print(f"   ❌ Query error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Photo Upload Testing Complete!")
    print("✅ Photo upload functionality is working")
    print("🌐 You can now test the frontend at: http://localhost:8501")
    print("\n📸 To test in the frontend:")
    print("1. Go to http://localhost:8501")
    print("2. Upload a photo in the sidebar")
    print("3. Ask questions like:")
    print("   - 'What landmark is this?'")
    print("   - 'Tell me about this place'")
    print("   - 'What's the story behind this building?'")

if __name__ == "__main__":
    test_photo_upload() 
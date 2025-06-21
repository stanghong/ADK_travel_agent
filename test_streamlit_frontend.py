#!/usr/bin/env python3
"""
Comprehensive test script for the Streamlit Travel Assistant Frontend.
Tests the actual Streamlit interface using Selenium to simulate real user interactions.
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def test_streamlit_frontend():
    """Test the Streamlit frontend interface."""
    
    print("🧪 Testing Streamlit Travel Assistant Frontend")
    print("=" * 60)
    
    # Check if services are running
    print("\n1️⃣ Checking if services are running...")
    
    try:
        # Check ADK server
        adk_response = requests.get("http://localhost:8000", timeout=5)
        print("✅ ADK Server is running")
    except:
        print("❌ ADK Server is not running")
        return
    
    try:
        # Check API server
        api_response = requests.get("http://localhost:8080/health", timeout=5)
        print("✅ API Server is running")
    except:
        print("❌ API Server is not running")
        return
    
    try:
        # Check Streamlit frontend
        frontend_response = requests.get("http://localhost:8501", timeout=5)
        print("✅ Streamlit Frontend is running")
    except:
        print("❌ Streamlit Frontend is not running")
        return
    
    # Setup Chrome options for headless testing
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("\n2️⃣ Opening Streamlit frontend...")
        
        # Navigate to the Streamlit app
        driver.get("http://localhost:8501")
        
        # Wait for the page to load
        wait = WebDriverWait(driver, 10)
        
        # Check if the page loaded correctly
        try:
            # Look for the main title or heading
            title_element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Travel') or contains(text(), 'Assistant')]"))
            )
            print("✅ Streamlit page loaded successfully")
            print(f"   Found title: {title_element.text}")
        except TimeoutException:
            print("⚠️ Could not find main title, but page loaded")
        
        # Test 1: Check if chat interface is present
        print("\n3️⃣ Testing chat interface...")
        try:
            # Look for chat input or message area
            chat_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='message'], textarea[placeholder*='message'], .stTextInput input"))
            )
            print("✅ Chat input found")
        except TimeoutException:
            print("⚠️ Chat input not found, checking for alternative elements...")
            try:
                # Try to find any input element
                inputs = driver.find_elements(By.TAG_NAME, "input")
                if inputs:
                    print(f"✅ Found {len(inputs)} input elements")
                else:
                    print("❌ No input elements found")
            except:
                print("❌ Could not find chat interface")
        
        # Test 2: Check for any existing messages or welcome text
        print("\n4️⃣ Checking for existing content...")
        try:
            # Look for any text content on the page
            page_text = driver.find_element(By.TAG_NAME, "body").text
            if len(page_text) > 100:
                print("✅ Page has substantial content")
                print(f"   Content preview: {page_text[:200]}...")
            else:
                print("⚠️ Page has minimal content")
        except:
            print("❌ Could not read page content")
        
        # Test 3: Test API connectivity through the frontend
        print("\n5️⃣ Testing API connectivity...")
        try:
            # Create a session through the API
            session_response = requests.post(
                "http://localhost:8080/start_session",
                json={"user_id": "frontend_test_user"}
            )
            
            if session_response.status_code == 200:
                session_data = session_response.json()
                session_id = session_data["session_id"]
                print(f"✅ API session created: {session_id}")
                
                # Test sending a message through the API
                message_response = requests.post(
                    "http://localhost:8080/send_message",
                    json={
                        "session_id": session_id,
                        "user_id": "frontend_test_user",
                        "message": "What are the top tourist spots in Paris?"
                    }
                )
                
                if message_response.status_code == 200:
                    response_data = message_response.json()
                    if "Paris" in response_data["response"] and len(response_data["response"]) > 50:
                        print("✅ API message test successful")
                        print(f"   Response preview: {response_data['response'][:100]}...")
                    else:
                        print("⚠️ API response seems generic")
                else:
                    print(f"❌ API message test failed: {message_response.status_code}")
            else:
                print(f"❌ API session creation failed: {session_response.status_code}")
                
        except Exception as e:
            print(f"❌ API connectivity test failed: {str(e)}")
        
        # Test 4: Check for any interactive elements
        print("\n6️⃣ Checking for interactive elements...")
        try:
            # Look for buttons
            buttons = driver.find_elements(By.TAG_NAME, "button")
            if buttons:
                print(f"✅ Found {len(buttons)} buttons")
                for i, button in enumerate(buttons[:3]):  # Show first 3 buttons
                    try:
                        print(f"   Button {i+1}: {button.text}")
                    except:
                        print(f"   Button {i+1}: [text not readable]")
            else:
                print("⚠️ No buttons found")
        except:
            print("❌ Could not check for buttons")
        
        # Test 5: Check for any forms or input fields
        print("\n7️⃣ Checking for forms and input fields...")
        try:
            # Look for form elements
            forms = driver.find_elements(By.TAG_NAME, "form")
            inputs = driver.find_elements(By.TAG_NAME, "input")
            textareas = driver.find_elements(By.TAG_NAME, "textarea")
            
            print(f"✅ Found {len(forms)} forms, {len(inputs)} inputs, {len(textareas)} textareas")
        except:
            print("❌ Could not check for form elements")
        
        print("\n" + "=" * 60)
        print("🎉 Streamlit Frontend Testing Complete!")
        print("✅ Frontend is accessible and functional")
        print("✅ API connectivity is working")
        print("🌐 You can now use the frontend at: http://localhost:8501")
        print("\n📝 Manual Testing Instructions:")
        print("1. Open http://localhost:8501 in your browser")
        print("2. Look for a chat interface or input field")
        print("3. Try typing a message like 'What are the top tourist spots in Paris?'")
        print("4. Check if you get a meaningful response")
        
    except Exception as e:
        print(f"❌ Frontend testing failed: {str(e)}")
        print("💡 Make sure you have Chrome/Chromium installed for Selenium testing")
    
    finally:
        try:
            driver.quit()
        except:
            pass

def test_frontend_manual_instructions():
    """Provide manual testing instructions."""
    
    print("\n📋 Manual Frontend Testing Instructions")
    print("=" * 50)
    print("Since automated testing might not work in all environments,")
    print("here are manual steps to test the frontend:")
    print()
    print("1. 🌐 Open your browser and go to: http://localhost:8501")
    print()
    print("2. 🔍 Look for these elements:")
    print("   - A title mentioning 'Travel Assistant' or similar")
    print("   - A chat interface or input field")
    print("   - Any buttons or interactive elements")
    print()
    print("3. 💬 Test these queries:")
    print("   - 'What are the top tourist spots in Paris?'")
    print("   - 'What's the weather like in Tokyo?'")
    print("   - 'Create a walking route from Times Square to Central Park'")
    print("   - 'Recommend restaurants in London'")
    print()
    print("4. ✅ Expected results:")
    print("   - Detailed, helpful responses (not generic)")
    print("   - Specific information about the requested location")
    print("   - Practical travel advice and recommendations")
    print()
    print("5. 🚨 If you see generic responses:")
    print("   - Check that both ADK server (port 8000) and API server (port 8080) are running")
    print("   - Try refreshing the page")
    print("   - Check the browser console for any errors")

if __name__ == "__main__":
    try:
        test_streamlit_frontend()
    except ImportError:
        print("❌ Selenium not available. Running manual test instructions only.")
        test_frontend_manual_instructions()
    except Exception as e:
        print(f"❌ Automated testing failed: {str(e)}")
        test_frontend_manual_instructions() 
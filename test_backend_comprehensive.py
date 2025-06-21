import requests
import json
import time

# --- Configuration ---
BASE_URL = "http://localhost:8080"
USER_ID = "comprehensive_tester"
SESSION_ID = None

# --- Helper Functions ---

def print_test_header(title):
    print("\n" + "="*60)
    print(f"🧪 TESTING: {title}")
    print("="*60)

def print_result(name, success, response_text=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status:<10} | {name}")
    if not success and response_text:
        print(f"           | Response: {response_text[:150]}...")
    return success

def start_session():
    global SESSION_ID
    print_test_header("Session Creation")
    try:
        response = requests.post(f"{BASE_URL}/start_session", json={"user_id": USER_ID})
        if response.status_code == 200:
            data = response.json()
            SESSION_ID = data.get("session_id")
            return print_result("Start Session", bool(SESSION_ID), response.text)
        return print_result("Start Session", False, response.text)
    except requests.RequestException as e:
        return print_result("Start Session", False, str(e))

def send_message(prompt, expected_keywords):
    if not SESSION_ID:
        print("❌ FAIL   | Skipping test, no session ID.")
        return False
    
    print(f"\n💬 Prompt: '{prompt}'")
    try:
        response = requests.post(
            f"{BASE_URL}/send_message",
            json={"session_id": SESSION_ID, "message": prompt, "user_id": USER_ID},
            timeout=90  # Increased timeout for generative tasks
        )
        
        if response.status_code != 200:
            return print_result(f"Agent Test for '{prompt}'", False, response.text)
            
        data = response.json()
        response_text = data.get("response", "").lower()
        
        all_keywords_found = all(keyword.lower() in response_text for keyword in expected_keywords)
        
        return print_result(f"Agent Test for '{prompt}'", all_keywords_found, response_text)

    except requests.RequestException as e:
        return print_result(f"Agent Test for '{prompt}'", False, str(e))

# --- Test Suite ---

def main():
    overall_success = True
    
    # 1. Health Check
    print_test_header("Health Check")
    try:
        health_response = requests.get(f"{BASE_URL}/health")
        overall_success &= print_result("Health Check", health_response.status_code == 200, health_response.text)
    except requests.RequestException as e:
        overall_success &= print_result("Health Check", False, str(e))

    # 2. Start Session
    if not start_session():
        print("\nHalting tests because session could not be created.")
        return

    # 3. Agent Routing Tests
    print_test_header("Agent Routing & Functionality")
    
    # Weather Agent
    overall_success &= send_message(
        "What's the weather like in London?",
        expected_keywords=["london", "weather", "°c"]
    )
    
    # Tourist Spots Agent
    overall_success &= send_message(
        "Tell me about some famous landmarks in Paris",
        expected_keywords=["paris", "eiffel tower", "louvre"]
    )
    
    # Restaurant Recommendation Agent
    overall_success &= send_message(
        "Can you recommend a good pizza place in Brooklyn?",
        expected_keywords=["recommend", "brooklyn", "pizza", "what kind"]
    )
    
    # Walking Routes Agent (Vague - should ask for clarification)
    overall_success &= send_message(
        "I want a walking route in Rome.",
        expected_keywords=["specific", "locations", "start"]
    )
    
    # Walking Routes Agent (Specific - should generate a link)
    overall_success &= send_message(
        "Give me a walking route from the Colosseum to the Pantheon in Rome",
        expected_keywords=["walking route", "google.com/maps", "colosseum", "pantheon"]
    )
    
    # Blog Writer Agent
    overall_success &= send_message(
        "Write a short blog post about a 3-day trip to Kyoto",
        expected_keywords=["kyoto", "day 1", "day 2", "day 3"]
    )

    # 4. Conversational Memory Test
    print_test_header("Conversational Memory")
    
    # First turn
    send_message(
        "How tall is the Eiffel Tower?",
        expected_keywords=["eiffel tower", "meters", "feet"]
    )
    
    # Follow-up turn
    overall_success &= send_message(
        "And where is it located?",
        expected_keywords=["paris", "france", "champ de mars"]
    )
    
    # --- Final Summary ---
    print("\n" + "="*60)
    if overall_success:
        print("🎉 ✅ All backend tests passed successfully!")
    else:
        print("🔥 ❌ Some backend tests failed. Please review the logs.")
    print("="*60)

if __name__ == "__main__":
    main() 
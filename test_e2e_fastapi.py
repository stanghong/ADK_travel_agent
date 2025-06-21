#!/usr/bin/env python3
"""
End-to-end test for Travel Assistant via FastAPI backend.
"""

import requests
import time

API_URL = "http://localhost:8080"
USER_ID = f"e2e_test_{int(time.time())}"

def start_session():
    resp = requests.post(f"{API_URL}/start_session", json={"user_id": USER_ID})
    data = resp.json()
    if not data.get("success"):
        print("❌ Failed to start session:", data)
        exit(1)
    print(f"✅ Session started: {data['session_id']}")
    return data["session_id"]

def send_message(session_id, message, photo_data=None):
    payload = {
        "session_id": session_id,
        "user_id": USER_ID,
        "message": message
    }
    if photo_data:
        payload["photo_data"] = photo_data
    resp = requests.post(f"{API_URL}/send_message", json=payload)
    try:
        data = resp.json()
    except Exception:
        print("❌ Invalid JSON response:", resp.text)
        return None
    return data

def print_result(title, data):
    print(f"\n--- {title} ---")
    if not data or not data.get("success"):
        print("❌ Error:", data)
        return
    print("✅ Success")
    print("Response:", data.get("response", "")[:400], "..." if len(data.get("response", "")) > 400 else "")
    if data.get("image_links"):
        print("Image links:", data["image_links"])

def main():
    session_id = start_session()

    tests = [
        ("Tourist Spots Agent", "What are the top tourist spots in Paris?"),
        ("Weather Agent", "What's the weather like in Tokyo?"),
        ("Walking Routes Agent", "Create a walking route from the Eiffel Tower to the Louvre Museum."),
        ("Restaurant Recommendation Agent", "Recommend restaurants in New York."),
        ("Blog Writer Agent", "Write a two-paragraph travel blog about Rome."),
        ("Current Time Tool", "What time is it in London?"),
        ("Orchestrator Agent", "What can you do?"),
    ]

    for title, query in tests:
        data = send_message(session_id, query)
        print_result(title, data)
        time.sleep(1)

    # Photo Story Agent test (simulate photo upload)
    try:
        from PIL import Image
        import base64
        from io import BytesIO
        # Create a dummy image for testing
        img = Image.new("RGB", (100, 100), color="red")
        buf = BytesIO()
        img.save(buf, format="JPEG")
        photo_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        data = send_message(session_id, "What landmark is this?", photo_data=photo_b64)
        print_result("Photo Story Agent (with photo)", data)
    except Exception as e:
        print("⚠️ Skipping photo story agent test (PIL not installed or error):", e)

if __name__ == "__main__":
    main() 
import requests
import os

# Base URL (assuming running locally on default port)
BASE_URL = "http://127.0.0.1:8000"

def test_home():
    import time
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/")
            print(f"GET /: {response.status_code}")
            print(response.json())
            return
        except requests.exceptions.ConnectionError:
            if i < max_retries - 1:
                print(f"Connection failed, retrying in 2s... ({i+1}/{max_retries})")
                time.sleep(2)
            else:
                print(f"Failed to connect to {BASE_URL} after {max_retries} attempts.")
                print("Make sure the server is running: uvicorn main:app --reload")

if __name__ == "__main__":
    print("Testing API endpoints...")
    test_home()
    print("\nTo fully test file uploads, run the server and use Postman or curl.")
    print("Example: curl -X POST -F 'files=@my.pdf' http://127.0.0.1:8000/unlock -o unlocked.zip")

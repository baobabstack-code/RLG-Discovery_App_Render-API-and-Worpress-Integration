# API Testing Guide

This guide explains three methods to test the `Discovery One-Stop API`:
1.  **Interactive Swagger UI** (Easiest, works in browser)
2.  **Automated Python Script** (Good for regression testing)
3.  **Manual cURL/Postman** (Good for specific debugging)

---

## 1. Interactive Swagger UI

FastAPI provides automatic interactive documentation. This is the easiest way to test endpoints manually.

### Steps:
1.  **Run the API locally**:
    ```bash
    uvicorn main:app --reload
    ```
2.  **Open your browser**:
    *   Navigate to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
3.  **Test an Endpoint**:
    *   Click on an endpoint (e.g., `POST /unlock`).
    *   Click **Try it out**.
    *   Upload files and fill in fields.
    *   Click **Execute**.
    *   View the response body and headers below.

---

## 2. Using the Python Test Script (`test_api.py`)

A pre-written script `test_api.py` is included in the project. It tests the Home, Unlock, and Bates Stamp endpoints.

### Prerequisites:
You need the `requests` library. If it's not installed:
```bash
pip install requests
```

### Configuration:
Open `test_api.py` and check the `BASE_URL` variable at the top.

*   **For Local Testing**:
    Ensure the local URL is active (you may need to uncomment it):
    ```python
    BASE_URL = "http://127.0.0.1:8000"
    ```

*   **For Live/Render Testing**:
    Use your deployment URL:
    ```python
    BASE_URL = "https://discovery-api-b4c9.onrender.com"
    ```

### Running the Test:
1.  Ensure your API is running (if testing locally).
2.  Run the script:
    ```bash
    python test_api.py
    ```
3.  Check the output in the terminal for `200 OK` messages.

---

## 3. Manual Testing (cURL)

You can use `curl` in your terminal to test endpoints.

### Test Home (Health Check)
```bash
curl -X GET http://127.0.0.1:8000/
```

### Test Unlock API
```bash
curl -X POST "http://127.0.0.1:8000/unlock" \
  -F "files=@/path/to/your/document.pdf" \
  -F "password_mode=Try no password" \
  --output unlocked.zip
```

### Test Bates Stamping
```bash
curl -X POST "http://127.0.0.1:8000/bates" \
  -F "files=@/path/to/your/document.pdf" \
  -F "prefix=CONFIDENTIAL" \
  -F "start_num=100" \
  --output labeled.zip
```

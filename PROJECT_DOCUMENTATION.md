# Project Documentation: Discovery One-Stop API

## Overview
The **Discovery One-Stop API** is a FastAPI-based web service designed to automate legal document processing tasks. It provides a suite of tools for unlocking PDFs, organizing files by year, applying Bates stamps, generating discovery indexes, and redacting sensitive information.

## System Architecture

The application is structured into a clean separation of concerns:
- **`main.py`**: The API Gateway. It handles HTTP requests, file uploads, and response streaming.
- **`logic.py`**: The Core Engine. It contains all business logic, independent of the web framework.
- **Dependencies**: Uses `PyMuPDF`, `Pillow`, `ReportLab`, and `Pandas` for heavy lifting.

```mermaid
graph TD
    Client[External Client / Web App] -->|HTTP POST| API[FastAPI (main.py)]
    
    subgraph "Application Core"
        API -->|Calls| Logic[Business Logic (logic.py)]
        Logic -->|Uses| PDF[PyMuPDF / PyPDF2]
        Logic -->|Uses| IMG[Pillow / Tesseract OCR]
        Logic -->|Uses| XLS[Pandas / OpenPyXL]
    end
    
    subgraph "Storage / IO"
        Logic -->|Reads/Writes| Temp[Temporary Directory]
        Temp -->|Zips| Output[Output ZIP]
    end
    
    Output -->|Streamed Response| Client
```

## Data Flow

### 1. File Processing Pipeline
Most endpoints follow a "Swiss Army Knife" pattern: Input Files → Process → Output ZIP.

```mermaid
sequenceDiagram
    participant User
    participant API as FastAPI (main.py)
    participant Logic as Logic Engine (logic.py)
    participant Temp as Temp Storage

    User->>API: POST /endpoint (Files + Config)
    API->>Logic: Invoke Processing Function
    Logic->>Temp: Create Secure Temp Dir
    Logic->>Temp: Extract/Save Input Files
    Logic->>Logic: Process Files (Unlock/Label/Redact)
    Logic->>Temp: Save Processed Files
    Logic->>Logic: Create ZIP from Output
    Logic-->>API: Return ZIP Bytes
    Logic->>Temp: Cleanup (Auto)
    API-->>User: Stream ZIP Download
```

## API Endpoints

| Endpoint | Method | Description | Input | Output |
| :--- | :--- | :--- | :--- | :--- |
| `/unlock` | `POST` | Removes passwords from PDFs | PDFs/ZIP + Password | ZIP of Unlocked PDFs |
| `/organize` | `POST` | Sorts files into folders by year | PDFs/ZIP | ZIP of Folders |
| `/bates` | `POST` | Stamps Bates numbers on pages | PDFs/ZIP + Config (Zone/Padding) | ZIP of Labeled Files |
| `/index` | `POST` | Generates Excel index from labeled files | Labeled ZIP | Excel (.xlsx) |
| `/redact` | `POST` | Redacts sensitive info (SSN, etc.) | PDF/ZIP + Patterns | ZIP of Redacted PDFs |

## Deployment Guide (Render)

This application is configured for deployment on **Render** as a Web Service.

### Prerequisites
1.  **GitHub Repository**: The code must be pushed to a GitHub repository.
2.  **Render Account**: Create an account at [render.com](https://render.com).

### Deployment Steps

1.  **New Web Service**:
    *   Go to the Render Dashboard.
    *   Click **New +** -> **Web Service**.
    *   Connect your GitHub repository.

2.  **Configuration**:
    Render will automatically detect the `render.yaml` file, but if you configure manually:
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3.  **System Dependencies**:
    The `packages.txt` file ensures that `poppler-utils` and `tesseract-ocr` are installed on the server. This is critical for PDF-to-Image conversion and OCR.

4.  **Environment Variables**:
    *   `PYTHON_VERSION`: `3.9.0` (or newer)
    *   `PORT`: (Set automatically by Render)

### Verification
Once deployed, Render will provide a URL (e.g., `https://discovery-app.onrender.com`).
*   Visit `https://discovery-app.onrender.com/docs` to see the interactive Swagger UI and test endpoints directly in the browser.

## Local Development

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Server**:
    ```bash
    uvicorn main:app --reload
    ```

3.  **Test**:
    Run the included test script:
    ```bash
    python test_api.py
    ```

## WordPress Integration

A custom plugin (`rlg-discovery-integration.zip`) is provided to seamlessly integrate these tools into your WordPress site.

### 1. Installation
1.  **Download Plugin**: Locate `rlg-discovery-integration.zip` in the project root.
2.  **Upload to WordPress**:
    *   Go to your WordPress Admin Dashboard.
    *   Navigate to **Plugins** > **Add New**.
    *   Click **Upload Plugin** at the top.
    *   Select the zip file and click **Install Now**.
    *   Click **Activate Plugin**.

### 2. Configuration
1.  **Get API URL**: Copy the URL of your deployed Render service (e.g., `https://your-app.onrender.com`).
2.  **Configure Plugin**:
    *   Go to **Settings** > **RLG Discovery** in the WordPress Admin menu.
    *   Paste your API URL into the **API URL** field.
    *   Click **Save Changes**.

### 3. Usage (Shortcodes)
You can embed the tools on any Page or Post using the following shortcodes:

| Tool | Shortcode | Description |
| :--- | :--- | :--- |
| **Unlock PDFs** | `[rlg_unlock]` | Form to remove passwords from PDFs. |
| **Organize by Year** | `[rlg_organize]` | Form to sort files into year-based folders. |
| **Bates Labeler** | `[rlg_bates]` | Form to apply Bates stamps with Zone support. |
| **Discovery Index** | `[rlg_index]` | Form to generate an Excel index from labeled files. |
| **Redaction Tool** | `[rlg_redact]` | Form to redact sensitive info (SSN, etc.). |

### 4. Troubleshooting
*   **CORS Errors**: If the forms fail immediately, ensure your FastAPI `main.py` has CORS enabled (it is enabled by default in this project).
*   **Timeouts**: Large files may take time to process. The plugin uses direct client-to-API communication to avoid WordPress server timeouts, but the browser connection must remain open.


# Render Deployment Guide

This guide provides a step-by-step walkthrough for deploying the **Discovery One-Stop API** to Render.

## Prerequisites

1.  **GitHub Repository**: Ensure your code is pushed to a GitHub repository (which we have already done).
2.  **Render Account**: You need an account at [render.com](https://render.com).

## Step-by-Step Deployment

### 1. Create a New Web Service
1.  Log in to your [Render Dashboard](https://dashboard.render.com).
2.  Click the **New +** button in the top right corner.
3.  Select **Web Service**.

### 2. Connect Your Repository
1.  You will see a list of your GitHub repositories.
2.  Find `RLG-Discovery_App_Render-API-and-Worpress-Integration` (or your repo name).
3.  Click **Connect**.

### 3. Configure the Service
Render will try to auto-detect settings, but you should verify them against this list:

*   **Name**: Give it a name (e.g., `discovery-api`).
*   **Region**: Choose the one closest to you (e.g., `Ohio (US East)`).
*   **Branch**: `main`
*   **Root Directory**: (Leave blank)
*   **Runtime**: `Python 3`
*   **Build Command**: `pip install -r requirements.txt`
*   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 4. Select Instance Type
*   Select **Free** (for testing/hobby) or a paid plan for production performance.
*   *Note: The Free tier spins down after 15 minutes of inactivity, causing a ~50s delay on the next request.*

### 5. Deploy
1.  Click **Create Web Service**.
2.  Render will start building your app. You will see a terminal window showing the build logs.
3.  **Wait for it to finish.** It will install Python dependencies (`fastapi`, `uvicorn`, etc.) and system packages (`poppler`, `tesseract`).

### 6. Verify Deployment
1.  Once the build finishes, you will see a green **Live** badge.
2.  At the top left, find your **Service URL** (e.g., `https://discovery-api.onrender.com`).
3.  Click it. You should see the JSON response: `{"message": "Discovery One-Stop API is running.", ...}`.
4.  Append `/docs` to the URL (e.g., `https://.../docs`) to see the interactive API testing page.

## Troubleshooting

### Build Failed?
*   Check the **Logs** tab.
*   Look for errors during `pip install`.
*   Ensure `requirements.txt` is in the root folder.

### Application Error (502 Bad Gateway)?
*   Check the **Logs** tab.
*   Ensure the **Start Command** matches exactly: `uvicorn main:app --host 0.0.0.0 --port $PORT`.
*   If it says "Module not found", ensure `main.py` is in the root folder.

### "Internal Server Error" on File Upload?
*   This might mean a missing system dependency.
*   We included a `packages.txt` file which Render reads automatically to install `poppler-utils` and `tesseract-ocr`. Ensure this file exists in your repo.

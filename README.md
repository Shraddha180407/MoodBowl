# MoodBowl AI System — Setup Guide

A production-ready MVP for a mood-aware food recommendation chatbot using **FastAPI, PostgreSQL, Redis, and Gemini LLM**.

## 📋 Prerequisites

Before setting up the project, ensure you have the following installed on your machine:
1. **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**: Mandatory for running the database (PostgreSQL) and session store (Redis).
2. **[Python 3.11+](https://www.python.org/downloads/)**: Required for the backend server.
3. **Google Gemini API Key**: Obtain one from the [Google AI Studio](https://aistudio.google.com/).

---

## 🚀 Quick Start Guide

### 1. Clone & Configure
Copy `.env.example` to `.env` and fill in your Gemini API Key.
```bash
cp .env.example .env
```
*Make sure `GOOGLE_GEMINI_API_KEY` is set correctly in the `.env` file.*

### 2. Start Infrastructure (Docker)
Ensure Docker Desktop is running, then start the database and Redis services:
```bash
docker-compose up -d
```

### 3. Setup Python Backend
Navigate to the `backend` folder and set up your virtual environment:
```powershell
cd backend
```
*(Windows)*:
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Seed Database
Populate the menu with 20+ initial food items:
```powershell
python -m app.seed
```

### 5. Run the Server
Launch the FastAPI application:
```powershell
uvicorn app.main:app --port 8000 --reload
```

---

## 🛠 Features Included
- **Mood Orchestrator**: Uses a two-pass approach (Regex + Gemini) for precise intent detection.
- **Deterministic Recommender**: Intelligent food filtering with progressive fallback (Dietary Prefs -> Mood Tags -> Top Rated).
- **Persistent Sessions**: Redis-based session tracking with a 30-minute TTL.
- **Rate Limiting**: Integrated `slowapi` to prevent abuse (e.g., 10 chat messages/min).

---

## 🧪 Testing the API
Once the server is running, you can:
- **Interactive UI**: Visit [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger).
- **Check Menu**: `GET http://localhost:8000/api/menu`
- **Chat with AI**: `POST http://localhost:8000/api/chat`
  - Body: `{ "user_id": 1, "message": "I'm feeling stressed", "session_id": "user_123" }`

---

## ⚠️ Common Troubleshooting
- **Port 8000 Conflict**: If the server fails to start, ensure no other `uvicorn` or Docker instances are using port 8000.
- **Docker Daemon Error**: If `docker-compose` fails, ensure Docker Desktop is open and the engine icon is green.
- **Gemini Timeout**: If AI responses are slow, check your internet connection or increase `GEMINI_TIMEOUT_SECONDS` in `.env`.


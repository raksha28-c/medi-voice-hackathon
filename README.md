# MediVoice Backend

MediVoice is a small FastAPI + Streamlit project for a healthcare voice assistant demo.
It supports Hindi and English symptom prompts, a simple triage flow, and Gemini-powered
responses with a local fallback when Gemini is unavailable.

## What is in this repo

- `main.py` - FastAPI backend with `/vapi-webhook`, `/test`, `/call-log`, and `/health`
- `streamlit_app_app.py` - dashboard for manual testing
- `mock_qdrant.py` - structured local symptom database
- `qdrant_service/search.py` - unified search entry point used by the backend
- `qdrant_service/local_store.py` - lightweight local text search over `data.txt`
- `prompt.py` - Gemini integration plus fallback response generation
- `test_gemini.py` - smoke test for response generation
- `test_qdrant.py` - simple interactive local-search test

## Setup

1. Create or activate a virtual environment.
2. Install dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Add your Gemini API key to `.env`:

```env
GEMINI_API_KEY=your_key_here
```

## Run the app

Backend:

```powershell
.\.venv\Scripts\python.exe main.py
```

Dashboard:

```powershell
.\.venv\Scripts\streamlit.exe run streamlit_app_app.py
```

Optional smoke test:

```powershell
.\.venv\Scripts\python.exe test_gemini.py
```

## Notes

- The backend currently uses the local search layer through `qdrant_service/search.py`.
- Gemini calls are used when available, but the app still returns a useful response if the API call fails.
- `.env`, virtualenv folders, and Python cache files are ignored by git.

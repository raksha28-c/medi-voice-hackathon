# MediVoice Setup Guide

## 1. Install dependencies

Use the existing virtual environment if you already have one:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 2. Configure environment variables

Set at least:

```env
GEMINI_API_KEY=your_key_here
```

If you later switch to a hosted vector database, you can also keep other keys in `.env`,
but the current integrated app does not require remote Qdrant to run.

## 3. Start the backend

```powershell
.\.venv\Scripts\python.exe main.py
```

Expected result:
- FastAPI starts on `http://127.0.0.1:8000`

## 4. Start the dashboard

```powershell
.\.venv\Scripts\streamlit.exe run streamlit_app_app.py
```

Expected result:
- Streamlit opens on `http://localhost:8501`

## 5. Verify response generation

```powershell
.\.venv\Scripts\python.exe test_gemini.py
```

If Gemini is reachable, you will see a live generated response.
If Gemini is unavailable, the backend still uses a built-in fallback response path.

## Common issues

`ModuleNotFoundError`
- Re-run the dependency install command inside `.venv`.

`connection refused`
- Make sure `main.py` is running before opening the dashboard.

Gemini network failure
- The backend will fall back to a local response so manual tests can still proceed.

@echo off
echo ============================================
echo MediVoice Quick Start
echo ============================================
echo.

.\.venv\Scripts\python.exe check_setup.py

echo.
echo Run the backend:
echo   .\.venv\Scripts\python.exe main.py
echo.
echo Run the dashboard:
echo   .\.venv\Scripts\streamlit.exe run streamlit_app_app.py
echo.
pause

#!/usr/bin/env python
"""Quick local validation for the MediVoice repo."""

from pathlib import Path
import sys


REQUIRED_FILES = [
    ".env",
    "requirements.txt",
    ".gitignore",
    "main.py",
    "prompt.py",
    "mock_qdrant.py",
    "streamlit_app_app.py",
    "test_gemini.py",
    "qdrant_service/search.py",
    "qdrant_service/local_store.py",
]


def check_setup() -> int:
    print("MediVoice setup check")
    print("-" * 40)
    print(f"Python {sys.version.split()[0]}")

    missing = []
    for file_name in REQUIRED_FILES:
        if Path(file_name).exists():
            print(f"[ok] {file_name}")
        else:
            print(f"[missing] {file_name}")
            missing.append(file_name)

    venv_present = Path(".venv").exists() or Path("venv").exists()
    print(f"[ok] virtualenv present: {venv_present}")

    print("-" * 40)
    if missing:
        print(f"Missing files: {len(missing)}")
        return 1

    print("Repo looks ready.")
    print("Next steps:")
    print(r"1. .\.venv\Scripts\python.exe -m pip install -r requirements.txt")
    print(r"2. .\.venv\Scripts\python.exe main.py")
    print(r"3. .\.venv\Scripts\streamlit.exe run streamlit_app_app.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(check_setup())

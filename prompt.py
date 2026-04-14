from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv

try:
    from google import genai
except ImportError:  # pragma: no cover - handled in runtime fallback
    genai = None

load_dotenv()

SYSTEM_PROMPT = """You are a warm, calm healthcare assistant for low-literacy patients in India.

Rules:
1. Reply in the same language the patient used (Hindi in = Hindi out)
2. Use maximum 2-3 short sentences only
3. Never diagnose - only suggest and comfort
4. Use simple everyday words only - no medical jargon
5. If triage is urgent: your first sentence MUST be "Abhi 108 par call karein" (Hindi) or "Call 108 immediately" (English)
6. Tone: warm, reassuring, and calm
7. Never use bullet points or lists - speak naturally as if talking to someone
"""


def _is_hindi(text: str) -> bool:
    return any("\u0900" <= char <= "\u097F" for char in text)


def is_gemini_configured() -> bool:
    return bool(os.getenv("GEMINI_API_KEY")) and genai is not None


def _get_client() -> Optional["genai.Client"]:
    if not is_gemini_configured():
        return None
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def _fallback_health_response(patient_query: str, symptom_data: dict) -> str:
    is_hindi = _is_hindi(patient_query)
    triage = symptom_data.get("triage", "mild")
    advice = symptom_data.get("advice_hi") if is_hindi else symptom_data.get("advice_en")
    condition = symptom_data.get("condition_hi") if is_hindi else symptom_data.get("condition")

    if triage == "urgent":
        return (
            f"Abhi 108 par call karein. {advice}"
            if is_hindi
            else f"Call 108 immediately. {advice}"
        )

    if advice:
        return (
            f"Lagta hai yeh {condition} se juda ho sakta hai. {advice}"
            if is_hindi
            else f"This may be related to {condition}. {advice}"
        )

    return (
        "Kripya aaram karein aur agar takleef badhe to doctor se milen."
        if is_hindi
        else "Please rest, and if the problem gets worse, see a doctor."
    )


def generate_health_response(patient_query: str, symptom_data: dict) -> str:
    """Generate a warm patient-facing response, with a safe local fallback."""
    is_hindi = _is_hindi(patient_query)
    language = "Hindi" if is_hindi else "English"
    triage = symptom_data.get("triage", "mild")
    advice = symptom_data.get("advice_hi") if is_hindi else symptom_data.get("advice_en")
    condition = symptom_data.get("condition", "a health condition")

    client = _get_client()
    if client is None:
        return _fallback_health_response(patient_query, symptom_data)

    prompt = f"""{SYSTEM_PROMPT}

Language: {language}
Patient said: {patient_query}
Detected condition: {condition}
Severity: {triage}
Suggested advice: {advice}

Generate a warm, short response in {language}."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"text": prompt}],
        )
        if response.text:
            return response.text.strip()
    except Exception as exc:
        print(f"Gemini health response fallback: {exc}")

    return _fallback_health_response(patient_query, symptom_data)


def generate_booking_confirmation(specialist: str) -> str:
    """Generate appointment confirmation with the same fallback behavior."""
    client = _get_client()
    if client is None:
        return f"Your appointment with the {specialist} has been booked."

    prompt = (
        "Generate a short, warm confirmation message in simple English "
        f"that the patient's appointment with a {specialist} has been booked."
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[{"text": prompt}],
        )
        if response.text:
            return response.text.strip()
    except Exception as exc:
        print(f"Gemini booking response fallback: {exc}")

    return f"Your appointment with the {specialist} has been booked."

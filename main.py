from datetime import datetime

from fastapi import FastAPI

from prompt import (
    generate_booking_confirmation,
    generate_health_response,
    is_gemini_configured,
)
from qdrant_service import SEARCH_PROVIDER, search_symptoms

app = FastAPI(title="MediVoice Backend")

call_log = []

DEFAULT_RESPONSE_HI = "Kripya apni samasya ke baare mein thoda aur batayen."
DEFAULT_RESPONSE_EN = "Please tell me a little more about the problem."


def _is_hindi(text: str) -> bool:
    return any("\u0900" <= char <= "\u097F" for char in text)


def _default_response(text: str) -> str:
    return DEFAULT_RESPONSE_HI if _is_hindi(text) else DEFAULT_RESPONSE_EN


def _record_call(transcript: str, symptom_data: dict, ai_response: str) -> None:
    call_log.append(
        {
            "timestamp": datetime.now().isoformat(),
            "patient_said": transcript,
            "condition": symptom_data.get("condition", "Unknown"),
            "triage": symptom_data.get("triage", "unknown"),
            "ai_response": ai_response,
        }
    )


@app.post("/vapi-webhook")
async def vapi_webhook(body: dict):
    """
    Handle incoming VAPI webhook messages.
    - assistant-request: Process patient query and return AI response
    - function-call: Handle appointment booking
    """
    try:
        message = body.get("message", {})
        message_type = message.get("type")

        if message_type == "assistant-request":
            transcript = message.get("transcript", "").strip()
            if not transcript:
                return {"assistant": {"content": DEFAULT_RESPONSE_HI}}

            search_results = search_symptoms(transcript, top_k=1)
            symptom_data = search_results[0] if search_results else {}
            ai_response = (
                generate_health_response(transcript, symptom_data)
                if symptom_data
                else _default_response(transcript)
            )
            _record_call(transcript, symptom_data, ai_response)
            return {"assistant": {"content": ai_response}}

        if message_type == "function-call" and message.get("functionName") == "book_appointment":
            specialist = message.get("arguments", {}).get("specialist", "Doctor")
            confirmation = generate_booking_confirmation(specialist)
            return {"assistant": {"content": confirmation}}

        return {"assistant": {"content": DEFAULT_RESPONSE_HI}}
    except Exception as exc:
        print(f"Error: {exc}")
        return {"assistant": {"content": DEFAULT_RESPONSE_HI}}


@app.get("/call-log")
async def get_call_log():
    return {"calls": call_log}


@app.get("/health")
async def health_check():
    return {
        "status": "MediVoice running",
        "total_calls": len(call_log),
        "search_provider": SEARCH_PROVIDER,
        "gemini_configured": is_gemini_configured(),
    }


@app.post("/test")
async def test_endpoint(body: dict):
    """Manual symptom-query endpoint used by the dashboard."""
    try:
        query = body.get("query", "").strip()
        if not query:
            return {"error": "No query provided"}

        search_results = search_symptoms(query, top_k=1)
        symptom_data = search_results[0] if search_results else {}
        ai_response = (
            generate_health_response(query, symptom_data)
            if symptom_data
            else _default_response(query)
        )
        result = {
            "query": query,
            "condition": symptom_data.get("condition", "Unknown"),
            "condition_hi": symptom_data.get("condition_hi", symptom_data.get("condition", "Unknown")),
            "triage": symptom_data.get("triage", "unknown"),
            "triage_hi": symptom_data.get("triage_hi", symptom_data.get("triage", "unknown")),
            "ai_response": ai_response,
        }
        _record_call(query, symptom_data, ai_response)
        return result
    except Exception as exc:
        print(f"Error: {exc}")
        return {"error": str(exc)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

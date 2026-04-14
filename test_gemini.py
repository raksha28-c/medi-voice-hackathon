from prompt import generate_health_response, is_gemini_configured

sample_symptom = {
    "condition": "Viral infection",
    "condition_hi": "Viral infection",
    "triage": "moderate",
    "advice_en": "Rest well and drink water.",
    "advice_hi": "Aram karein aur pani piyen.",
}

print("Testing response generation...")
print("-" * 50)
print(f"Gemini configured: {is_gemini_configured()}")

response = generate_health_response("I have fever", sample_symptom)
print("Response:")
print(response)
print("-" * 50)
print("Response generation successful.")

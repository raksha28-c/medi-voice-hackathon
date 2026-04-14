# On integration day replace: from mock_qdrant import search_symptoms
# with: from qdrant_service.search import search_symptoms

SYMPTOM_DATABASE = [
    {
        "hi": "पेट दर्द",
        "en": "Stomach pain",
        "condition": "Gastroenteritis or Indigestion",
        "condition_hi": "गैस्ट्रोएंटेराइटिस या अपच",
        "triage": "moderate",
        "triage_hi": "मध्यम",
        "advice_hi": "हल्का खाना खाएं और ढेर सारा पानी पिएं। दो दिन में बेहतर न हो तो डॉक्टर से मिलें।",
        "advice_en": "Eat light food and drink plenty of water. See a doctor if it doesn't improve in 2 days.",
        "specialist": "General Physician"
    },
    {
        "hi": "बुखार",
        "en": "Fever",
        "condition": "Viral infection",
        "condition_hi": "वायरल संक्रमण",
        "triage": "moderate",
        "triage_hi": "मध्यम",
        "advice_hi": "खूब आराम करें और पानी पिएं। बुखार कम करने के लिए ठंडा पानी से पोंछ सकते हैं।",
        "advice_en": "Rest well and drink water. Use cold water to cool down your body.",
        "specialist": "General Physician"
    },
    {
        "hi": "सांस लेने में तकलीफ",
        "en": "Breathing difficulty",
        "condition": "Asthma or Respiratory infection",
        "condition_hi": "दमा या श्वसन संक्रमण",
        "triage": "urgent",
        "triage_hi": "तुरंत",
        "advice_hi": "Abhi 108 par call karein। यह गंभीर हो सकता है।",
        "advice_en": "Call 108 immediately. This can be serious.",
        "specialist": "Pulmonologist"
    },
    {
        "hi": "सीने में दर्द",
        "en": "Chest pain",
        "condition": "Cardiac or Musculoskeletal",
        "condition_hi": "हृदय या मांसपेशी संबंधी",
        "triage": "urgent",
        "triage_hi": "तुरंत",
        "advice_hi": "Abhi 108 par call karein। तुरंत अस्पताल जाएं।",
        "advice_en": "Call 108 immediately. Go to hospital urgently.",
        "specialist": "Cardiologist"
    },
    {
        "hi": "सिरदर्द",
        "en": "Headache",
        "condition": "Tension or Migraine",
        "condition_hi": "तनाव या माइग्रेन",
        "triage": "mild",
        "triage_hi": "हल्का",
        "advice_hi": "आराम करें, ठंडा पानी से सिर धोएं। ज्यादा दर्द हो तो दवा ले सकते हैं।",
        "advice_en": "Rest and wash your head with cool water. You can take pain relief if needed.",
        "specialist": "General Physician"
    },
    {
        "hi": "खांसी",
        "en": "Cough",
        "condition": "Common cold or Bronchitis",
        "condition_hi": "सर्दी या ब्रोंकाइटिस",
        "triage": "mild",
        "triage_hi": "हल्का",
        "advice_hi": "गर्म पानी, शहद और अदरक चाय पिएं। तीन दिन से ज्यादा हो तो डॉक्टर देखें।",
        "advice_en": "Drink warm water with honey and ginger. See doctor if it lasts more than 3 days.",
        "specialist": "General Physician"
    },
    {
        "hi": "उल्टी",
        "en": "Vomiting",
        "condition": "Food poisoning or Infection",
        "condition_hi": "भोजन विषाक्तता या संक्रमण",
        "triage": "moderate",
        "triage_hi": "मध्यम",
        "advice_hi": "मसालेदार खाना न खाएं। नारियल का पानी या दाल का पानी पिएं।",
        "advice_en": "Avoid spicy food. Drink coconut water or lentil soup.",
        "specialist": "General Physician"
    },
    {
        "hi": "दस्त",
        "en": "Diarrhea",
        "condition": "Gastroenteritis",
        "condition_hi": "गैस्ट्रोएंटेराइटिस",
        "triage": "moderate",
        "triage_hi": "मध्यम",
        "advice_hi": "ढेर सारा पानी पिएं ताकि शरीर में नमी न घटे। खिचड़ी और सादा खाना खाएं।",
        "advice_en": "Drink plenty of water to prevent dehydration. Eat khichdi and plain food.",
        "specialist": "General Physician"
    },
    {
        "hi": "चक्कर आना",
        "en": "Dizziness",
        "condition": "Low blood pressure or Blood sugar",
        "condition_hi": "कम रक्तचाप या कम ब्लड शुगर",
        "triage": "mild",
        "triage_hi": "हल्का",
        "advice_hi": "बैठ जाएं और कुछ देर आराम करें। कुछ मीठा खा लें।",
        "advice_en": "Sit down and rest. Eat something sweet.",
        "specialist": "General Physician"
    },
    {
        "hi": "जोड़ों में दर्द",
        "en": "Joint pain",
        "condition": "Arthritis or Inflammation",
        "condition_hi": "गठिया या सूजन",
        "triage": "mild",
        "triage_hi": "हल्का",
        "advice_hi": "प्रभावित जगह पर गर्म पानी की सेंक दें। हल्का व्यायाम करें।",
        "advice_en": "Apply warm water fomentation. Do light exercise.",
        "specialist": "Orthopedist"
    }
]


def search_symptoms(query: str, top_k: int = 3) -> list:
    """
    Search symptoms by Hindi or English text.
    Returns top_k matching symptoms with relevance scores.
    """
    query_lower = query.lower()
    results = []
    
    for symptom in SYMPTOM_DATABASE:
        score = 0
        
        # Check English field
        if query_lower in symptom["en"].lower():
            score += 10
        elif any(word in symptom["en"].lower() for word in query_lower.split()):
            score += 5
        
        # Check Hindi field (direct match without lowercase - Hindi doesn't have case)
        if query in symptom["hi"]:
            score += 10
        # Also check partial matches
        elif query.lower() in symptom["hi"].lower():
            score += 8
        # Check if any word matches
        elif any(word in symptom["hi"] for word in query.split()):
            score += 5
        
        # Check condition field
        if query_lower in symptom["condition"].lower():
            score += 3
        
        if score > 0:
            results.append({
                "score": score,
                "symptom": symptom
            })
    
    # Sort by score and return top_k
    results.sort(key=lambda x: x["score"], reverse=True)
    return [r["symptom"] for r in results[:top_k]]

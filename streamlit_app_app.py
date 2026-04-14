import streamlit as st
import httpx
import time
from datetime import datetime

st.set_page_config(page_title="MediVoice Dashboard", layout="wide")

# Initialize session state
if "test_result" not in st.session_state:
    st.session_state.test_result = None
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

st.title("🏥 MediVoice Dashboard")

# Top metrics row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Languages", "Hindi + English")
with col2:
    st.metric("Literacy Needed", "Zero")
with col3:
    st.metric("Symptoms", "10+")
with col4:
    st.metric("Emergency", "108")

st.divider()

# Two columns layout
col_left, col_right = st.columns([1.5, 1])

# LEFT COLUMN: Live Call Feed
with col_left:
    st.subheader("📞 Live Call Feed")
    
    backend_url = "http://localhost:8000"
    
    try:
        response = httpx.get(f"{backend_url}/call-log", timeout=5)
        calls = response.json().get("calls", [])
        
        if calls:
            # Show last 6 calls in reverse order (most recent first)
            for call in calls[-6:][::-1]:
                with st.container(border=True):
                    # Triage color icon
                    triage = call.get("triage", "unknown").lower()
                    if triage == "urgent":
                        triage_icon = "🔴"
                    elif triage == "moderate":
                        triage_icon = "🟡"
                    else:
                        triage_icon = "🟢"
                    
                    st.write(f"**Patient:** {call.get('patient_said', 'N/A')}")
                    st.write(f"**Condition:** {call.get('condition', 'Unknown')}")
                    st.write(f"**Severity:** {triage_icon} {triage.capitalize()}")
                    st.write(f"**AI Response:** {call.get('ai_response', 'N/A')}")
                    st.caption(f"Time: {call.get('timestamp', 'N/A')}")
        else:
            st.info("💬 No calls yet. Patients will appear here.")
    
    except Exception as e:
        st.warning(f"⚠️ Backend not running")

# RIGHT COLUMN: Manual Test Box
with col_right:
    st.subheader("🧪 Simulate Patient Call")
    
    test_query = st.text_input("Enter patient query (Hindi or English):", value=st.session_state.last_query)
    test_button = st.button("Simulate patient call", use_container_width=True)
    
    if test_button and test_query:
        st.session_state.last_query = test_query
        try:
            with st.spinner("Getting response..."):
                response = httpx.post(
                    "http://localhost:8000/test",
                    json={"query": test_query},
                    timeout=10
                )
                result = response.json()
                
                # Store in session state
                if isinstance(result, dict) and "error" not in result:
                    st.session_state.test_result = result
                    st.session_state.show_result = True
                    st.rerun()  # Refresh page to show updated call feed
                else:
                    st.error("Error getting response")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Display result if available (stays visible)
    if st.session_state.show_result and st.session_state.test_result:
        result = st.session_state.test_result
        st.success("✓ Response received")
        
        # Detect language from query
        is_hindi = any('\u0900' <= c <= '\u097F' for c in st.session_state.last_query)
        
        triage = result.get("triage", "unknown").lower()
        if triage == "urgent":
            triage_icon = "🔴"
        elif triage == "moderate":
            triage_icon = "🟡"
        else:
            triage_icon = "🟢"
        
        # Show in patient's language
        if is_hindi:
            condition_text = result.get("condition_hi", result.get("condition", "Unknown"))
            triage_text = result.get("triage_hi", triage.capitalize())
            st.write(f"**स्थिति:** {condition_text}")
            st.write(f"**गंभीरता:** {triage_icon} {triage_text}")
            st.write(f"**AI प्रतिक्रिया:**\n\n{result.get('ai_response', 'N/A')}")
            if triage == "urgent":
                st.error("🚨 अभी 108 पर कॉल करें!")
        else:
            st.write(f"**Condition:** {result.get('condition', 'Unknown')}")
            st.write(f"**Severity:** {triage_icon} {triage.capitalize()}")
            st.write(f"**AI Response:**\n\n{result.get('ai_response', 'N/A')}")
            if triage == "urgent":
                st.error("🚨 Call 108 immediately!")
    


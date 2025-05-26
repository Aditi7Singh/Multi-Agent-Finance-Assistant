import streamlit as st
import httpx
import json
from typing import Dict, List

# Configure page settings
st.set_page_config(
    page_title="Finance Assistant",
    page_icon="💹",
    layout="wide"
)

# Constants for service URLs
SERVICE_URLS = {
    "orchestrator": "http://localhost:8000",
    "voice": "http://localhost:8005"
}

def check_services_health() -> Dict[str, bool]:
    """Check the health of all required services."""
    health_status = {}
    for service, url in SERVICE_URLS.items():
        try:
            with httpx.Client(timeout=2.0) as client:
                response = client.get(f"{url}/health")
                health_status[service] = response.status_code == 200
        except:
            health_status[service] = False
    return health_status

def get_market_brief(query: str = "") -> Dict:
    """Get market brief from the orchestrator."""
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f"{SERVICE_URLS['orchestrator']}/get_market_brief",
                json={"query": query}
            )
            return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    st.title("🤖 AI Finance Assistant")
    
    # Check services health
    health_status = check_services_health()
    
    # Display service status
    with st.expander("Service Status"):
        for service, is_healthy in health_status.items():
            st.write(
                f":{':green_circle' if is_healthy else ':red_circle'}: {service.title()}"
            )
    
    # Main interface
    st.write("### Market Brief Generator")
    
    # User input
    query = st.text_area(
        "What would you like to know about the market?",
        placeholder="E.g., Give me a brief on Asian tech stocks and recent earnings surprises",
        height=100
    )
    
    # Additional options
    col1, col2 = st.columns(2)
    with col1:
        enable_voice = st.checkbox("Enable voice output", value=True)
    with col2:
        auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
    
    # Generate brief button
    if st.button("Generate Brief", type="primary", disabled=not all(health_status.values())):
        with st.spinner("Generating market brief..."):
            result = get_market_brief(query)
            
            if "error" in result:
                st.error(f"Error generating brief: {result['error']}")
            else:
                # Display text brief
                st.write("### Generated Brief")
                st.write(result["brief"])
                
                # Handle voice output
                if enable_voice and "audio_url" in result:
                    st.audio(result["audio_url"], format="audio/mp3")
    
    # Display additional information
    st.sidebar.write("### Market Data Sources")
    st.sidebar.write(
        "- Real-time stock data via Yahoo Finance\n"
        "- Market sentiment from financial news\n"
        "- Company filings and earnings reports\n"
        "- Global market indices"
    )
    
    # Auto-refresh logic
    if auto_refresh:
        st.empty()
        st.rerun()

if __name__ == "__main__":
    main()
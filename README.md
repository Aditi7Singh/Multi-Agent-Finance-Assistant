🧠 Multi-Agent Finance Assistant

An advanced AI-powered finance assistant that delivers spoken daily market briefs via a Streamlit web interface. The system leverages multiple specialized agents to perform real-time data ingestion, financial analysis, document retrieval, and natural language processing — all orchestrated via microservices.

🚀 Features
🔍 Real-time market data fetching using the Yahoo Finance API

📰 Web scraping for company filings and market sentiment

📊 Advanced financial analysis and portfolio risk metrics

🧠 Natural Language Generation (NLG) for market brief synthesis

🔈 Speech-to-text (STT) and text-to-speech (TTS) pipelines using Whisper and open-source TTS

📁 Vector-based document retrieval using FAISS or Pinecone

🌐 Interactive Streamlit frontend for voice and text interaction

🏗️ Architecture
The system is composed of modular microservices, each running independently via FastAPI:

Agent	Role	Port
API Agent	Fetches real-time & historical market data	8001
Scraping Agent	Crawls market filings and sentiment from public sources	8002
Analysis Agent	Analyzes portfolio data, calculates exposure & performance	8003
Retriever Agent	Embeds & retrieves documents using vector similarity search	8004
Voice Agent	Converts voice to text (STT) and text to voice (TTS)	8005
Language Agent	Generates market briefs using LLMs and LangGraph/CrewAI	8006
Orchestrator	Routes requests between agents and manages agent coordination	8000
Streamlit UI	Web-based interface for user interaction	8501

🛠️ Installation & Setup
Clone the repository

bash
Copy
Edit
git clone https://github.com/Aditi7Singh/multi-agent-finance-assistant.git
cd multi-agent-finance-assistant
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run agents and orchestrator (in separate terminals or use a process manager like pm2)

bash
Copy
Edit
uvicorn api_agent:app --port 8001
uvicorn scraping_agent:app --port 8002
uvicorn analysis_agent:app --port 8003
uvicorn retriever_agent:app --port 8004
uvicorn voice_agent:app --port 8005
uvicorn language_agent:app --port 8006
uvicorn orchestrator:app --port 8000
Launch Streamlit UI

bash
Copy
Edit
streamlit run streamlit_app.py
📂 Project Structure
bash
Copy
Edit
/data_ingestion       # API & scraping pipelines
/agents               # Specialized microservice agents
/orchestrator         # Central router & workflow manager
/streamlit_app        # Frontend user interface
/docs                 # Architecture diagrams & AI-tool logs
requirements.txt      # Project dependencies
README.md             # Project overview and setup
📄 Documentation
🧠 AI Tool Usage Logs: See /docs/ai_tool_usage.md for detailed records of prompt engineering, model configs, and generated code.

🖼️ Architecture Diagrams: Visual overview of system components and communication.

🧪 Benchmarks: Performance metrics for latency, accuracy, and response quality (optional).

👩‍💻 Contributor
Aditi Singh – Architected and implemented the entire system, including agent orchestration, voice pipelines, and financial analytics.

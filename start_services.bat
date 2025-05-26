@echo off
echo Starting Multi-Agent Finance Assistant Services...

:: Start all agents in separate windows
start "API Agent" cmd /k "uvicorn agents.api_agent:app --host 0.0.0.0 --port 8001"
start "Scraping Agent" cmd /k "uvicorn agents.scraping_agent:app --host 0.0.0.0 --port 8002"
start "Analysis Agent" cmd /k "uvicorn agents.analysis_agent:app --host 0.0.0.0 --port 8003"
start "Retriever Agent" cmd /k "uvicorn agents.retriever_agent:app --host 0.0.0.0 --port 8004"
start "Voice Agent" cmd /k "uvicorn agents.voice_agent:app --host 0.0.0.0 --port 8005"
start "Language Agent" cmd /k "uvicorn agents.language_agent:app --host 0.0.0.0 --port 8006"

:: Wait a few seconds for agents to initialize
timeout /t 5 /nobreak

:: Start the orchestrator
start "Orchestrator" cmd /k "uvicorn orchestrator.coordinator:app --host 0.0.0.0 --port 8000"

:: Wait for orchestrator to initialize
timeout /t 3 /nobreak

:: Start the Streamlit interface
start "Streamlit Interface" cmd /k "streamlit run streamlit_app/app.py"

echo All services have been started!
echo Access the interface at http://localhost:8501
# Multi-Agent Finance Assistant

An advanced AI-powered finance assistant that delivers spoken market briefs via a Streamlit interface. The system utilizes multiple specialized agents for data ingestion, analysis, and natural language processing.

## Features

- Real-time market data fetching via Yahoo Finance API
- Web scraping for market sentiment and company filings
- Advanced data analysis and portfolio metrics
- Natural language processing for market brief generation
- Text-to-speech and speech-to-text capabilities
- Vector-based document retrieval system
- Interactive Streamlit web interface

## Architecture

The system consists of several microservices:

1. **API Agent** (Port 8001): Handles real-time market data fetching
2. **Scraping Agent** (Port 8002): Manages web scraping operations
3. **Analysis Agent** (Port 8003): Processes financial data and metrics
4. **Retriever Agent** (Port 8004): Manages vector storage and similarity search
5. **Voice Agent** (Port 8005): Handles speech-to-text and text-to-speech conversion
6. **Language Agent** (Port 8006): Processes natural language and generates market briefs
7. **Orchestrator** (Port 8000): Coordinates all agents and manages workflow
8. **Streamlit Frontend** (Port 8501): Provides the user interface

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
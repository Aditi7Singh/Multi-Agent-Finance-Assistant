from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import httpx
import asyncio

class MarketQuery(BaseModel):
    query: str
    portfolio_id: Optional[str] = None
    region: str = "Asia"
    sector: str = "Technology"

class OrchestrationResponse(BaseModel):
    text_response: str
    audio_response: Optional[bytes] = None
    analysis_data: Dict
    timestamp: str

app = FastAPI()

class ServiceOrchestrator:
    def __init__(self):
        self.services = {
            'api': 'http://localhost:8000',
            'scraping': 'http://localhost:8001',
            'voice': 'http://localhost:8002',
            'retriever': 'http://localhost:8003',
            'analysis': 'http://localhost:8004',
            'language': 'http://localhost:8005'
        }
        self.client = httpx.AsyncClient(timeout=30.0)

    async def check_services_health(self) -> Dict[str, bool]:
        health_status = {}
        for service, url in self.services.items():
            try:
                response = await self.client.get(f"{url}/health")
                health_status[service] = response.status_code == 200
            except Exception:
                health_status[service] = False
        return health_status

    async def get_market_data(self, region: str, sector: str) -> Dict:
        try:
            # Get market data from API agent
            response = await self.client.get(
                f"{self.services['api']}/stock-data",
                params={"region": region, "sector": sector}
            )
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching market data: {str(e)}")

    async def get_sentiment_data(self, region: str) -> Dict:
        try:
            response = await self.client.get(
                f"{self.services['scraping']}/market-sentiment/{region}"
            )
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching sentiment data: {str(e)}")

    async def process_query(self, query: MarketQuery) -> OrchestrationResponse:
        try:
            # Gather data in parallel
            market_data, sentiment_data = await asyncio.gather(
                self.get_market_data(query.region, query.sector),
                self.get_sentiment_data(query.region)
            )

            # Analyze data
            analysis_response = await self.client.post(
                f"{self.services['analysis']}/analyze",
                json={
                    "market_data": market_data,
                    "sentiment_data": sentiment_data
                }
            )
            analysis_results = analysis_response.json()

            # Generate language response
            language_response = await self.client.post(
                f"{self.services['language']}/analyze",
                json={
                    "portfolio_metrics": analysis_results["portfolio_metrics"],
                    "earnings_analysis": analysis_results["earnings_analysis"],
                    "market_sentiment": analysis_results["market_sentiment"],
                    "query": query.query
                }
            )
            text_response = language_response.json()["response"]

            # Convert to speech
            voice_response = await self.client.post(
                f"{self.services['voice']}/text-to-speech",
                json={"text": text_response}
            )
            audio_data = voice_response.content

            return OrchestrationResponse(
                text_response=text_response,
                audio_response=audio_data,
                analysis_data=analysis_results,
                timestamp=datetime.now().isoformat()
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Orchestration error: {str(e)}")

orchestrator = ServiceOrchestrator()

@app.post("/process-query", response_model=OrchestrationResponse)
async def process_market_query(query: MarketQuery):
    return await orchestrator.process_query(query)

@app.get("/health")
async def health_check():
    health_status = await orchestrator.check_services_health()
    all_healthy = all(health_status.values())
    return {
        "status": "healthy" if all_healthy else "degraded",
        "services": health_status
    }
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from data_ingestion.scraper import FinancialScraper

app = FastAPI()
scraper = FinancialScraper()

class ScrapingRequest(BaseModel):
    symbol: Optional[str] = None
    region: Optional[str] = None

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/market-sentiment/{region}")
async def get_market_sentiment(region: str):
    sentiment = scraper.get_market_sentiment(region)
    return sentiment

@app.get("/company-filings/{symbol}")
async def get_company_filings(symbol: str):
    filings = scraper.get_company_filings(symbol)
    return {"filings": filings}

@app.get("/yield-data")
async def get_yield_data():
    data = scraper.get_yield_data()
    return data
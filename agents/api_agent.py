from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from data_ingestion.api_fetcher import MarketDataFetcher

app = FastAPI()
market_data_fetcher = MarketDataFetcher()

class Portfolio(BaseModel):
    positions: List[Dict]

class SymbolList(BaseModel):
    symbols: List[str]

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/asia-tech-exposure")
async def get_asia_tech_exposure(portfolio: Portfolio):
    exposure = market_data_fetcher.get_asia_tech_exposure(portfolio.positions)
    return exposure

@app.post("/earnings-surprises")
async def get_earnings_surprises(symbols: SymbolList):
    surprises = market_data_fetcher.get_earnings_surprises(symbols.symbols)
    return {"surprises": surprises}

@app.get("/stock/{symbol}")
async def get_stock_data(symbol: str):
    data = market_data_fetcher.get_stock_data(symbol)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Data not found for symbol {symbol}")
    return data
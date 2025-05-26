from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import numpy as np
from enum import Enum

class MarketSentiment(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"

class AnalysisRequest(BaseModel):
    market_data: Dict
    earnings_data: List[Dict]
    sentiment_data: Dict
    portfolio_data: Dict

class RiskMetrics(BaseModel):
    volatility: float
    beta: float
    sharpe_ratio: float
    max_drawdown: float

app = FastAPI()

class FinancialAnalyzer:
    def __init__(self):
        self.risk_free_rate = 0.02  # 2% annual risk-free rate

    def calculate_portfolio_metrics(self, portfolio_data: Dict) -> Dict:
        try:
            total_value = portfolio_data.get('total_value', 0)
            positions = portfolio_data.get('positions', [])
            
            # Calculate sector exposures
            sector_exposure = {}
            for position in positions:
                sector = position.get('sector', 'Unknown')
                value = position.get('value', 0)
                sector_exposure[sector] = sector_exposure.get(sector, 0) + value
            
            # Convert to percentages
            sector_allocation = {
                sector: (value / total_value * 100) if total_value > 0 else 0
                for sector, value in sector_exposure.items()
            }
            
            return {
                'total_value': total_value,
                'sector_allocation': sector_allocation
            }
        except Exception as e:
            raise ValueError(f"Error calculating portfolio metrics: {str(e)}")

    def analyze_earnings_surprises(self, earnings_data: List[Dict]) -> Dict:
        try:
            total_surprises = len(earnings_data)
            positive_surprises = sum(1 for e in earnings_data if e.get('surprise_percentage', 0) > 0)
            negative_surprises = sum(1 for e in earnings_data if e.get('surprise_percentage', 0) < 0)
            
            avg_surprise = np.mean([e.get('surprise_percentage', 0) for e in earnings_data]) if earnings_data else 0
            
            return {
                'total_reports': total_surprises,
                'positive_surprises': positive_surprises,
                'negative_surprises': negative_surprises,
                'average_surprise': avg_surprise
            }
        except Exception as e:
            raise ValueError(f"Error analyzing earnings surprises: {str(e)}")

    def determine_market_sentiment(self, sentiment_data: Dict) -> MarketSentiment:
        try:
            indicators = sentiment_data.get('indicators', [])
            positive_signals = 0
            negative_signals = 0
            
            for indicator in indicators:
                change = indicator.get('change', 0)
                if isinstance(change, str):
                    change = float(change.strip('%'))
                if change > 0:
                    positive_signals += 1
                elif change < 0:
                    negative_signals += 1
            
            total_signals = len(indicators)
            if total_signals == 0:
                return MarketSentiment.NEUTRAL
            
            positive_ratio = positive_signals / total_signals
            negative_ratio = negative_signals / total_signals
            
            if positive_ratio > 0.6:
                return MarketSentiment.BULLISH
            elif negative_ratio > 0.6:
                return MarketSentiment.BEARISH
            else:
                return MarketSentiment.NEUTRAL
        except Exception as e:
            raise ValueError(f"Error determining market sentiment: {str(e)}")

analyzer = FinancialAnalyzer()

@app.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    try:
        # Perform various analyses
        portfolio_metrics = analyzer.calculate_portfolio_metrics(request.portfolio_data)
        earnings_analysis = analyzer.analyze_earnings_surprises(request.earnings_data)
        market_sentiment = analyzer.determine_market_sentiment(request.sentiment_data)
        
        return {
            "portfolio_metrics": portfolio_metrics,
            "earnings_analysis": earnings_analysis,
            "market_sentiment": market_sentiment,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
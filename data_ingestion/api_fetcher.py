import yfinance as yf
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class MarketDataFetcher:
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(minutes=15)

    def get_stock_data(self, symbol: str) -> Optional[Dict]:
        """Fetch current stock data from Yahoo Finance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                'symbol': symbol,
                'price': info.get('regularMarketPrice'),
                'change': info.get('regularMarketChangePercent'),
                'volume': info.get('regularMarketVolume'),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def get_asia_tech_exposure(self, portfolio: List[Dict]) -> Dict:
        """Calculate Asia tech exposure from portfolio"""
        total_aum = sum(position['value'] for position in portfolio)
        asia_tech_value = sum(
            position['value'] for position in portfolio
            if position.get('region') == 'Asia' and position.get('sector') == 'Technology'
        )
        
        return {
            'exposure_percentage': (asia_tech_value / total_aum * 100) if total_aum > 0 else 0,
            'total_value': asia_tech_value
        }

    def get_earnings_surprises(self, symbols: List[str]) -> List[Dict]:
        """Get earnings surprises for given symbols"""
        surprises = []
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                earnings = ticker.earnings
                if earnings is not None and not earnings.empty:
                    latest = earnings.iloc[-1]
                    expected = latest.get('Expected')
                    actual = latest.get('Actual')
                    if expected and actual:
                        surprise_pct = ((actual - expected) / expected) * 100
                        surprises.append({
                            'symbol': symbol,
                            'surprise_percentage': surprise_pct,
                            'actual': actual,
                            'expected': expected
                        })
            except Exception as e:
                print(f"Error fetching earnings data for {symbol}: {e}")
                continue
        return surprises
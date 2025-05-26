import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from datetime import datetime
import json
import time

class FinancialScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.base_urls = {
            'yahoo_finance': 'https://finance.yahoo.com',
            'market_watch': 'https://www.marketwatch.com'
        }

    def _make_request(self, url: str) -> Optional[str]:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def get_market_sentiment(self, region: str = 'Asia') -> Dict:
        """Scrape market sentiment indicators"""
        sentiment_data = {
            'sentiment': 'neutral',
            'indicators': [],
            'timestamp': datetime.now().isoformat()
        }

        # Example: Scrape Yahoo Finance Asia Markets page
        url = f"{self.base_urls['yahoo_finance']}/world-indices"
        html = self._make_request(url)
        
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            # Extract market indicators and calculate sentiment
            market_summary = soup.find('div', {'id': 'market-summary'})
            if market_summary:
                indicators = market_summary.find_all('tr')
                for indicator in indicators:
                    try:
                        name = indicator.find('td', {'class': 'name'}).text.strip()
                        change = indicator.find('td', {'class': 'change'}).text.strip()
                        sentiment_data['indicators'].append({
                            'name': name,
                            'change': change
                        })
                    except:
                        continue

        return sentiment_data

    def get_company_filings(self, symbol: str) -> List[Dict]:
        """Get recent company filings"""
        filings = []
        url = f"{self.base_urls['market_watch']}/investing/stock/{symbol}/financials"
        html = self._make_request(url)

        if html:
            soup = BeautifulSoup(html, 'html.parser')
            filing_tables = soup.find_all('table', {'class': 'filing'})
            
            for table in filing_tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    try:
                        cols = row.find_all('td')
                        filings.append({
                            'date': cols[0].text.strip(),
                            'type': cols[1].text.strip(),
                            'description': cols[2].text.strip()
                        })
                    except:
                        continue

        return filings

    def get_yield_data(self) -> Dict:
        """Get current yield data"""
        url = f"{self.base_urls['yahoo_finance']}/bonds"
        html = self._make_request(url)
        yield_data = {
            'timestamp': datetime.now().isoformat(),
            'yields': []
        }

        if html:
            soup = BeautifulSoup(html, 'html.parser')
            yield_table = soup.find('table', {'class': 'bonds'})
            if yield_table:
                rows = yield_table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    try:
                        cols = row.find_all('td')
                        yield_data['yields'].append({
                            'term': cols[0].text.strip(),
                            'rate': cols[1].text.strip()
                        })
                    except:
                        continue

        return yield_data
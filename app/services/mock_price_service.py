"""
Mock price service for development to avoid API calls to Finnhub/Exchange Rate APIs.
Returns realistic but fake prices that update periodically.
"""
import random
from typing import Dict
from datetime import datetime, timedelta


class MockPriceService:
    """Mock service that returns fake prices without hitting any external APIs."""
    
    def __init__(self):
        # Base prices for common Indian stocks
        self._base_prices = {
            "INFY": 1450.0,
            "INFY.NS": 1450.0,
            "TCS": 3500.0,
            "TCS.NS": 3500.0,
            "RELIANCE": 2450.0,
            "RELIANCE.NS": 2450.0,
            "HDFCBANK": 1650.0,
            "HDFCBANK.NS": 1650.0,
            "ICICIBANK": 950.0,
            "ICICIBANK.NS": 950.0,
        }
        self._last_update = datetime.now()
        self._current_prices = self._base_prices.copy()
    
    def _update_prices(self):
        """Simulate price changes every 15 seconds."""
        now = datetime.now()
        if now - self._last_update > timedelta(seconds=15):
            # Update prices with small random changes (-1% to +1%)
            for ticker, base_price in self._base_prices.items():
                change_percent = random.uniform(-0.01, 0.01)
                self._current_prices[ticker] = base_price * (1 + change_percent)
            self._last_update = now
    
    def get_quote(self, ticker: str) -> Dict:
        """Get a mock quote for a ticker."""
        self._update_prices()
        
        ticker_upper = ticker.upper()
        
        # Add .NS if not present for known Indian stocks
        if ticker_upper in self._base_prices:
            actual_ticker = ticker_upper if ticker_upper.endswith('.NS') else f"{ticker_upper}.NS"
        else:
            actual_ticker = ticker_upper if ticker_upper.endswith('.NS') else f"{ticker_upper}.NS"
        
        # Get price or generate random one
        price = self._current_prices.get(ticker_upper) or self._current_prices.get(actual_ticker) or random.uniform(100, 3000)
        
        # Determine if Indian stock
        is_indian = actual_ticker.endswith('.NS') or actual_ticker.endswith('.BO')
        
        return {
            'ticker': actual_ticker,
            'price': round(price, 2),
            'currency': 'INR' if is_indian else 'USD',
            'exchange': 'NSE' if actual_ticker.endswith('.NS') else 'BSE' if actual_ticker.endswith('.BO') else 'NASDAQ',
            'name': f"Mock Company {actual_ticker}",
            'is_indian': is_indian,
            'mock': True  # Flag to indicate this is mock data
        }
    
    def get_status(self) -> Dict:
        """Get service status."""
        return {
            'mock_mode': True,
            'message': 'Using mock data - no external API calls',
            'rate_limited': False,
            'base_prices': len(self._base_prices),
            'last_update': self._last_update.isoformat()
        }


# Singleton instance
mock_price_service = MockPriceService()

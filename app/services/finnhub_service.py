"""
Finnhub API service for stock quotes and symbol search.

Free tier: 60 API calls per minute
Supports: US stocks, some ADRs, symbol search
"""

import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import deque
import time


class FinnhubService:
    """Service for fetching stock data from Finnhub API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://finnhub.io/api/v1"
        
        # Rate limiting: 60 calls per minute
        self.max_calls_per_minute = 60
        self.call_timestamps = deque()  # Track request timestamps
        
        # Caching to reduce API calls
        self._cache: Dict[str, Dict] = {}
        self._cache_duration = timedelta(minutes=5)  # 5-minute cache
        
        # Known Indian stocks that might have ADRs
        self.indian_stocks_adr = {
            "INFY": "Infosys Limited",
            "WIT": "Wipro Limited", 
            "HDB": "HDFC Bank Limited",
            "IBN": "ICICI Bank Limited",
            "TTM": "Tata Motors Limited",
            "VEDL": "Vedanta Limited",
            "RDY": "Dr. Reddy's Laboratories",
            "SIFY": "Sify Technologies Limited"
        }
    
    def _wait_for_rate_limit(self):
        """Enforce rate limit of 60 calls per minute."""
        now = time.time()
        
        # Remove timestamps older than 1 minute
        while self.call_timestamps and self.call_timestamps[0] < now - 60:
            self.call_timestamps.popleft()
        
        # If we've made 60 calls in the last minute, wait
        if len(self.call_timestamps) >= self.max_calls_per_minute:
            sleep_time = 60 - (now - self.call_timestamps[0])
            if sleep_time > 0:
                print(f"⏳ Rate limit: sleeping {sleep_time:.1f}s")
                time.sleep(sleep_time)
                # Clear old timestamps after sleeping
                now = time.time()
                while self.call_timestamps and self.call_timestamps[0] < now - 60:
                    self.call_timestamps.popleft()
        
        # Record this call
        self.call_timestamps.append(now)
    
    def get_quote(self, ticker: str) -> Dict:
        """
        Get real-time quote for a ticker.
        
        Returns:
            {
                'ticker': str,
                'price': float (USD),
                'found': bool,
                'is_indian_adr': bool,
                'warning': str (optional)
            }
        """
        ticker = ticker.upper().strip()
        original_ticker = ticker
        
        # Detect and reject NSE/BSE tickers (Finnhub free tier doesn't support them)
        if ticker.endswith('.NS') or ticker.endswith('.BO'):
            return {
                'ticker': ticker,
                'price': None,
                'found': False,
                'is_indian_adr': False,
                'warning': f"⚠️ NSE/BSE stocks (like {ticker}) are not available on Finnhub free tier. Try US stocks (AAPL, MSFT, etc.) or Indian ADRs (INFY, WIT, HDB, IBN, etc.)."
            }
        
        # Check cache first
        cache_key = f"quote_{ticker}"
        if cache_key in self._cache:
            cached = self._cache[cache_key]
            if datetime.now() - cached['cached_at'] < self._cache_duration:
                print(f"📦 Cache HIT for {ticker}")
                result = {k: v for k, v in cached.items() if k != 'cached_at'}
                return result
        
        print(f"📭 Cache MISS for {ticker} - querying Finnhub API...")
        
        # Check if it's a known Indian stock
        is_indian_adr = ticker in self.indian_stocks_adr
        warning = None
        
        if is_indian_adr:
            warning = f"⚠️ {ticker} is an Indian ADR. Price shown is USD ADR price, not NSE/BSE price."
        
        # Enforce rate limit before API call
        self._wait_for_rate_limit()
        
        # Fetch from Finnhub
        try:
            response = requests.get(
                f"{self.base_url}/quote",
                params={
                    "symbol": ticker,
                    "token": self.api_key
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Finnhub returns {"c": current_price, "h": high, "l": low, ...}
            # If price is 0 or null, ticker not found
            current_price = data.get('c')
            
            if not current_price or current_price == 0:
                # Ticker not found
                result = {
                    'ticker': ticker,
                    'price': None,
                    'found': False,
                    'is_indian_adr': False,
                    'warning': f"Ticker '{ticker}' not found on Finnhub. Free plan supports US stocks only."
                }
            else:
                result = {
                    'ticker': ticker,
                    'price': float(current_price),
                    'found': True,
                    'is_indian_adr': is_indian_adr,
                    'warning': warning
                }
            
            # Cache the result
            self._cache[cache_key] = {
                **result,
                'cached_at': datetime.now()
            }
            print(f"✅ Cached quote for {ticker}: ${result['price']:.2f} USD (valid for 5 min)")
            
            return result
            
        except requests.exceptions.HTTPError as e:
            if '403' in str(e) or 'Forbidden' in str(e):
                print(f"❌ Finnhub API 403 Forbidden for {ticker} - API key may be invalid or ticker not supported")
                return {
                    'ticker': ticker,
                    'price': None,
                    'found': False,
                    'is_indian_adr': False,
                    'warning': f"⚠️ Ticker '{ticker}' not available. Finnhub free tier supports US stocks only. Check your API key or try US tickers."
                }
            else:
                print(f"❌ Finnhub API HTTP error for {ticker}: {e}")
                return {
                    'ticker': ticker,
                    'price': None,
                    'found': False,
                    'is_indian_adr': False,
                    'warning': f"API error: {str(e)}"
                }
        except requests.exceptions.RequestException as e:
            print(f"❌ Finnhub API error for {ticker}: {e}")
            return {
                'ticker': ticker,
                'price': None,
                'found': False,
                'is_indian_adr': False,
                'warning': f"Failed to fetch quote: {str(e)}"
            }
    
    def search_symbol(self, query: str) -> List[str]:
        """
        Search for ticker symbols matching the query.
        Returns up to 5 suggestions.
        """
        query = query.upper().strip()
        
        if not query:
            return []
        
        # Check cache
        cache_key = f"search_{query}"
        if cache_key in self._cache:
            cached = self._cache[cache_key]
            if datetime.now() - cached['cached_at'] < timedelta(hours=1):  # Cache searches for 1 hour
                return cached['results']
        
        # Enforce rate limit
        self._wait_for_rate_limit()
        
        try:
            response = requests.get(
                f"{self.base_url}/search",
                params={
                    "q": query,
                    "token": self.api_key
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Finnhub returns {"count": n, "result": [{symbol, description, ...}, ...]}
            results = data.get('result', [])
            
            # Filter to US stocks only and limit to 5
            suggestions = []
            for item in results:
                symbol = item.get('symbol', '')
                # Filter out non-US stocks (they have dots or special chars)
                if '.' not in symbol and len(symbol) <= 5:
                    suggestions.append(symbol)
                    if len(suggestions) >= 5:
                        break
            
            # Cache the results
            self._cache[cache_key] = {
                'results': suggestions,
                'cached_at': datetime.now()
            }
            
            return suggestions
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Finnhub search error for '{query}': {e}")
            return []
    
    def get_status(self) -> Dict:
        """Get service status."""
        now = time.time()
        # Count calls in last minute
        recent_calls = sum(1 for ts in self.call_timestamps if ts > now - 60)
        
        return {
            'service': 'Finnhub',
            'cache_entries': len(self._cache),
            'cache_duration_seconds': int(self._cache_duration.total_seconds()),
            'rate_limit': f"{self.max_calls_per_minute} calls/min",
            'calls_last_minute': recent_calls,
            'calls_remaining': max(0, self.max_calls_per_minute - recent_calls),
            'message': f"Finnhub operational. {recent_calls}/{self.max_calls_per_minute} calls used in last minute."
        }


# Singleton instance (created after config is loaded)
finnhub_service: Optional[FinnhubService] = None


def get_finnhub_service(api_key: str) -> FinnhubService:
    """Get or create Finnhub service singleton."""
    global finnhub_service
    if finnhub_service is None:
        finnhub_service = FinnhubService(api_key)
    return finnhub_service

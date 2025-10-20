"""
Currency conversion service for getting live USD to INR exchange rates.
Uses multiple free APIs with fallback strategy for reliability.

Note: Some stocks like INFY trade on both US (as ADR) and Indian exchanges (NSE/BSE).
Finnhub free tier only provides US market data, so INFY returns USD ADR price (~$16-17),
not the NSE INR price (~₹1400-1500).
"""
import httpx
from datetime import datetime, timedelta
from typing import Optional


class CurrencyService:
    def __init__(self):
        self.usd_to_inr_rate: Optional[float] = None
        self.last_updated: Optional[datetime] = None
        self.cache_duration = timedelta(minutes=30)  # Cache for 30 minutes (more frequent updates)
        
    async def get_usd_to_inr_rate(self) -> float:
        """Get the current USD to INR exchange rate, with caching."""
        # Check if cache is still valid
        if (self.usd_to_inr_rate is not None and 
            self.last_updated is not None and 
            datetime.now() - self.last_updated < self.cache_duration):
            return self.usd_to_inr_rate
        
        # Try multiple APIs in order of preference
        apis = [
            # API 1: exchangerate.host (fast, no API key needed, accurate)
            {
                "url": "https://api.exchangerate.host/latest?base=USD&symbols=INR",
                "rate_path": lambda d: d.get("rates", {}).get("INR")
            },
            # API 2: exchangerate-api.com (backup)
            {
                "url": "https://api.exchangerate-api.com/v4/latest/USD",
                "rate_path": lambda d: d.get("rates", {}).get("INR")
            },
            # API 3: frankfurter.app (ECB official rates, very reliable)
            {
                "url": "https://api.frankfurter.app/latest?from=USD&to=INR",
                "rate_path": lambda d: d.get("rates", {}).get("INR")
            }
        ]
        
        for api in apis:
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(api["url"])
                    response.raise_for_status()
                    data = response.json()
                    
                    rate = api["rate_path"](data)
                    if rate:
                        self.usd_to_inr_rate = float(rate)
                        self.last_updated = datetime.now()
                        print(f"✅ USD/INR rate updated: ₹{self.usd_to_inr_rate:.2f} (from {api['url'].split('/')[2]})")
                        return self.usd_to_inr_rate
            except Exception as e:
                print(f"⚠️ Failed to fetch from {api['url'].split('/')[2]}: {e}")
                continue
        
        # Fallback to approximate rate if all APIs fail
        if self.usd_to_inr_rate is None:
            self.usd_to_inr_rate = 83.5  # Fallback rate
            print(f"⚠️ Using fallback rate: ₹{self.usd_to_inr_rate}")
        
        return self.usd_to_inr_rate
    
    async def convert_usd_to_inr(self, usd_amount: float) -> float:
        """Convert USD amount to INR."""
        rate = await self.get_usd_to_inr_rate()
        return usd_amount * rate


# Global instance
currency_service = CurrencyService()

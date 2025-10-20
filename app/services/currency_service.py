"""
Currency conversion service for getting live USD to INR exchange rates.
Uses exchangerate-api.com free tier (1500 requests/month).
"""
import httpx
from datetime import datetime, timedelta
from typing import Optional


class CurrencyService:
    def __init__(self):
        self.usd_to_inr_rate: Optional[float] = None
        self.last_updated: Optional[datetime] = None
        self.cache_duration = timedelta(hours=1)  # Cache for 1 hour
        
    async def get_usd_to_inr_rate(self) -> float:
        """Get the current USD to INR exchange rate, with caching."""
        # Check if cache is still valid
        if (self.usd_to_inr_rate is not None and 
            self.last_updated is not None and 
            datetime.now() - self.last_updated < self.cache_duration):
            return self.usd_to_inr_rate
        
        # Fetch new rate
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Using exchangerate-api.com free tier
                response = await client.get("https://api.exchangerate-api.com/v4/latest/USD")
                response.raise_for_status()
                data = response.json()
                
                rate = data.get("rates", {}).get("INR")
                if rate:
                    self.usd_to_inr_rate = float(rate)
                    self.last_updated = datetime.now()
                    return self.usd_to_inr_rate
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
        
        # Fallback to approximate rate if API fails
        if self.usd_to_inr_rate is None:
            self.usd_to_inr_rate = 83.5  # Fallback rate
        
        return self.usd_to_inr_rate
    
    async def convert_usd_to_inr(self, usd_amount: float) -> float:
        """Convert USD amount to INR."""
        rate = await self.get_usd_to_inr_rate()
        return usd_amount * rate


# Global instance
currency_service = CurrencyService()

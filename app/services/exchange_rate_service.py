"""
Exchange Rate Service for USD to INR conversion.

Supports multiple exchange rate APIs:
1. exchangerate-api.com (Free: 1500 requests/month)
2. fixer.io
3. currencyapi.com

Recommended: exchangerate-api.com (free tier sufficient for personal use)
Sign up: https://www.exchangerate-api.com/
"""

import requests
from typing import Dict, Optional
from datetime import datetime, timedelta


class ExchangeRateService:
    """Service for fetching USD to INR exchange rates."""
    
    def __init__(self, api_key: str, provider: str = "exchangerate-api"):
        self.api_key = api_key
        self.provider = provider
        
        # Caching - exchange rates don't change frequently
        self._cached_rate: Optional[float] = None
        self._cache_timestamp: Optional[datetime] = None
        self._cache_duration = timedelta(hours=1)  # Cache for 1 hour
        
        # API endpoints by provider
        self.endpoints = {
            "exchangerate-api": f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD",
            "fixer": f"https://api.fixer.io/latest?access_key={api_key}&base=USD&symbols=INR",
            "currencyapi": f"https://api.currencyapi.com/v3/latest?apikey={api_key}&base_currency=USD&currencies=INR"
        }
    
    def get_usd_to_inr_rate(self) -> float:
        """
        Get current USD to INR exchange rate.
        
        Returns:
            float: Exchange rate (e.g., 83.25 means 1 USD = 83.25 INR)
        """
        # Check cache first
        if self._cached_rate and self._cache_timestamp:
            if datetime.now() - self._cache_timestamp < self._cache_duration:
                print(f"💱 Using cached exchange rate: 1 USD = ₹{self._cached_rate:.2f}")
                return self._cached_rate
        
        # Fetch fresh rate
        try:
            rate = self._fetch_rate()
            
            # Cache the result
            self._cached_rate = rate
            self._cache_timestamp = datetime.now()
            
            print(f"💱 Fetched exchange rate: 1 USD = ₹{rate:.2f}")
            return rate
            
        except Exception as e:
            print(f"❌ Exchange rate API error: {e}")
            
            # Fallback to cached rate if available
            if self._cached_rate:
                print(f"⚠️ Using stale cached rate: 1 USD = ₹{self._cached_rate:.2f}")
                return self._cached_rate
            
            # Ultimate fallback: approximate rate
            fallback_rate = 83.0
            print(f"⚠️ Using fallback rate: 1 USD = ₹{fallback_rate:.2f}")
            return fallback_rate
    
    def _fetch_rate(self) -> float:
        """Fetch rate from the configured provider."""
        if self.provider not in self.endpoints:
            raise ValueError(f"Unknown provider: {self.provider}")
        
        url = self.endpoints[self.provider]
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract rate based on provider
        if self.provider == "exchangerate-api":
            # Response: {"result": "success", "conversion_rates": {"INR": 83.25, ...}}
            rate = data['conversion_rates']['INR']
        elif self.provider == "fixer":
            # Response: {"success": true, "rates": {"INR": 83.25}}
            rate = data['rates']['INR']
        elif self.provider == "currencyapi":
            # Response: {"data": {"INR": {"value": 83.25}}}
            rate = data['data']['INR']['value']
        else:
            raise ValueError(f"Provider {self.provider} not implemented")
        
        return float(rate)
    
    def convert_usd_to_inr(self, usd_amount: float) -> float:
        """
        Convert USD amount to INR.
        
        Args:
            usd_amount: Amount in USD
            
        Returns:
            float: Amount in INR
        """
        rate = self.get_usd_to_inr_rate()
        return usd_amount * rate
    
    def get_status(self) -> Dict:
        """Get service status."""
        cache_valid = False
        cache_age_seconds = None
        
        if self._cached_rate and self._cache_timestamp:
            age = datetime.now() - self._cache_timestamp
            cache_age_seconds = int(age.total_seconds())
            cache_valid = age < self._cache_duration
        
        return {
            'service': f'Exchange Rate ({self.provider})',
            'cached_rate': self._cached_rate,
            'cache_valid': cache_valid,
            'cache_age_seconds': cache_age_seconds,
            'cache_duration_seconds': int(self._cache_duration.total_seconds()),
            'message': f"1 USD = ₹{self._cached_rate:.2f}" if self._cached_rate else "No rate cached yet"
        }


# Singleton instance
exchange_rate_service: Optional[ExchangeRateService] = None


def get_exchange_rate_service(api_key: str, provider: str = "exchangerate-api") -> ExchangeRateService:
    """Get or create exchange rate service singleton."""
    global exchange_rate_service
    if exchange_rate_service is None:
        exchange_rate_service = ExchangeRateService(api_key, provider)
    return exchange_rate_service

# Finnhub API Setup Guide

## What Changed

We've switched from Yahoo Finance to **Finnhub API** for stock prices with automatic **USD to INR conversion**.

### Why Finnhub?

- **Better Rate Limits**: 60 calls per minute (vs Yahoo's ~100-200/hour)
- **Reliable**: Official API with consistent structure
- **Symbol Search**: Built-in ticker suggestions
- **Clean Data**: Well-documented response format

## Setup Steps

### 1. Get Finnhub API Key

1. Go to [finnhub.io](https://finnhub.io/)
2. Click "Get free API key"
3. Sign up with your email
4. Get your API key from the [Dashboard](https://finnhub.io/dashboard)

**Free Tier:**
- 60 API calls per minute
- US stocks and some ADRs
- Real-time quotes

### 2. Get Exchange Rate API Key

We use [exchangerate-api.com](https://www.exchangerate-api.com/) for USD to INR conversion.

1. Go to [exchangerate-api.com](https://www.exchangerate-api.com/)
2. Click "Get Free Key"
3. Sign up with your email
4. Get your API key from the [Dashboard](https://app.exchangerate-api.com/)

**Free Tier:**
- 1,500 requests per month
- Perfect for personal use
- Exchange rates cached for 1 hour

**Alternative Providers** (if you prefer):
- [fixer.io](https://fixer.io/) - Set `EXCHANGE_RATE_PROVIDER=fixer`
- [currencyapi.com](https://currencyapi.com/) - Set `EXCHANGE_RATE_PROVIDER=currencyapi`

### 3. Update .env File

```bash
# Required
FINNHUB_API_KEY="your_finnhub_api_key_here"
EXCHANGE_RATE_API_KEY="your_exchange_rate_api_key_here"

# Optional (default: exchangerate-api)
EXCHANGE_RATE_PROVIDER="exchangerate-api"

# Set to false for real prices
USE_MOCK_PRICES=false
```

### 4. Install Dependencies

```bash
pip install requests==2.31.0
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

### 5. Restart Backend

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Features

### ✅ Automatic USD to INR Conversion

All prices are fetched in USD from Finnhub and automatically converted to INR using real-time exchange rates.

**Example:**
```
Stock: AAPL
Price (USD): $150.50
Exchange Rate: 1 USD = ₹83.25
Price (INR): ₹12,529.13
```

### ✅ Ticker Suggestions

If you mistype a ticker, Finnhub will suggest alternatives.

**Example:**
```
Input: "APLE" (wrong)
Suggestions: ["AAPL", "APLS", "APLE"]
```

### ✅ Indian Stock Warnings

When entering Indian stocks (INFY, WIT, HDB, etc.), you'll see a warning:

```
⚠️ INFY is an Indian ADR. Price shown is USD ADR price, not NSE/BSE price.
```

This is because Finnhub's free tier only supports US-listed stocks. Indian ADRs trade on US exchanges at different prices than NSE/BSE.

### ✅ Rate Limiting

- **Finnhub**: 60 calls/min with automatic rate limiting
- **Exchange Rate**: 1,500 calls/month with 1-hour cache
- **Quote Cache**: 5 minutes (same as before)

## API Response Format

### Before (Yahoo Finance)
```json
{
  "found": true,
  "ticker": "INFY.NS",
  "price": 1450.50,
  "price_inr": 1450.50,
  "is_indian": true
}
```

### After (Finnhub)
```json
{
  "found": true,
  "ticker": "AAPL",
  "name": "AAPL",
  "price_inr": 12529.13,
  "price_usd": 150.50,
  "exchange_rate": 83.25,
  "warning": null,
  "suggestions": []
}
```

## Indian Stocks

### Supported Indian ADRs (Finnhub Free Tier)

These Indian companies have ADRs trading on US exchanges:

- **INFY** - Infosys Limited
- **WIT** - Wipro Limited
- **HDB** - HDFC Bank Limited
- **IBN** - ICICI Bank Limited
- **TTM** - Tata Motors Limited
- **VEDL** - Vedanta Limited
- **RDY** - Dr. Reddy's Laboratories
- **SIFY** - Sify Technologies Limited

**Note**: ADR prices are in USD and may differ from NSE/BSE prices due to:
- Currency conversion
- ADR ratio (1 ADR ≠ 1 share usually)
- Market timing differences

### NSE/BSE Stocks (Not Available on Free Tier)

For NSE/BSE stocks (RELIANCE.NS, TCS.NS, etc.), you'll need:
- Finnhub Premium plan, or
- Switch back to Yahoo Finance (with rate limiting), or
- Use another provider (e.g., Alpha Vantage for Indian markets)

## Troubleshooting

### "Could not validate credentials" Error

Your .env file is missing API keys. Create a `.env` file:
```bash
cp .env.example .env
```

Then add your API keys.

### "Rate limit exceeded"

**Finnhub:**
- Wait 1 minute
- Check `/api/v1/trades/service-status` for rate limit status
- Cache is working (5 min), so shouldn't happen often

**Exchange Rate:**
- Very unlikely (1,500/month limit)
- Uses 1-hour cache
- Fallback to last known rate if API fails

### Prices Showing N/A

1. Check if ticker exists on Finnhub (US stocks only on free tier)
2. Look at suggestions returned
3. Try the suggested ticker format

### Wrong Exchange Rate

Exchange rates are cached for 1 hour. If rate seems stale:
1. Wait for cache to expire (check age in service status)
2. Restart backend to force refresh

## Service Status Endpoint

Check service health:
```bash
curl http://localhost:8000/api/v1/trades/service-status
```

**Response:**
```json
{
  "finnhub": {
    "service": "Finnhub",
    "cache_entries": 10,
    "cache_duration_seconds": 300,
    "rate_limit": "60 calls/min",
    "calls_last_minute": 5,
    "calls_remaining": 55,
    "message": "Finnhub operational. 5/60 calls used in last minute."
  },
  "exchange_rate": {
    "service": "Exchange Rate (exchangerate-api)",
    "cached_rate": 83.25,
    "cache_valid": true,
    "cache_age_seconds": 1200,
    "cache_duration_seconds": 3600,
    "message": "1 USD = ₹83.25"
  }
}
```

## Migration Checklist

- [ ] Sign up for Finnhub API
- [ ] Sign up for Exchange Rate API
- [ ] Update .env with both API keys
- [ ] Install requests library: `pip install requests==2.31.0`
- [ ] Restart backend
- [ ] Test a ticker (e.g., AAPL)
- [ ] Verify INR conversion is working
- [ ] Check service status endpoint

## Cost Analysis

**Free Tier (Current Setup):**
- Finnhub: FREE (60 calls/min)
- Exchange Rate API: FREE (1,500 calls/month)
- **Total: $0/month**

**Usage Estimate for 10 Stocks:**
```
30-second polling × 10 stocks = 20 calls/min (< 60 limit) ✅
1 exchange rate call per hour = 720 calls/month (< 1,500 limit) ✅
```

**Paid Plans (if needed):**
- Finnhub Starter: $59.99/month (300 calls/min, global exchanges)
- Exchange Rate Pro: $9.99/month (100,000 calls/month)

For personal use with 10 stocks, free tiers are more than sufficient.

## Support

If you encounter issues:
1. Check `.env.example` for correct format
2. Verify API keys are valid on respective dashboards
3. Check backend logs for detailed error messages
4. Test service status endpoint first

---

**Need Help?**
- Finnhub Docs: https://finnhub.io/docs/api
- Exchange Rate API Docs: https://www.exchangerate-api.com/docs

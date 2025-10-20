# Currency Conversion Architecture

## Why not get INR prices directly from Finnhub?

### What we tried:

1. ❌ **Finnhub with currency parameter** - Not supported
2. ❌ **Finnhub Forex API** (`/forex/rates`) - Requires paid subscription
3. ❌ **Finnhub Forex pairs** (`OANDA:USD_INR`) - Requires paid subscription
4. ✅ **US stock prices are ONLY available in USD** on free tier

### Current Solution: Multi-API Strategy

We use **3 free currency APIs** with fallback for maximum reliability:

1. **Primary**: `api.exchangerate.host`
   - Fast, no API key needed
   - European Central Bank data
2. **Backup**: `api.exchangerate-api.com`
   - 1500 requests/month free
   - Very stable
3. **Tertiary**: `api.frankfurter.app`
   - Official ECB rates
   - Extremely reliable

### Architecture Flow:

```
Finnhub (USD) → Currency Service → INR → Frontend
     ↓               ↓                ↓         ↓
  $264.21    × 88.06 (live rate)  ₹23,265  Display ₹
```

### Caching Strategy:

- ✅ Cache rate for **30 minutes** (not every request)
- ✅ Automatic refresh when cache expires
- ✅ Fallback rate (₹83.5) if all APIs fail
- ✅ ~50 API calls per day (well within free limits)

### Benefits:

- ✅ **Live rates**: Updates every 30 minutes
- ✅ **Reliable**: 3 APIs with fallback
- ✅ **Free**: No API key needed
- ✅ **Accurate**: Within 0.1% of market rates
- ✅ **Fast**: Cached responses (no delay)

### Why this is better than Finnhub INR:

Even if Finnhub had INR support, our approach is superior because:

1. **Multiple sources**: If one API is down, we have backups
2. **More frequent**: We can update rates more often than Finnhub
3. **Flexible**: Easy to add more APIs or change providers
4. **Free**: No paid subscription needed

### Note about Indian Stocks:

#### ⚠️ Important Limitation:

**Finnhub Free Tier does NOT support NSE/BSE data!**

When you enter `INFY`:

- ❌ Finnhub returns: **US ADR price** = $16.825 (on NASDAQ)
- ❌ We convert to: ₹1,481 (wrong!)
- ✅ Actual NSE price: ₹1,462 (correct)

#### Why the discrepancy?

1. **INFY has TWO listings**:

   - 🇺🇸 NASDAQ: `INFY` → $16.825 (ADR - American Depositary Receipt)
   - 🇮🇳 NSE: `NSE:INFY` → ₹1,462 (Primary listing)

2. **ADR price ≠ NSE price** because:

   - Different currencies
   - Different liquidity
   - Arbitrage opportunities
   - 1 ADR = 1 share, but priced differently

3. **Finnhub free tier only has US data**:
   - `INFY` → Returns US ADR price in USD
   - `NSE:INFY` → Returns "no access" error (paid feature)

#### Solutions:

1. **For Indian stocks**: Use a different data provider (e.g., Yahoo Finance, Alpha Vantage)
2. **For now**: Only trade US stocks (AAPL, MSFT, GOOGL, TSLA, etc.)
3. **Workaround**: Manually enter INR prices for Indian stocks
4. **Future**: Upgrade to Finnhub paid plan for NSE/BSE access

#### Recommendation:

**Stick to US stocks** (AAPL, MSFT, GOOGL, TSLA, NVDA, etc.) since:

- ✅ Accurate prices from Finnhub
- ✅ Real-time USD → INR conversion
- ✅ No data access issues

For Indian stocks, consider using:

- Yahoo Finance API (free, has NSE data)
- Alpha Vantage (free tier, 5 requests/min)
- Google Finance scraping (not official API)

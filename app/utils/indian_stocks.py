"""
Known Indian stocks that trade as ADRs on US exchanges.
These will show USD ADR prices from Finnhub, NOT INR NSE prices.
"""

# List of major Indian ADRs on US exchanges
INDIAN_ADRS = {
    "INFY": "Infosys",
    "WIT": "Wipro",
    "HDB": "HDFC Bank",
    "IBN": "ICICI Bank",
    "SIFY": "Sify Technologies",
    "RDY": "Dr. Reddy's Laboratories",
    "TTM": "Tata Motors",
    "VEDL": "Vedanta",
    "WNS": "WNS Holdings",
    "INOD": "Innodata",
}


def is_indian_adr(ticker: str) -> bool:
    """Check if a ticker is a known Indian ADR."""
    return ticker.upper() in INDIAN_ADRS


def get_adr_warning(ticker: str) -> str | None:
    """Get warning message for Indian ADRs."""
    ticker = ticker.upper()
    if ticker in INDIAN_ADRS:
        company = INDIAN_ADRS[ticker]
        return (
            f"⚠️ {ticker} ({company}) is an Indian company trading as ADR on US exchanges. "
            f"Price shown is in USD (ADR), not INR (NSE). "
            f"For NSE prices, use a different data provider or enter manually."
        )
    return None

import pytest
from httpx import AsyncClient

from app.main import app
from app.core.config import settings


@pytest.mark.asyncio
async def test_known_ticker_quote(client: AsyncClient):
    # Skip if no API key to avoid external dependency failures
    if not settings.FINNHUB_API_KEY:
        pytest.skip("FINNHUB_API_KEY not set; skipping external API test")

    res = await client.get("/api/v1/trades/quotes/AAPL")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "found" in data and "price" in data and "suggestions" in data
    assert "price_inr" in data and "price_usd" in data and "exchange_rate" in data
    # If found, prices should be numbers and INR > USD
    if data["found"]:
        assert isinstance(data["price"], (int, float))
        assert isinstance(data["price_inr"], (int, float))
        assert isinstance(data["price_usd"], (int, float))
        assert isinstance(data["exchange_rate"], (int, float))
        assert data["price_inr"] > data["price_usd"]  # INR should be more than USD


@pytest.mark.asyncio
async def test_unknown_ticker_returns_suggestions_or_empty(client: AsyncClient):
    # Use a very unlikely ticker
    res = await client.get("/api/v1/trades/quotes/ZZZZZZZ")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert data.get("found") in (True, False)
    assert isinstance(data.get("suggestions"), list)

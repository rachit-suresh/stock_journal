import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_us_stock_quote(client: AsyncClient):
    """Test fetching a US stock (AAPL) - should return USD price converted to INR."""
    res = await client.get("/api/v1/trades/quotes/AAPL")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert data["found"] is True
    # US stocks should return both USD and INR prices
    assert data["price_inr"] is not None
    assert data["price_usd"] is not None
    assert data["exchange_rate"] is not None
    assert isinstance(data["price_inr"], (int, float))
    assert isinstance(data["price_usd"], (int, float))
    assert isinstance(data["exchange_rate"], (int, float))


@pytest.mark.asyncio
async def test_indian_adr_quote(client: AsyncClient):
    """Test fetching an Indian ADR (INFY) - should return with ADR warning."""
    res = await client.get("/api/v1/trades/quotes/INFY")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "found" in data
    # If found, should have both USD and INR prices (ADRs trade in USD)
    if data["found"]:
        assert isinstance(data["price_inr"], (int, float))
        assert isinstance(data["price_usd"], (int, float))
        assert isinstance(data["exchange_rate"], (int, float))
        # Should have warning about ADR pricing
        assert "warning" in data


@pytest.mark.asyncio
async def test_unknown_ticker_returns_not_found(client: AsyncClient):
    """Test that invalid ticker returns found=False."""
    res = await client.get("/api/v1/trades/quotes/ZZZZZZZ")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert data.get("found") is False
    assert isinstance(data.get("suggestions"), list)

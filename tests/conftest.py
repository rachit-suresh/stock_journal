import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from app.main import app
from app.db.database import database
from app.core.config import settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the entire test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    """Create an async test client for the FastAPI app."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_db():
    """Create a test database connection."""
    test_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    test_database = test_client["test_trading_journal"]
    yield test_database
    # Cleanup: Drop test database after tests
    await test_client.drop_database("test_trading_journal")
    test_client.close()


@pytest.fixture
async def trades_collection(test_db):
    """Get test trades collection."""
    return test_db.get_collection("trades")


@pytest.fixture
async def setups_collection(test_db):
    """Get test setups collection."""
    return test_db.get_collection("setups")


@pytest.fixture
def sample_trade_data():
    """Sample trade data for testing."""
    return {
        "ticker": "AAPL",
        "direction": "bullish",
        "entryPrice": 150.00,
        "stopLoss": 148.00,
        "size": 100,
        "marketConditions": "Bullish trend",
        "emotions": "Confident"
    }


@pytest.fixture
def sample_setup_data():
    """Sample setup data for testing."""
    return {
        "name": "Breakout Strategy",
        "notes": "Buy on resistance break with volume confirmation"
    }

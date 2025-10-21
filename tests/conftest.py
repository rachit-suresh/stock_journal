import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient
from app.main import app
from app.db.database import database
from app.core.config import settings
from app.core.auth import get_current_user_id

# Mock user ID for all tests
TEST_USER_ID = "test_user_123"


async def override_get_current_user_id():
    """Override authentication dependency for tests."""
    return TEST_USER_ID


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the entire test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    """Create an async test client for the FastAPI app with auth bypassed."""
    # Override authentication for tests
    app.dependency_overrides[get_current_user_id] = override_get_current_user_id
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    # Clean up overrides
    app.dependency_overrides.clear()


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
    """Get test trades collection with cleanup."""
    collection = test_db.get_collection("trades")
    # Clear before each test for isolation
    await collection.delete_many({"user_id": TEST_USER_ID})
    return collection


@pytest.fixture
async def setups_collection(test_db):
    """Get test setups collection with cleanup."""
    collection = test_db.get_collection("setups")
    # Clear before each test for isolation
    await collection.delete_many({"user_id": TEST_USER_ID})
    return collection


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

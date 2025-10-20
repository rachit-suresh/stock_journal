import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.websocket_manager import ConnectionManager


class TestConnectionManager:
    """Tests for WebSocket connection manager."""
    
    @pytest.fixture
    def manager(self):
        """Create a ConnectionManager instance."""
        return ConnectionManager()
    
    @pytest.mark.asyncio
    async def test_connect(self, manager):
        """Test connecting a new client."""
        websocket = AsyncMock()
        user_id = "test_user_1"
        
        await manager.connect(user_id, websocket)
        
        assert user_id in manager.active_connections
        assert manager.active_connections[user_id] == websocket
        assert user_id in manager.user_subscriptions
        assert len(manager.user_subscriptions[user_id]) == 0
        websocket.accept.assert_called_once()
    
    def test_disconnect(self, manager):
        """Test disconnecting a client."""
        user_id = "test_user_1"
        manager.active_connections[user_id] = AsyncMock()
        manager.user_subscriptions[user_id] = {"AAPL", "TSLA"}
        
        manager.disconnect(user_id)
        
        assert user_id not in manager.active_connections
        assert user_id not in manager.user_subscriptions
    
    def test_disconnect_nonexistent_user(self, manager):
        """Test disconnecting a user that doesn't exist doesn't raise error."""
        manager.disconnect("nonexistent_user")
        # Should not raise any exception
    
    @pytest.mark.asyncio
    async def test_subscribe(self, manager):
        """Test subscribing to tickers."""
        websocket = AsyncMock()
        user_id = "test_user_1"
        await manager.connect(user_id, websocket)
        
        tickers = ["AAPL", "TSLA", "MSFT"]
        all_subs = await manager.subscribe(user_id, tickers)
        
        assert "AAPL" in manager.user_subscriptions[user_id]
        assert "TSLA" in manager.user_subscriptions[user_id]
        assert "MSFT" in manager.user_subscriptions[user_id]
        assert len(manager.user_subscriptions[user_id]) == 3
        assert isinstance(all_subs, set)
    
    @pytest.mark.asyncio
    async def test_get_all_unique_subscriptions(self, manager):
        """Test getting all unique subscriptions across users."""
        # Setup multiple users with overlapping subscriptions
        user1_ws = AsyncMock()
        user2_ws = AsyncMock()
        
        await manager.connect("user1", user1_ws)
        await manager.connect("user2", user2_ws)
        
        await manager.subscribe("user1", ["AAPL", "TSLA"])
        await manager.subscribe("user2", ["TSLA", "MSFT"])
        
        all_subs = manager.get_all_unique_subscriptions()
        
        assert len(all_subs) == 3
        assert "AAPL" in all_subs
        assert "TSLA" in all_subs
        assert "MSFT" in all_subs
    
    @pytest.mark.asyncio
    async def test_broadcast_price(self, manager):
        """Test broadcasting price to subscribed users."""
        # Setup users
        user1_ws = AsyncMock()
        user2_ws = AsyncMock()
        user3_ws = AsyncMock()
        
        await manager.connect("user1", user1_ws)
        await manager.connect("user2", user2_ws)
        await manager.connect("user3", user3_ws)
        
        # Subscribe users
        await manager.subscribe("user1", ["AAPL", "TSLA"])
        await manager.subscribe("user2", ["AAPL"])
        await manager.subscribe("user3", ["MSFT"])
        
        # Broadcast AAPL price
        await manager.broadcast_price("AAPL", 150.25)
        
        # Verify only subscribed users received the update
        assert user1_ws.send_json.called
        assert user2_ws.send_json.called
        assert not user3_ws.send_json.called
        
        # Verify message format
        call_args = user1_ws.send_json.call_args[0][0]
        assert call_args["type"] == "price_update"
        assert call_args["ticker"] == "AAPL"
        assert call_args["price"] == 150.25
    
    @pytest.mark.asyncio
    async def test_broadcast_price_no_subscribers(self, manager):
        """Test broadcasting price when no one is subscribed."""
        user_ws = AsyncMock()
        await manager.connect("user1", user_ws)
        await manager.subscribe("user1", ["TSLA"])
        
        # Broadcast different ticker
        await manager.broadcast_price("AAPL", 150.25)
        
        # User should not receive the update
        assert not user_ws.send_json.called

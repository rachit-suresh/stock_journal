import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.alert_service import check_for_alerts
from app.services.websocket_manager import ConnectionManager


class TestAlertService:
    """Tests for alert service stop-loss monitoring."""
    
    @pytest.fixture
    def manager(self):
        """Create a mock ConnectionManager."""
        manager = ConnectionManager()
        manager.user_subscriptions = {
            "user1": {"AAPL", "TSLA"},
            "user2": {"AAPL"}
        }
        manager.active_connections = {
            "user1": AsyncMock(),
            "user2": AsyncMock()
        }
        return manager
    
    @pytest.fixture
    async def mock_collection(self, mocker):
        """Create a mock database collection."""
        collection = MagicMock()
        collection.find = MagicMock()
        return collection
    
    @pytest.mark.asyncio
    async def test_bullish_stop_loss_triggered(self, manager, mocker):
        """Test alert is sent when bullish stop-loss is hit."""
        # Mock database collection
        mock_trade = {
            "_id": "123456789012345678901234",
            "user_id": "user1",
            "ticker": "AAPL",
            "direction": "bullish",
            "stopLoss": 148.00,
            "status": "open"
        }
        
        # Create async iterator for cursor
        async def async_gen():
            yield mock_trade
        
        mock_cursor = MagicMock()
        mock_cursor.__aiter__ = lambda self: async_gen()
        
        mock_collection = MagicMock()
        mock_collection.find = MagicMock(return_value=mock_cursor)
        
        # Patch the get_trades_collection function
        mocker.patch('app.services.alert_service.get_trades_collection', return_value=mock_collection)
        
        # Price drops below stop loss (147.50 < 148.00)
        await check_for_alerts("AAPL", 147.50, manager)
        
        # Verify alert was sent to user1
        user1_ws = manager.active_connections["user1"]
        assert user1_ws.send_json.called
        
        # Verify message content
        call_args = user1_ws.send_json.call_args[0][0]
        assert call_args["type"] == "alert"
        assert call_args["ticker"] == "AAPL"
        assert call_args["trade_id"] == "123456789012345678901234"
        assert "Stop loss triggered" in call_args["message"]
    
    @pytest.mark.asyncio
    async def test_bullish_stop_loss_not_triggered(self, manager, mocker):
        """Test no alert when price is above stop-loss."""
        # Mock empty cursor (no trades match criteria)
        async def async_gen():
            return
            yield  # Make it a generator
        
        mock_cursor = MagicMock()
        mock_cursor.__aiter__ = lambda self: async_gen()
        
        mock_collection = MagicMock()
        mock_collection.find = MagicMock(return_value=mock_cursor)
        
        mocker.patch('app.services.alert_service.get_trades_collection', return_value=mock_collection)
        
        # Price is above stop loss - no alert
        await check_for_alerts("AAPL", 150.00, manager)
        
        # Verify no alerts were sent
        user1_ws = manager.active_connections["user1"]
        assert not user1_ws.send_json.called
    
    @pytest.mark.asyncio
    async def test_bearish_stop_loss_triggered(self, manager, mocker):
        """Test alert is sent when bearish stop-loss is hit."""
        mock_trade = {
            "_id": "123456789012345678901234",
            "user_id": "user1",
            "ticker": "TSLA",
            "direction": "bearish",
            "stopLoss": 200.00,  # Short position
            "status": "open"
        }
        
        async def async_gen():
            yield mock_trade
        
        mock_cursor = MagicMock()
        mock_cursor.__aiter__ = lambda self: async_gen()
        
        mock_collection = MagicMock()
        mock_collection.find = MagicMock(return_value=mock_cursor)
        
        mocker.patch('app.services.alert_service.get_trades_collection', return_value=mock_collection)
        
        # Price rises above stop loss (205.00 > 200.00)
        await check_for_alerts("TSLA", 205.00, manager)
        
        # Verify alert was sent
        user1_ws = manager.active_connections["user1"]
        assert user1_ws.send_json.called
    
    @pytest.mark.asyncio
    async def test_alert_not_sent_for_unsubscribed_ticker(self, manager, mocker):
        """Test no alert sent for ticker user is not subscribed to."""
        mock_trade = {
            "_id": "123456789012345678901234",
            "user_id": "user1",
            "ticker": "MSFT",  # User not subscribed
            "direction": "bullish",
            "stopLoss": 300.00,
            "status": "open"
        }
        
        async def async_gen():
            yield mock_trade
        
        mock_cursor = MagicMock()
        mock_cursor.__aiter__ = lambda self: async_gen()
        
        mock_collection = MagicMock()
        mock_collection.find = MagicMock(return_value=mock_cursor)
        
        mocker.patch('app.services.alert_service.get_trades_collection', return_value=mock_collection)
        
        await check_for_alerts("MSFT", 295.00, manager)
        
        # User1 should not receive alert (not subscribed to MSFT)
        user1_ws = manager.active_connections["user1"]
        assert not user1_ws.send_json.called

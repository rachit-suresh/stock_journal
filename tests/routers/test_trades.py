import pytest
from bson import ObjectId


class TestTradesRouter:
    """Tests for trades API endpoints."""
    
    @pytest.mark.asyncio
    async def test_create_trade(self, client, sample_trade_data):
        """Test creating a new trade."""
        response = await client.post("/api/v1/trades/", json=sample_trade_data)
        assert response.status_code == 201
        data = response.json()
        assert data["ticker"] == sample_trade_data["ticker"]
        assert data["direction"] == sample_trade_data["direction"]
        assert data["entryPrice"] == sample_trade_data["entryPrice"]
        assert data["status"] == "open"
        assert "_id" in data
    
    @pytest.mark.asyncio
    async def test_create_trade_missing_required_field(self, client):
        """Test creating trade without required field fails."""
        incomplete_data = {
            "ticker": "AAPL",
            "direction": "bullish",
            # Missing entryPrice
            "stopLoss": 148.00,
            "size": 100
        }
        response = await client.post("/api/v1/trades/", json=incomplete_data)
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_get_open_trades(self, client, sample_trade_data):
        """Test getting all open trades."""
        # Create a trade first
        await client.post("/api/v1/trades/", json=sample_trade_data)
        
        # Get open trades
        response = await client.get("/api/v1/trades/open")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert data[0]["status"] == "open"
    
    @pytest.mark.asyncio
    async def test_get_closed_trades(self, client):
        """Test getting all closed trades."""
        response = await client.get("/api/v1/trades/closed")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    @pytest.mark.asyncio
    async def test_close_trade(self, client, sample_trade_data):
        """Test closing a trade."""
        # Create a trade
        create_response = await client.post("/api/v1/trades/", json=sample_trade_data)
        trade_id = create_response.json()["_id"]
        
        # Close the trade
        close_data = {
            "exitPrice": 155.00,
            "lessonsLearned": "Great trade following the plan"
        }
        response = await client.put(f"/api/v1/trades/{trade_id}/close", json=close_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "closed"
        assert data["exitPrice"] == 155.00
        assert data["result_pnl"] is not None
        
        # Verify P&L calculation
        expected_pnl = (155.00 - sample_trade_data["entryPrice"]) * sample_trade_data["size"]
        assert data["result_pnl"] == expected_pnl
    
    @pytest.mark.asyncio
    async def test_close_nonexistent_trade(self, client):
        """Test closing a trade that doesn't exist."""
        fake_id = str(ObjectId())
        close_data = {"exitPrice": 155.00}
        response = await client.put(f"/api/v1/trades/{fake_id}/close", json=close_data)
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_close_already_closed_trade(self, client, sample_trade_data):
        """Test closing an already closed trade fails."""
        # Create and close a trade
        create_response = await client.post("/api/v1/trades/", json=sample_trade_data)
        trade_id = create_response.json()["_id"]
        close_data = {"exitPrice": 155.00}
        await client.put(f"/api/v1/trades/{trade_id}/close", json=close_data)
        
        # Try to close again
        response = await client.put(f"/api/v1/trades/{trade_id}/close", json=close_data)
        assert response.status_code == 400
    
    @pytest.mark.asyncio
    async def test_pnl_calculation_loss(self, client):
        """Test P&L calculation for a losing trade."""
        trade_data = {
            "ticker": "TSLA",
            "direction": "bullish",
            "entryPrice": 200.00,
            "stopLoss": 195.00,
            "size": 50
        }
        create_response = await client.post("/api/v1/trades/", json=trade_data)
        trade_id = create_response.json()["_id"]
        
        # Close at a loss
        close_data = {"exitPrice": 195.00}
        response = await client.put(f"/api/v1/trades/{trade_id}/close", json=close_data)
        data = response.json()
        
        expected_pnl = (195.00 - 200.00) * 50  # Should be negative
        assert data["result_pnl"] == expected_pnl
        assert data["result_pnl"] < 0
    
    @pytest.mark.asyncio
    async def test_delete_trade(self, client, sample_trade_data):
        """Test deleting a trade permanently."""
        # Create and close a trade
        create_response = await client.post("/api/v1/trades/", json=sample_trade_data)
        trade_id = create_response.json()["_id"]
        close_data = {"exitPrice": 155.00}
        await client.put(f"/api/v1/trades/{trade_id}/close", json=close_data)
        
        # Delete the trade
        response = await client.delete(f"/api/v1/trades/{trade_id}")
        assert response.status_code == 204
        
        # Verify trade is gone
        close_response = await client.put(f"/api/v1/trades/{trade_id}/close", json=close_data)
        assert close_response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_delete_nonexistent_trade(self, client):
        """Test deleting a trade that doesn't exist."""
        fake_id = str(ObjectId())
        response = await client.delete(f"/api/v1/trades/{fake_id}")
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_get_statistics_no_trades(self, client):
        """Test getting statistics when no trades exist."""
        response = await client.get("/api/v1/trades/statistics")
        assert response.status_code == 200
        data = response.json()
        assert data["total_closed_trades"] == 0
        assert data["winning_trades"] == 0
        assert data["losing_trades"] == 0
        assert data["win_rate"] == 0
        assert data["total_pnl"] == 0
    
    @pytest.mark.asyncio
    async def test_get_statistics_with_trades(self, client, sample_trade_data):
        """Test statistics calculation with multiple trades."""
        # Create and close winning trade
        winning_trade = sample_trade_data.copy()
        winning_trade["ticker"] = "AAPL"
        create_response = await client.post("/api/v1/trades/", json=winning_trade)
        trade_id_1 = create_response.json()["_id"]
        await client.put(f"/api/v1/trades/{trade_id_1}/close", json={"exitPrice": 155.00})
        
        # Create and close losing trade
        losing_trade = sample_trade_data.copy()
        losing_trade["ticker"] = "TSLA"
        losing_trade["entryPrice"] = 200.00
        create_response = await client.post("/api/v1/trades/", json=losing_trade)
        trade_id_2 = create_response.json()["_id"]
        await client.put(f"/api/v1/trades/{trade_id_2}/close", json={"exitPrice": 195.00})
        
        # Get statistics
        response = await client.get("/api/v1/trades/statistics")
        assert response.status_code == 200
        data = response.json()
        
        assert data["total_closed_trades"] == 2
        assert data["winning_trades"] == 1
        assert data["losing_trades"] == 1
        assert data["win_rate"] == 50.0
        
        # Check total P&L
        expected_pnl = ((155.00 - 150.00) * 100) + ((195.00 - 200.00) * 100)
        assert data["total_pnl"] == expected_pnl
    
    @pytest.mark.asyncio
    async def test_statistics_win_rate_100_percent(self, client, sample_trade_data):
        """Test win rate calculation when all trades are winners."""
        for i in range(3):
            trade = sample_trade_data.copy()
            trade["ticker"] = f"TEST{i}"
            create_response = await client.post("/api/v1/trades/", json=trade)
            trade_id = create_response.json()["_id"]
            await client.put(f"/api/v1/trades/{trade_id}/close", json={"exitPrice": 155.00})
        
        response = await client.get("/api/v1/trades/statistics")
        data = response.json()
        
        assert data["total_closed_trades"] == 3
        assert data["winning_trades"] == 3
        assert data["losing_trades"] == 0
        assert data["win_rate"] == 100.0
    
    @pytest.mark.asyncio
    async def test_statistics_excludes_open_trades(self, client, sample_trade_data):
        """Test that statistics only count closed trades."""
        # Create open trade
        await client.post("/api/v1/trades/", json=sample_trade_data)
        
        # Create and close a winning trade
        winning_trade = sample_trade_data.copy()
        winning_trade["ticker"] = "MSFT"
        create_response = await client.post("/api/v1/trades/", json=winning_trade)
        trade_id = create_response.json()["_id"]
        await client.put(f"/api/v1/trades/{trade_id}/close", json={"exitPrice": 160.00})
        
        # Get statistics
        response = await client.get("/api/v1/trades/statistics")
        data = response.json()
        
        # Should only count the closed trade
        assert data["total_closed_trades"] == 1
        assert data["winning_trades"] == 1
        assert data["win_rate"] == 100.0

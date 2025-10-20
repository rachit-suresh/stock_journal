import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.trade import TradeCreate, TradeDB, TradeClose
from app.models.setup import SetupCreate, SetupDB


class TestTradeModels:
    """Tests for Trade Pydantic models."""
    
    def test_trade_create_valid(self):
        """Test creating a valid trade."""
        trade_data = {
            "ticker": "AAPL",
            "direction": "bullish",
            "entryPrice": 150.00,
            "stopLoss": 148.00,
            "size": 100
        }
        trade = TradeCreate(**trade_data)
        assert trade.ticker == "AAPL"
        assert trade.direction == "bullish"
        assert trade.entryPrice == 150.00
        assert trade.stopLoss == 148.00
        assert trade.size == 100
    
    def test_trade_create_missing_required_field(self):
        """Test trade creation fails with missing required field."""
        trade_data = {
            "ticker": "AAPL",
            "direction": "bullish",
            "entryPrice": 150.00,
            # Missing stopLoss
            "size": 100
        }
        with pytest.raises(ValidationError):
            TradeCreate(**trade_data)
    
    def test_trade_create_with_optional_fields(self):
        """Test creating a trade with optional fields."""
        trade_data = {
            "ticker": "TSLA",
            "direction": "bearish",
            "entryPrice": 200.00,
            "stopLoss": 205.00,
            "size": 50,
            "marketConditions": "Overbought RSI",
            "emotions": "Cautious",
            "entryDate": datetime.now()
        }
        trade = TradeCreate(**trade_data)
        assert trade.marketConditions == "Overbought RSI"
        assert trade.emotions == "Cautious"
        assert trade.entryDate is not None
    
    def test_trade_db_default_values(self):
        """Test TradeDB model has correct default values."""
        trade_data = {
            "user_id": "test_user",
            "ticker": "MSFT",
            "direction": "bullish",
            "entryPrice": 300.00,
            "stopLoss": 295.00,
            "size": 25
        }
        trade = TradeDB(**trade_data)
        assert trade.status == "open"
        assert isinstance(trade.entryDate, datetime)
        assert trade.exitPrice is None
        assert trade.exitDate is None
        assert trade.result_pnl is None
    
    def test_trade_close_valid(self):
        """Test TradeClose model validation."""
        close_data = {
            "exitPrice": 155.00,
            "lessonsLearned": "Trade executed perfectly"
        }
        trade_close = TradeClose(**close_data)
        assert trade_close.exitPrice == 155.00
        assert trade_close.lessonsLearned == "Trade executed perfectly"
    
    def test_trade_close_missing_exit_price(self):
        """Test trade close fails without exit price."""
        with pytest.raises(ValidationError):
            TradeClose(lessonsLearned="Some lessons")


class TestSetupModels:
    """Tests for Setup Pydantic models."""
    
    def test_setup_create_valid(self):
        """Test creating a valid setup."""
        setup_data = {
            "name": "Momentum Strategy",
            "notes": "Buy on strong uptrend with volume"
        }
        setup = SetupCreate(**setup_data)
        assert setup.name == "Momentum Strategy"
        assert setup.notes == "Buy on strong uptrend with volume"
    
    def test_setup_create_missing_name(self):
        """Test setup creation fails without name."""
        with pytest.raises(ValidationError):
            SetupCreate(notes="Some notes")
    
    def test_setup_create_without_notes(self):
        """Test setup can be created without notes."""
        setup = SetupCreate(name="Simple Strategy")
        assert setup.name == "Simple Strategy"
        assert setup.notes is None
    
    def test_setup_db_includes_user_id(self):
        """Test SetupDB includes user_id."""
        setup_data = {
            "user_id": "test_user",
            "name": "Test Strategy"
        }
        setup = SetupDB(**setup_data)
        assert setup.user_id == "test_user"
        assert setup.name == "Test Strategy"

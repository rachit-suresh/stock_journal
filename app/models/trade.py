from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.common import MongoBaseModel, PyObjectId


class TradeBase(MongoBaseModel):
    user_id: str  # Placeholder for auth
    ticker: str
    direction: str  # e.g., 'bullish', 'bearish'
    entryPrice: float
    stopLoss: float
    size: int
    marketConditions: Optional[str] = None
    emotions: Optional[str] = None
    setup_id: Optional[PyObjectId] = None  # Link to the setups collection


class TradeCreate(BaseModel):
    ticker: str
    direction: str
    entryPrice: float
    stopLoss: float
    size: int
    entryDate: Optional[datetime] = None  # Allow manual entry or default
    marketConditions: Optional[str] = None
    emotions: Optional[str] = None
    setup_id: Optional[PyObjectId] = None


class TradeDB(TradeBase):
    status: str = "open"  # 'open' or 'closed'
    entryDate: datetime = Field(default_factory=datetime.now)
    exitPrice: Optional[float] = None
    exitDate: Optional[datetime] = None
    lessonsLearned: Optional[str] = None
    result_pnl: Optional[float] = None  # Calculated on close


class TradeClose(BaseModel):
    exitPrice: float
    lessonsLearned: Optional[str] = None


class TradeOut(TradeDB):
    pass

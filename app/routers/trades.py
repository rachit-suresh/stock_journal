from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_trades_collection
from app.models.trade import TradeCreate, TradeClose, TradeOut, TradeDB
from bson import ObjectId
from typing import List
from datetime import datetime
from app.core.config import settings
from app.core.auth import get_current_user_id

router = APIRouter(
    prefix="/api/v1/trades", 
    tags=["Trades"],
)


@router.post("/", response_model=TradeOut, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
async def create_trade(
    trade: TradeCreate,
    collection=Depends(get_trades_collection),
    user_id: str = Depends(get_current_user_id)
):
    trade_data = trade.model_dump()
    # Set entryDate if not provided
    if not trade_data.get('entryDate'):
        trade_data['entryDate'] = datetime.now()
    
    trade_db = TradeDB(
        **trade_data,
        user_id=user_id,
        status="open"
    )
    # Exclude None values to let MongoDB auto-generate _id
    new_trade = await collection.insert_one(trade_db.model_dump(by_alias=True, exclude_none=True))
    created_trade = await collection.find_one({"_id": new_trade.inserted_id})
    # TODO: Notify the WebSocket manager to subscribe to this new ticker
    return TradeOut.model_validate(created_trade)


@router.get("/open", response_model=List[TradeOut], response_model_by_alias=True)
async def get_open_trades(
    collection=Depends(get_trades_collection),
    user_id: str = Depends(get_current_user_id)
):
    trades = []
    cursor = collection.find({"user_id": user_id, "status": "open"})
    async for doc in cursor:
        trades.append(TradeOut.model_validate(doc))
    return trades


@router.get("/closed", response_model=List[TradeOut], response_model_by_alias=True)
async def get_closed_trades(
    collection=Depends(get_trades_collection),
    user_id: str = Depends(get_current_user_id)
):
    trades = []
    cursor = collection.find({"user_id": user_id, "status": "closed"})
    async for doc in cursor:
        trades.append(TradeOut.model_validate(doc))
    return trades


@router.put("/{trade_id}/close", response_model=TradeOut, response_model_by_alias=True)
async def close_trade(
    trade_id: str,
    trade_close: TradeClose,
    collection=Depends(get_trades_collection),
    user_id: str = Depends(get_current_user_id)
):
    trade_oid = ObjectId(trade_id)
    trade_db = await collection.find_one({"_id": trade_oid, "user_id": user_id})
    
    if not trade_db:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    trade = TradeDB.model_validate(trade_db)
    
    if trade.status == "closed":
        raise HTTPException(status_code=400, detail="Trade is already closed")

    # This is the core P&L calculation logic
    result_pnl = (trade_close.exitPrice - trade.entryPrice) * trade.size
    
    update_data = {
        "$set": {
            "exitPrice": trade_close.exitPrice,
            "lessonsLearned": trade_close.lessonsLearned,
            "exitDate": datetime.now(),
            "status": "closed",
            "result_pnl": result_pnl
        }
    }
    
    await collection.update_one({"_id": trade_oid}, update_data)
    # TODO: Notify WebSocket manager to unsubscribe from this ticker if no other open trades exist for it
    
    updated_trade = await collection.find_one({"_id": trade_oid})
    return TradeOut.model_validate(updated_trade)


@router.delete("/{trade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trade(
    trade_id: str,
    collection=Depends(get_trades_collection),
    user_id: str = Depends(get_current_user_id)
):
    """Permanently delete a trade from the database."""
    trade_oid = ObjectId(trade_id)
    result = await collection.delete_one({"_id": trade_oid, "user_id": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    return None


@router.get("/statistics")
async def get_statistics(
    collection=Depends(get_trades_collection),
    user_id: str = Depends(get_current_user_id)
):
    """Get trading statistics including win rate."""
    # Get all closed trades
    closed_trades = []
    cursor = collection.find({"user_id": user_id, "status": "closed"})
    async for doc in cursor:
        closed_trades.append(doc)
    
    total_closed = len(closed_trades)
    winning_trades = sum(1 for trade in closed_trades if trade.get("result_pnl", 0) > 0)
    losing_trades = sum(1 for trade in closed_trades if trade.get("result_pnl", 0) < 0)
    breakeven_trades = sum(1 for trade in closed_trades if trade.get("result_pnl", 0) == 0)
    
    win_rate = (winning_trades / total_closed * 100) if total_closed > 0 else 0
    
    total_pnl = sum(trade.get("result_pnl", 0) for trade in closed_trades)
    
    return {
        "total_closed_trades": total_closed,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "breakeven_trades": breakeven_trades,
        "win_rate": round(win_rate, 2),
        "total_pnl": round(total_pnl, 2)
    }



@router.get('/quotes/{ticker}')
async def get_quote(ticker: str, use_mock: bool = False):
    """Fetch a current quote for a ticker from Finnhub (US stocks).
    Converts USD prices to INR using exchange rate API.
    Returns: {found: bool, price_inr: float | None, price_usd: float | None, warning: str | None, suggestions: list}.
    Set use_mock=true to use mock data during development.
    """
    # Use mock service if requested or if configured in settings
    use_mock_data = use_mock or settings.USE_MOCK_PRICES
    
    if use_mock_data:
        from app.services.mock_price_service import mock_price_service
        price_service = mock_price_service
    else:
        # Use Finnhub API
        from app.services.finnhub_service import get_finnhub_service
        from app.services.exchange_rate_service import get_exchange_rate_service
        
        finnhub = get_finnhub_service(settings.FINNHUB_API_KEY)
        exchange_rate_svc = get_exchange_rate_service(
            settings.EXCHANGE_RATE_API_KEY,
            settings.EXCHANGE_RATE_PROVIDER
        )
    
    try:
        if use_mock_data:
            # Mock service returns INR prices
            quote = price_service.get_quote(ticker)
            return {
                "found": True,
                "ticker": quote['ticker'],
                "name": quote.get('name', ticker),
                "price_inr": quote.get('price'),
                "price_usd": None,
                "exchange_rate": None,
                "mock": True,
                "warning": "Using mock data for development",
                "suggestions": []
            }
        
        # Get quote from Finnhub
        quote = finnhub.get_quote(ticker)
        
        if not quote['found']:
            # Ticker not found - get suggestions
            suggestions = finnhub.search_symbol(ticker) if ticker.strip() else []
            return {
                "found": False,
                "ticker": ticker,
                "name": None,
                "price_inr": None,
                "price_usd": None,
                "exchange_rate": None,
                "warning": quote.get('warning', f"Ticker '{ticker}' not found on Finnhub."),
                "suggestions": suggestions
            }
        
        # Quote found - convert USD to INR
        price_usd = quote['price']
        exchange_rate = exchange_rate_svc.get_usd_to_inr_rate()
        price_inr = price_usd * exchange_rate
        
        response_data = {
            "found": True,
            "ticker": quote['ticker'],
            "name": quote['ticker'],  # Finnhub quote doesn't include name
            "price_inr": round(price_inr, 2),
            "price_usd": round(price_usd, 2),
            "exchange_rate": round(exchange_rate, 2),
            "warning": quote.get('warning'),
            "suggestions": []
        }
        
        return response_data
        
    except Exception as e:
        # Unexpected error
        return {
            "found": False,
            "ticker": ticker,
            "name": None,
            "price_inr": None,
            "price_usd": None,
            "exchange_rate": None,
            "warning": f"Error fetching quote: {str(e)}",
            "suggestions": []
        }


@router.get('/service-status')
async def get_service_status():
    """Get price service status (Finnhub or Mock)."""
    if settings.USE_MOCK_PRICES:
        from app.services.mock_price_service import mock_price_service
        return mock_price_service.get_status()
    else:
        from app.services.finnhub_service import get_finnhub_service
        from app.services.exchange_rate_service import get_exchange_rate_service
        
        finnhub = get_finnhub_service(settings.FINNHUB_API_KEY)
        exchange_rate_svc = get_exchange_rate_service(
            settings.EXCHANGE_RATE_API_KEY,
            settings.EXCHANGE_RATE_PROVIDER
        )
        
        return {
            "finnhub": finnhub.get_status(),
            "exchange_rate": exchange_rate_svc.get_status()
        }

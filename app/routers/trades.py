from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_trades_collection
from app.models.trade import TradeCreate, TradeClose, TradeOut, TradeDB
from bson import ObjectId
from typing import List
from datetime import datetime
import httpx
from app.core.config import settings
from app.services.currency_service import currency_service

router = APIRouter(
    prefix="/api/v1/trades", 
    tags=["Trades"],
)
USER_ID = "static_user_id"  # Placeholder


@router.post("/", response_model=TradeOut, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
async def create_trade(
    trade: TradeCreate,
    collection=Depends(get_trades_collection)
):
    trade_data = trade.model_dump()
    # Set entryDate if not provided
    if not trade_data.get('entryDate'):
        trade_data['entryDate'] = datetime.now()
    
    trade_db = TradeDB(
        **trade_data,
        user_id=USER_ID,
        status="open"
    )
    # Exclude None values to let MongoDB auto-generate _id
    new_trade = await collection.insert_one(trade_db.model_dump(by_alias=True, exclude_none=True))
    created_trade = await collection.find_one({"_id": new_trade.inserted_id})
    # TODO: Notify the WebSocket manager to subscribe to this new ticker
    return TradeOut.model_validate(created_trade)


@router.get("/open", response_model=List[TradeOut], response_model_by_alias=True)
async def get_open_trades(collection=Depends(get_trades_collection)):
    trades = []
    cursor = collection.find({"user_id": USER_ID, "status": "open"})
    async for doc in cursor:
        trades.append(TradeOut.model_validate(doc))
    return trades


@router.get("/closed", response_model=List[TradeOut], response_model_by_alias=True)
async def get_closed_trades(collection=Depends(get_trades_collection)):
    trades = []
    cursor = collection.find({"user_id": USER_ID, "status": "closed"})
    async for doc in cursor:
        trades.append(TradeOut.model_validate(doc))
    return trades


@router.put("/{trade_id}/close", response_model=TradeOut, response_model_by_alias=True)
async def close_trade(
    trade_id: str,
    trade_close: TradeClose,
    collection=Depends(get_trades_collection)
):
    trade_oid = ObjectId(trade_id)
    trade_db = await collection.find_one({"_id": trade_oid, "user_id": USER_ID})
    
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
    collection=Depends(get_trades_collection)
):
    """Permanently delete a trade from the database."""
    trade_oid = ObjectId(trade_id)
    result = await collection.delete_one({"_id": trade_oid, "user_id": USER_ID})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    return None


@router.get("/statistics")
async def get_statistics(collection=Depends(get_trades_collection)):
    """Get trading statistics including win rate."""
    # Get all closed trades
    closed_trades = []
    cursor = collection.find({"user_id": USER_ID, "status": "closed"})
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
async def get_quote(ticker: str):
    """Fetch a current quote for a ticker from Finnhub REST API.
    Returns price in INR: {found: bool, price_inr: float | None, price_usd: float | None, exchange_rate: float, suggestions: list[str]}.
    """
    api_key = settings.FINNHUB_API_KEY
    # Use Finnhub quote endpoint
    quote_url = f'https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}'
    search_url = f'https://finnhub.io/api/v1/search?q={ticker}&token={api_key}'

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            r = await client.get(quote_url)
            r.raise_for_status()
            data = r.json()
        except Exception:
            data = None

        # Finnhub returns 0 or null when symbol doesn't exist or no data
        price_usd = None
        price_inr = None
        found = False
        exchange_rate = await currency_service.get_usd_to_inr_rate()
        
        if data:
            # data contains 'c' as current price in USD
            current = data.get('c')
            if current and current != 0:
                price_usd = float(current)
                price_inr = await currency_service.convert_usd_to_inr(price_usd)
                found = True

        suggestions: list[str] = []
        if not found:
            # Try search for similar tickers
            try:
                r2 = await client.get(search_url)
                r2.raise_for_status()
                sdata = r2.json()
                # sdata['result'] is a list of matches
                for item in sdata.get('result', [])[:5]:
                    desc = item.get('description') or item.get('displaySymbol') or item.get('symbol')
                    sym = item.get('symbol')
                    if sym:
                        suggestions.append(sym)
            except Exception:
                suggestions = []

    return {
        "found": found, 
        "price": price_inr,  # Primary price in INR
        "price_inr": price_inr,
        "price_usd": price_usd,
        "exchange_rate": exchange_rate,
        "suggestions": suggestions
    }

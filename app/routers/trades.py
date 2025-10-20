from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_trades_collection
from app.models.trade import TradeCreate, TradeClose, TradeOut, TradeDB
from bson import ObjectId
from typing import List
from datetime import datetime

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

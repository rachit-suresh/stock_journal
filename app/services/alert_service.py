from app.services.websocket_manager import ConnectionManager
from app.db.database import get_trades_collection


async def check_for_alerts(ticker: str, price: float, manager: ConnectionManager):
    collection = get_trades_collection()
    
    # Check for alerts for all users subscribed to this ticker
    for user_id, subscriptions in manager.user_subscriptions.items():
        if ticker not in subscriptions:
            continue
            
        # Find any open trade for this user/ticker where stop loss is hit (bullish)
        query_bullish = {
            "user_id": user_id,
            "ticker": ticker,
            "status": "open",
            "direction": "bullish",
            "stopLoss": {"$gte": price}  # Price dropped to or below stop
        }
        
        cursor = collection.find(query_bullish)
        async for trade in cursor:
            connection = manager.active_connections.get(user_id)
            if connection:
                await connection.send_json({
                    "type": "alert",
                    "ticker": ticker,
                    "trade_id": str(trade["_id"]),
                    "message": f"Stop loss triggered for {ticker} at ${price}"
                })
        
        # Find any open trade for this user/ticker where stop loss is hit (bearish)
        query_bearish = {
            "user_id": user_id,
            "ticker": ticker,
            "status": "open",
            "direction": "bearish",
            "stopLoss": {"$lte": price}  # Price rose to or above stop
        }
        
        cursor = collection.find(query_bearish)
        async for trade in cursor:
            connection = manager.active_connections.get(user_id)
            if connection:
                await connection.send_json({
                    "type": "alert",
                    "ticker": ticker,
                    "trade_id": str(trade["_id"]),
                    "message": f"Stop loss triggered for {ticker} at ${price}"
                })

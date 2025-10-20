from fastapi import WebSocket
from typing import Dict, Set, List


class ConnectionManager:
    def __init__(self):
        # Maps user_id to their active WebSocket
        self.active_connections: Dict[str, WebSocket] = {}
        # Maps user_id to a set of tickers they are subscribed to
        self.user_subscriptions: Dict[str, Set[str]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_subscriptions[user_id] = set()

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_subscriptions:
            del self.user_subscriptions[user_id]

    async def subscribe(self, user_id: str, tickers: List[str]):
        for ticker in tickers:
            self.user_subscriptions[user_id].add(ticker)
        # Return all unique tickers currently needed by any user
        return self.get_all_unique_subscriptions()

    def get_all_unique_subscriptions(self) -> Set[str]:
        all_tickers = set()
        for tickers in self.user_subscriptions.values():
            all_tickers.update(tickers)
        return all_tickers

    async def broadcast_price(self, ticker: str, price: float):
        for user_id, connection in self.active_connections.items():
            if ticker in self.user_subscriptions.get(user_id, set()):
                await connection.send_json({
                    "type": "price_update",
                    "ticker": ticker,
                    "price": price
                })

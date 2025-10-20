import websocket  # Note: use the 'websocket-client' library
import json
import threading
import asyncio
from typing import List, Set
from app.services.websocket_manager import ConnectionManager
from app.services.alert_service import check_for_alerts
from app.services.currency_service import currency_service


class FinnhubDataProvider:
    def __init__(self, api_key: str, manager: ConnectionManager):
        self.api_key = api_key
        self.manager = manager
        self.ws_url = f"wss://ws.finnhub.io?token={self.api_key}"
        self.ws = None
        self.thread = None
        self.subscribed_tickers: Set[str] = set()

    def on_message(self, ws, message):
        data = json.loads(message)
        if data['type'] == 'trade':
            for trade in data['data']:
                ticker = trade['s']
                price_usd = trade['p']
                
                # Get the asyncio event loop of the main thread
                loop = asyncio.get_event_loop()
                
                # Convert USD to INR and broadcast
                asyncio.run_coroutine_threadsafe(
                    self._process_price_update(ticker, price_usd), loop
                )
    
    async def _process_price_update(self, ticker: str, price_usd: float):
        """Convert USD price to INR and broadcast."""
        price_inr = await currency_service.convert_usd_to_inr(price_usd)
        
        # Broadcast price in INR
        await self.manager.broadcast_price(ticker, price_inr)
        
        # Check for alerts using INR price
        await check_for_alerts(ticker, price_inr, self.manager)

    def on_open(self, ws):
        print("Finnhub WebSocket connection opened")
        # On (re)connect, re-subscribe to all needed tickers
        current_subs = self.manager.get_all_unique_subscriptions()
        self.update_subscriptions(list(current_subs))

    def update_subscriptions(self, tickers: List[str]):
        # Unsubscribe from tickers no longer needed
        for ticker in self.subscribed_tickers - set(tickers):
            self.ws.send(json.dumps({'type': 'unsubscribe', 'symbol': ticker}))
        
        # Subscribe to new tickers
        for ticker in set(tickers) - self.subscribed_tickers:
            self.ws.send(json.dumps({'type': 'subscribe', 'symbol': ticker}))
            
        self.subscribed_tickers = set(tickers)

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message
        )
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()

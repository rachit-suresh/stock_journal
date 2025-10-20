from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.services.websocket_manager import ConnectionManager
from app.services.data_provider import FinnhubDataProvider
from app.routers import trades, setups
from app.db.database import get_trades_collection
import asyncio

# Create singletons
manager = ConnectionManager()
data_provider = FinnhubDataProvider(settings.FINNHUB_API_KEY, manager)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    print("Starting Finnhub Data Provider...")
    data_provider.start()
    
    # Give it a second to connect
    await asyncio.sleep(2)
    
    # Pre-populate subscriptions from all open trades in DB
    collection = get_trades_collection()
    cursor = collection.find({"status": "open"}, {"ticker": 1})
    initial_tickers = set()
    async for doc in cursor:
        initial_tickers.add(doc['ticker'])
    
    if initial_tickers:
        print(f"Pre-subscribing to: {initial_tickers}")
        data_provider.update_subscriptions(list(initial_tickers))
        
    yield
    # On shutdown
    print("Stopping Finnhub Data Provider...")
    data_provider.ws.close()


app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include HTTP Routers
app.include_router(trades.router)
app.include_router(setups.router)


# Root endpoint
@app.get("/")
def read_root():
    return {"status": "Trading Journal API is running"}


# Our server's WebSocket endpoint for frontend clients
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "subscribe":
                tickers = data.get("tickers", [])
                all_subs = await manager.subscribe(user_id, tickers)
                # Tell Finnhub to update its subscriptions
                data_provider.update_subscriptions(list(all_subs))
                
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        # Optionally, update subscriptions if user was last one watching a ticker
        all_subs = manager.get_all_unique_subscriptions()
        data_provider.update_subscriptions(list(all_subs))

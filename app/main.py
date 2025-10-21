from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.services.websocket_manager import ConnectionManager
from app.routers import trades, setups, auth

# Create singleton WebSocket manager
manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    print("Trading Journal API starting...")
    print(f"📊 Price Service: {'MOCK MODE (Development)' if settings.USE_MOCK_PRICES else 'Finnhub + Exchange Rate API (Production)'}")
    yield
    # On shutdown
    print("Trading Journal API shutting down...")


app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # Development
        "http://localhost:5173",  # Vite dev server (primary)
        "http://localhost:5174",  # Vite dev server (alternate port)
        "http://localhost:3000",  # Alternative dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
        # Production - Add your Vercel frontend URL here
        "https://stock-journal-three.vercel.app",  # Update with your actual Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include HTTP Routers
app.include_router(auth.router)
app.include_router(trades.router)
app.include_router(setups.router)


# Root endpoint
@app.get("/")
def read_root():
    return {"status": "Trading Journal API is running"}


# Our server's WebSocket endpoint for frontend clients
# Note: Currently used for future real-time features
# Prices are fetched via polling from frontend
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "subscribe":
                tickers = data.get("tickers", [])
                await manager.subscribe(user_id, tickers)
                
    except WebSocketDisconnect:
        manager.disconnect(user_id)

# Stock Market Trading Journal API

A real-time, persistent stock market journal built with FastAPI, MongoDB, and WebSockets. This backend provides complete CRUD operations for managing trades and setups, along with live price feeds and automatic stop-loss alerts.

## Features

- **Trade Management**: Create, view, and close trades with full P&L calculation
- **Setup Library**: Maintain a collection of trading setups/strategies
- **Real-Time Price Feeds**: Live stock price updates via Finnhub WebSocket API
- **Automatic Alerts**: Server-side stop-loss monitoring with instant notifications
- **Async Architecture**: Built on FastAPI with async/await for high concurrency
- **MongoDB**: Flexible document storage for journal entries

## Technology Stack

- **FastAPI**: Modern async Python web framework
- **MongoDB + Motor**: Async NoSQL database
- **Pydantic**: Data validation and settings management
- **WebSockets**: Real-time bidirectional communication
- **Finnhub.io**: Stock market data provider

## Project Structure

```
/trading_journal_project
|-- /app
|   |-- main.py                      # FastAPI app entry point
|   |-- /core
|   |   |-- config.py                # Settings and env management
|   |-- /db
|   |   |-- database.py              # MongoDB client
|   |-- /models
|   |   |-- common.py                # Shared models
|   |   |-- setup.py                 # Setup data models
|   |   |-- trade.py                 # Trade data models
|   |-- /routers
|   |   |-- setups.py                # Setup CRUD endpoints
|   |   |-- trades.py                # Trade CRUD endpoints
|   |-- /services
|       |-- websocket_manager.py     # Client connection manager
|       |-- data_provider.py         # Finnhub integration
|       |-- alert_service.py         # Stop-loss monitoring
|-- .env                             # Environment variables
|-- requirements.txt                 # Python dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- MongoDB (local or cloud instance)
- Finnhub API key (free tier available at https://finnhub.io/)

### Installation

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Configure environment variables:**

Edit the `.env` file with your credentials:

```
MONGO_CONNECTION_STRING="mongodb://user:pass@localhost:27017/"
MONGO_DB_NAME="trading_journal"
FINNHUB_API_KEY="your_actual_api_key"
```

3. **Run the application:**

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Trades

- `POST /api/v1/trades/` - Create a new trade
- `GET /api/v1/trades/open` - Get all open trades
- `GET /api/v1/trades/closed` - Get all closed trades
- `PUT /api/v1/trades/{trade_id}/close` - Close a trade with exit price

### Setups

- `POST /api/v1/setups/` - Create a new setup
- `GET /api/v1/setups/` - Get all setups

### WebSocket

- `WS /ws/{user_id}` - Connect to real-time price feed

## WebSocket Protocol

### Client → Server

Subscribe to tickers:
```json
{
  "type": "subscribe",
  "tickers": ["AAPL", "TSLA", "MSFT"]
}
```

### Server → Client

Price update:
```json
{
  "type": "price_update",
  "ticker": "AAPL",
  "price": 150.25
}
```

Stop-loss alert:
```json
{
  "type": "alert",
  "ticker": "AAPL",
  "trade_id": "507f1f77bcf86cd799439011",
  "message": "Stop loss triggered for AAPL at $148.50"
}
```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Example Usage

### Create a Trade

```bash
curl -X POST "http://localhost:8000/api/v1/trades/" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "direction": "bullish",
    "entryPrice": 150.00,
    "stopLoss": 148.00,
    "size": 100,
    "marketConditions": "Bullish trend, support at 148",
    "emotions": "Confident"
  }'
```

### Close a Trade

```bash
curl -X PUT "http://localhost:8000/api/v1/trades/{trade_id}/close" \
  -H "Content-Type: application/json" \
  -d '{
    "exitPrice": 155.00,
    "lessonsLearned": "Trade went as planned, respected the setup"
  }'
```

## Architecture Notes

### Real-Time System

The application maintains two WebSocket connections:

1. **External (Finnhub)**: Consumes live market data
2. **Internal (Clients)**: Broadcasts to connected frontend clients

The data provider runs in a separate thread and uses `asyncio.run_coroutine_threadsafe` to bridge to FastAPI's event loop.

### Stop-Loss Monitoring

The `alert_service` automatically checks every incoming price tick against all open trades. When a stop-loss threshold is crossed, it sends an immediate alert to the relevant user's WebSocket connection.

### P&L Calculation

Profit/Loss is automatically calculated when a trade is closed:

```
result_pnl = (exitPrice - entryPrice) * size
```

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Trade filtering and search
- [ ] Performance analytics and statistics
- [ ] Export functionality (CSV, PDF)
- [ ] Multiple exchange support
- [ ] Advanced charting integration

## License

MIT

# Stock Market Trading Journal API

A real-time, persistent stock market journal built with FastAPI, MongoDB, and WebSockets. This backend provides complete CRUD operations for managing trades and setups, along with live price feeds and automatic stop-loss alerts.

## Features

- **Trade Management**: Create, view, and close trades with full P&L calculation
- **Setup Library**: Maintain a collection of trading setups/strategies
- **Real-Time Price Feeds**: US stock quotes via Finnhub API with automatic USD to INR conversion
- **Authentication**: JWT-based secure authentication and authorization
- **Smart Caching**: 5-minute quote cache + 1-hour exchange rate cache to minimize API calls
- **Ticker Search**: Automatic suggestions when ticker not found
- **Async Architecture**: Built on FastAPI with async/await for high concurrency
- **MongoDB**: Flexible document storage for journal entries

## Technology Stack

- **FastAPI**: Modern async Python web framework
- **MongoDB + Motor**: Async NoSQL database
- **Pydantic**: Data validation and settings management
- **Finnhub.io**: Stock market data provider (60 calls/min free tier)
- **Exchange Rate API**: USD to INR currency conversion (1,500 calls/month free tier)

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
||   |-- /services
||       |-- finnhub_service.py       # Finnhub API client with rate limiting
||       |-- exchange_rate_service.py # USD to INR conversion
||       |-- mock_price_service.py    # Mock prices for development
||       |-- websocket_manager.py     # WebSocket connection manager
||       |-- alert_service.py         # Stop-loss monitoring (future)
|-- .env                             # Environment variables
|-- requirements.txt                 # Python dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- MongoDB (local or cloud instance)
- Finnhub API key (free tier: https://finnhub.io/dashboard)
- Exchange Rate API key (free tier: https://www.exchangerate-api.com/)

### Installation

1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

2. **Configure environment variables:**

Create a `.env` file (see `.env.example` for template):

```bash
MONGO_CONNECTION_STRING="mongodb://user:pass@localhost:27017/"
MONGO_DB_NAME="trading_journal"
FINNHUB_API_KEY="your_finnhub_api_key"
EXCHANGE_RATE_API_KEY="your_exchange_rate_api_key"
USE_MOCK_PRICES=false  # Set to true for development without API calls
```

See **`FINNHUB_SETUP_GUIDE.md`** for detailed API key setup instructions.

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

### Price Service

The application uses Finnhub REST API for stock quotes:

1. **Quote Caching**: 5-minute cache per ticker to minimize API calls
2. **Rate Limiting**: 60 calls/minute with automatic enforcement
3. **Symbol Search**: Suggests alternative tickers when not found
4. **Indian ADR Detection**: Warns when viewing ADR prices vs NSE/BSE prices

### Currency Conversion

- Fetches USD to INR exchange rate from Exchange Rate API
- 1-hour cache (exchange rates change infrequently)
- All prices displayed in INR with USD reference
- Fallback to last known rate if API fails

### WebSocket Support

WebSocket infrastructure is implemented but currently not used. Frontend polls every 30 seconds (sufficient with 5-minute cache). WebSocket can be enabled later for real-time streaming.

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

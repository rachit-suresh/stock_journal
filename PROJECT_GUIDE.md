# Stock Market Trading Journal - Complete Setup Guide

A full-stack, real-time stock market trading journal with Python FastAPI backend and React TypeScript frontend.

## 🚀 Quick Start

### Backend Setup

1. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

2. **Configure environment variables:**

Edit `.env` file with your credentials:

```
MONGO_CONNECTION_STRING="mongodb://user:pass@localhost:27017/"
MONGO_DB_NAME="trading_journal"
FINNHUB_API_KEY="your_finnhub_api_key"
```

3. **Start the backend server:**

```bash
uvicorn app.main:app --reload
```

Backend will run at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**

```bash
cd frontend
```

2. **Install npm dependencies:**

```bash
npm install
```

3. **Configure environment variables:**

Create `frontend/.env`:

```
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_BASE_URL=ws://localhost:8000
```

4. **Start the frontend dev server:**

```bash
npm run dev
```

Frontend will run at `http://localhost:5173`

## 📋 Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **MongoDB** (local or MongoDB Atlas)
- **Finnhub API Key** (free tier: https://finnhub.io/)

## 🏗️ Architecture

### Backend (Python FastAPI)

```
/app
├── main.py                 # FastAPI app with WebSocket
├── /core
│   └── config.py          # Environment configuration
├── /db
│   └── database.py        # MongoDB connection
├── /models
│   ├── common.py          # Base models
│   ├── setup.py           # Setup models
│   └── trade.py           # Trade models
├── /routers
│   ├── setups.py          # Setup endpoints
│   └── trades.py          # Trade endpoints
└── /services
    ├── websocket_manager.py    # Client connections
    ├── data_provider.py        # Finnhub integration
    └── alert_service.py        # Stop-loss monitoring
```

### Frontend (React + TypeScript)

```
/frontend/src
├── /api                   # API client
├── /components            # Reusable components
├── /pages                 # Application pages
├── /services              # WebSocket service
├── /types                 # TypeScript interfaces
└── App.tsx               # Root component
```

## 🧪 Running Tests

### Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/routers/test_trades.py

# Run specific test
pytest tests/services/test_websocket_manager.py::TestConnectionManager::test_connect
```

### Test Structure

```
/tests
├── conftest.py                      # Shared fixtures
├── /models
│   └── test_models.py              # Model validation tests
├── /routers
│   ├── test_trades.py              # Trade API tests
│   └── test_setups.py              # Setup API tests
└── /services
    ├── test_websocket_manager.py   # WebSocket tests
    └── test_alert_service.py       # Alert logic tests
```

## 📡 API Endpoints

### Trades

- `POST /api/v1/trades/` - Create new trade
- `GET /api/v1/trades/open` - Get open trades
- `GET /api/v1/trades/closed` - Get closed trades
- `PUT /api/v1/trades/{id}/close` - Close trade

### Setups

- `POST /api/v1/setups/` - Create setup
- `GET /api/v1/setups/` - Get all setups

### WebSocket

- `WS /ws/{user_id}` - Real-time price updates and alerts

## 🔌 WebSocket Protocol

### Subscribe to Tickers

```json
{
  "type": "subscribe",
  "tickers": ["AAPL", "TSLA", "MSFT"]
}
```

### Price Update (Server → Client)

```json
{
  "type": "price_update",
  "ticker": "AAPL",
  "price": 150.25
}
```

### Stop-Loss Alert (Server → Client)

```json
{
  "type": "alert",
  "ticker": "AAPL",
  "trade_id": "507f1f77bcf86cd799439011",
  "message": "Stop loss triggered for AAPL at $148.50"
}
```

## 🎨 Features

### Completed

✅ Full CRUD API for trades and setups  
✅ Real-time WebSocket price feeds  
✅ Automatic stop-loss monitoring  
✅ P&L calculation (realized and unrealized)  
✅ Responsive React frontend  
✅ Comprehensive test suite  
✅ Type-safe TypeScript  
✅ Beautiful Tailwind CSS UI  

### Roadmap

- [ ] User authentication (JWT)
- [ ] Trade analytics and charts
- [ ] Export to CSV/PDF
- [ ] Multiple exchange support
- [ ] Mobile app (React Native)

## 🐛 Troubleshooting

### Backend Issues

**MongoDB connection failed:**
- Verify MongoDB is running: `mongosh` or check MongoDB Atlas
- Check connection string in `.env`

**Finnhub WebSocket not connecting:**
- Verify API key is valid
- Check Finnhub status page
- Ensure firewall allows WebSocket connections

### Frontend Issues

**API requests failing:**
- Ensure backend is running on port 8000
- Check CORS settings in `main.py`
- Verify `.env` file has correct URLs

**WebSocket not connecting:**
- Ensure backend WebSocket server is running
- Check browser console for errors
- Verify `VITE_WS_BASE_URL` in `.env`

## 📊 Database Schema

### Trades Collection

```javascript
{
  "_id": ObjectId,
  "user_id": "string",
  "ticker": "string",
  "direction": "bullish" | "bearish",
  "entryPrice": number,
  "stopLoss": number,
  "size": number,
  "status": "open" | "closed",
  "entryDate": ISODate,
  "exitPrice": number?,
  "exitDate": ISODate?,
  "marketConditions": "string"?,
  "emotions": "string"?,
  "lessonsLearned": "string"?,
  "result_pnl": number?,
  "setup_id": ObjectId?
}
```

### Setups Collection

```javascript
{
  "_id": ObjectId,
  "user_id": "string",
  "name": "string",
  "notes": "string"?
}
```

## 🔐 Security Notes

- Never commit `.env` files
- Use strong MongoDB credentials
- Keep Finnhub API key private
- Implement rate limiting for production
- Add authentication before deploying

## 📝 License

MIT

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📧 Support

For issues and questions, please open a GitHub issue.

# Trading Journal

**A fullstack web application for tracking and analyzing stock trades with real-time pricing**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-19-61dafb.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-blue.svg)](https://typescriptlang.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688.svg)](https://fastapi.tiangolo.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248.svg)](https://mongodb.com)

---
### Please do sign up to log into the website or use hihi(username) and hihello(pswd)

## 🚀 Features

- ✅ **User Registration & Authentication** with JWT
- ✅ **Trade Management** - Create, view, close, and delete trades
- ✅ **Real-Time Pricing** from Finnhub API (US stocks)
- ✅ **USD to INR Conversion** for Indian traders
- ✅ **Analytics Dashboard** - Win rate, P&L tracking
- ✅ **Smart Caching** - 5-minute price cache, 1-hour exchange rate cache
- ✅ **Modern UI** - React + TypeScript + Tailwind CSS
- ✅ **Free Deployment** - Render (backend) + Vercel (frontend)

---

## 📚 Documentation

For complete documentation, setup instructions, API reference, and deployment guide, see:

**[📖 PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)**

---

## 🏃‍♂️ Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB Atlas account (free)
- Finnhub API key (free)
- Exchange Rate API key (free)

### Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
MONGO_CONNECTION_STRING=your_mongodb_connection
MONGO_DB_NAME=trading_journal
FINNHUB_API_KEY=your_finnhub_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_key
USE_MOCK_PRICES=false

# Run backend
uvicorn app.main:app --reload
```

Backend runs at: `http://localhost:8000`

### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Run frontend
npm run dev
```

Frontend runs at: `http://localhost:5173`

### Access the App

1. Visit `http://localhost:5173`
2. Click **"Sign up"** to create an account
3. Login and start tracking trades!

---

## 🌐 Live Demo

Deploy your own instance in 3 steps:

1. **Backend** → [Render](https://render.com) (Free)
2. **Frontend** → [Vercel](https://vercel.com) (Free)
3. **Database** → [MongoDB Atlas](https://mongodb.com/cloud/atlas) (Free 512MB)

See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md#7-deployment-guide) for detailed deployment instructions.

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async Python framework
- **MongoDB** - NoSQL database with Motor async driver
- **JWT** - Secure authentication
- **Finnhub API** - Stock quotes (60 calls/min free)
- **ExchangeRate API** - Currency conversion (1,500 calls/month free)

### Frontend
- **React 19** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client

---

## 📁 Project Structure

```
trading_journal/
├── app/                    # FastAPI backend
│   ├── core/              # Auth & config
│   ├── routers/           # API endpoints
│   ├── services/          # External API clients
│   └── models/            # Data models
├── frontend/              # React frontend
│   └── src/
│       ├── pages/         # Page components
│       ├── components/    # Reusable components
│       └── services/      # API clients
└── PROJECT_DOCUMENTATION.md  # Complete docs
```

---

## 🎯 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user

### Trades
- `POST /api/v1/trades/` - Create trade
- `GET /api/v1/trades/open` - Get open trades
- `GET /api/v1/trades/closed` - Get closed trades
- `PUT /api/v1/trades/{id}/close` - Close trade
- `DELETE /api/v1/trades/{id}` - Delete trade
- `GET /api/v1/trades/statistics` - Get statistics
- `GET /api/v1/trades/quotes/{ticker}` - Get current price

**Interactive API Docs:** `http://localhost:8000/docs`

---

## 📖 Key Features Explained

### Trade Management
Track your stock trades from entry to exit with:
- Entry price and stop loss
- Position size
- Market conditions and emotions
- Automatic P&L calculation

### Real-Time Pricing
- Fetches current prices from Finnhub
- Converts USD prices to INR
- 5-minute caching to stay within free tier limits
- Supports US stocks and Indian ADRs

### Analytics
- Win rate calculation
- Total P&L tracking
- Trade history
- Performance statistics

---

## 🔑 Getting API Keys

### Finnhub (Free)
1. Visit [finnhub.io/dashboard](https://finnhub.io/dashboard)
2. Sign up for free account
3. Copy API key
4. **Limit:** 60 calls/minute

### Exchange Rate API (Free)
1. Visit [exchangerate-api.com](https://www.exchangerate-api.com/)
2. Sign up for free account
3. Copy API key
4. **Limit:** 1,500 calls/month

### MongoDB Atlas (Free)
1. Visit [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster (512MB)
3. Get connection string
4. Whitelist IPs: `0.0.0.0/0`

---

## 🐛 Troubleshooting

### Backend Issues
```bash
# Module not found
pip install -r requirements.txt

# MongoDB connection error
# Check .env file and MongoDB Atlas IP whitelist
```

### Frontend Issues
```bash
# Module not found
cd frontend && npm install

# CORS errors
# Verify backend is running on port 8000
```

For detailed troubleshooting, see [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md#11-troubleshooting).

---

## 📝 License

MIT License - Free for personal and commercial use

---

## 🔗 Links

- **Complete Documentation:** [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
- **Repository:** [github.com/rachit-suresh/stock_journal](https://github.com/rachit-suresh/stock_journal)
- **Finnhub API:** [finnhub.io/docs/api](https://finnhub.io/docs/api)
- **FastAPI Docs:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **React Docs:** [react.dev](https://react.dev)

---

**Project Status:** ✅ Production Ready

**Last Updated:** 2025-01-21

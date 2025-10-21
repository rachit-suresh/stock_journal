# Trading Journal - Complete Project Documentation

**A comprehensive fullstack trading journal application for tracking stock trades with real-time pricing**

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack](#2-technology-stack)
3. [Features](#3-features)
4. [Project Structure](#4-project-structure)
5. [Setup & Installation](#5-setup--installation)
6. [API Documentation](#6-api-documentation)
7. [Deployment Guide](#7-deployment-guide)
8. [Finnhub Setup](#8-finnhub-setup)
9. [Quick Commands](#9-quick-commands)
10. [Migration Notes](#10-migration-notes)
11. [Troubleshooting](#11-troubleshooting)

---

## 1. Project Overview

### What is Trading Journal?

A fullstack web application for tracking and analyzing stock trades with:
- **Real-time price fetching** from Finnhub API (US stocks)
- **USD to INR conversion** for displaying prices in Indian Rupees
- **Trade management** (create, view, close, delete trades)
- **Statistics & analytics** (win rate, P&L tracking)
- **User authentication** with JWT
- **Persistent storage** with MongoDB

### Target Users

- Individual stock traders
- Especially useful for Indian traders trading US stocks
- Personal portfolio tracking and analysis

### Key Design Decisions

- **FastAPI** for async performance and auto-documentation
- **React + TypeScript** for type-safe frontend
- **MongoDB** for flexible trade data storage
- **Finnhub API** for reliable US stock quotes
- **JWT authentication** for secure access

---

## 2. Technology Stack

### Backend
```
FastAPI (Python 3.11+)
├── Motor (Async MongoDB Driver)
├── Pydantic (Data Validation)
├── python-jose (JWT)
├── passlib + bcrypt (Password Hashing)
├── httpx (HTTP Client for APIs)
└── Finnhub & Exchange Rate APIs
```

### Frontend
```
React 19 + TypeScript
├── Vite (Build Tool)
├── React Router (Routing)
├── Axios (HTTP Client)
├── Tailwind CSS (Styling)
└── Lucide React (Icons)
```

### Database
- **MongoDB Atlas** (Cloud NoSQL Database)
- Collections: `trades`, `setups`, `users` (future)

### External APIs
- **Finnhub.io** - Stock quotes (60 calls/min free tier)
- **ExchangeRate-API.com** - USD to INR conversion (1,500 calls/month free tier)

---

## 3. Features

### Authentication
- ✅ User registration with validation
- ✅ JWT-based secure login
- ✅ Password hashing with bcrypt
- ✅ Protected routes and API endpoints

### Trade Management
- ✅ Create new trades with entry price and stop loss
- ✅ View all open trades
- ✅ Close trades with exit price
- ✅ Automatic P&L calculation
- ✅ Delete trades
- ✅ Link trades to setups/strategies

### Real-Time Pricing
- ✅ Fetch current prices from Finnhub
- ✅ USD to INR conversion
- ✅ 5-minute price caching
- ✅ 1-hour exchange rate caching
- ✅ Ticker search and suggestions
- ✅ Support for US stocks

### Analytics
- ✅ Win rate calculation
- ✅ Total P&L tracking
- ✅ Trade statistics (wins/losses/breakeven)
- ✅ Historical trade data

### User Interface
- ✅ Modern, responsive design with Tailwind CSS
- ✅ Dashboard with live prices
- ✅ Trade history page
- ✅ User profile page
- ✅ Mobile-friendly

---

## 4. Project Structure

```
trading_journal/
├── app/                           # Backend (FastAPI)
│   ├── main.py                    # Application entry point
│   ├── core/
│   │   ├── auth.py                # JWT authentication
│   │   └── config.py              # Settings & environment
│   ├── db/
│   │   └── database.py            # MongoDB connection
│   ├── models/
│   │   ├── common.py              # Shared models
│   │   ├── trade.py               # Trade models
│   │   └── setup.py               # Setup models
│   ├── routers/
│   │   ├── auth.py                # Auth endpoints
│   │   ├── trades.py              # Trade endpoints
│   │   └── setups.py              # Setup endpoints
│   └── services/
│       ├── finnhub_service.py     # Finnhub API client
│       ├── exchange_rate_service.py  # Currency conversion
│       └── mock_price_service.py  # Development mock data
│
├── frontend/                      # Frontend (React)
│   ├── src/
│   │   ├── main.tsx               # React entry point
│   │   ├── App.tsx                # Root component
│   │   ├── api/
│   │   │   └── client.ts          # Axios HTTP client
│   │   ├── services/
│   │   │   ├── auth.ts            # Auth service
│   │   │   └── websocket.ts       # WebSocket client
│   │   ├── components/
│   │   │   ├── MainLayout.tsx     # App layout
│   │   │   ├── ProtectedRoute.tsx # Auth guard
│   │   │   ├── NewTradeForm.tsx   # Create trade
│   │   │   ├── TradeCard.tsx      # Trade display
│   │   │   └── CloseTradeForm.tsx # Close trade
│   │   ├── pages/
│   │   │   ├── Login.tsx          # Login page
│   │   │   ├── Register.tsx       # Registration page
│   │   │   ├── Dashboard.tsx      # Main dashboard
│   │   │   ├── History.tsx        # Trade history
│   │   │   └── UserProfile.tsx    # User profile
│   │   └── types/
│   │       └── index.ts           # TypeScript types
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
├── .env                           # Environment variables
├── requirements.txt               # Python dependencies
└── README.md                      # Project summary
```

---

## 5. Setup & Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- MongoDB (Atlas or local)
- Finnhub API key
- Exchange Rate API key

### Backend Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env` file:**
   ```bash
   MONGO_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/
   MONGO_DB_NAME=trading_journal
   FINNHUB_API_KEY=your_finnhub_api_key
   EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
   USE_MOCK_PRICES=false
   ```

4. **Run backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

   Backend runs at: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run frontend:**
   ```bash
   npm run dev
   ```

   Frontend runs at: `http://localhost:5173`

### Getting API Keys

#### Finnhub API (Free)
1. Go to [finnhub.io](https://finnhub.io/dashboard)
2. Sign up for free account
3. Copy your API key
4. Free tier: 60 calls/minute

#### Exchange Rate API (Free)
1. Go to [exchangerate-api.com](https://www.exchangerate-api.com/)
2. Sign up for free account
3. Copy your API key
4. Free tier: 1,500 calls/month

#### MongoDB Atlas (Free)
1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create free cluster (512MB)
3. Create database user
4. Get connection string
5. Whitelist IPs (0.0.0.0/0 for testing)

---

## 6. API Documentation

### Base URL
- Development: `http://localhost:8000/api/v1`
- Production: `https://your-backend.onrender.com/api/v1`

### Authentication Endpoints

#### POST `/auth/register`
Register a new user.

**Request:**
```json
{
  "username": "john_doe",
  "password": "securepass123",
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### POST `/auth/login`
Login existing user.

**Request:**
```json
{
  "username": "john_doe",
  "password": "securepass123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### GET `/auth/me`
Get current user info (requires auth).

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "user_id": "user_123",
  "username": "john_doe",
  "email": "john@example.com"
}
```

### Trade Endpoints

#### POST `/trades/`
Create a new trade.

**Request:**
```json
{
  "ticker": "AAPL",
  "direction": "bullish",
  "entryPrice": 150.50,
  "stopLoss": 145.00,
  "size": 100,
  "marketConditions": "Strong uptrend",
  "emotions": "Confident"
}
```

#### GET `/trades/open`
Get all open trades for current user.

#### GET `/trades/closed`
Get all closed trades for current user.

#### PUT `/trades/{trade_id}/close`
Close a trade.

**Request:**
```json
{
  "exitPrice": 155.00,
  "lessonsLearned": "Trade went as planned"
}
```

#### DELETE `/trades/{trade_id}`
Delete a trade.

#### GET `/trades/statistics`
Get trading statistics.

**Response:**
```json
{
  "total_closed_trades": 10,
  "winning_trades": 6,
  "losing_trades": 4,
  "breakeven_trades": 0,
  "win_rate": 60.0,
  "total_pnl": 15000.50
}
```

#### GET `/trades/quotes/{ticker}`
Get current quote for a ticker.

**Response:**
```json
{
  "found": true,
  "ticker": "AAPL",
  "price_usd": 150.50,
  "price_inr": 12540.75,
  "exchange_rate": 83.35,
  "name": "Apple Inc.",
  "currency": "USD"
}
```

---

## 7. Deployment Guide

### Quick Deployment (3 Steps)

#### Step 1: Deploy Backend to Render

1. Go to [render.com](https://render.com) → Sign up/Login
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub repo: `rachit-suresh/stock_journal`
4. Configure:
   - **Name:** `stock-journal-api`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`

5. Add environment variables:
   ```
   MONGO_CONNECTION_STRING=<mongodb_connection_string>
   MONGO_DB_NAME=trading_journal
   FINNHUB_API_KEY=<finnhub_api_key>
   EXCHANGE_RATE_API_KEY=<exchange_rate_api_key>
   USE_MOCK_PRICES=false
   PYTHON_VERSION=3.11.0
   ```

6. Click **"Create Web Service"** → Wait 2-5 minutes

7. Copy your backend URL: `https://stock-journal-api.onrender.com`

#### Step 2: Deploy Frontend to Vercel

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy frontend:
   ```bash
   cd frontend
   vercel
   ```

3. Follow prompts:
   - Project name: `stock-journal`
   - Build settings: Auto-detected ✓

4. Update backend URL in:
   
   **`frontend/src/services/auth.ts`:**
   ```typescript
   private baseUrl = "https://stock-journal-api.onrender.com/api/v1/auth";
   ```
   
   **`frontend/src/api/client.ts`:**
   ```typescript
   const API_BASE_URL = "https://stock-journal-api.onrender.com/api/v1";
   ```

5. Redeploy:
   ```bash
   vercel --prod
   ```

#### Step 3: Test Deployment

1. Visit your Vercel frontend URL
2. Click **"Sign up"**
3. Create account (username: `test`, password: `test123`)
4. Add a trade with ticker `AAPL` or `INFY`
5. Verify price fetching works

### Important Notes for Render Free Tier

- **Cold starts:** Free tier spins down after 15 minutes of inactivity
- **First request delay:** 30-60 seconds after cold start
- **Monthly limits:** 750 hours/month (enough for 24/7)
- **Automatic deploys:** Enabled on push to main branch

---

## 8. Finnhub Setup

### Getting Your API Key

1. Visit [https://finnhub.io/register](https://finnhub.io/register)
2. Sign up for a free account
3. Verify your email
4. Go to Dashboard: [https://finnhub.io/dashboard](https://finnhub.io/dashboard)
5. Copy your API Key

### Free Tier Limits

- **60 API calls per minute**
- **For US stocks and ADRs only**
- **30 requests per second**

### Supported Tickers

**US Stocks:**
- `AAPL` (Apple)
- `MSFT` (Microsoft)
- `GOOGL` (Google)
- `TSLA` (Tesla)
- Any US-listed stock

**Indian ADRs (American Depositary Receipts):**
- `INFY` (Infosys ADR)
- `WIT` (Wipro ADR)
- `HDB` (HDFC Bank ADR)

**NOT Supported (Free Tier):**
- ❌ Indian stocks with `.NS` or `.BO` suffix
- ❌ `RELIANCE.NS`, `TCS.NS`, etc.
- ❌ NSE/BSE direct listings

### Rate Limiting

Our implementation includes:
- **5-minute quote cache** - Reduces API calls by 90%
- **1-hour exchange rate cache** - Minimal currency API usage
- **Automatic rate limit detection** - Handles 429 errors
- **Exponential backoff** - Waits before retrying

### Usage Calculation

For 10 tickers with 5-minute cache:
```
Requests per hour: 12 (every 5 minutes)
Daily requests: 288
Monthly requests: 8,640

Finnhub free tier: 60/min = 3,600/hour = 86,400/day
Usage: < 1% of daily limit ✅
```

---

## 9. Quick Commands

### Development

```bash
# Backend
uvicorn app.main:app --reload       # Start backend with hot reload
uvicorn app.main:app --port 8001    # Start on different port

# Frontend
cd frontend && npm run dev          # Start frontend dev server
cd frontend && npm run build        # Build for production
cd frontend && npm run preview      # Preview production build
cd frontend && npm run lint         # Lint frontend code

# Database
mongosh <connection_string>         # Connect to MongoDB
```

### Testing

```bash
# Test API endpoints
curl http://localhost:8000/         # Health check
curl http://localhost:8000/docs     # Interactive API docs

# Test quote endpoint
curl http://localhost:8000/api/v1/trades/quotes/AAPL
```

### Deployment

```bash
# Git
git add -A
git commit -m "Your message"
git push origin main

# Vercel (frontend)
cd frontend
vercel                              # Deploy preview
vercel --prod                       # Deploy to production

# Check deployment
curl https://your-backend.onrender.com/
```

### Useful MongoDB Commands

```javascript
// Show all trades
db.trades.find({})

// Show open trades
db.trades.find({ status: "open" })

// Show trades for specific user
db.trades.find({ user_id: "demo_user_id" })

// Delete all trades (careful!)
db.trades.deleteMany({})

// Get statistics
db.trades.aggregate([
  { $match: { status: "closed" } },
  { $group: {
      _id: null,
      total: { $sum: 1 },
      total_pnl: { $sum: "$result_pnl" }
  }}
])
```

---

## 10. Migration Notes

### From Yahoo Finance to Finnhub

The project was originally built with Yahoo Finance but migrated to Finnhub for better reliability and API limits.

#### What Changed

**Backend:**
- ✅ New `finnhub_service.py` replaces `yahoo_finance_service.py`
- ✅ Added `exchange_rate_service.py` for USD to INR conversion
- ✅ Updated quote response to include both USD and INR prices
- ✅ Removed Indian stock filtering logic

**Frontend:**
- ✅ Updated to use `price_inr` field from API
- ✅ Changed ticker placeholders from `RELIANCE.NS` to `AAPL or INFY`
- ✅ Improved error handling for unsupported tickers
- ✅ Added better user guidance for supported ticker formats

**API Response Format:**
```json
{
  "found": true,
  "ticker": "AAPL",
  "price_usd": 150.50,
  "price_inr": 12540.75,
  "exchange_rate": 83.35,
  "currency": "USD",
  "name": "Apple Inc."
}
```

---

## 11. Troubleshooting

### Common Issues

#### Backend Won't Start

**Issue:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
pip install -r requirements.txt
```

**Issue:** `MongoDB connection failed`

**Solution:**
- Check MongoDB connection string in `.env`
- Verify MongoDB cluster is running
- Whitelist your IP in MongoDB Atlas
- Check username/password are correct

#### Frontend Won't Start

**Issue:** `Cannot find module 'react'`

**Solution:**
```bash
cd frontend
npm install
```

**Issue:** `API calls failing with CORS error`

**Solution:**
- Verify backend is running at `http://localhost:8000`
- Check CORS origins in `app/main.py`
- Clear browser cache

#### Deployment Issues

**Issue:** Render cold start timeout

**Solution:**
- Normal for free tier (30-60 seconds)
- First request after inactivity takes longer
- Subsequent requests are fast

**Issue:** Finnhub rate limit errors

**Solution:**
- Use mock mode for development: `USE_MOCK_PRICES=true`
- Wait for cooldown period (5-10 minutes)
- Check you're not making duplicate requests
- Verify cache is working (5-minute TTL)

**Issue:** MongoDB connection timeout on Render

**Solution:**
- Whitelist `0.0.0.0/0` in MongoDB Atlas
- Or add Render's IP addresses
- Check connection string format

### Getting Help

- **API Documentation:** `http://localhost:8000/docs`
- **Finnhub Docs:** [https://finnhub.io/docs/api](https://finnhub.io/docs/api)
- **Render Docs:** [https://docs.render.com](https://docs.render.com)
- **MongoDB Atlas Docs:** [https://docs.atlas.mongodb.com](https://docs.atlas.mongodb.com)

---

## License

MIT License - Free for personal and commercial use

---

**Project Status:** ✅ Production Ready

**Last Updated:** 2025-01-21

**Repository:** [https://github.com/rachit-suresh/stock_journal](https://github.com/rachit-suresh/stock_journal)

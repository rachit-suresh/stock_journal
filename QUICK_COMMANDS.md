# Quick Commands Reference

## 🚀 Start Everything

### 1. Get API Keys (First Time Only)

**Required APIs:**
1. **Finnhub API** (Stock Prices)
   - Sign up: https://finnhub.io/
   - Free tier: 60 calls/minute
   - Get API key: https://finnhub.io/dashboard

2. **Exchange Rate API** (USD to INR)
   - Sign up: https://www.exchangerate-api.com/
   - Free tier: 1,500 calls/month
   - Get API key: https://app.exchangerate-api.com/

**Update .env:**
```bash
FINNHUB_API_KEY="your_key_here"
EXCHANGE_RATE_API_KEY="your_key_here"
```

See `FINNHUB_SETUP_GUIDE.md` for detailed setup instructions.

### 2. Install Dependencies

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
```

### 3. Start MongoDB

```bash
# Windows
# Open Services (services.msc) → MongoDB → Start

# Or use MongoDB Compass and start from there

# Linux/Mac
mongod
# or
sudo systemctl start mongod
```

### 4. Start Backend (Terminal 1)

```bash
uvicorn app.main:app --reload
```

✅ Backend running on: `http://localhost:8000`
✅ API Docs: `http://localhost:8000/docs`

### 5. Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

✅ Frontend running on: `http://localhost:5173` or `http://localhost:5174`

### 6. Login

Open browser: `http://localhost:5173/login`

**Demo credentials:**
- Username: `demo`
- Password: `demo123`

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Tests with Details

```bash
pytest -v
```

### Run Specific Test

```bash
pytest tests/test_quotes.py
pytest tests/routers/test_trades.py -v
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html
```

## 🔍 Check Status

### Check if MongoDB is Running

```bash
mongosh
# Should connect if MongoDB is running

# Or
mongo
```

### Check Backend Health

```bash
curl http://localhost:8000/
# Should return: {"status": "Trading Journal API is running"}
```

### Check Finnhub Service

```bash
curl http://localhost:8000/api/v1/trades/service-status
```

**Expected Response:**
```json
{
  "finnhub": {
    "service": "Finnhub",
    "calls_last_minute": 5,
    "calls_remaining": 55,
    "message": "Finnhub operational. 5/60 calls used in last minute."
  },
  "exchange_rate": {
    "cached_rate": 83.25,
    "message": "1 USD = ₹83.25"
  }
}
```

### Test Quote API

```bash
# US stock (converts USD to INR)
curl http://localhost:8000/api/v1/trades/quotes/AAPL

# Indian ADR (shows warning)
curl http://localhost:8000/api/v1/trades/quotes/INFY

# Wrong ticker (shows suggestions)
curl http://localhost:8000/api/v1/trades/quotes/APLE
```

## 🛠️ Common Issues

### Backend won't start

```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process if needed (Windows)
taskkill /PID <pid> /F

# Or use different port
uvicorn app.main:app --reload --port 8001
```

### Frontend won't start

```bash
# Port 5173 in use, will auto-use 5174
# Or specify port
npm run dev -- --port 5175
```

### MongoDB not connecting

```bash
# Check connection string in .env
MONGO_CONNECTION_STRING="mongodb://localhost:27017/"

# Try connecting manually
mongosh mongodb://localhost:27017/
```

### Tests failing

```bash
# Make sure MongoDB is running
mongosh

# Clear test database
mongosh
use test_trading_journal
db.dropDatabase()

# Re-run tests
pytest -v
```

### Finnhub rate limited

```bash
# Check service status
curl http://localhost:8000/api/v1/trades/service-status

# Finnhub: 60 calls/min (rarely hit with 5-min cache)
# Exchange Rate: 1,500 calls/month (cached for 1 hour)
# Both caches serve data if rate limit hit
```

## 📝 Development Workflow

### 1. Start coding session

```bash
# Terminal 1: Backend
uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: Watch tests
pytest -v --watch
```

### 2. Make changes

- Backend: Edit files in `app/`
- Frontend: Edit files in `frontend/src/`
- Tests: Edit files in `tests/`

### 3. Test changes

```bash
# Backend tests
pytest tests/routers/test_trades.py -v

# Manual API test
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'
```

### 4. Check frontend

- Navigate to `http://localhost:5173/login`
- Login with demo/demo123
- Test new features

## 🔐 Authentication Examples

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'

# Response: {"access_token":"eyJ...","token_type":"bearer"}
```

### Use Token

```bash
# Save token
TOKEN="eyJ..."

# Get open trades
curl http://localhost:8000/api/v1/trades/open \
  -H "Authorization: Bearer $TOKEN"

# Create trade
curl -X POST http://localhost:8000/api/v1/trades/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "RELIANCE.NS",
    "direction": "bullish",
    "entryPrice": 2500,
    "stopLoss": 2450,
    "size": 10
  }'
```

## 📊 Database Commands

### MongoDB Shell

```bash
# Connect
mongosh

# Switch to trading_journal database
use trading_journal

# View collections
show collections

# Count trades
db.trades.countDocuments()

# View all trades
db.trades.find().pretty()

# View open trades for demo user
db.trades.find({user_id: "demo_user_id", status: "open"}).pretty()

# Clear all trades for demo user
db.trades.deleteMany({user_id: "demo_user_id"})

# Drop test database
use test_trading_journal
db.dropDatabase()
```

## 🎯 Quick Verification

### Full Stack Check (5 commands)

```bash
# 1. MongoDB
mongosh --eval "db.version()"

# 2. Backend
curl http://localhost:8000/

# 3. Frontend
curl http://localhost:5173/

# 4. Tests
pytest --co -q

# 5. Finnhub Service
curl http://localhost:8000/api/v1/trades/service-status
```

All should return success! ✅

## 📦 Production Deployment

### Build Frontend

```bash
cd frontend
npm run build
# Creates frontend/dist/
```

### Environment Variables

```bash
# .env for production
MONGO_CONNECTION_STRING="mongodb://prod-server:27017/"
MONGO_DB_NAME="trading_journal_prod"
SECRET_KEY="<generate-secure-key>"

# Frontend .env
VITE_API_BASE_URL="https://api.yourdomain.com"
VITE_WS_BASE_URL="wss://api.yourdomain.com"
```

### Run in Production

```bash
# Backend (with gunicorn)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend (serve static files)
npm install -g serve
serve -s frontend/dist -p 3000
```

## 🎉 That's It!

You're all set. Happy trading! 📈

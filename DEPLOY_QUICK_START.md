# 🚀 Quick Start: Deploy to Render (Free)

## Step 1: Deploy Backend to Render

1. Go to **[render.com](https://render.com)** → Sign up/Login
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub repo: `rachit-suresh/stock_journal`
4. Configure:
   - **Name:** `stock-journal-api`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`

5. Click **"Advanced"** and add environment variables:
   ```
   MONGO_CONNECTION_STRING=<your_mongodb_atlas_connection_string>
   MONGO_DB_NAME=trading_journal
   FINNHUB_API_KEY=<your_finnhub_api_key>
   EXCHANGE_RATE_API_KEY=<your_exchange_rate_api_key>
   USE_MOCK_PRICES=false
   PYTHON_VERSION=3.11.0
   ```

6. Click **"Create Web Service"** → Wait 2-5 minutes

7. Copy your backend URL: `https://stock-journal-api.onrender.com`

---

## Step 2: Get API Keys

### MongoDB Atlas (Free):
- Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
- Create free cluster → Get connection string

### Finnhub API:
- Go to [finnhub.io/dashboard](https://finnhub.io/dashboard)
- Sign up → Copy API key

### Exchange Rate API:
- Go to [exchangerate-api.com](https://www.exchangerate-api.com/)
- Sign up → Copy API key

---

## Step 3: Deploy Frontend to Vercel

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
   
   **`frontend/src/services/auth.ts`** (line 25):
   ```typescript
   private baseUrl = "https://stock-journal-api.onrender.com/api/v1/auth";
   ```
   
   **`frontend/src/api/client.ts`** (line 1):
   ```typescript
   const API_BASE_URL = "https://stock-journal-api.onrender.com/api/v1";
   ```

5. Redeploy:
   ```bash
   vercel --prod
   ```

6. Done! Visit your frontend URL 🎉

---

## ✅ Test Your Deployment

1. Visit your Vercel frontend URL
2. Click **"Sign up"**
3. Create account (username: `test`, password: `test123`)
4. Add a trade with ticker `AAPL` or `INFY`
5. Verify price fetching works

---

## ⚠️ Known Issues

- **First load slow?** Render free tier "cold starts" after 15 mins inactivity (30-60s delay)
- **Can't connect to MongoDB?** Check if your IP is whitelisted in MongoDB Atlas (allow all: `0.0.0.0/0`)
- **CORS errors?** Already configured in backend - should work automatically

---

## 📚 Full Documentation

See `DEPLOYMENT_GUIDE.md` for detailed instructions and troubleshooting.

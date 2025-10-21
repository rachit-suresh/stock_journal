# Deployment Guide

## ✅ Changes Deployed to GitHub

All changes have been committed and pushed to: `https://github.com/rachit-suresh/stock_journal.git`

### New Features Added:
- ✅ User registration endpoint (`/api/v1/auth/register`)
- ✅ Registration page in frontend (`/register`)
- ✅ Links between login and register pages
- ✅ Finnhub API integration for US stocks
- ✅ USD to INR conversion
- ✅ Fixed frontend to work with Finnhub API

---

## 🚀 Backend Deployment (Railway)

### Option 1: Deploy via Railway CLI

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize and deploy:**
   ```bash
   railway init
   railway up
   ```

### Option 2: Deploy via Railway Dashboard

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `rachit-suresh/stock_journal`
4. Railway will auto-detect the Python app

### Required Environment Variables (Railway):

Add these in Railway dashboard under Variables:

```
MONGO_CONNECTION_STRING=your_mongodb_connection_string
MONGO_DB_NAME=trading_journal
FINNHUB_API_KEY=your_finnhub_api_key
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
USE_MOCK_PRICES=false
```

### Configure Start Command:

Railway Settings → Deploy → Start Command:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Get your backend URL:
Railway will provide a URL like: `https://your-app.railway.app`

---

## 🎨 Frontend Deployment (Vercel - Recommended)

### Deploy to Vercel:

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

4. **Follow prompts:**
   - Link to existing project? No
   - Project name: stock-journal
   - Directory: `./`
   - Build settings: Auto-detected

### Update API URL:

After backend is deployed, update frontend to use production backend URL:

**Edit `frontend/src/services/auth.ts`:**
```typescript
private baseUrl = "https://your-app.railway.app/api/v1/auth";
```

**Edit `frontend/src/api/client.ts`:**
```typescript
const API_BASE_URL = "https://your-app.railway.app/api/v1";
```

### Redeploy frontend:
```bash
vercel --prod
```

---

## 🎨 Alternative: Frontend Deployment (Netlify)

### Deploy to Netlify:

1. **Install Netlify CLI:**
   ```bash
   npm i -g netlify-cli
   ```

2. **Build the frontend:**
   ```bash
   cd frontend
   npm run build
   ```

3. **Deploy:**
   ```bash
   netlify deploy --prod --dir=dist
   ```

4. **Or use Netlify Dashboard:**
   - Go to [netlify.com](https://www.netlify.com)
   - New site from Git → Select repo
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
   - Base directory: `frontend`

---

## 🔧 MongoDB Setup

If you don't have MongoDB yet:

1. **MongoDB Atlas (Free):**
   - Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
   - Create free cluster
   - Get connection string
   - Add to Railway environment variables

---

## 📝 Post-Deployment Checklist

- [ ] Backend deployed and running on Railway
- [ ] MongoDB connection working
- [ ] Environment variables set correctly
- [ ] Frontend deployed to Vercel/Netlify
- [ ] Frontend API URLs updated to production backend
- [ ] Test user registration at `/register`
- [ ] Test user login at `/login`
- [ ] Test creating trades
- [ ] Test price fetching with real Finnhub API

---

## 🎯 Quick Test

After deployment:

1. Visit your frontend URL (e.g., `https://your-app.vercel.app`)
2. Click "Sign up" 
3. Create a new account (e.g., username: `test`, password: `test123`)
4. Should auto-login and redirect to dashboard
5. Click "New Trade" and test with ticker `AAPL` or `INFY`
6. Verify price fetch works with Finnhub

---

## 🐛 Troubleshooting

### Backend issues:
- Check Railway logs: `railway logs`
- Verify all environment variables are set
- Check MongoDB connection string format

### Frontend issues:
- Verify API URLs point to correct backend
- Check browser console for errors
- Verify CORS is enabled in backend (already done in `app/main.py`)

### API Issues:
- Verify Finnhub API key is valid (test at finnhub.io/dashboard)
- Check rate limits (60 calls/min for free tier)
- Verify Exchange Rate API key is valid

---

## 🔐 Security Notes

**Before going live:**
1. Change `SECRET_KEY` in `app/core/auth.py` to a secure random string
2. Add it to Railway environment variables
3. Use proper MongoDB user with limited permissions
4. Enable HTTPS (Railway and Vercel do this automatically)

---

## 📞 Need Help?

- Railway docs: https://docs.railway.app
- Vercel docs: https://vercel.com/docs
- Netlify docs: https://docs.netlify.com
- FastAPI deployment: https://fastapi.tiangolo.com/deployment/

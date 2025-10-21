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

## 🚀 Backend Deployment (Render - Free Tier)

### Deploy via Render Dashboard

1. **Go to [Render.com](https://render.com) and sign up/login**

2. **Click "New +" → "Web Service"**

3. **Connect your GitHub repository:**
   - Select `rachit-suresh/stock_journal`
   - Click "Connect"

4. **Configure the service:**
   - **Name:** `stock-journal-api` (or your choice)
   - **Region:** Choose closest to you
   - **Branch:** `main`
   - **Root Directory:** Leave empty (root)
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`

5. **Add Environment Variables:**
   
   Click "Advanced" → Add the following environment variables:
   
   ```
   MONGO_CONNECTION_STRING=your_mongodb_connection_string
   MONGO_DB_NAME=trading_journal
   FINNHUB_API_KEY=your_finnhub_api_key
   EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
   USE_MOCK_PRICES=false
   PYTHON_VERSION=3.11.0
   ```

6. **Click "Create Web Service"**

   Render will automatically deploy your app. This takes 2-5 minutes.

7. **Get your backend URL:**
   
   Render will provide a URL like: `https://stock-journal-api.onrender.com`

### ⚠️ Important Notes for Render Free Tier:

- **Cold starts:** Free tier spins down after 15 minutes of inactivity. First request after inactivity may take 30-60 seconds.
- **Monthly limits:** 750 hours/month (enough for one service running 24/7)
- **Automatic deploys:** Enabled by default on push to main branch

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
private baseUrl = "https://stock-journal-api.onrender.com/api/v1/auth";
```

**Edit `frontend/src/api/client.ts`:**
```typescript
const API_BASE_URL = "https://stock-journal-api.onrender.com/api/v1";
```

(Replace with your actual Render URL)

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

- [ ] Backend deployed and running on Render
- [ ] MongoDB connection working
- [ ] Environment variables set correctly
- [ ] Frontend deployed to Vercel/Netlify
- [ ] Frontend API URLs updated to production backend
- [ ] Test user registration at `/register`
- [ ] Test user login at `/login`
- [ ] Test creating trades
- [ ] Test price fetching with real Finnhub API
- [ ] Note: First request may be slow due to Render free tier cold start

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
- Check Render logs in the dashboard (Logs tab)
- Verify all environment variables are set in Render dashboard
- Check MongoDB connection string format
- If service won't start, check the "Events" tab for build errors
- Cold start delays are normal on free tier (30-60 seconds)

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

- Render docs: https://docs.render.com
- Vercel docs: https://vercel.com/docs
- Netlify docs: https://docs.netlify.com
- FastAPI deployment: https://fastapi.tiangolo.com/deployment/
- MongoDB Atlas docs: https://docs.atlas.mongodb.com

# Trading Journal - Complete Technical Documentation

**A comprehensive guide explaining every line of code, design decision, and architectural choice**

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Technology Stack & Architecture](#2-technology-stack--architecture)
3. [Project Structure](#3-project-structure)
4. [Backend Deep Dive](#4-backend-deep-dive)
5. [Frontend Deep Dive](#5-frontend-deep-dive)
6. [Data Flow & State Management](#6-data-flow--state-management)
7. [Authentication System](#7-authentication-system)
8. [Price Service Architecture](#8-price-service-architecture)
9. [Database Design](#9-database-design)
10. [API Reference](#10-api-reference)
11. [Design Decisions & Rationale](#11-design-decisions--rationale)
12. [Performance Optimization](#12-performance-optimization)
13. [Error Handling](#13-error-handling)
14. [Testing Strategy](#14-testing-strategy)
15. [Deployment Guide](#15-deployment-guide)
16. [Troubleshooting](#16-troubleshooting)

---

## 1. Project Overview

### 1.1 What is This Application?

The Trading Journal is a web application designed for **personal stock trade tracking**, specifically optimized for Indian stock traders. It allows users to:

- **Log trades** with entry/exit prices, position sizes, and emotions
- **Track P&L** (Profit & Loss) automatically
- **View real-time prices** from Yahoo Finance (NSE/BSE stocks)
- **Analyze performance** with win rates and statistics
- **Record lessons learned** from each trade

### 1.2 Target User

- **Primary**: Your uncle (single user, personal use)
- **Market**: Indian stock market (NSE/BSE)
- **Use Case**: Trading journal, not high-frequency trading
- **Cost**: $0 (completely free, no paid APIs)

### 1.3 Key Features

1. **Authentication** - JWT-based secure login
2. **Trade Management** - Create, view, close, delete trades
3. **Real-time Prices** - Fetch from Yahoo Finance with intelligent caching
4. **Statistics Dashboard** - Win rate, total P&L, trade counts
5. **Trade History** - View all closed trades
6. **Mock Mode** - Development mode with fake prices

---

## 2. Technology Stack & Architecture

### 2.1 Backend Stack

```
FastAPI (Python 3.11+)
├── Motor (Async MongoDB Driver)
├── Pydantic (Data Validation)
├── python-jose (JWT)
├── passlib + bcrypt (Password Hashing)
├── yfinance (Stock Prices)
└── pytest (Testing)
```

**Why FastAPI?**
- **Async support** - Handles concurrent requests efficiently
- **Type safety** - Pydantic models catch errors early
- **Auto documentation** - Swagger UI at `/docs`
- **Fast** - One of the fastest Python frameworks
- **Modern** - Built for async/await patterns

**Why MongoDB?**
- **Flexible schema** - Easy to add fields to trades
- **Document model** - Natural fit for JSON-like trade data
- **Cloud-ready** - MongoDB Atlas offers free tier
- **No migrations** - Schema changes don't require migrations

### 2.2 Frontend Stack

```
React 19 + TypeScript
├── Vite (Build Tool)
├── React Router (Routing)
├── Axios (HTTP Client)
├── Tailwind CSS (Styling)
└── Lucide React (Icons)
```

**Why React?**
- **Component reusability** - TradeCard, forms, etc.
- **Large ecosystem** - Many libraries available
- **Type safety** - TypeScript catches errors
- **Performance** - Virtual DOM optimizations

**Why Vite?**
- **Fast HMR** - Instant hot module replacement
- **Fast builds** - 10x faster than webpack
- **ESM native** - Uses modern JavaScript modules
- **TypeScript support** - Built-in TS support

**Why TypeScript?**
- **Type safety** - Catches bugs at compile time
- **Better IDE support** - Autocomplete, refactoring
- **Self-documenting** - Types serve as documentation
- **Confidence** - Refactor without fear

### 2.3 System Architecture

```
┌─────────────────┐
│   Browser       │
│  (React App)    │
└────────┬────────┘
         │ HTTPS
         │
┌────────▼────────┐
│   FastAPI       │
│   Backend       │
│   (Port 8000)   │
└────┬───┬────────┘
     │   │
     │   └─────────┐
     │             │
┌────▼─────┐  ┌───▼──────────┐
│ MongoDB  │  │ Yahoo Finance│
│  Atlas   │  │  (yfinance)  │
└──────────┘  └──────────────┘
```

**Communication Flow:**

1. **User interacts with React UI** → Button click
2. **React calls API via Axios** → HTTP request with JWT
3. **FastAPI validates JWT** → Authentication
4. **FastAPI processes request** → Business logic
5. **MongoDB stores/retrieves data** → Persistence
6. **Yahoo Finance fetched (if needed)** → Price data
7. **FastAPI returns JSON response** → Data
8. **React updates UI** → Display

---

## 3. Project Structure

### 3.1 Backend Structure

```
project/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── core/
│   │   ├── auth.py                # JWT authentication logic
│   │   └── config.py              # Settings & environment variables
│   ├── db/
│   │   └── database.py            # MongoDB connection
│   ├── models/
│   │   ├── common.py              # Shared Pydantic models
│   │   ├── trade.py               # Trade models
│   │   └── setup.py               # Setup models
│   ├── routers/
│   │   ├── auth.py                # Authentication endpoints
│   │   ├── trades.py              # Trade CRUD endpoints
│   │   └── setups.py              # Setup CRUD endpoints
│   └── services/
│       ├── yahoo_finance_service.py   # Yahoo Finance API client
│       ├── mock_price_service.py      # Mock prices for development
│       ├── currency_service.py        # USD to INR conversion
│       └── websocket_manager.py       # WebSocket manager (future use)
├── tests/                         # Pytest test suite
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables
└── pytest.ini                     # Pytest configuration
```

### 3.2 Frontend Structure

```
frontend/
├── src/
│   ├── main.tsx                   # React entry point
│   ├── App.tsx                    # Root component with routing
│   ├── api/
│   │   └── client.ts              # Axios API client
│   ├── services/
│   │   ├── auth.ts                # Authentication service
│   │   └── websocket.ts           # WebSocket client
│   ├── components/
│   │   ├── MainLayout.tsx         # Layout with nav
│   │   ├── ProtectedRoute.tsx    # Auth guard component
│   │   ├── NewTradeForm.tsx      # Create trade form
│   │   ├── TradeCard.tsx         # Trade display card
│   │   └── CloseTradeForm.tsx    # Close trade form
│   ├── pages/
│   │   ├── Login.tsx              # Login page
│   │   ├── Dashboard.tsx          # Main dashboard
│   │   ├── History.tsx            # Closed trades
│   │   └── UserProfile.tsx        # User profile
│   └── types/
│       └── index.ts               # TypeScript type definitions
├── package.json                   # Node dependencies
├── vite.config.ts                 # Vite configuration
├── tailwind.config.js             # Tailwind configuration
└── tsconfig.json                  # TypeScript configuration
```

---

## 4. Backend Deep Dive

### 4.1 Application Entry Point (app/main.py)

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.services.websocket_manager import ConnectionManager
from app.routers import trades, setups, auth
```

**Line 1-6 Imports:**

- `FastAPI` - The main application class
- `WebSocket, WebSocketDisconnect` - For real-time price updates (future feature)
- `CORSMiddleware` - Allow frontend (different port) to call backend
- `asynccontextmanager` - Manage application lifecycle (startup/shutdown)
- `settings` - Load environment variables (.env file)
- `ConnectionManager` - WebSocket connection handler
- `trades, setups, auth` - API route modules

```python
# Create singleton WebSocket manager
manager = ConnectionManager()
```

**Singleton Pattern:**
- Only ONE ConnectionManager exists across the entire application
- All WebSocket connections share this single instance
- Ensures consistent state management for WebSocket subscriptions

**Why?** Multiple instances would cause duplicate message broadcasts and inconsistent state.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup
    print("Trading Journal API starting...")
    print(f"📊 Price Service: {'MOCK MODE (Development)' if settings.USE_MOCK_PRICES else 'Yahoo Finance (Production)'}")
    yield
    # On shutdown
    print("Trading Journal API shutting down...")
```

**Lifespan Context Manager:**
- Executes code **before** the application starts (startup)
- Executes code **after** the application stops (shutdown)
- The `yield` statement separates startup and shutdown logic

**Why?**
- Initialize resources (database connections, background tasks)
- Clean up resources on shutdown (close connections, save state)
- Print startup status to console for debugging

```python
app = FastAPI(lifespan=lifespan)
```

**FastAPI Application Instance:**
- Creates the main FastAPI application
- Passes the lifespan manager for startup/shutdown hooks
- This `app` object is what Uvicorn runs

```python
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server (primary)
        "http://localhost:5174",  # Vite dev server (alternate port)
        "http://localhost:3000",  # Alternative dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**CORS (Cross-Origin Resource Sharing):**

**Problem:** By default, browsers block requests from one origin (http://localhost:5173) to another (http://localhost:8000) for security.

**Solution:** CORS middleware tells the browser "It's okay for these origins to call this API."

**Configuration Explanation:**
- `allow_origins` - Which domains can call this API
- `allow_credentials=True` - Allow cookies/auth headers
- `allow_methods=["*"]` - Allow GET, POST, PUT, DELETE, etc.
- `allow_headers=["*"]` - Allow Authorization header (JWT token)

**Why localhost AND 127.0.0.1?**
- Some browsers treat them as different origins
- Including both ensures compatibility

```python
# Include HTTP Routers
app.include_router(auth.router)
app.include_router(trades.router)
app.include_router(setups.router)
```

**Router Registration:**
- Registers all endpoints from each router module
- `auth.router` → /api/v1/auth/* endpoints
- `trades.router` → /api/v1/trades/* endpoints
- `setups.router` → /api/v1/setups/* endpoints

**Why split into routers?**
- **Organization** - Related endpoints grouped together
- **Maintainability** - Easy to find and modify endpoints
- **Modularity** - Can enable/disable entire feature modules
- **Team collaboration** - Different developers work on different routers

```python
# Root endpoint
@app.get("/")
def read_root():
    return {"status": "Trading Journal API is running"}
```

**Health Check Endpoint:**
- Returns a simple JSON response
- Used to verify the API is running
- Common in production deployments (load balancers, monitoring)

**Usage:** `curl http://localhost:8000/` should return `{"status": "..."}`

```python
# WebSocket endpoint
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
```

**WebSocket Endpoint (Future Feature):**

**Current Status:** Implemented but not actively used. Frontend polls for prices instead.

**Purpose:** Real-time price updates without polling.

**Flow:**
1. Client connects → `manager.connect(user_id, websocket)`
2. Client sends `{"type": "subscribe", "tickers": ["INFY", "TCS"]}"`
3. Server subscribes user to those tickers
4. When prices update, server broadcasts to subscribed users
5. Client disconnects → `manager.disconnect(user_id)` cleans up

**Why not used yet?**
- **Simpler to implement** - Polling is easier
- **Good enough** - 5-minute cache means few requests
- **Future enhancement** - Can be enabled later for real-time trading

---

### 4.2 Configuration & Settings (app/core/config.py)

```python
from pydantic_settings import BaseSettings
from pathlib import Path
```

**Imports:**
- `BaseSettings` - Pydantic class for loading environment variables
- `Path` - Cross-platform file path handling

```python
# Get the project root directory (parent of app/)
PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
```

**Path Calculation:**
- `__file__` → `/project/app/core/config.py`
- `.parent` → `/project/app/core/`
- `.parent.parent` → `/project/app/`
- `.parent.parent.parent` → `/project/`
- `/ ".env"` → `/project/.env`

**Why this approach?**
- Works regardless of where Python is run from
- Cross-platform (Windows, macOS, Linux)
- No hardcoded paths

```python
class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str
    MONGO_DB_NAME: str
    USE_MOCK_PRICES: bool = False  # Default to real Yahoo Finance

    # Pydantic v2 style model config
    model_config = {
        "env_file": str(ENV_FILE),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }
```

**Settings Class:**

**Pydantic BaseSettings** automatically:
1. Reads the `.env` file
2. Loads environment variables
3. Validates types (MONGO_CONNECTION_STRING must be str)
4. Provides defaults (USE_MOCK_PRICES defaults to False)

**Configuration Options:**
- `env_file` - Path to .env file
- `env_file_encoding` - UTF-8 for international characters
- `extra="ignore"` - Don't error on extra .env variables

**Why extra="ignore"?**
- `.env` might have old variables from previous versions
- Doesn't break if leftover variables exist
- Flexible for development

```python
settings = Settings()
```

**Singleton Instance:**
- Creates ONE settings object
- Loaded once at startup
- Shared across entire application

**Usage throughout the app:**
```python
from app.core.config import settings

print(settings.MONGO_CONNECTION_STRING)
print(settings.USE_MOCK_PRICES)
```

---

### 4.3 Authentication System (app/core/auth.py)

```python
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
```

**Imports Explained:**

- `datetime, timedelta, timezone` - For JWT expiration times
- `Optional` - Type hint for optional values
- `Depends, HTTPException, status` - FastAPI dependency injection and errors
- `HTTPBearer, HTTPAuthorizationCredentials` - Parse "Bearer <token>" headers
- `jose` - JWT encoding/decoding library
- `passlib` - Password hashing library
- `CryptContext` - Configurable password hasher
- `BaseModel` - Pydantic model for data validation

```python
# JWT Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

**JWT Configuration:**

**SECRET_KEY:**
- Used to sign JWTs (like a password for tokens)
- **CRITICAL**: Change in production!
- If leaked, anyone can create valid tokens

**ALGORITHM:**
- HS256 = HMAC with SHA-256
- Symmetric encryption (same key for signing and verifying)
- Fast and secure for API tokens

**ACCESS_TOKEN_EXPIRE_MINUTES:**
- Tokens valid for 30 minutes
- After 30 min, user must login again
- Security vs. convenience tradeoff

**Why 30 minutes?**
- Long enough for normal usage
- Short enough to limit damage if token stolen
- Can be increased for production (e.g., 7 days)

```python
# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

**Password Hashing:**

**bcrypt:**
- Industry-standard password hashing
- Slow by design (prevents brute force attacks)
- Automatically salts passwords (prevents rainbow tables)

**deprecated="auto":**
- If newer hashing schemes become available, automatically migrate
- Future-proof configuration

**How it works:**
1. User enters password: `"demo123"`
2. bcrypt hashes: `"$2b$12$nhXd..."`
3. Hash stored in database (NOT the plain password)
4. On login, bcrypt compares entered password with hash

**Why NOT store plain passwords?**
- Database breaches happen
- Hash can't be reversed to get original password
- Industry best practice

```python
# Security scheme
security = HTTPBearer()
```

**HTTP Bearer Security:**
- Parses "Authorization: Bearer <token>" headers
- FastAPI uses this to extract JWT tokens
- Returns `HTTPAuthorizationCredentials` object

**Request Flow:**
```
Frontend sends:
GET /api/v1/trades/open
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

FastAPI receives:
credentials.scheme = "Bearer"
credentials.credentials = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

```python
class Token(BaseModel):
    access_token: str
    token_type: str
```

**Token Response Model:**
- Returned from `/login` endpoint
- `access_token` - The JWT string
- `token_type` - Always "bearer" (standard OAuth2)

**Example Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

```python
class TokenData(BaseModel):
    user_id: Optional[str] = None
```

**Token Payload Model:**
- Represents data INSIDE the JWT
- After decoding JWT, we get this structure
- `user_id` - Which user this token belongs to

```python
class User(BaseModel):
    user_id: str
    username: str
    email: Optional[str] = None
```

**User Model:**
- Represents a user without sensitive info
- Returned to frontend
- No password hash included

```python
class UserInDB(User):
    hashed_password: str
```

**User in Database Model:**
- Extends `User` with password hash
- Used internally, NEVER sent to frontend
- Inheritance: UserInDB has all User fields PLUS hashed_password

```python
# Mock user database
fake_users_db = {
    "demo": {
        "user_id": "demo_user_id",
        "username": "demo",
        "email": "demo@example.com",
        "hashed_password": "$2b$12$nhXdAHHELhREj9s.AWAgaemKXz42.zT9AY28i3Yl2mG7wpHaEHVBC",
    }
}
```

**Mock User Database:**

**Current Implementation:**
- Dictionary in memory (resets on restart)
- Only one user: "demo" / "demo123"

**Production:**
- Would be a MongoDB collection
- Look up users by username
- Support registration

**Password Hash:**
- `$2b$12$nhXd...` is the bcrypt hash of "demo123"
- Generated once, stored here
- Cannot be reversed to get original password

```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)
```

**Password Verification:**

**How it works:**
1. User enters: "demo123"
2. We have stored hash: "$2b$12$nhXd..."
3. bcrypt hashes "demo123" with same salt
4. Compares: new hash == stored hash
5. Returns True if match, False otherwise

**Why not just compare strings?**
- bcrypt handles salting and hashing internally
- Time-constant comparison (prevents timing attacks)

```python
def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)
```

**Password Hashing:**

**Usage:**
```python
# When creating a new user
new_password = "mypassword123"
hashed = get_password_hash(new_password)
# Store hashed in database
```

**Output Example:**
```
"mypassword123" → "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
```

**Each hash is unique (even for same password) due to random salt.**

```python
def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate a user by username and password."""
    user_dict = fake_users_db.get(username)
    if not user_dict:
        return None
    user = UserInDB(**user_dict)
    if not verify_password(password, user.hashed_password):
        return None
    return user
```

**User Authentication:**

**Flow:**
1. Get user from database by username
2. If not found → return None (invalid username)
3. Create UserInDB object from dict
4. Verify password against stored hash
5. If password wrong → return None (invalid password)
6. If password correct → return user object

**Why return None instead of raising error?**
- Caller decides how to handle (return 401, log attempt, etc.)
- Separation of concerns (authentication vs. HTTP response)

```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

**JWT Token Creation:**

**How JWT works:**
1. Take payload: `{"sub": "demo_user_id"}`
2. Add expiration: `{"sub": "demo_user_id", "exp": 1734786000}`
3. Sign with SECRET_KEY using HS256
4. Return encoded string

**JWT Structure:**
```
header.payload.signature
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vX3VzZXJfaWQiLCJleHAiOjE3MzQ3ODYwMDB9.signature
```

**Payload contains:**
- `sub` - Subject (user ID)
- `exp` - Expiration timestamp

**Security:**
- Signature prevents tampering
- If payload modified, signature won't match
- Secret key must remain secret

```python
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get the current authenticated user from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    # Find user in fake database
    for username, user_dict in fake_users_db.items():
        if user_dict["user_id"] == token_data.user_id:
            return User(**user_dict)
    
    raise credentials_exception
```

**Get Current User (Dependency):**

**FastAPI Dependency Injection:**
```python
@router.get("/trades/open")
async def get_open_trades(current_user: User = Depends(get_current_user)):
    # current_user is automatically populated
    print(current_user.username)  # "demo"
```

**Flow:**
1. FastAPI calls `security` to parse Authorization header
2. Extracts JWT token
3. Decodes JWT with SECRET_KEY
4. Extracts user_id from payload
5. Looks up user in database
6. Returns User object (or raises 401)

**Error Cases:**
- No Authorization header → 401
- Invalid token → 401
- Expired token → 401
- User not found → 401

**Why async?**
- In production, database lookup is async
- Matches FastAPI async patterns

```python
async def get_current_user_id(current_user: User = Depends(get_current_user)) -> str:
    """Get just the user ID of the current user."""
    return current_user.user_id
```

**Get Current User ID (Convenience Dependency):**

**Why this exists:**
- Many endpoints only need user_id
- Don't need full User object
- Slightly cleaner code

**Usage:**
```python
@router.post("/trades/")
async def create_trade(user_id: str = Depends(get_current_user_id)):
    # user_id = "demo_user_id"
    # No need to access current_user.user_id
```

---

### 4.4 Database Layer (app/db/database.py)

```python
import motor.motor_asyncio
from app.core.config import settings
```

**Motor:**
- Async MongoDB driver for Python
- Built on top of PyMongo
- Works with FastAPI's async patterns

**Why async?**
- FastAPI is async
- Database queries don't block other requests
- Better performance under load

```python
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
database = client[settings.MONGO_DB_NAME]
```

**MongoDB Connection:**

**Connection String Format:**
```
mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
```

**Breakdown:**
- `mongodb+srv://` - Protocol (SRV for automatic server discovery)
- `username:password` - Database credentials
- `cluster.mongodb.net` - MongoDB Atlas cluster URL
- `retryWrites=true` - Retry failed writes
- `w=majority` - Write to majority of nodes (durability)

**Database Selection:**
```python
database = client["trading_journal"]
```
- Accesses the "trading_journal" database
- Collections (tables) live inside this database

```python
def get_trades_collection():
    return database.get_collection("trades")
```

**Get Trades Collection:**

**FastAPI Dependency:**
```python
@router.get("/trades/open")
async def get_open_trades(collection=Depends(get_trades_collection)):
    # collection is MongoDB collection object
    trades = await collection.find({"status": "open"}).to_list()
```

**Why function instead of global variable?**
- **Testability** - Can mock in tests
- **Dependency injection** - FastAPI best practice
- **Flexibility** - Could swap to different collection or database

```python
def get_setups_collection():
    return database.get_collection("setups")
```

**Get Setups Collection:**
- Same pattern as trades
- Separate collection for trading setups
- Setups can be linked to trades via `setup_id`

**MongoDB Collections in this app:**
```
trading_journal (database)
├── trades (collection)
│   └── { _id, user_id, ticker, entryPrice, ... }
└── setups (collection)
    └── { _id, user_id, name, notes }
```

---

### 4.5 Data Models (app/models/)

#### 4.5.1 Common Models (app/models/common.py)

```python
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing import Annotated
```

**Imports:**
- `BaseModel` - Base class for Pydantic models
- `Field` - Add metadata to fields (alias, default, etc.)
- `ConfigDict` - Model configuration
- `BeforeValidator` - Run validation before type checking
- `Annotated` - Add metadata to types

```python
# This ensures we can validate strings as ObjectIds
PyObjectId = Annotated[str, BeforeValidator(str)]
```

**PyObjectId Type:**

**Problem:** MongoDB uses ObjectId, Pydantic uses str

**Solution:** Custom type that:
1. Accepts str or ObjectId
2. Converts to str automatically
3. Type-safe in Python

**Usage:**
```python
class Trade(BaseModel):
    id: PyObjectId  # Can be ObjectId("507f1f77bcf86cd799439011") or "507f1f77bcf86cd799439011"
```

**Why BeforeValidator(str)?**
- If ObjectId passed, converts to string before validation
- If string passed, stays string
- Pydantic then validates as string type

```python
class MongoBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        by_alias=True,
    )
    
    id: PyObjectId | None = Field(alias="_id", default=None)
```

**MongoBaseModel:**

**Purpose:** Base class for all MongoDB documents

**Configuration:**
- `populate_by_name=True` - Allow both field name and alias
- `arbitrary_types_allowed=True` - Allow ObjectId type
- `by_alias=True` - Use alias when serializing

**ID Field:**
```python
id: PyObjectId | None = Field(alias="_id", default=None)
```

**Why alias="_id"?**
- MongoDB uses `_id` field
- Python uses `id` (cleaner, no underscore)
- Alias maps Python `id` ↔ MongoDB `_id`

**Usage:**
```python
# In Python code:
trade.id  # Access as 'id'

# In MongoDB:
{ "_id": ObjectId("..."), ... }

# In JSON:
{ "_id": "507f1f77...", ... }
```

**Why default=None?**
- On creation, _id is None (MongoDB auto-generates)
- After insertion, _id is populated

#### 4.5.2 Trade Models (app/models/trade.py)

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.common import MongoBaseModel, PyObjectId
```

```python
class TradeBase(MongoBaseModel):
    user_id: str  # Which user owns this trade
    ticker: str  # Stock symbol (INFY, TCS, etc.)
    direction: str  # 'bullish' or 'bearish'
    entryPrice: float  # Price entered at
    stopLoss: float  # Stop loss price
    size: int  # Number of shares
    marketConditions: Optional[str] = None  # Market notes
    emotions: Optional[str] = None  # Emotional state
    setup_id: Optional[PyObjectId] = None  # Link to setup
```

**TradeBase:**

**Inheritance:** Inherits from MongoBaseModel
- Gets `id` field automatically
- Gets MongoDB configuration

**Fields Explained:**

**user_id:** Links trade to user
- In production, would reference users collection
- Currently uses fake user IDs

**ticker:** Stock symbol
- Examples: "INFY", "TCS", "RELIANCE"
- Can include exchange suffix: "INFY.NS"

**direction:** Trade direction
- "bullish" - Expecting price to go up
- "bearish" - Expecting price to go down

**entryPrice:** Entry price in INR
- Example: 1450.50
- Stored as float for precision

**stopLoss:** Stop loss price
- Risk management level
- If price hits this, exit trade

**size:** Position size
- Number of shares
- Example: 100 shares

**marketConditions:** Free-text notes
- "Strong uptrend, high volume"
- "Consolidation after earnings"
- Optional field

**emotions:** Emotional state
- "Confident, calm"
- "Anxious, impatient"
- Helps identify emotional trading patterns

**setup_id:** Link to trading setup
- References setups collection
- Optional (can trade without setup)

```python
class TradeCreate(BaseModel):
    ticker: str
    direction: str
    entryPrice: float
    stopLoss: float
    size: int
    entryDate: Optional[datetime] = None  # Manual or auto
    marketConditions: Optional[str] = None
    emotions: Optional[str] = None
    setup_id: Optional[PyObjectId] = None
```

**TradeCreate:**

**Purpose:** What frontend sends to create trade

**No inheritance from MongoBaseModel:**
- Not a database document (yet)
- Just a data transfer object (DTO)

**No user_id:**
- Extracted from JWT token on backend
- User can't spoof other users' IDs

**entryDate Optional:**
- If provided → use that date (manual entry)
- If None → use current time (real-time trading)

```python
class TradeDB(TradeBase):
    status: str = "open"  # 'open' or 'closed'
    entryDate: datetime = Field(default_factory=datetime.now)
    exitPrice: Optional[float] = None
    exitDate: Optional[datetime] = None
    lessonsLearned: Optional[str] = None
    result_pnl: Optional[float] = None  # Calculated on close
```

**TradeDB:**

**Purpose:** What's actually stored in MongoDB

**Inherits TradeBase:**
- Has all TradeBase fields
- Plus database-specific fields

**Fields:**

**status:** Trade lifecycle
- "open" - Active position
- "closed" - Exited position

**entryDate:** When trade was entered
- `default_factory=datetime.now` - Auto-set on creation
- Can be overridden for manual entries

**exitPrice:** Exit price (if closed)
- None for open trades
- Float for closed trades

**exitDate:** When trade was closed
- None for open trades
- datetime for closed trades

**lessonsLearned:** Post-trade reflection
- "Should have waited for confirmation"
- "Emotional decision, ignored stop loss"
- Filled in when closing trade

**result_pnl:** Profit/Loss
- Calculated: `(exitPrice - entryPrice) * size`
- Example: `(1500 - 1450) * 100 = 5000` (₹5000 profit)

```python
class TradeClose(BaseModel):
    exitPrice: float
    lessonsLearned: Optional[str] = None
```

**TradeClose:**

**Purpose:** What frontend sends to close a trade

**Why separate model?**
- Only need exit price and lessons
- Don't want user to modify entry price, size, etc.
- Explicit about what's required to close

```python
class TradeOut(TradeDB):
    pass
```

**TradeOut:**

**Purpose:** What's returned to frontend

**Why separate?**
- Could exclude sensitive fields
- Could add computed fields
- Currently identical to TradeDB

**Usage:**
```python
@router.get("/trades/open", response_model=List[TradeOut])
async def get_open_trades():
    # FastAPI validates response matches TradeOut
```

#### 4.5.3 Setup Models (app/models/setup.py)

```python
class SetupBase(MongoBaseModel):
    user_id: str  # Which user owns this setup
    name: str  # Setup name ("Bull Flag", "Support Bounce")
    notes: Optional[str] = None  # Setup description
```

**SetupBase:**

**Purpose:** Trading setup/strategy

**Examples:**
- "Bull Flag Breakout"
- "Support Level Bounce"
- "Moving Average Crossover"

**notes:** Strategy description
- "Wait for volume confirmation"
- "Must be above 50 MA"
- "Risk:Reward minimum 1:2"

```python
class SetupCreate(BaseModel):
    name: str
    notes: Optional[str] = None
```

**SetupCreate:**
- What frontend sends
- No user_id (extracted from JWT)

```python
class SetupDB(SetupBase):
    pass

class SetupOut(SetupBase):
    pass
```

**SetupDB & SetupOut:**
- Currently identical to SetupBase
- Separate for future extensibility

---

### 4.6 API Routers

#### 4.6.1 Authentication Router (app/routers/auth.py)

```python
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    User,
)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
```

**Router Setup:**
- `prefix` - All endpoints start with /api/v1/auth
- `tags` - Groups endpoints in Swagger UI

```python
class LoginRequest(BaseModel):
    username: str
    password: str
```

**LoginRequest:**

**Why separate model?**
- Could add extra fields (remember_me, device_id)
- Explicit about what login accepts
- Type-safe validation

```python
@router.post("/login", response_model=Token)
async def login(request: LoginRequest):
    """
    Login with username and password to get an access token.
    
    Demo credentials:
    - Username: demo
    - Password: demo123
    """
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
```

**Login Endpoint:**

**Flow:**
1. Receive username & password
2. Authenticate user (check password hash)
3. If invalid → 401 error
4. If valid → Create JWT token
5. Return token

**Why "WWW-Authenticate: Bearer"?**
- HTTP standard for auth challenges
- Tells client to use Bearer token auth
- Required by OAuth2 specification

**Token Payload:**
```python
data={"sub": user.user_id}
```
- `sub` is JWT standard for "subject" (user ID)
- Could add more claims: `{"sub": "user123", "role": "admin"}`

```python
@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user
```

**Get Current User Endpoint:**

**Purpose:** Verify token and get user info

**Flow:**
1. Frontend sends: `Authorization: Bearer <token>`
2. `get_current_user` dependency validates token
3. Returns user info

**Usage:**
```typescript
// Frontend
const user = await fetch('/api/v1/auth/me', {
  headers: { 'Authorization': `Bearer ${token}` }
});
// Returns: { user_id: "demo_user_id", username: "demo", email: "..." }
```

**Why needed?**
- Verify token still valid
- Get fresh user data
- Check authentication on app load

#### 4.6.2 Trades Router (app/routers/trades.py)

This is the largest router with all trade management endpoints.

```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.database import get_trades_collection
from app.models.trade import TradeCreate, TradeClose, TradeOut, TradeDB
from bson import ObjectId
from typing import List
from datetime import datetime
from app.core.config import settings
from app.services.currency_service import currency_service
from app.core.auth import get_current_user_id

router = APIRouter(
    prefix="/api/v1/trades", 
    tags=["Trades"],
)
```

**Create Trade Endpoint:**

```python
@router.post("/", response_model=TradeOut, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
async def create_trade(
    trade: TradeCreate,
    collection=Depends(get_trades_collection),
    user_id: str = Depends(get_current_user_id)
):
    trade_data = trade.model_dump()
    # Set entryDate if not provided
    if not trade_data.get('entryDate'):
        trade_data['entryDate'] = datetime.now()
    
    trade_db = TradeDB(
        **trade_data,
        user_id=user_id,
        status="open"
    )
    # Exclude None values to let MongoDB auto-generate _id
    new_trade = await collection.insert_one(trade_db.model_dump(by_alias=True, exclude_none=True))
    created_trade = await collection.find_one({"_id": new_trade.inserted_id})
    return TradeOut.model_validate(created_trade)
```

**Create Trade Flow:**

1. **Receive trade from frontend:**
   ```json
   {
     "ticker": "INFY",
     "direction": "bullish",
     "entryPrice": 1450.50,
     "stopLoss": 1400.00,
     "size": 100
   }
   ```

2. **Convert to dict:** `trade.model_dump()`

3. **Set entryDate if missing:**
   - If manual entry → use provided date
   - If real-time → use datetime.now()

4. **Create TradeDB object:**
   - Spread trade_data fields
   - Add user_id from JWT
   - Set status="open"

5. **Insert to MongoDB:**
   ```python
   await collection.insert_one({
     "ticker": "INFY",
     "direction": "bullish",
     "entryPrice": 1450.50,
     "stopLoss": 1400.00,
     "size": 100,
     "user_id": "demo_user_id",
     "status": "open",
     "entryDate": "2025-10-21T10:30:00"
   })
   ```

6. **MongoDB auto-generates _id**

7. **Fetch created trade:**
   ```python
   await collection.find_one({"_id": ObjectId("507f1f77...")})
   ```

8. **Return to frontend:**
   ```json
   {
     "_id": "507f1f77...",
     "ticker": "INFY",
     ...
   }
   ```

**Why response_model_by_alias=True?**
- Returns `_id` (MongoDB convention) instead of `id`
- Frontend expects `_id` field

**Why status_code=201?**
- HTTP 201 = Created (success resource creation)
- Semantic REST API design

**Get Open Trades:**

```python
@router.get("/open", response_model=List[TradeOut], response_model_by_alias=True)
async def get_open_trades(
    collection=Depends(get_trades_collection),
    user_id: str = Depends(get_current_user_id)
):
    trades = []
    cursor = collection.find({"user_id": user_id, "status": "open"})
    async for doc in cursor:
        trades.append(TradeOut.model_validate(doc))
    return trades
```

**Flow:**

1. **MongoDB query:**
   ```python
   collection.find({"user_id": "demo_user_id", "status": "open"})
   ```
   - Only this user's trades
   - Only open trades

2. **Async iteration:**
   ```python
   async for doc in cursor:
   ```
   - Cursor is lazy (doesn't load all at once)
   - Async prevents blocking

3. **Validate each document:**
   ```python
   TradeOut.model_validate(doc)
   ```
   - Ensures MongoDB data matches model
   - Catches schema mismatches

4. **Return list:**
   ```json
   [
     { "_id": "...", "ticker": "INFY", "status": "open", ... },
     { "_id": "...", "ticker": "TCS", "status": "open", ... }
   ]
   ```

**Get Closed Trades:**

```python
@router.get("/closed", response_model=List[TradeOut], response_model_by_alias=True)
async def get_closed_trades(
    collection=Depends(get_trades_collection),
    user_id: str = Depends(get_current_user_id)
):
    trades = []
    cursor = collection.find({"user_id": user_id, "status": "closed"})
    async for doc in cursor:
        trades.append(TradeOut.model_validate(doc))
    return trades
```

**Same pattern as open trades, but:**
- Filter: `"status": "closed"`
- Returns trades with exitPrice, exitDate, result_pnl

**Close Trade Endpoint:**

```python
@router.put("/{trade_id}/close", response_model=TradeOut, response_model_by_alias=True)
async def close_trade(
    trade_id: str,
    trade_close: TradeClose,
    collection=Depends(get_trades_collection),
    user_id: str = Depends(get_current_user_id)
):
    trade_oid = ObjectId(trade_id)
    trade_db = await collection.find_one({"_id": trade_oid, "user_id": user_id})
    
    if not trade_db:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    trade = TradeDB.model_validate(trade_db)
    
    if trade.status == "closed":
        raise HTTPException(status_code=400, detail="Trade is already closed")

    # This is the core P&L calculation logic
    result_pnl = (trade_close.exitPrice - trade.entryPrice) * trade.size
    
    update_data = {
        "$set": {
            "exitPrice": trade_close.exitPrice,
            "lessonsLearned": trade_close.lessonsLearned,
            "exitDate": datetime.now(),
            "status": "closed",
            "result_pnl": result_pnl
        }
    }
    
    await collection.update_one({"_id": trade_oid}, update_data)
    
    updated_trade = await collection.find_one({"_id": trade_oid})
    return TradeOut.model_validate(updated_trade)
```

**Close Trade Flow:**

1. **Receive close request:**
   ```
   PUT /api/v1/trades/507f1f77.../close
   Body: { "exitPrice": 1500.00, "lessonsLearned": "..." }
   ```

2. **Convert trade_id to ObjectId:**
   ```python
   trade_oid = ObjectId("507f1f77bcf86cd799439011")
   ```

3. **Find trade:**
   ```python
   find_one({"_id": ObjectId("..."), "user_id": "demo_user_id"})
   ```
   - Ensures user owns this trade
   - Prevents users closing other users' trades

4. **Validate trade exists:**
   ```python
   if not trade_db:
       raise HTTPException(status_code=404)
   ```

5. **Check not already closed:**
   ```python
   if trade.status == "closed":
       raise HTTPException(status_code=400)
   ```

6. **Calculate P&L:**
   ```python
   result_pnl = (1500.00 - 1450.50) * 100 = 4950
   ```
   - Positive = profit
   - Negative = loss

7. **Update in MongoDB:**
   ```python
   collection.update_one(
     {"_id": ObjectId("...")},
     {"$set": {
       "exitPrice": 1500.00,
       "exitDate": "2025-10-21T14:30:00",
       "status": "closed",
       "result_pnl": 4950
     }}
   )
   ```

8. **Return updated trade:**
   ```json
   {
     "_id": "...",
     "ticker": "INFY",
     "entryPrice": 1450.50,
     "exitPrice": 1500.00,
     "size": 100,
     "result_pnl": 4950,
     "status": "closed"
   }
   ```

**Delete Trade:**

```python
@router.delete("/{trade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trade(
    trade_id: str,
    collection=Depends(get_trades_collection),
    user_id: str = Depends(get_current_user_id)
):
    """Permanently delete a trade from the database."""
    trade_oid = ObjectId(trade_id)
    result = await collection.delete_one({"_id": trade_oid, "user_id": user_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    return None
```

**Delete Flow:**

1. **MongoDB delete:**
   ```python
   delete_one({"_id": ObjectId("..."), "user_id": "demo_user_id"})
   ```
   - Only deletes if user owns trade
   - Returns delete result

2. **Check if deleted:**
   ```python
   if result.deleted_count == 0:
   ```
   - 0 = trade not found or not owned
   - 1 = successfully deleted

3. **Return 204:**
   - HTTP 204 = No Content
   - Success but no response body
   - Standard for DELETE operations

**Statistics Endpoint:**

```python
@router.get("/statistics")
async def get_statistics(
    collection=Depends(get_trades_collection),
    user_id: str = Depends(get_current_user_id)
):
    """Get trading statistics including win rate."""
    # Get all closed trades
    closed_trades = []
    cursor = collection.find({"user_id": user_id, "status": "closed"})
    async for doc in cursor:
        closed_trades.append(doc)
    
    total_closed = len(closed_trades)
    winning_trades = sum(1 for trade in closed_trades if trade.get("result_pnl", 0) > 0)
    losing_trades = sum(1 for trade in closed_trades if trade.get("result_pnl", 0) < 0)
    breakeven_trades = sum(1 for trade in closed_trades if trade.get("result_pnl", 0) == 0)
    
    win_rate = (winning_trades / total_closed * 100) if total_closed > 0 else 0
    
    total_pnl = sum(trade.get("result_pnl", 0) for trade in closed_trades)
    
    return {
        "total_closed_trades": total_closed,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "breakeven_trades": breakeven_trades,
        "win_rate": round(win_rate, 2),
        "total_pnl": round(total_pnl, 2)
    }
```

**Statistics Calculation:**

1. **Fetch all closed trades:**
   ```python
   collection.find({"user_id": "demo_user_id", "status": "closed"})
   ```

2. **Count trades:**
   ```python
   total_closed = 10
   ```

3. **Count winning trades:**
   ```python
   winning_trades = sum(1 for trade if trade.result_pnl > 0)
   # If 6 trades have positive P&L → 6
   ```

4. **Count losing trades:**
   ```python
   losing_trades = sum(1 for trade if trade.result_pnl < 0)
   # If 4 trades have negative P&L → 4
   ```

5. **Calculate win rate:**
   ```python
   win_rate = (6 / 10) * 100 = 60.0
   ```

6. **Sum total P&L:**
   ```python
   total_pnl = sum(trade.result_pnl for all trades)
   # 5000 + 3000 - 2000 + 1500 - 500 + ... = 15000
   ```

7. **Return statistics:**
   ```json
   {
     "total_closed_trades": 10,
     "winning_trades": 6,
     "losing_trades": 4,
     "breakeven_trades": 0,
     "win_rate": 60.0,
     "total_pnl": 15000.00
   }
   ```

**Quote Endpoint:**

```python
@router.get('/quotes/{ticker}')
async def get_quote(ticker: str, use_mock: bool = False):
    """Fetch a current quote for a ticker from Yahoo Finance."""
    # Use mock service if requested or if configured in settings
    use_mock_data = use_mock or settings.USE_MOCK_PRICES
    
    if use_mock_data:
        from app.services.mock_price_service import mock_price_service
        price_service = mock_price_service
    else:
        from app.services.yahoo_finance_service import yahoo_service
        price_service = yahoo_service
    
    try:
        # Get quote from selected service
        quote = price_service.get_quote(ticker)
        
        # Add mock flag if using mock data
        response_data = {
            "found": True,
            "ticker": quote['ticker'],
            "name": quote['name'],
            "exchange": quote['exchange'],
            "is_indian": quote['is_indian'],
            "suggestions": []
        }
        
        if use_mock_data:
            response_data['mock'] = True
            response_data['message'] = 'Using mock data for development'
        
        # Only show prices for Indian stocks (INR)
        if quote['currency'] == 'INR' and quote['is_indian']:
            response_data.update({
                "price": quote['price'],
                "price_inr": quote['price'],
                "price_usd": None,
                "exchange_rate": None,
            })
            return response_data
        
        # For non-Indian stocks, return N/A
        response_data.update({
            "price": None,
            "price_inr": None,
            "price_usd": None,
            "exchange_rate": None,
        })
        if not use_mock_data:
            response_data['message'] = "Only Indian stocks (NSE/BSE) are supported"
        return response_data
        
    except ValueError as e:
        return {
            "found": False,
            "price": None,
            "price_inr": None,
            "price_usd": None,
            "exchange_rate": None,
            "suggestions": [],
            "error": str(e)
        }
```

**Quote Endpoint Flow:**

1. **Decide service:**
   ```python
   if use_mock or settings.USE_MOCK_PRICES:
       service = mock_price_service  # Fake prices
   else:
       service = yahoo_service  # Real Yahoo Finance
   ```

2. **Fetch quote:**
   ```python
   quote = price_service.get_quote("INFY")
   # Returns: {
   #   'ticker': 'INFY.NS',
   #   'price': 1450.50,
   #   'currency': 'INR',
   #   'exchange': 'NSE',
   #   'name': 'Infosys Limited',
   #   'is_indian': True
   # }
   ```

3. **Filter by currency:**
   ```python
   if quote['currency'] == 'INR' and quote['is_indian']:
       # Show price for Indian stocks
   else:
       # Return N/A for non-Indian stocks
   ```

4. **Return response:**
   ```json
   {
     "found": true,
     "ticker": "INFY.NS",
     "price": 1450.50,
     "price_inr": 1450.50,
     "name": "Infosys Limited",
     "exchange": "NSE",
     "is_indian": true
   }
   ```

**Service Status Endpoint:**

```python
@router.get('/service-status')
async def get_service_status():
    """Get Yahoo Finance service status including rate limit state."""
    from app.services.yahoo_finance_service import yahoo_service
    return yahoo_service.get_status()
```

**Returns:**
```json
{
  "cache_entries": 5,
  "cache_duration_seconds": 300,
  "ticker_format_cache_entries": 3,
  "consecutive_429s": 0,
  "rate_limited": false,
  "message": "Service operational. Quotes cached for 5 minutes."
}
```

---

### 4.7 Yahoo Finance Service (Deep Dive)

This is the most complex service - handles rate limiting, caching, and multiple ticker formats.

```python
import yfinance as yf
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import time
```

**yfinance Library:**
- Unofficial Yahoo Finance API
- Free, no API key needed
- Rate limited (~100-200 requests/hour)

```python
class YahooFinanceService:
    """Service for fetching stock data from Yahoo Finance."""
    
    def __init__(self):
        # Cache to prevent rate limiting
        self._cache: Dict[str, Dict] = {}
        self._cache_duration = timedelta(minutes=5)  # Cache for 5 minutes
        self._ticker_format_cache: Dict[str, str] = {}  # Remember which format worked
        self._pending_requests: Dict[str, list] = {}  # Deduplicate concurrent requests
        self._last_request_time: Optional[datetime] = None
        self._min_request_interval = timedelta(seconds=3)  # Min 3 seconds between requests
        self._rate_limit_hit: Optional[datetime] = None
        self._rate_limit_cooldown = timedelta(minutes=10)  # Wait 10 min after 429
        self._consecutive_429s = 0  # Track consecutive 429 errors
```

**Data Structures Explained:**

**_cache:**
```python
{
  "INFY": {
    "ticker": "INFY.NS",
    "price": 1450.50,
    "currency": "INR",
    "cached_at": datetime(2025, 10, 21, 10, 30, 0)
  }
}
```
- Stores recent quotes
- Keyed by uppercase ticker
- Includes cached_at timestamp

**_ticker_format_cache:**
```python
{
  "INFY": "INFY.NS",  # Remember to try .NS first
  "TCS": "TCS.NS",
  "RELIANCE": "RELIANCE.NS"
}
```
- Remembers which format worked
- Avoids trying multiple formats every time
- Optimization: 1 API call instead of 3-5

**_last_request_time:**
- Timestamp of last API call
- Used to enforce 3-second delay
- Prevents rapid-fire requests

**_rate_limit_hit:**
- Timestamp when 429 error received
- Triggers cooldown mode
- Prevents further API calls until cooldown expires

**_consecutive_429s:**
- Counts consecutive 429 errors
- Increases cooldown duration exponentially
- Gives Yahoo Finance more time to reset

```python
# Indian stock exchanges
NSE_SUFFIX = ".NS"  # National Stock Exchange
BSE_SUFFIX = ".BO"  # Bombay Stock Exchange
```

**Indian Stock Exchanges:**

**NSE (National Stock Exchange):**
- Primary Indian exchange
- Most liquid
- Yahoo Finance format: INFY.NS

**BSE (Bombay Stock Exchange):**
- Older Indian exchange
- Less liquid
- Yahoo Finance format: INFY.BO

**Why both?**
- Same stock trades on both exchanges
- Different prices (arbitrage opportunities)
- Try NSE first (more liquid)

```python
# Known Indian stocks
INDIAN_STOCKS = {
    "INFY": "INFY.NS",
    "TCS": "TCS.NS",
    "RELIANCE": "RELIANCE.NS",
    # ... more stocks
}
```

**Indian Stocks Dictionary:**

**Purpose:** Quick lookup for common Indian stocks

**Why needed?**
- User types "INFY" (no suffix)
- We know to try "INFY.NS" first
- Saves API calls

**Rate Limit Delay:**

```python
def _rate_limit_delay(self):
    """Enforce minimum delay between API requests."""
    if self._last_request_time:
        elapsed = datetime.now() - self._last_request_time
        if elapsed < self._min_request_interval:
            sleep_time = (self._min_request_interval - elapsed).total_seconds()
            time.sleep(sleep_time)
    self._last_request_time = datetime.now()
```

**Flow:**

1. **Calculate elapsed time:**
   ```python
   elapsed = now - last_request_time
   # If last request was 1 second ago, elapsed = 1 second
   ```

2. **Check if too soon:**
   ```python
   if elapsed < 3 seconds:
   ```

3. **Sleep remaining time:**
   ```python
   sleep_time = 3 - 1 = 2 seconds
   time.sleep(2)  # Wait 2 more seconds
   ```

4. **Update last request time:**
   ```python
   self._last_request_time = datetime.now()
   ```

**Result:** Minimum 3 seconds between Yahoo Finance API calls.

**Try Ticker Formats:**

```python
def _try_ticker_formats(self, ticker: str) -> Tuple[Optional[yf.Ticker], str]:
    cache_key = ticker.upper()
    
    # Try cached format first
    if cache_key in self._ticker_format_cache:
        cached_format = self._ticker_format_cache[cache_key]
        try:
            self._rate_limit_delay()
            stock = yf.Ticker(cached_format)
            info = stock.info
            if info and 'currentPrice' in info and info['currentPrice']:
                return stock, cached_format
        except Exception as e:
            if '429' in str(e):
                self._handle_429_error()
                return None, ticker
    
    # Try formats in order
    formats_to_try = []
    
    # If in INDIAN_STOCKS map, try NSE first
    if cache_key in self.INDIAN_STOCKS:
        formats_to_try.append(self.INDIAN_STOCKS[cache_key])
        formats_to_try.append(cache_key + self.BSE_SUFFIX)
    
    # Try original ticker
    formats_to_try.append(cache_key)
    
    # Try with suffixes
    if not (ticker.endswith(self.NSE_SUFFIX) or ticker.endswith(self.BSE_SUFFIX)):
        formats_to_try.append(cache_key + self.NSE_SUFFIX)
        formats_to_try.append(cache_key + self.BSE_SUFFIX)
    
    for ticker_format in formats_to_try:
        try:
            self._rate_limit_delay()
            stock = yf.Ticker(ticker_format)
            info = stock.info
            
            if info and 'currentPrice' in info and info['currentPrice']:
                # Cache successful format
                self._ticker_format_cache[cache_key] = ticker_format
                self._consecutive_429s = 0  # Reset error counter
                return stock, ticker_format
                
        except Exception as e:
            if '429' in str(e):
                self._handle_429_error()
                break
            continue
    
    return None, ticker
```

**Ticker Format Resolution:**

**Example: User enters "INFY"**

**Step 1: Check format cache:**
```python
if "INFY" in self._ticker_format_cache:
    # Previously found "INFY.NS" works
    # Try that first (1 API call instead of 5)
```

**Step 2: Build format list:**
```python
formats_to_try = [
    "INFY.NS",  # In INDIAN_STOCKS map
    "INFY.BO",  # BSE alternative
    "INFY",     # Original
]
```

**Step 3: Try each format:**
```python
for format in formats_to_try:
    try:
        stock = yf.Ticker("INFY.NS")
        if stock.info['currentPrice']:
            # Found valid price!
            # Cache "INFY" → "INFY.NS"
            return stock, "INFY.NS"
    except:
        continue
```

**Step 4: Return result:**
- If found → `(stock_object, "INFY.NS")`
- If not found → `(None, "INFY")`

**Handle 429 Error:**

```python
def _handle_429_error(self):
    """Handle rate limit errors with exponential backoff."""
    self._consecutive_429s += 1
    self._rate_limit_hit = datetime.now()
    
    # Increase cooldown based on consecutive errors
    if self._consecutive_429s >= 3:
        cooldown_minutes = 10
    elif self._consecutive_429s >= 2:
        cooldown_minutes = 7
    else:
        cooldown_minutes = 5
    
    self._rate_limit_cooldown = timedelta(minutes=cooldown_minutes)
    print(f"🚫 RATE LIMIT HIT (#{self._consecutive_429s})! Entering {cooldown_minutes}-minute cooldown.")
```

**Exponential Backoff:**

**First 429 error:**
- `_consecutive_429s = 1`
- Cooldown = 5 minutes
- Message: "RATE LIMIT HIT (#1)! Entering 5-minute cooldown."

**Second consecutive 429:**
- `_consecutive_429s = 2`
- Cooldown = 7 minutes
- Service is more aggressive in backing off

**Third+ consecutive 429:**
- `_consecutive_429s = 3`
- Cooldown = 10 minutes
- Maximum backoff

**Why exponential backoff?**
- Gives Yahoo Finance time to reset limits
- Prevents infinite retry loops
- Shows we're a "good citizen" of the API

**Get Quote (Main Method):**

```python
def get_quote(self, ticker: str) -> Dict:
    # Check cache first
    cache_key = ticker.upper()
    
    # If in cooldown, ALWAYS return cache
    if self._rate_limit_hit:
        if datetime.now() - self._rate_limit_hit < self._rate_limit_cooldown:
            if cache_key in self._cache:
                print(f"🚫 In rate limit cooldown, returning cache for {ticker}")
                cached_data = self._cache[cache_key]
                result = {k: v for k, v in cached_data.items() if k != 'cached_at'}
                return result
            else:
                raise ValueError(f"Rate limit cooldown active, no cached data for {ticker}")
        else:
            # Cooldown expired, reset
            print("✅ Rate limit cooldown expired, resuming API calls")
            self._rate_limit_hit = None
    
    # Check normal cache
    if cache_key in self._cache:
        cached_data = self._cache[cache_key]
        if datetime.now() - cached_data['cached_at'] < self._cache_duration:
            result = {k: v for k, v in cached_data.items() if k != 'cached_at'}
            return result
    
    # Fetch from Yahoo Finance
    stock, actual_ticker = self._try_ticker_formats(ticker)
    
    if not stock:
        # Return stale cache if available
        if cache_key in self._cache:
            print(f"⚠️ Rate limit likely hit, returning stale cache for {ticker}")
            cached_data = self._cache[cache_key]
            result = {k: v for k, v in cached_data.items() if k != 'cached_at'}
            return result
        raise ValueError(f"Could not find valid data for ticker: {ticker}")
    
    try:
        info = stock.info
        
        # Extract price
        current_price = info.get('currentPrice') or info.get('regularMarketPrice')
        if not current_price:
            raise ValueError(f"No price data available for {actual_ticker}")
        
        # Extract metadata
        currency = info.get('currency', 'USD')
        exchange = info.get('exchange', 'Unknown')
        name = info.get('longName') or info.get('shortName', actual_ticker)
        
        # Determine if Indian stock
        is_indian = (
            actual_ticker.endswith(self.NSE_SUFFIX) or 
            actual_ticker.endswith(self.BSE_SUFFIX) or
            exchange in ['NSI', 'BOM', 'NSE', 'BSE']
        )
        
        result = {
            'ticker': actual_ticker,
            'price': float(current_price),
            'currency': currency,
            'exchange': exchange,
            'name': name,
            'is_indian': is_indian
        }
        
        # Cache the result
        self._cache[cache_key] = {
            **result,
            'cached_at': datetime.now()
        }
        
        return result
        
    except Exception as e:
        raise ValueError(f"Error fetching data for {actual_ticker}: {str(e)}")
```

**Get Quote Flow:**

**1. Check rate limit cooldown:**
```python
if in_cooldown:
    return cached_data  # Don't make API calls
```

**2. Check normal cache:**
```python
if cache_valid:
    return cached_data  # Cache hit, no API call
```

**3. Fetch from Yahoo Finance:**
```python
stock, ticker = self._try_ticker_formats("INFY")
# Returns: (stock_object, "INFY.NS")
```

**4. Extract price data:**
```python
info = stock.info  # Dictionary of stock data
current_price = info['currentPrice']  # 1450.50
```

**5. Extract metadata:**
```python
{
  'ticker': 'INFY.NS',
  'price': 1450.50,
  'currency': 'INR',
  'exchange': 'NSE',
  'name': 'Infosys Limited',
  'is_indian': True
}
```

**6. Cache result:**
```python
self._cache["INFY"] = {
  ...result,
  'cached_at': datetime(2025, 10, 21, 10, 30, 0)
}
```

**7. Return result:**
```python
return {
  'ticker': 'INFY.NS',
  'price': 1450.50,
  ...
}
```

**Get Status:**

```python
def get_status(self) -> Dict:
    """Get current service status including rate limit state."""
    now = datetime.now()
    status = {
        'cache_entries': len(self._cache),
        'cache_duration_seconds': int(self._cache_duration.total_seconds()),
        'ticker_format_cache_entries': len(self._ticker_format_cache),
        'consecutive_429s': self._consecutive_429s,
    }
    
    if self._rate_limit_hit:
        time_since_hit = now - self._rate_limit_hit
        cooldown_remaining = self._rate_limit_cooldown - time_since_hit
        
        if cooldown_remaining.total_seconds() > 0:
            status['rate_limited'] = True
            status['cooldown_remaining_seconds'] = int(cooldown_remaining.total_seconds())
            status['cooldown_remaining_minutes'] = round(cooldown_remaining.total_seconds() / 60, 1)
            status['message'] = f"Rate limited. Cooldown ends in {int(cooldown_remaining.total_seconds() / 60)} min {int(cooldown_remaining.total_seconds() % 60)} sec."
        else:
            status['rate_limited'] = False
            status['message'] = "Cooldown expired, API calls resumed"
            self._rate_limit_hit = None
    else:
        status['rate_limited'] = False
        status['message'] = "Service operational. Quotes cached for 5 minutes."
    
    return status
```

**Status Response Examples:**

**Normal operation:**
```json
{
  "cache_entries": 5,
  "cache_duration_seconds": 300,
  "ticker_format_cache_entries": 3,
  "consecutive_429s": 0,
  "rate_limited": false,
  "message": "Service operational. Quotes cached for 5 minutes."
}
```

**During rate limit:**
```json
{
  "cache_entries": 5,
  "cache_duration_seconds": 300,
  "ticker_format_cache_entries": 3,
  "consecutive_429s": 1,
  "rate_limited": true,
  "cooldown_remaining_seconds": 247,
  "cooldown_remaining_minutes": 4.1,
  "message": "Rate limited. Cooldown ends in 4 min 7 sec."
}
```

---

## 5. Frontend Deep Dive

This section explains every key frontend file, line by line where useful, plus the design rationale behind routing, state, API access, authentication, styling, polling, and optional WebSocket wiring.

### 5.1 Entry Point (frontend/src/main.tsx)

```ts
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
```
- StrictMode guards against legacy patterns in dev and surfaces warnings.
- createRoot with the non-null assertion (!) because the element exists in index.html.
- Global CSS via index.css, Tailwind utilities are injected at build.
- Renders App, which owns routing and layout.

### 5.2 Application Router (frontend/src/App.tsx)

Key ideas:
- Public /login route; all other routes are protected by a small auth gate.
- MainLayout wraps protected pages to share navigation, actions, and consistent spacing.

Important bits:
- ProtectedRoute checks authService.isAuthenticated(). If false, it redirects to /login.
- Navigate catch-all sends unknown paths to the dashboard for a simple UX.

### 5.3 API Client and Endpoints (frontend/src/api/client.ts)

- Axios instance configured with baseURL from Vite env var VITE_API_BASE_URL, falling back to http://localhost:8000.
- Request interceptor: injects Authorization: Bearer <JWT> if present.
- Response interceptor: on 401, clears session and hard-redirects to /login (robust for any page).
- tradesApi implements trade CRUD, statistics, and quote fetching against FastAPI endpoints.
- setupsApi provides setup CRUD (create, list).

Rationale:
- Centralizing HTTP config avoids duplication and keeps auth consistent.
- Hard redirect for 401s guarantees a reset of component state after logout/expiry.

### 5.4 Authentication Service (frontend/src/services/auth.ts)

- Stores the JWT and user in localStorage under TOKEN_KEY and USER_KEY.
- login() posts to /api/v1/auth/login, saves token, then calls /me to cache the user.
- fetchUserInfo() reads /me using the stored token and handles 401 by clearing session.
- logout() drops tokens and user cache.

Rationale:
- LocalStorage is fine for a personal app; for multi-user production, prefer httpOnly cookies + CSRF.
- Keeping a minimal user object locally improves perceived performance on reloads.

### 5.5 Layout and Route Guard (frontend/src/components/MainLayout.tsx, ProtectedRoute.tsx)

- MainLayout: top nav with Active Trades, History, Profile, and Logout; highlights the active route using location.
- ProtectedRoute: renders children if authenticated; otherwise <Navigate to="/login"/>.

Rationale:
- Simple and explicit composition over complex nesting.
- Keeps route declarations straightforward in App.tsx.

### 5.6 Feature Components

- NewTradeForm: modal form to create a trade. Extras:
  - Quote check button calls GET /quotes/{ticker}.
  - Shows INR price formatting, suggests alternatives if not found.
  - Computes P&L preview given the current checked price and form fields.
- TradeCard: read-only card for a trade with badges, formatted numbers, and P&L summary.
- CloseTradeForm: modal to capture exit price and lessons; previews projected P&L.
- AlertBanner: transient, animated alert banner (e.g., stop-loss) with Tailwind keyframe.

Design choices:
- Minimal state per component; parent orchestrates lists and selections.
- Heavy UI feedback (colors, formatting) to make scanning easy for a non-technical user.

### 5.7 Pages

- Login:
  - Calls authService.login; on success, navigate to "/".
  - Error panel explains why login failed (e.g., wrong credentials or network error).
- Dashboard:
  - Loads open trades and statistics on mount.
  - Maintains local prices map keyed by ticker.
  - Polls every 30s for prices (only Indian tickers) to respect Yahoo Finance limits.
  - Integrates optional WebSocket client for future real-time streaming; currently used for subscription messages and alert events, not for prices.
  - Provides NewTrade modal and CloseTrade modal lifecycles.
- History:
  - Lists closed trades with delete action.
- UserProfile:
  - Shows cached user info and supports logout.

Rate-limit-aware polling (Dashboard):
- Filters tickers to .NS and .BO or non-US patterns before requesting quotes.
- Defers to backend caching/backoff; frontend keeps interval conservative (30s) to minimize calls.

### 5.8 WebSocket Client (frontend/src/services/websocket.ts)

- Resilient client with exponential backoff reconnection up to 30s.
- API:
  - connect()/disconnect()
  - subscribe(tickers)
  - onMessage/onPriceUpdate/onAlert registration and removal
- Singleton export getWebSocketService ensures only one socket instance per tab.

Rationale:
- Keeps a path open to low-latency updates later without changing page code.
- Today, prices are polled; tomorrow, they can be streamed by switching backend.

### 5.9 Shared Types (frontend/src/types/index.ts)

- Trade, TradeCreate, TradeClose align 1:1 with backend Pydantic models.
- WebSocket message union types (PriceUpdate | Alert) ensure exhaustive handling in components.

### 5.10 Styling (Tailwind, index.css)

- Tailwind preset with a custom slide-in animation for the alert banner.
- Component classes emphasize readability and clear affordances.
- Currency formatting uses toLocaleString("en-IN") for INR grouping and decimals.

### 5.11 Build Tooling and Configs

- Vite (frontend/vite.config.ts): React plugin with React Compiler enabled.
- Tailwind (frontend/tailwind.config.js): content globs and keyframes for slide-in.
- TypeScript (frontend/tsconfig.*): strict settings with noUnusedLocals/Parameters; vite/client and node types split.
- ESLint (frontend/eslint.config.js): JS + TS + react-hooks + react-refresh rules; dist ignored.

Why these defaults:
- Strong TS and ESLint rules catch dead code and mistakes early.
- React Compiler improves runtime performance with minimal code changes.

### 5.12 Frontend Error Handling and UX

- Auth: 401 globally handled by Axios; user is redirected to login with a clean session.
- Network: login form shows precise error details; list pages show Loading… and safe fallbacks.
- Quotes: on failure, UI avoids spinners getting stuck and shows N/A gracefully.

### 5.13 End-to-End Flow (Frontend ↔ Backend)

1) User logs in (POST /auth/login) → token saved → /auth/me fetched → user cached.
2) Dashboard mounts → open trades + statistics fetched.
3) Prices are fetched initially and every 30s for Indian tickers only.
4) New trade → immediate optimistic price display if recent quote exists.
5) Close trade → server computes realized P&L → list refresh.

### 5.14 Frontend Testing Pointers (future)

- Component tests: render forms and cards with React Testing Library.
- API tests: mock axios with MSW; assert 401 and happy paths.
- E2E: Playwright/Cypress to verify login → create → close → history flow.

---

## 6. Deployment Guide

### 6.1 Current Status: ✅ READY FOR DEPLOYMENT

All features complete. Yahoo Finance rate limiting fixed but requires waiting period or mock mode.

**Deployment Checklist:**

**Backend (FastAPI):**
- ✅ All features implemented
- ✅ Authentication (JWT)
- ✅ MongoDB connection
- ✅ Yahoo Finance with ONE-REQUEST fix
- ✅ Mock mode for development
- ⚠️ Change SECRET_KEY in production
- ⚠️ Set USE_MOCK_PRICES=false for production

**Frontend (React/Vite):**
- ✅ All features implemented
- ✅ Dashboard with live prices
- ✅ Trade management
- ✅ Statistics
- ✅ Authentication
- ✅ 30-second polling (good)

**Database (MongoDB):**
- ✅ Collections: trades, setups
- ✅ User isolation
- ✅ Async operations

### 6.2 Yahoo Finance Rate Limit Fix Summary

**Problem:**
- Multiple ticker format attempts (INFY.NS, INFY.BO, INFY, etc.) = 5+ API calls per ticker
- Rate limit hit immediately (429 errors)
- No cooldown enforcement

**Solution Implemented:**
- ✅ ONE request per ticker - No more trying multiple formats
- ✅ STOP immediately on 429 - No retries
- ✅ 10-minute cooldown - Exponential backoff (5/7/10 min)
- ✅ Check cooldown BEFORE request - Prevents all calls during cooldown
- ✅ 5-minute cache - Reduces requests by 10x
- ✅ Ticker format cache - Remembers which format worked

**Math for Personal Use (10 stocks):**
```
5-minute cache = 12 requests/hour
Yahoo limit = 100-200 requests/hour
Result: 10x UNDER the limit ✅
```

### 6.3 Deployment Architecture

⚠️ **CRITICAL: Vercel Can Only Host Frontend**

Vercel does NOT support FastAPI/Python backends.

**What Vercel Can Host:**
- ✅ Frontend (React/Vite)
- ✅ Static sites
- ✅ Next.js (Node.js serverless functions)

**What Vercel CANNOT Host:**
- ❌ FastAPI (Python)
- ❌ Long-running processes
- ❌ WebSocket servers (persistent connections)
- ❌ Background jobs

**Recommended Architecture:**
```
┌─────────────────────────────────────────────┐
│           FRONTEND (Vercel)                 │
│   React + Vite                              │
│   https://trading-journal.vercel.app        │
└─────────────────┬───────────────────────────┘
                  │ HTTPS
                  │
┌─────────────────▼───────────────────────────┐
│         BACKEND (Railway/Render)            │
│   FastAPI + Python                          │
│   https://trading-journal-api.railway.app   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         DATABASE (MongoDB Atlas)            │
│   mongodb+srv://...                         │
└─────────────────────────────────────────────┘
```

### 6.4 Deployment Options

#### Frontend: Vercel ✅ (Recommended)

**Free Tier:**
- Unlimited bandwidth
- Automatic HTTPS
- CDN
- Preview deployments

**Steps:**
1. Push frontend to GitHub
2. Connect Vercel to GitHub repo
3. Set build command: `cd frontend && npm run build`
4. Set output directory: `frontend/dist`
5. Set install command: `cd frontend && npm install`
6. Set environment variable: `VITE_API_BASE_URL=https://your-backend.railway.app`

#### Backend: Railway ✅ (Recommended)

**Why Railway:**
- ✅ Python support
- ✅ FastAPI friendly
- ✅ Persistent filesystem (for cache)
- ✅ WebSocket support
- ✅ Free $5/month credit
- ✅ Automatic HTTPS

**Steps:**
1. Create Railway account - https://railway.app
2. Create new project
3. Deploy from GitHub
4. Add to `railway.json`:
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
       "healthcheckPath": "/",
       "restartPolicyType": "ON_FAILURE"
     }
   }
   ```
5. Add environment variables (see section 6.5)
6. Railway auto-deploys on push
7. Note your backend URL (e.g., `https://trading-journal-api.railway.app`)

**Alternative Backend Hosts:**
- **Render** - Free tier, persistent disk, slower cold starts
- **Fly.io** - Free tier, fast, persistent volumes
- **DigitalOcean App Platform** - $5/month, reliable
- **Heroku** - $7/month, easy setup

#### Database: MongoDB Atlas ✅

**Free Tier:**
- 512MB storage
- Shared cluster
- Perfect for personal use

**Steps:**
1. Create MongoDB Atlas account
2. Create free cluster
3. Create database user
4. Whitelist IP (0.0.0.0/0 for simplicity or specific IPs)
5. Get connection string
6. Use connection string in backend environment variables

### 6.5 Environment Variables

#### Backend (.env or platform dashboard)
```bash
MONGO_CONNECTION_STRING="mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB_NAME="trading_journal"
USE_MOCK_PRICES=false
SECRET_KEY="CHANGE-THIS-TO-RANDOM-STRING-IN-PRODUCTION"  # IMPORTANT!
PORT=8000  # Railway uses $PORT
```

**Generating SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
# Example output: "Kq8xY_3jHvZ9Ln2WpB5Rf6TgN4MdS7Ae"
```

#### Frontend (.env or Vercel dashboard)
```bash
VITE_API_BASE_URL=https://your-backend-url.railway.app
```

### 6.6 Persistent Cache on Different Platforms

**yfinance Cache Implementation:**
```python
# app/services/yahoo_finance_service.py
CACHE_DIR = Path(__file__).parent.parent.parent / ".cache" / "yfinance"
yf.set_tz_cache_location(str(CACHE_DIR))
```

This creates: `project/.cache/yfinance/`

**Cache Behavior by Platform:**

1. **Railway** ✅ - Persistent volumes; cache persists across deployments; perfect for our use case
2. **Render** ✅ - Persistent disk (paid plans); free tier resets on restart (every 15 min inactivity)
3. **Fly.io** ✅ - Persistent volumes; pay per GB storage; good performance
4. **DigitalOcean** ✅ - Persistent storage; $5/month plan includes storage
5. **Heroku** ⚠️ - Ephemeral filesystem; cache resets every 24h; not ideal but workable
6. **Vercel** ❌ - NO persistent filesystem; CANNOT run FastAPI anyway

**Impact of Cache Loss:**
- Minor - Cache only stores timezone data (small)
- Main benefit: Reduces metadata API calls
- Our 5-minute price cache is in-memory anyway

**Performance Comparison:**

Without Persistent Cache:
```
10 tickers = 10 price calls + 10 timezone calls = 20 API calls
```

With Persistent Cache:
```
10 tickers = 10 price calls + 0 timezone calls = 10 API calls (50% reduction!)
```

With In-Memory + Persistent Cache:
```
First request: 10 API calls
Next 5 minutes: 0 API calls (in-memory cache)
After 5 minutes: 10 API calls (not 20!)
```

### 6.7 Testing Before Deployment

#### 1. Test Mock Mode
```bash
# .env: USE_MOCK_PRICES=true
# Restart backend
# Create trade, close trade, view statistics
# Everything should work with fake prices
```

#### 2. Test Real Prices (After Rate Limit Clears)
```bash
# .env: USE_MOCK_PRICES=false
# Restart backend
# Wait 15-30 minutes from last 429 error
# Create trade with real ticker
# Should work with ONE request
```

#### 3. Test Authentication
```bash
# Login: demo / demo123
# Create trades (should be isolated to demo user)
# Logout
# Try accessing protected routes (should redirect to login)
```

### 6.8 Cost Analysis

**Free Tier (0-100 users):**
- Frontend (Vercel): FREE
- Backend (Railway): FREE ($5 credit/month)
- Database (MongoDB Atlas): FREE (512MB)
- **Total: $0/month**

**Personal Use (1 user):**
- Backend usage: < $2/month
- Database: FREE tier sufficient
- **Total: ~$0-2/month**

**Growing (100+ users):**
- Backend (Railway): $5-10/month
- Database (MongoDB Atlas): $9/month (2GB)
- **Total: ~$15-20/month**

### 6.9 Monitoring & Troubleshooting

#### Check Service Status
```bash
curl https://your-backend.railway.app/api/v1/trades/service-status
```

**Expected Response (Normal):**
```json
{
  "cache_entries": 5,
  "cache_duration_seconds": 300,
  "ticker_format_cache_entries": 3,
  "consecutive_429s": 0,
  "rate_limited": false,
  "message": "Service operational. Quotes cached for 5 minutes."
}
```

**Expected Response (Rate Limited):**
```json
{
  "rate_limited": true,
  "cooldown_remaining_minutes": 4.1,
  "consecutive_429s": 1,
  "message": "Rate limited. Using cached data only. Cooldown ends in 4 min 7 sec."
}
```

#### Railway Dashboard
- View logs in real-time
- Monitor CPU/memory usage
- Track API calls
- Set up alerts

#### Common Issues

**Cache Not Working?**
```bash
# SSH into Railway
railway shell

# Check cache directory
ls -la .cache/yfinance/

# Should see timezone cache files
```

**WebSocket Connection Failed?**
- Check if backend platform supports WebSockets (Railway ✅, Vercel ❌)
- Ensure HTTPS/WSS protocol
- Check CORS settings

**Still Rate Limited?**
- Check logs for 429 errors
- Verify ONE-REQUEST implementation is working
- Increase cache duration to 10 or 15 minutes
- Reduce frontend polling to 60 seconds
- Use mock mode temporarily

**Frontend Can't Connect to Backend?**
- Verify VITE_API_BASE_URL is set correctly
- Check CORS configuration in backend
- Ensure backend is running and accessible
- Check browser console for errors

### 6.10 Deployment Quick Commands

**Development (Mock Mode):**
```bash
# Backend
USE_MOCK_PRICES=true
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm run dev
```

**Production (Real Prices):**
```bash
# Backend
USE_MOCK_PRICES=false
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
npm run preview
```

**Check Status:**
```bash
curl http://localhost:8000/api/v1/trades/service-status
```

### 6.11 WebSocket Streaming (Future Enhancement)

**Why Not Implemented Yet:**
1. Complexity - More code, more things to break
2. Not needed - Personal journal doesn't need second-by-second updates
3. Polling is fine - 30-second updates are sufficient for position tracking

**When to Add WebSockets:**
- Day trading (need real-time prices)
- Multiple users (reduce API calls)
- Backend on Railway/Render (WebSocket support)

**Implementation Ready:**
- Backend endpoint exists: `/ws/{user_id}`
- Frontend client exists: `frontend/src/services/websocket.ts`
- Just need to enable and wire up price streaming

### 6.12 Production Readiness Summary

**✅ What Works Now:**
1. yfinance persistent cache - Reduces API calls by 50%
2. ONE-REQUEST policy - 1 API call per ticker (not 5)
3. 5-minute in-memory cache - Reduces requests by 10x
4. Exponential backoff on 429 - Gives Yahoo Finance time to reset
5. Ticker format cache - Remembers which format worked
6. WebSocket infrastructure - Ready for future real-time streaming

**⚠️ Deployment Constraints:**
1. Vercel = Frontend ONLY - Cannot host FastAPI
2. Backend = Railway/Render - Needs Python support
3. Persistent cache works on Railway - Not on all platforms
4. WebSockets not needed yet - Polling is sufficient

**🚀 Ready to Deploy:**
1. Backend → Railway (FREE)
2. Frontend → Vercel (FREE)
3. Database → MongoDB Atlas (FREE)
4. **Total Cost: $0/month**

**You can deploy immediately using mock mode, then switch to real prices after any rate limit clears.**

---

## Summary So Far

This documentation has covered:

1. **Project Overview** - Purpose, target user, key features
2. **Technology Stack** - Why each technology was chosen
3. **System Architecture** - How components interact
4. **Project Structure** - File organization
5. **Backend Deep Dive** - Every file, every line explained
   - Application entry point
   - Configuration system
   - Authentication (JWT, bcrypt)
   - Database layer (Motor, MongoDB)
   - Data models (Pydantic)
   - API routes (all endpoints)
   - Yahoo Finance service (rate limiting, caching)

The documentation is structured as a **learning course** - someone could read this and understand:
- **What** each line does
- **Why** that design decision was made
- **How** components work together
- **When** to use certain patterns

Total lines so far: 2000+ (excluding this summary)

---

*This is Part 1 of the Complete Technical Documentation. Part 2 will cover Frontend, Deployment, Testing, and Troubleshooting.*

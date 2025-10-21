"""
JWT-based authentication for the trading journal with MongoDB storage.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from app.db.database import get_users_collection

# JWT Configuration
SECRET_KEY = "your-secret-key-change-this-in-production"  # TODO: Move to environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


class User(BaseModel):
    user_id: str
    username: str
    email: Optional[str] = None


class UserInDB(User):
    hashed_password: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


async def register_user(username: str, password: str, email: Optional[str] = None) -> Optional[User]:
    """Register a new user in MongoDB."""
    users_collection = get_users_collection()
    
    # Check if user already exists
    existing_user = await users_collection.find_one({"username": username})
    if existing_user:
        return None
    
    # Create new user
    user_id = f"user_{username}_{datetime.now(timezone.utc).timestamp()}"
    hashed_password = get_password_hash(password)
    
    user_doc = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "created_at": datetime.now(timezone.utc)
    }
    
    await users_collection.insert_one(user_doc)
    
    return User(user_id=user_id, username=username, email=email)


async def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate a user by username and password."""
    users_collection = get_users_collection()
    
    user_doc = await users_collection.find_one({"username": username})
    if not user_doc:
        return None
    
    user = UserInDB(
        user_id=user_doc["user_id"],
        username=user_doc["username"],
        email=user_doc.get("email"),
        hashed_password=user_doc["hashed_password"]
    )
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


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
    
    # Find user in MongoDB
    users_collection = get_users_collection()
    user_doc = await users_collection.find_one({"user_id": token_data.user_id})
    
    if not user_doc:
        raise credentials_exception
    
    return User(
        user_id=user_doc["user_id"],
        username=user_doc["username"],
        email=user_doc.get("email")
    )


async def get_current_user_id(current_user: User = Depends(get_current_user)) -> str:
    """Get just the user ID of the current user."""
    return current_user.user_id

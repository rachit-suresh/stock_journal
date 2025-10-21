"""
Simple JWT-based authentication for the trading journal.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

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


# Mock user database (replace with MongoDB in production)
# Using a pre-hashed password to avoid hashing at import time
# Original password: demo123
fake_users_db = {
    "demo": {
        "user_id": "demo_user_id",
        "username": "demo",
        "email": "demo@example.com",
        "hashed_password": "$2b$12$nhXdAHHELhREj9s.AWAgaemKXz42.zT9AY28i3Yl2mG7wpHaEHVBC",  # demo123
    }
}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def register_user(username: str, password: str, email: Optional[str] = None) -> Optional[User]:
    """Register a new user."""
    if username in fake_users_db:
        return None
    
    user_id = f"user_{username}_{datetime.now(timezone.utc).timestamp()}"
    hashed_password = get_password_hash(password)
    
    fake_users_db[username] = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
    }
    
    return User(user_id=user_id, username=username, email=email)


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Authenticate a user by username and password."""
    user_dict = fake_users_db.get(username)
    if not user_dict:
        return None
    user = UserInDB(**user_dict)
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
    
    # Find user in fake database
    for username, user_dict in fake_users_db.items():
        if user_dict["user_id"] == token_data.user_id:
            return User(**user_dict)
    
    raise credentials_exception


async def get_current_user_id(current_user: User = Depends(get_current_user)) -> str:
    """Get just the user ID of the current user."""
    return current_user.user_id


from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext

# --- Password Hashing ---
pwd_context = CryptContext(schemes=["bycrypt"], depracted=["auto"])

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

# --- JWT Configuration ---
# IMPORTANT: Use environment variables for SECRET_KEY in production!
# Example: SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-default")
SECRET_KEY = "a-very-secret-key-that-should-be-in-env-vars-in-prod" # CHANGE THIS!
ALGORITHM = "HS256"  # JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time in minutes

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    """Decodes and validates a JWT access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # 'sub' (subject) is typically the user identifier
        if username is None:
            raise JWTError("Invalid token payload: 'sub' claim missing.")
        return payload
    except JWTError:
        # This catches various JWT errors like invalid signature, expired token, etc.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}, # Standard header for OAuth2
        )
    
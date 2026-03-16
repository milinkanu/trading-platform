import os
import time
from typing import Dict, Any
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-jwt-key-change-this")
ALGORITHM = "HS256"

def create_access_token(data: dict) -> str:
    payload = data.copy()
    expires = time.time() + 24 * 3600  # 24 hours
    payload.update({"exp": expires})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str) -> Dict[str, Any]:
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded if decoded["exp"] >= time.time() else None
    except JWTError:
        return None

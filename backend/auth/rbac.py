from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from backend.auth.jwt_handler import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or expired token."
        )
    return payload

async def get_optional_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        return None
    try:
        token = authorization.split(" ")[1] if " " in authorization else authorization
        payload = decode_token(token)
        return payload
    except:
        return None

async def trader_required(user: dict = Depends(get_current_user)):
    role = user.get("role")
    if role not in ["trader", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough privileges."
        )
    return user

async def admin_required(user: dict = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required."
        )
    return user

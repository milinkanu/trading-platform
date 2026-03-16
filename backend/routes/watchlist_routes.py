from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from database import watchlist_collection
from auth.rbac import trader_required

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])

class WatchlistRequest(BaseModel):
    symbol: str

@router.get("")
async def get_watchlist(user: dict = Depends(trader_required)):
    user_id = user.get("user_id")
    cursor = watchlist_collection.find({"user_id": user_id})
    watchlist = await cursor.to_list(length=100)
    return [item["symbol"] for item in watchlist]

@router.post("")
async def add_to_watchlist(request: WatchlistRequest, user: dict = Depends(trader_required)):
    user_id = user.get("user_id")
    symbol = request.symbol.upper()
    
    # Check if already exists
    existing = await watchlist_collection.find_one({"user_id": user_id, "symbol": symbol})
    if existing:
        return {"message": f"{symbol} already in watchlist"}
        
    await watchlist_collection.insert_one({
        "user_id": user_id,
        "symbol": symbol
    })
    return {"message": f"{symbol} added to watchlist"}

@router.delete("/{symbol}")
async def remove_from_watchlist(symbol: str, user: dict = Depends(trader_required)):
    user_id = user.get("user_id")
    symbol = symbol.upper()
    
    result = await watchlist_collection.delete_one({
        "user_id": user_id, 
        "symbol": symbol
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Symbol not in watchlist"
        )
        
    return {"message": f"{symbol} removed from watchlist"}

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import httpx
from backend.database import sip_collection
from backend.auth.rbac import trader_required
from bson import ObjectId

router = APIRouter(prefix="/sip", tags=["SIP"])

class SIPCreateRequest(BaseModel):
    fund_name: str
    scheme_code: str
    monthly_amount: float
    units_held: float
    avg_buy_nav: float
    start_date: str

async def fetch_nav(scheme_code: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://api.mfapi.in/mf/{scheme_code}")
            data = response.json()
            if data and "data" in data and len(data["data"]) > 0:
                return float(data["data"][0]["nav"])
    except Exception as e:
        print(f"Error fetching NAV for {scheme_code}: {e}")
    return None

@router.get("")
async def get_sip_entries(current_user: dict = Depends(trader_required)):
    user_id = current_user.get("user_id")
    cursor = sip_collection.find({"user_id": user_id})
    entries = await cursor.to_list(length=100)
    
    enriched_entries = []
    for entry in entries:
        current_nav = await fetch_nav(entry["scheme_code"])
        
        # Calculations
        units = entry["units_held"]
        avg_nav = entry["avg_buy_nav"]
        
        invested_value = units * avg_nav
        current_value = 0
        gain_loss = 0
        gain_pct = 0
        
        if current_nav:
            current_value = units * current_nav
            gain_loss = current_value - invested_value
            gain_pct = ((current_nav - avg_nav) / avg_nav) * 100
            
        enriched_entries.append({
            "id": str(entry["_id"]),
            "fund_name": entry["fund_name"],
            "scheme_code": entry["scheme_code"],
            "monthly_amount": entry["monthly_amount"],
            "units_held": units,
            "avg_buy_nav": avg_nav,
            "current_nav": current_nav,
            "invested_value": round(invested_value, 2),
            "current_value": round(current_value, 2),
            "gain_loss": round(gain_loss, 2),
            "gain_pct": round(gain_pct, 2),
            "start_date": entry["start_date"]
        })
        
    return enriched_entries

@router.post("")
async def create_sip_entry(request: SIPCreateRequest, current_user: dict = Depends(trader_required)):
    print(f"Adding SIP: {request.fund_name} for user {current_user.get('email')}")
    user_id = current_user.get("user_id")
    
    new_entry = {
        "user_id": user_id,
        "fund_name": request.fund_name,
        "scheme_code": request.scheme_code,
        "monthly_amount": request.monthly_amount,
        "units_held": request.units_held,
        "avg_buy_nav": request.avg_buy_nav,
        "start_date": request.start_date,
        "added_at": datetime.utcnow()
    }
    
    result = await sip_collection.insert_one(new_entry)
    return {"message": "SIP entry created", "id": str(result.inserted_id)}

@router.delete("/{entry_id}")
async def delete_sip_entry(entry_id: str, current_user: dict = Depends(trader_required)):
    user_id = current_user.get("user_id")
    try:
        obj_id = ObjectId(entry_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    result = await sip_collection.delete_one({"_id": obj_id, "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Entry not found")
        
    return {"message": "Entry deleted"}

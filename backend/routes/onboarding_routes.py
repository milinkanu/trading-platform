from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime
from backend.database import users_collection
from backend.auth.rbac import get_optional_user
from bson import ObjectId

router = APIRouter(prefix="/onboarding", tags=["Onboarding"])

class ProfileRequest(BaseModel):
    answers: Dict[str, str]

@router.post("/profile")
async def calculate_risk_profile(request: ProfileRequest, user: Optional[dict] = Depends(get_optional_user)):
    ans = request.answers
    score = 0
    
    # Q1: Investment goal
    goals = {"wealth_creation": 3, "regular_income": 1, "capital_protection": 0}
    score += goals.get(ans.get("q1"), 0)
    
    # Q2: Investment horizon
    horizon = {"less_1yr": 0, "1_to_3yr": 1, "3_plus_yr": 3}
    score += horizon.get(ans.get("q2"), 0)
    
    # Q3: Market fluctuation comfort
    comfort = {"uncomfortable": 0, "somewhat_ok": 2, "very_comfortable": 3}
    score += comfort.get(ans.get("q3"), 0)
    
    # Q4: Existing market experience
    exp = {"none": 0, "some_mf_sip": 1, "active_trader": 3}
    score += exp.get(ans.get("q4"), 0)
    
    # Q5: Capital deployed
    capital = {"less_25": 0, "25_to_50": 1, "more_50": 2}
    score += capital.get(ans.get("q5"), 0)
    
    # Profile mapping
    if score <= 4:
        p_type = "Conservative Investor"
        desc = "Capital protection focus. Low volatility tolerance."
        alloc = {"equity": 20, "mf": 40, "gold": 20, "debt": 20}
    elif score <= 8:
        p_type = "Moderate Investor"
        desc = "Balanced growth with manageable risk."
        alloc = {"equity": 40, "mf": 35, "gold": 15, "debt": 10}
    elif score <= 12:
        p_type = "Growth Investor"
        desc = "Comfortable with market cycles for better returns."
        alloc = {"equity": 60, "mf": 25, "gold": 10, "debt": 5}
    else:
        p_type = "Aggressive Investor"
        desc = "High risk tolerance. Long-term wealth creation."
        alloc = {"equity": 75, "mf": 20, "gold": 5, "debt": 0}
        
    profile_data = {
        "type": p_type,
        "score": score,
        "description": desc,
        "allocation": alloc,
        "taken_at": datetime.utcnow()
    }
    
    # Save to user if logged in
    if user:
        try:
            user_id = user.get("user_id")
            await users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"risk_profile": profile_data}}
            )
            profile_data["saved"] = True
        except Exception as e:
            print(f"Error saving risk profile: {e}")
            
    return profile_data

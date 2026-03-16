from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from bson import ObjectId
from backend.database import users_collection
from backend.auth.rbac import admin_required, get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

class RoleUpdateRequest(BaseModel):
    role: str

@router.get("/users")
async def get_users(current_user: dict = Depends(admin_required)):
    users_cursor = users_collection.find()
    users = await users_cursor.to_list(length=100)
    
    return [{
        "id": str(u["_id"]),
        "name": u["name"],
        "email": u["email"],
        "role": u["role"],
        "created_at": u.get("created_at")
    } for u in users]

@router.patch("/users/{user_id}/role")
async def update_user_role(user_id: str, request: RoleUpdateRequest, current_user: dict = Depends(admin_required)):
    if request.role not in ["trader", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role. Must be 'trader' or 'admin'.")
        
    try:
        obj_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format.")
        
    result = await users_collection.update_one(
        {"_id": obj_id},
        {"$set": {"role": request.role}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")
        
    updated_user = await users_collection.find_one({"_id": obj_id})
    return {
        "id": str(updated_user["_id"]),
        "name": updated_user["name"],
        "email": updated_user["email"],
        "role": updated_user["role"],
        "created_at": updated_user.get("created_at")
    }

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: dict = Depends(admin_required)):
    if user_id == str(current_user.get("user_id")):
        raise HTTPException(status_code=400, detail="You cannot delete yourself.")
        
    try:
        obj_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid user ID format.")
        
    result = await users_collection.delete_one({"_id": obj_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")
        
    return {"message": "User deleted"}

@router.get("/stats")
async def get_stats(current_user: dict = Depends(admin_required)):
    total_users = await users_collection.count_documents({})
    total_admins = await users_collection.count_documents({"role": "admin"})
    total_traders = await users_collection.count_documents({"role": "trader"})
    
    recent_users_cursor = users_collection.find().sort("created_at", -1).limit(5)
    recent_users = await recent_users_cursor.to_list(length=5)
    
    return {
        "total_users": total_users,
        "total_admins": total_admins,
        "total_traders": total_traders,
        "recent_users": [{
            "id": str(u["_id"]),
            "name": u["name"],
            "email": u["email"],
            "role": u["role"],
            "created_at": u.get("created_at")
        } for u in recent_users]
    }

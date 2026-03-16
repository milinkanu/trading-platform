from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from backend.database import users_collection
from backend.auth.hash_helper import hash_password, verify_password
from backend.auth.jwt_handler import create_access_token
from backend.models.user_model import UserModel, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(request: RegisterRequest):
    print(f"Registering user: {request.email}")
    try:
        # Check if user exists
        existing_user = await users_collection.find_one({"email": request.email})
        print(f"Existing user search done: {existing_user}")
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

        hashed_pw = hash_password(request.password)
        new_user = UserModel(
            name=request.name,
            email=request.email,
            password=hashed_pw,
            role="trader"  # default
        )
        print("UserModel created")
        
        user_dict = new_user.model_dump(by_alias=True, exclude={"id"})
        print(f"User dict for insertion: {user_dict}")
        
        result = await users_collection.insert_one(user_dict)
        print(f"User inserted with id: {result.inserted_id}")
        
        token = create_access_token({
            "user_id": str(result.inserted_id),
            "email": new_user.email,
            "role": new_user.role
        })
        
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        print(f"Error during registration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(request: LoginRequest):
    user = await users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )
        
    if not verify_password(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )
        
    token = create_access_token({
        "user_id": str(user["_id"]),
        "email": user["email"],
        "role": user["role"]
    })
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    }

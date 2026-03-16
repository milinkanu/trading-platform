from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime

class UserModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: EmailStr
    password: str
    role: Literal["admin", "trader"] = "trader"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "johndoe@example.com",
                "password": "strongpassword",
                "role": "trader"
            }
        }

class UserResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        populate_by_name = True

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from auth.hash_helper import hash_password
from dotenv import load_dotenv

# Load .env
load_dotenv()

async def create_admin():
    # 1. Get MongoDB URI from .env
    mongo_uri = os.getenv("MONGO_URI")
    
    if not mongo_uri or "localhost" in mongo_uri:
        print("ERROR: Please update your MONGO_URI in backend/.env to your MongoDB Atlas connection string first!")
        return

    print(f"Connecting to: {mongo_uri[:20]}...")
    client = AsyncIOMotorClient(mongo_uri)
    db = client.trading_db
    users_collection = db.users

    # 2. Admin Details
    admin_email = "admin@test.com"
    admin_pass = "admin123"
    
    # 3. Check if exists
    existing = await users_collection.find_one({"email": admin_email})
    if existing:
        print(f"Admin {admin_email} already exists in Atlas!")
        return

    # 4. Create User
    new_admin = {
        "name": "Super Admin",
        "email": admin_email,
        "password": hash_password(admin_pass),
        "role": "admin",
        "created_at": None # You can add datetime.utcnow() if needed
    }

    try:
        await users_collection.insert_one(new_admin)
        print("------------------------------------------")
        print("SUCCESS: Admin user created in MongoDB Atlas!")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_pass}")
        print("------------------------------------------")
    except Exception as e:
        print(f"FAILED to create admin: {e}")

if __name__ == "__main__":
    asyncio.run(create_admin())

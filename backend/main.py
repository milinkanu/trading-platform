from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from routes.auth_routes import router as auth_router
from routes.stock_routes import router as stock_router
from routes.admin_routes import router as admin_router
from routes.sip_routes import router as sip_router
from routes.onboarding_routes import router as onboarding_router
from routes.watchlist_routes import router as watchlist_router

app = FastAPI(title="TradingView API")

# Add CORS
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route includes
app.include_router(auth_router)
app.include_router(stock_router)
app.include_router(admin_router)
app.include_router(sip_router)
app.include_router(onboarding_router)
app.include_router(watchlist_router)

@app.get("/")
async def root():
    try:
        from database import users_collection
        # Try a simple operation to check DB connection
        count = await users_collection.count_documents({})
        return {"status": "TradingView API running", "database": "connected", "user_count": count}
    except Exception as e:
        return {"status": "TradingView API running", "database": "error", "error": str(e)}

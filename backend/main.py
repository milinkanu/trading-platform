from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from backend.routes.auth_routes import router as auth_router
from backend.routes.stock_routes import router as stock_router
from backend.routes.admin_routes import router as admin_router
from backend.routes.sip_routes import router as sip_router
from backend.routes.onboarding_routes import router as onboarding_router
from backend.routes.watchlist_routes import router as watchlist_router

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
app.include_router(auth_router, prefix="/api")
app.include_router(stock_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(sip_router, prefix="/api")
app.include_router(onboarding_router, prefix="/api")
app.include_router(watchlist_router, prefix="/api")

@app.get("/api")
@app.get("/api/status")
async def root():
    try:
        from backend.database import users_collection
        # Try a simple operation to check DB connection
        count = await users_collection.count_documents({})
        return {"status": "TradingView API running", "database": "connected", "user_count": count}
    except Exception as e:
        return {"status": "TradingView API running", "database": "error", "error": str(e)}

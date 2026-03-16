from fastapi import FastAPI
app = FastAPI()

@app.get("/api/status")
async def status():
    return {"status": "ok", "message": "Minimal API is running"}

@app.get("/api/{path:path}")
async def catch_all(path: str):
    return {"status": "ok", "path": path}

from fastapi import APIRouter, Depends, HTTPException
from backend.auth.rbac import trader_required
from backend.services.stock_service import get_stock_data
from backend.services.ai_service import get_ai_analysis

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.get("/{symbol}")
async def get_stock(symbol: str, user: dict = Depends(trader_required)):
    try:
        print(f"Fetching stock: {symbol}")
        data = await get_stock_data(symbol)
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock data: {str(e)}")

@router.get("/{symbol}/ai")
async def get_stock_ai(symbol: str, user: dict = Depends(trader_required)):
    try:
        # Fetch stock data first
        data = await get_stock_data(symbol)
        
        # Call AI service
        analysis = await get_ai_analysis(
            symbol=symbol,
            indicators=data["indicators"],
            signal=data["signal"],
            company_name=data["company_name"]
        )
        
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating AI analysis: {str(e)}")

@router.get("/search/{query}")
async def search_stocks(query: str, user: dict = Depends(trader_required)):
    popular_symbols = [
        {"symbol": "AAPL", "name": "Apple Inc."},
        {"symbol": "TSLA", "name": "Tesla, Inc."},
        {"symbol": "GOOGL", "name": "Alphabet Inc."},
        {"symbol": "MSFT", "name": "Microsoft Corporation"},
        {"symbol": "AMZN", "name": "Amazon.com, Inc."},
        {"symbol": "META", "name": "Meta Platforms, Inc."},
        {"symbol": "RELIANCE.NS", "name": "Reliance Industries Limited"},
        {"symbol": "TCS.NS", "name": "Tata Consultancy Services Limited"},
        {"symbol": "INFY.NS", "name": "Infosys Limited"},
        {"symbol": "HDFCBANK.NS", "name": "HDFC Bank Limited"},
    ]
    
    query = query.upper()
    results = [s for s in popular_symbols if query in s["symbol"] or query in s["name"].upper()]
    return results

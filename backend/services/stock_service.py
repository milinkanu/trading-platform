import math

async def get_stock_data(symbol: str):
    # Mock data to allow the app to run on Vercel without yfinance/pandas
    return {
        "symbol": symbol.upper(),
        "company_name": f"{symbol.upper()} Mock Inc.",
        "current_price": 150.0,
        "change_pct": 1.5,
        "signal": "HOLD",
        "signal_reason": "Vercel environment restriction: yfinance/pandas disabled. Using mock data.",
        "indicators": {
            "rsi": 50.0,
            "macd": 0.0,
            "macd_signal": 0.0,
            "bb_upper": 160.0,
            "bb_lower": 140.0,
            "sma20": 145.0,
            "sma50": 140.0,
        },
        "chart_data": [
            {
                "date": "2026-03-16",
                "open":  148.0,
                "high":  152.0,
                "low":   147.0,
                "close": 150.0,
                "volume": 1000000,
                "sma20": 145.0,
                "sma50": 140.0,
                "rsi":   50.0,
                "macd":  0.0,
                "macd_signal": 0.0,
                "bb_upper": 160.0,
                "bb_lower": 140.0,
            }
        ],
    }

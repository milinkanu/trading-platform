import math
from datetime import datetime, timedelta

async def get_stock_data(symbol: str):
    # Mock data to allow the app to run on Vercel without yfinance/pandas
    # Generating 30 days of data to make charts visible
    chart_data = []
    base_price = 150.0
    end_date = datetime.now()
    
    for i in range(30):
        date = (end_date - timedelta(days=29-i)).strftime("%Y-%m-%d")
        # Add some variation to the price
        variation = math.sin(i / 5.0) * 5.0
        price = round(base_price + variation, 2)
        
        chart_data.append({
            "date": date,
            "open":  round(price - 1.0, 2),
            "high":  round(price + 2.0, 2),
            "low":   round(price - 2.0, 2),
            "close": price,
            "volume": 1000000 + (i * 10000),
            "sma20": round(base_price - 2.0, 2),
            "sma50": round(base_price - 5.0, 2),
            "rsi":   round(50.0 + variation * 2, 2),
            "macd":  round(variation / 2.0, 4),
            "macd_signal": round(variation / 3.0, 4),
            "bb_upper": round(price + 10.0, 2),
            "bb_lower": round(price - 10.0, 2),
        })

    last = chart_data[-1]
    
    return {
        "symbol": symbol.upper(),
        "company_name": f"{symbol.upper()} Mock Inc.",
        "current_price": last["close"],
        "change_pct": 1.5,
        "signal": "HOLD",
        "signal_reason": "Note: Using simulated data due to Vercel environment restrictions on data-science libraries.",
        "indicators": {
            "rsi": last["rsi"],
            "macd": last["macd"],
            "macd_signal": last["macd_signal"],
            "bb_upper": last["bb_upper"],
            "bb_lower": last["bb_lower"],
            "sma20": last["sma20"],
            "sma50": last["sma50"],
        },
        "chart_data": chart_data,
    }

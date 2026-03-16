from yahooquery import Ticker
import pandas as pd
import pandas_ta as ta
import math
from datetime import datetime

async def get_stock_data(symbol: str):
    try:
        ticker = Ticker(symbol)
        # yahooquery history returns a dataframe with MultiIndex (symbol, date) by default
        df = ticker.history(period="6mo", interval="1d")

        if df.empty:
            raise ValueError(f"No data found for symbol: {symbol}")

        # If MultiIndex, reset index and get the symbol data
        if isinstance(df.index, pd.MultiIndex):
            df = df.reset_index()
            df.set_index('date', inplace=True)
            # Filter for just this symbol (though ticker.history for single symbol should be fine)
            if 'symbol' in df.columns:
                df = df[df['symbol'].str.upper() == symbol.upper()]

        # Calculate indicators using pandas-ta
        df["RSI_14"] = ta.rsi(df["adjclose"] if "adjclose" in df.columns else df["close"], length=14)
        macd = ta.macd(df["adjclose"] if "adjclose" in df.columns else df["close"], fast=12, slow=26, signal=9)
        df = pd.concat([df, macd], axis=1)
        bbands = ta.bbands(df["adjclose"] if "adjclose" in df.columns else df["close"], length=20)
        df = pd.concat([df, bbands], axis=1)
        df["SMA20"] = ta.sma(df["adjclose"] if "adjclose" in df.columns else df["close"], length=20)
        df["SMA50"] = ta.sma(df["adjclose"] if "adjclose" in df.columns else df["close"], length=50)

        # Clean NaN rows
        df = df.dropna()
        if df.empty:
            raise ValueError(f"Not enough data to calculate indicators for symbol: {symbol}")
            
        last = df.iloc[-1]

        # Signal logic
        rsi_val = round(float(last["RSI_14"]), 2)
        if rsi_val < 30:
            signal = "BUY"
            signal_reason = f"RSI is {rsi_val} — stock is oversold"
        elif rsi_val > 70:
            signal = "SELL"
            signal_reason = f"RSI is {rsi_val} — stock is overbought"
        else:
            signal = "HOLD"
            signal_reason = f"RSI is {rsi_val} — no strong signal"

        # Last 90 days chart data
        chart_df = df.tail(90)

        def safe(val):
            if val is None: return None
            try:
                v = float(val)
                return None if math.isnan(v) else round(v, 4)
            except:
                return None

        # Dynamic column finding for indicators
        def get_col(df, prefix):
            cols = [c for c in df.columns if str(c).startswith(prefix)]
            return cols[0] if cols else None

        macd_col = get_col(df, "MACD_")
        macd_s_col = get_col(df, "MACDs_")
        bbu_col = get_col(df, "BBU_")
        bbl_col = get_col(df, "BBL_")

        chart_data = [
            {
                "date": str(idx.date()) if hasattr(idx, 'date') else str(idx),
                "open":  safe(row["open"]),
                "high":  safe(row["high"]),
                "low":   safe(row["low"]),
                "close": safe(row["adjclose"] if "adjclose" in row else row["close"]),
                "volume": int(row["volume"]),
                "sma20": safe(row["SMA20"]),
                "sma50": safe(row["SMA50"]),
                "rsi":   safe(row["RSI_14"]),
                "macd":  safe(row[macd_col]) if macd_col else None,
                "macd_signal": safe(row[macd_s_col]) if macd_s_col else None,
                "bb_upper": safe(row[bbu_col]) if bbu_col else None,
                "bb_lower": safe(row[bbl_col]) if bbl_col else None,
            }
            for idx, row in chart_df.iterrows()
        ]

        # Ticker info for company name
        try:
            profile = ticker.price[symbol]
            company_name = profile.get("longName", symbol)
        except:
            company_name = symbol
            
        current_price = safe(last["adjclose"] if "adjclose" in last else last["close"])
        prev_close = safe(df.iloc[-2]["adjclose"] if "adjclose" in df.iloc[-2] else df.iloc[-2]["close"])
        change_pct = round(((current_price - prev_close) / prev_close) * 100, 2) if prev_close else 0

        return {
            "symbol": symbol.upper(),
            "company_name": company_name,
            "current_price": current_price,
            "change_pct": change_pct,
            "signal": signal,
            "signal_reason": signal_reason,
            "indicators": {
                "rsi": rsi_val,
                "macd": safe(last[macd_col]) if macd_col else None,
                "macd_signal": safe(last[macd_s_col]) if macd_s_col else None,
                "bb_upper": safe(last[bbu_col]) if bbu_col else None,
                "bb_lower": safe(last[bbl_col]) if bbl_col else None,
                "sma20": safe(last["SMA20"]),
                "sma50": safe(last["SMA50"]),
            },
            "chart_data": chart_data,
        }
    except Exception as e:
        print(f"Error fetching data with yahooquery: {str(e)}")
        # Fallback to a minimal mock if yahooquery fails in prod for some reason
        # to prevent hard 500 error
        return {
            "symbol": symbol.upper(),
            "company_name": symbol.upper(),
            "current_price": 0.0,
            "change_pct": 0.0,
            "signal": "ERROR",
            "signal_reason": f"Data retrieval failed: {str(e)}",
            "indicators": {},
            "chart_data": []
        }

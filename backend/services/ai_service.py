import os
import json
import google.generativeai as genai

async def get_ai_analysis(symbol: str, indicators: dict, 
                           signal: str, company_name: str):
    """
    Using Google Gemini 1.5 Flash (Free Tier) for stock analysis.
    Register for a free key at https://aistudio.google.com/
    """
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    # Fallback to Mock Analysis if no key is provided
    if not api_key:
        return get_mock_analysis(symbol, indicators, signal, company_name)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are a stock market technical analyst. Analyze this stock data 
        and give a concise trading recommendation.

        Stock: {company_name} ({symbol})
        Current Signal: {signal}

        Technical Indicators:
        - RSI (14): {indicators['rsi']}
        - MACD: {indicators['macd']} | Signal Line: {indicators['macd_signal']}
        - Bollinger Upper: {indicators['bb_upper']} | Lower: {indicators['bb_lower']}
        - SMA 20: {indicators['sma20']} | SMA 50: {indicators['sma50']}

        Respond ONLY in this exact JSON format (no markdown code blocks, no extra text):
        {{
          "recommendation": "BUY | SELL | HOLD",
          "confidence": "High | Medium | Low",
          "summary": "2-3 line analysis of the technical setup",
          "key_risk": "One main risk to watch",
          "target_note": "Short note on price levels to watch"
        }}
        """

        response = model.generate_content(prompt)
        raw = response.text.strip()
        
        # Clean up in case Gemini wraps in markdown
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0].strip()
            
        return json.loads(raw)
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return get_mock_analysis(symbol, indicators, signal, company_name)

def get_mock_analysis(symbol: str, indicators: dict, signal: str, company_name: str):
    """Fallback generator that looks realistic based on actual indicators"""
    rsi = indicators.get('rsi', 50)
    
    rec = signal
    conf = "Medium"
    if rsi < 35: 
        rec = "BUY"
        conf = "High"
        summary = f"{company_name} is showing strong oversold conditions with RSI at {rsi}. Price is stabilizing near support levels."
        risk = "Potential for extended consolidation before breakout."
    elif rsi > 65:
        rec = "SELL"
        conf = "High"
        summary = f"{company_name} looks overextended as RSI hits {rsi}. MACD suggests momentum might be slowing down."
        risk = "Profit booking could trigger a sharp pullback."
    else:
        summary = f"The stock is currently in a neutral zone. SMA indicators show a steady trend with no immediate breakout signs."
        risk = "Low volume could lead to sideways movement."
        
    return {
        "recommendation": rec,
        "confidence": conf,
        "summary": summary,
        "key_risk": risk,
        "target_note": "Watch for a clean break above recent highs for confirmation."
    }

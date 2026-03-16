# TradeAI Platform

A TradingView-style mini trading analytics platform redesigned for wealth management visibility.

## Tech Stack
- **Backend:** FastAPI (Python), MongoDB (Motor), JWT Auth
- **Frontend:** Vue.js 3, Tailwind CSS, Chart.js
- **Services:** yfinance (Stocks), pandas-ta (Indicators), Claude AI (Analysis), AMFI API (Mutual Funds)

## Dhanilal Platform Alignment
This project is built as a working prototype of the Dhanilal wealth management platform vision:

| Dhanilal Feature | Implemented As |
|---|---|
| Trading Insights | Stock charts + RSI/MACD/BB signals |
| AI Recommendations | Claude AI buy/sell analysis |
| Investor Profiling | 5-question risk assessment quiz |
| SIP/MF Tracking | AMFI NAV integration + P&L calculator |
| Portfolio View | Watchlist with live prices |
| RBAC | Admin (advisor) / Trader (client) roles |

## Key Features
- **Stock Dashboard:** Real-time data fetching with technical indicators.
- **AI Analysis:** Deep technical setup review using Claude-3.5-Sonnet.
- **Risk Profiling:** Automated investor classification based on goals and horizon.
- **MF/SIP Tracker:** Live NAV tracking for major Indian Mutual Funds via AMFI integration.
- **Admin Dashboard:** Full user management and platform analytics.

## Setup
### Backend
1. `cd backend`
2. `python -m venv venv`
3. `venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. Create `.env` with `ANTHROPIC_API_KEY` and `MONGO_URI`
6. `uvicorn main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

import yfinance as yf

def build_portfolio(goal="balanced", risk_level="medium"):
    """Build a portfolio using live ticker information based on goal and risk."""

    # Define example sector-focused ETFs (easy, real-time safe)
    portfolios = {
        "growth": ["QQQ", "VUG", "ARKK", "AAPL", "NVDA"],
        "income": ["VYM", "SCHD", "KO", "PG", "T"],
        "balanced": ["VTI", "VOO", "MSFT", "UNH", "BRK-B"]
    }
    
    allocation = {
        "low": [50, 20, 10, 10, 10],
        "medium": [30, 25, 20, 15, 10],
        "high": [20, 20, 20, 20, 20]
    }

    selected_stocks = portfolios.get(goal.lower(), portfolios["balanced"])
    selected_allocation = allocation.get(risk_level.lower(), allocation["medium"])

    portfolio = {}

    for ticker, weight in zip(selected_stocks, selected_allocation):
        try:
            stock_info = yf.Ticker(ticker).info
            company_name = stock_info.get('shortName', ticker)
            portfolio[company_name] = f"{weight}% allocation ({ticker})"
        except Exception as e:
            portfolio[ticker] = f"{weight}% allocation (info unavailable)"

    return portfolio

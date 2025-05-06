

import yfinance as yf
import pandas as pd

def fetch_portfolio_prices(tickers):
    prices = {}
    missing = []

    try:
        data = yf.download(tickers, period="1d", group_by='ticker', auto_adjust=True, progress=False)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch data from yFinance: {e}")

    for ticker in tickers:
        try:
            # Handle both single and multiple ticker cases
            if len(tickers) == 1:
                df = data
            else:
                df = data[ticker]
            
            # Prefer 'Adj Close', fallback to 'Close'
            if 'Adj Close' in df.columns:
                price = df['Adj Close'].iloc[-1]
            elif 'Close' in df.columns:
                price = df['Close'].iloc[-1]
            else:
                raise KeyError("No 'Adj Close' or 'Close' found")

            if pd.notna(price):
                prices[ticker] = float(price)
            else:
                missing.append(ticker)

        except Exception as e:
            print(f"⚠️ Error retrieving price for {ticker}: {e}")
            missing.append(ticker)

    if missing:
        raise ValueError(f"Price data missing for: {', '.join(missing)}")

    print("✅ Final fetched prices:", prices)
    return prices






def calculate_current_allocation(tickers, weights, prices):
    """Returns current value of each holding and % allocation."""

    if not prices or not isinstance(prices, dict):
        raise ValueError("Price data is missing or invalid.")

    values = []
    for i, ticker in enumerate(tickers):
        price = prices.get(ticker)
        if price is None:
            raise ValueError(f"Missing price data for ticker: {ticker}")
        values.append(weights[i] * price)

    total_value = sum(values)
    if total_value == 0:
        raise ZeroDivisionError("Total portfolio value is zero. Cannot calculate allocation.")

    allocation = [v / total_value for v in values]
    return values, allocation


def generate_rebalance_plan(tickers, target_weights, current_weights, total_value):
    """Returns the dollar and % changes needed to rebalance."""
    rebalance_plan = []
    for i, ticker in enumerate(tickers):
        current = current_weights[i]
        target = target_weights[i]
        delta = target - current
        dollar_change = delta * total_value
        rebalance_plan.append({
            "Ticker": ticker,
            "Current %": round(current * 100, 2),
            "Target %": round(target * 100, 2),
            "Change %": round(delta * 100, 2),
            "Trade Amount ($)": round(dollar_change, 2)
        })
    return pd.DataFrame(rebalance_plan)

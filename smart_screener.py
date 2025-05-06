import yfinance as yf
import pandas as pd
from openai_client import client


def fetch_candidate_stocks(tickers=None):
    if tickers is None:
        tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]  # Example default list

    data = yf.download(tickers, period="1d")

    # Handle both single and multiple tickers
    if isinstance(data.columns, pd.MultiIndex):
        # Multiple tickers case
        if 'Adj Close' in data.columns.levels[0]:
            prices = data['Adj Close'].iloc[-1]
        elif 'Close' in data.columns.levels[0]:
            prices = data['Close'].iloc[-1]
        else:
            raise KeyError("Neither 'Adj Close' nor 'Close' found in MultiIndex data.")
    else:
        # Single ticker case
        if 'Adj Close' in data.columns:
            prices = data['Adj Close'].iloc[-1]
        elif 'Close' in data.columns:
            prices = data['Close'].iloc[-1]
        else:
            raise KeyError("Neither 'Adj Close' nor 'Close' found in data.")

    return prices

def screen_stocks_with_gpt(prompt, stock_data: pd.DataFrame):
    if isinstance(stock_data, pd.Series):
        stock_list = stock_data.to_frame().T.to_dict(orient="records")
    else:
        stock_list = stock_data.to_dict(orient="records")

    formatted = "\n".join([f"{row.get('index', 'Unknown')}: ${row.get('Price', 0):.2f}" for row in stock_list])

    query = (
        f"User prompt: {prompt}\n\n"
        f"Here is a list of stocks and their prices:\n{formatted}\n\n"
        "Based on the user prompt, return 5 stocks that best match it with 1-sentence reasons."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a smart stock screener."},
            {"role": "user", "content": query}
        ],
        temperature=0.6,
        max_tokens=500
    )

    return response.choices[0].message.content

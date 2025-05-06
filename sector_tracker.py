# sector_tracker.py

import yfinance as yf
import pandas as pd
import numpy as np

sector_etfs = {
    "Technology": "XLK",
    "Healthcare": "XLV",
    "Financials": "XLF",
    "Energy": "XLE",
    "Consumer Discretionary": "XLY",
    "Utilities": "XLU"
}

def fetch_sector_performance(period="3mo"):
    data = {}
    for sector, symbol in sector_etfs.items():
        df = yf.download(symbol, period=period)["Close"]

        if df is not None and not df.empty:
            # Handle the case where df might be a DataFrame with multiple columns
            if isinstance(df, pd.Series):
                start_price = df.iloc[0]
                end_price = df.iloc[-1]
            else:
                start_price = df.iloc[0].mean()
                end_price = df.iloc[-1].mean()

            returns = (end_price - start_price) / start_price
            data[sector] = round(returns * 100, 2)
        else:
            data[sector] = np.nan  # Use np.nan for compatibility

    return pd.Series(data).dropna().sort_values(ascending=False)

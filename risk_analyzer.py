import yfinance as yf
import pandas as pd
import numpy as np

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    excess_returns = returns.mean() * 252 - risk_free_rate
    volatility = returns.std() * np.sqrt(252)
    if volatility == 0:
        return None, 0  # Avoid division by zero
    sharpe = excess_returns / volatility
    return round(sharpe, 3), round(volatility, 4)

def calculate_beta(ticker, benchmark="^GSPC", period="6mo"):
    try:
        df = yf.download([ticker, benchmark], period=period, auto_adjust=True)

        # Handle multi or flat structure
        if isinstance(df.columns, pd.MultiIndex) and "Close" in df.columns.levels[0]:
            df = df["Close"].dropna()
        elif "Close" in df.columns:
            df = df[["Close"]].dropna()
        else:
            print("🔴 No 'Close' column found.")
            return None

        if df.shape[1] != 2:
            print("🔴 Not enough data columns for beta calculation")
            return None

        returns = df.pct_change().dropna()
        cov_matrix = returns.cov()
        beta = cov_matrix.iloc[0, 1] / cov_matrix.iloc[1, 1]
        return round(beta, 3)

    except Exception as e:
        print(f"🔴 Error in calculate_beta for {ticker}: {e}")
        return None

def run_risk_analysis(ticker):
    try:
        df = yf.download(ticker, period="6mo", auto_adjust=True)

        # Handle MultiIndex or flat structure
        if isinstance(df.columns, pd.MultiIndex) and 'Close' in df.columns.levels[0]:
            close_prices = df['Close'][ticker].dropna()
        elif "Adj Close" in df.columns:
            close_prices = df["Adj Close"].dropna()
        elif "Close" in df.columns:
            close_prices = df["Close"].dropna()
        else:
            print("⚠️ No valid close price column found.")
            return None, None

        returns = close_prices.pct_change().dropna()
        if returns.empty:
            print("⚠️ Returns are empty after pct_change.")
            return None, None

        sharpe, std_dev = calculate_sharpe_ratio(returns)
        beta = calculate_beta(ticker)

        print(f"✅ Sharpe: {sharpe}, Volatility (std): {std_dev}, Beta: {beta}")
        return sharpe, beta

    except Exception as e:
        print(f"🔴 Error in run_risk_analysis for {ticker}: {e}")
        return None, None

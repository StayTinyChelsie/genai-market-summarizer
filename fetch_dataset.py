# fetch_dataset.py
import os
import pandas as pd
import yfinance as yf
import streamlit as st

def fetch_yfinance_multiindex_data(tickers, period="6mo", interval="1d"):
    if isinstance(tickers, str):
        tickers = [t.strip().upper() for t in tickers.split(",") if t.strip()]

    try:
        data = yf.download(
            tickers=tickers,
            period=period,
            interval=interval,
            group_by="column",
            auto_adjust=True,
            threads=True
        )

        if data.empty or len(data.columns) == 0:
            raise ValueError("No data returned from yfinance.")

        if not isinstance(data.columns, pd.MultiIndex):
            ticker = tickers[0]
            data.columns = pd.MultiIndex.from_product([data.columns, [ticker]], names=["Metric", "Ticker"])

        if not pd.api.types.is_datetime64_any_dtype(data.index):
            data.index = pd.to_datetime(data.index)

        return data

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def fetch_valuation_metrics(tickers):
    summaries = []
    for t in tickers:
        try:
            info = yf.Ticker(t).info
            pe = info.get("trailingPE", "N/A")
            mc = info.get("marketCap", "N/A")
            summaries.append(f"**{t}**\n- P/E Ratio: {pe}\n- Market Cap: {mc:,}" if mc != "N/A" else f"**{t}**: Valuation unavailable")
        except:
            summaries.append(f"**{t}**: Error retrieving data")
    return summaries

def fetch_sector_info(tickers):
    sector_info = []
    for t in tickers:
        try:
            info = yf.Ticker(t).info
            sector = info.get("sector", "Unknown")
            sector_info.append(f"**{t}** → Sector: {sector}")
        except:
            sector_info.append(f"**{t}** → Sector data unavailable")
    return sector_info

def compare_vs_benchmark(tickers, df, benchmark="^GSPC"):
    try:
        benchmark_data = yf.download(benchmark, period="6mo", interval="1d", auto_adjust=True)
        if benchmark_data.empty or "Close" not in benchmark_data.columns:
            return ["⚠️ Benchmark data unavailable."]

        insights = []
        for t in tickers:
            try:
                stock_close = df.xs(t, level=1, axis=1)['Close'].pct_change().dropna()
                bench_close = benchmark_data['Close'].pct_change().dropna().reindex(stock_close.index, method='pad')
                relative_return = (stock_close - bench_close).mean()
                insights.append(f"**{t}** performed {'above' if relative_return > 0 else 'below'} the benchmark with a daily alpha of {relative_return:.4f}")
            except:
                insights.append(f"**{t}**: Benchmark comparison failed")
        return insights
    except Exception as e:
        return [f"⚠️ Failed to compare benchmark: {e}"]

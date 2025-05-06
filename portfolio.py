# portfolio.py
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

def simulate_portfolio(df, tickers, weights):
    returns = pd.DataFrame()
    for t in tickers:
        try:
            close = df.xs(t, level=1, axis=1)['Close']
            returns[t] = close.pct_change()
        except:
            continue
    portfolio_returns = (returns * weights).sum(axis=1)
    cumulative = (1 + portfolio_returns).cumprod()
    return cumulative

def efficient_frontier(df, tickers):
    weights_list = []
    returns_list = []
    risks_list = []
    for _ in range(500):
        weights = np.random.random(len(tickers))
        weights /= weights.sum()
        portfolio_return = 0
        portfolio_variance = 0
        for i, t in enumerate(tickers):
            try:
                data = df.xs(t, level=1, axis=1)['Close'].pct_change().dropna()
                portfolio_return += weights[i] * data.mean() * 252
                portfolio_variance += (weights[i] ** 2) * data.var() * 252
            except:
                continue
        weights_list.append(weights)
        returns_list.append(portfolio_return)
        risks_list.append(np.sqrt(portfolio_variance))
    frontier_df = pd.DataFrame({"Return": returns_list, "Risk": risks_list})
    fig = px.scatter(frontier_df, x="Risk", y="Return", title="Efficient Frontier")
    st.plotly_chart(fig)

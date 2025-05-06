import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def simulate_monte_carlo(tickers, weights, years=10, simulations=1000, expected_return=0.07, volatility=0.15):
    results = []
    np.random.seed(42)
    initial_investment = 10000

    for _ in range(simulations):
        simulated_growth = [initial_investment]
        for _ in range(years):
            annual_return = np.random.normal(expected_return, volatility)
            new_value = simulated_growth[-1] * (1 + annual_return)
            simulated_growth.append(new_value)
        results.append(simulated_growth)

    df = pd.DataFrame(results).T
    return df

def plot_simulation(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df, color="gray", alpha=0.1)
    ax.plot(df.mean(axis=1), color="blue", label="Mean")
    ax.set_title("Monte Carlo Simulation of Portfolio Growth")
    ax.set_xlabel("Years")
    ax.set_ylabel("Portfolio Value ($)")
    ax.legend()
    return fig

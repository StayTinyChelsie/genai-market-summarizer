# summary.py
import os
import pandas as pd
from openai_client import client

def generate_ai_insight(ticker, df, output_dir="data"):
    os.makedirs(output_dir, exist_ok=True)
    try:
        prompt = f"Analyze the stock trends and price behavior for {ticker} using this data:\n{df[['Close', 'Volume']].tail(10).to_string()}\n\nProvide a 2-3 sentence insight."
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=200
        )
        insight = response.choices[0].message.content.strip()
        insight_path = f"{output_dir}/{ticker.replace('^', '')}_ai_insight.txt"
        with open(insight_path, "w") as f:
            f.write(insight)
        return insight
    except Exception as e:
        print(f"⚠️ Failed to generate insight for {ticker}:", e)
        return None

def generate_comparison_summary(tickers, df):
    try:
        prompt = "Compare the following stocks based on recent price and volume behavior:\n\n"
        for t in tickers:
            try:
                close = df.xs(t, level=1, axis=1)['Close'].tail(5).tolist()
                volume = df.xs(t, level=1, axis=1)['Volume'].tail(5).tolist()
                prompt += f"\n{t} - Close: {close}, Volume: {volume}"
            except:
                continue
        prompt += "\n\nGive 2-3 key insights comparing them: trends, volatility, momentum."
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error generating comparison summary: {e}"

def generate_market_overview_and_insights(df, tickers):
    try:
        close_prices = {}
        for t in tickers:
            try:
                close = df.xs(t, level=1, axis=1)['Close']
                close_prices[t] = close.tail(7).to_list()
            except:
                continue

        prompt = (
            f"You're a financial analyst. Here is the latest weekly closing price data for stocks: {close_prices}.\n"
            "1. Write a concise 'Market Overview' explaining the general market direction, volatility, or trends.\n"
            "2. Then write 3–4 bullet points as 'Key Insights' about specific stock behavior, momentum, or anomalies.\n\n"
            "Format:\nMarket Overview: <short paragraph>\nKey Insights:\n- Bullet 1\n- Bullet 2..."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=400
        )

        content = response.choices[0].message.content.strip()
        market_overview = ""
        key_insights = []

        if "Market Overview:" in content and "Key Insights:" in content:
            market_overview = content.split("Market Overview:")[1].split("Key Insights:")[0].strip()
            insights_section = content.split("Key Insights:")[1].strip()
            key_insights = [line.strip("- ").strip() for line in insights_section.split("\n") if line.strip()]
        else:
            market_overview = content[:250]
            key_insights = content[250:].split("\n")

        return market_overview, key_insights

    except Exception as e:
        print(f"⚠️ Failed to generate market overview and insights: {e}")
        return "", []

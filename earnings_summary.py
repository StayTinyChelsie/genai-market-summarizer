import yfinance as yf
from openai_client import client

def fetch_earnings_summary(ticker):
    stock = yf.Ticker(ticker)
    try:
        earnings = stock.calendar.T
        last_eps = earnings["EPS actual"].iloc[-1]
        last_rev = earnings["Revenue actual"].iloc[-1]
        return f"Last earnings for {ticker}: EPS = {last_eps}, Revenue = {last_rev}"
    except:
        return f"No earnings data found for {ticker}."

def generate_ai_earnings_summary(ticker):
    text = fetch_earnings_summary(ticker)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a financial analyst summarizing earnings."},
            {"role": "user", "content": f"Summarize this earnings result: {text}"}
        ],
        temperature=0.6,
        max_tokens=300
    )
    return response.choices[0].message.content

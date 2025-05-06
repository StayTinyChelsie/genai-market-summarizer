import yfinance as yf
from openai_client import client

def fetch_basic_ticker_data(ticker):
    """Get price, market cap, PE ratio, and sector."""
    try:
        data = yf.Ticker(ticker).info
        return {
            "symbol": ticker.upper(),
            "name": data.get("shortName", "N/A"),
            "price": data.get("currentPrice", "N/A"),
            "sector": data.get("sector", "N/A"),
            "marketCap": data.get("marketCap", "N/A"),
            "peRatio": data.get("trailingPE", "N/A"),
            "summary": data.get("longBusinessSummary", "")
        }
    except Exception as e:
        return {"error": f"Could not fetch data for {ticker}: {e}"}

def generate_ticker_analysis(ticker):
    info = fetch_basic_ticker_data(ticker)
    if "error" in info:
        return info["error"]

    prompt = (
        f"Write an investment-grade analysis of the following company:\n\n"
        f"Name: {info['name']}\n"
        f"Symbol: {info['symbol']}\n"
        f"Sector: {info['sector']}\n"
        f"Price: ${info['price']}\n"
        f"Market Cap: {info['marketCap']}\n"
        f"P/E Ratio: {info['peRatio']}\n"
        f"Business Summary: {info['summary'][:500]}\n\n"
        "Include potential growth opportunities, risks, and a valuation comment."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional financial analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=700
    )

    return response.choices[0].message.content

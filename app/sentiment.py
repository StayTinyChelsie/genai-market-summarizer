
def classify_sentiment(summary):
    if "strong" in summary.lower() or "positive outlook" in summary.lower():
        return "Bullish"
    elif "decline" in summary.lower() or "warning" in summary.lower():
        return "Bearish"
    else:
        return "Neutral"

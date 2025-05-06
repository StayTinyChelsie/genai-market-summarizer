
def classify_sentiment(summary):
    if "strong" in summary.lower() or "positive outlook" in summary.lower():
        return "Bullish"
    elif "decline" in summary.lower() or "warning" in summary.lower():
        return "Bearish"
    else:
        return "Neutral"
if __name__ == "__main__":
    test_summary = "The market shows a strong recovery with a positive outlook."
    sentiment = classify_sentiment(test_summary)
    print(f"Sentiment: {sentiment}")
    
import os
import requests
import datetime
from dotenv import load_dotenv
from summarizer import summarize_text

load_dotenv()
NYT_API_KEY = os.getenv("NYT_API_KEY")
OUTPUT_DIR = "data"
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "nyt_summaries.txt")


# ✅ Fetch from keyword search (used by main.py)
def fetch_nyt_articles(query, max_results=5):
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        "q": query,
        "api-key": NYT_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ Failed to fetch NYT articles: {response.status_code}")
        return []

    docs = response.json().get("response", {}).get("docs", [])
    articles = []
    for doc in docs[:max_results]:
        articles.append({
            "title": doc.get("headline", {}).get("main", "No title"),
            "url": doc.get("web_url", "#"),
            "date": doc.get("pub_date", "")[:10],
            "summary": summarize_text(doc.get("abstract", "") or doc.get("lead_paragraph", ""))
        })
    return articles


# ✅ Optional: Top stories (still usable from command line)
def fetch_top_stories(section="business"):
    url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json"
    params = {"api-key": NYT_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ Failed to fetch NYT top stories: {response.status_code}")
        return []
    return response.json().get("results", [])


def summarize_articles(articles):
    summaries = []
    for article in articles[:5]:
        title = article.get("title")
        abstract = article.get("abstract")
        url = article.get("url")
        combined_text = f"{title}\n\n{abstract}"
        try:
            summary = summarize_text(combined_text)
            summaries.append(f"\n📰 {title}\n🔗 {url}\n📄 {summary}\n")
        except Exception as e:
            print(f"⚠️ Error summarizing article '{title}':", e)
    return summaries


def save_summaries(summaries):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(SUMMARY_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n===== NYT Business Summaries — {timestamp} =====\n")
        for summary in summaries:
            f.write(summary + "\n")
    print(f"✅ Saved {len(summaries)} NYT summaries to {SUMMARY_FILE}")


# CLI test mode
if __name__ == "__main__":
    articles = fetch_top_stories()
    if articles:
        summaries = summarize_articles(articles)
        save_summaries(summaries)


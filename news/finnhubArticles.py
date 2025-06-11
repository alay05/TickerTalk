import requests
import os
from datetime import datetime, timedelta, UTC

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")

def get_finnhub_articles(ticker, MAX_ARTICLES):
    today = datetime.now(UTC).date()
    timeframe = 5 # past amount of days
    start_date = today - timedelta(days=timeframe)
    
    url = "https://finnhub.io/api/v1/company-news"
    params = {
        "symbol": ticker.upper(),
        "from": start_date.isoformat(),
        "to": today.isoformat(),
        "token": FINNHUB_API_KEY
    }
    feed = requests.get(url, params=params)

    articles = []
    if feed.ok:
        for item in feed.json():
            articles.append({
                "title": item.get("headline", ""),
                "summary": item.get("summary", "").strip(),
                "url": item.get("url", "")
            })

            if len(articles) >= MAX_ARTICLES:
                break

    return articles
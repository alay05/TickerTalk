import feedparser

def get_google_news_articles(ticker, MAX_ARTICLES):
    query = f"{ticker} stock"
    rss_url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)

    articles = []
    for entry in feed.entries:
        title = entry.get("title", "")

        articles.append({
            "title": title,
            "summary": title, # no summary on google
            "url": entry.get("link", "")
        })

        if len(articles) >= MAX_ARTICLES:
            break

    return articles
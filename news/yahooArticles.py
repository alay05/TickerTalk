import yfinance as yf

def get_yahoo_articles(ticker, MAX_ARTICLES):
    stock = yf.Ticker(ticker)
    feed = stock.news
    
    articles = []
    for art in feed:
        cont = art.get("content", {})
        url = (
            (art.get("clickThroughUrl") or {}).get("url")
            or (art.get("canonicalUrl") or {}).get("url")
            or (cont.get("clickThroughUrl") or {}).get("url")
            or (cont.get("canonicalUrl") or {}).get("url")
            or None
        )
        articles.append({
            "title": cont.get("title"),
            "summary": cont.get("summary") or cont.get("description"),
            "url": url
        })

        if len(articles) >= MAX_ARTICLES:
            break

    return articles
import yfinance as yf
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions
from config import nlu

def analyze_ticker(ticker):
    ticker = ticker.upper()
    stock = yf.Ticker(ticker)
    name = (stock.info.get("displayName") or stock.info.get("shortName") or stock.info.get("longName") or ticker).lower()

    articles = stock.news
    simplified = []

    for art in articles:
        cont = art.get("content", {})
        url = (
            (art.get("clickThroughUrl") or {}).get("url")
            or (art.get("canonicalUrl") or {}).get("url")
            or (cont.get("clickThroughUrl") or {}).get("url")
            or (cont.get("canonicalUrl") or {}).get("url")
            or None
        )
        simplified.append({
            "title": cont.get("title"),
            "summary": cont.get("summary") or cont.get("description"),
            "url": url,
            "pubDate": cont.get("pubDate")
        })

    scores = []
    for art in simplified:
        text = f"{art.get('title', '')}. {art.get('summary', '')}"
        if not text.strip():
            continue

        response = nlu.analyze(
            text=text,
            features=Features(
                entities=EntitiesOptions(sentiment=True, limit=10)
            )
        ).get_result()

        for ent in response.get("entities", []):
            ent_text = ent.get("text", "").lower()
            if  ent_text == ticker.lower() or ent_text == name:
                score = ent["sentiment"]["score"]
                scores.append(score)
                break

    avg_score = sum(scores) / len(scores) if scores else 0.0
    threshold = 2 # for score 0-10
    if avg_score >= threshold/5:
        decision = "BUY"
    elif avg_score <= -threshold/5:
        decision = "SELL"
    else:
        decision = "HOLD"

    return {
        "ticker": ticker,
        "company_name": name.title(),
        "sentiment_score": round(avg_score*5 + 5, 1),
        "recommendation": decision,
    }

# for testing
if __name__ == '__main__':
    import sys
    ticker = sys.argv[1] if len(sys.argv) > 1 else 'HOOD'
    result = analyze_ticker(ticker)
    print(result)

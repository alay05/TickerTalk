from flask import Flask, request, jsonify, render_template
import yfinance as yf
from analyzer import analyze_ticker
from news.yahooArticles import get_yahoo_articles
from news.googleArticles import get_google_news_articles
from news.finnhubArticles import get_finnhub_articles
from news.deduplicate import deduplicate_articles

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

article_cache = {}

@app.route("/")
def home():
    return render_template("base.html")

@app.route('/analyze', methods=['GET'])
def analyze():
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        return jsonify({'error': 'Ticker required'}), 400

    try:
        # determine article counts based on slider
        article_count = int(request.args.get("article_count", 10)) # defaults 10
        
        yahoo_count = 10
        google_count = int((article_count-10)*0.25)
        finnhub_count = int((article_count-10)*0.75)

        total = yahoo_count+google_count+finnhub_count

        if total < article_count:
            finnhub_count += article_count-total

        # fetch articles once here
        yahoo_articles = get_yahoo_articles(ticker, yahoo_count) 
        google_articles = get_google_news_articles(ticker, google_count)
        finnhub_articles = get_finnhub_articles(ticker, finnhub_count)
        articles = deduplicate_articles([yahoo_articles, google_articles, finnhub_articles])

        # cache for reuse
        article_cache[ticker] = articles

        result = analyze_ticker(ticker, preloaded_articles=articles)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/price-history', methods=['GET'])
def price_history():
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        return jsonify({'error': 'Ticker required'}), 400

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1y")
        hist = hist.resample("W").mean()

        if hist.empty:
            return jsonify({'error': 'No data found for this ticker'}), 404

        labels = [d.strftime("%b") if d.day < 8 else "" for d in hist.index]
        prices = hist["Close"].round(2).tolist()
        return jsonify({"labels": labels, "prices": prices})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/articles', methods=['GET'])
def get_articles():
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        return jsonify({'error': 'Ticker required'}), 400

    try:
        if ticker not in article_cache:
            return jsonify({'error': 'No cached data found. Please analyze the ticker first.'}), 404

        articles = article_cache[ticker]
        return jsonify([
            {
                "title": art.get("title", "No title"),
                "summary": art.get("summary", "No summary available."),
                "url": art.get("url") or art.get("link") or "#"
            }
            for art in articles
        ])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)

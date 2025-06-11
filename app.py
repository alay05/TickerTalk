from flask import Flask, request, jsonify
import yfinance as yf
from analyzer import analyze_ticker

app = Flask(__name__, static_folder='frontend', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/analyze', methods=['GET'])
def analyze():
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        return jsonify({'error': 'Ticker required'}), 400

    try:
        result = analyze_ticker(ticker)
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

if __name__ == '__main__':
    app.run(debug=True)

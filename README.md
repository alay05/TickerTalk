# TickerTalk

## Project Description

TickerTalk is a full-stack web application that analyzes recent news headlines of publicly traded stocks. Users are able to input a stock ticker to fetch relevant articles, which are processed using IBM NLU for sentiment analysis. The output is visualized with an interactive dashboard that includes a sentiment score bar, an investment recommendation (Buy/Hold/Sell), and a historical price chart. Users can also view a page showcasing each of the articles used during analysis, each with a clickable link to the full article.

ADD A VIDEO LINK

## Features

- **User Input**: Allows users to enter a stock ticker (e.g., `TSLA`, `GOOG`)
- **Sentiment Analysis**: Articles are processed using IBM Watson NLU to extract and score sentiment
- **Investment Advice**: Displays a "Buy", "Hold", or "Sell" label based on average sentiment
- **Visualization**:
  - Horizontal sentiment bar indicator
  - Historical price line chart using Chart.js
  - Expandable news article list with summaries and links

## Tech Stack

- **Frontend**: HTML (Jinja templates), Tailwind CSS, JavaScript
- **Backend**: Python with Flask
- **Data & Analysis**: IBM NLU

## Running Locally

### Backend

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/TickerTalk.git
   cd TickerTalk
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
3. Install dependencies:
   ```bash
   Install dependencies:
4. Create a '.env' file and add your IBM NLU & Finnhub credentials:
   ```bash
   IBM_API_KEY=your_key_here
   IBM_URL=your_url_here
   FINNHUB_API_KEY=your_key_here
5. Start the server:
   ```bash
   python app.py
6. Visit http://localhost:5000 or http://127.0.0.1:5000 in your browser.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

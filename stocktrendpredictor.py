import requests
import openai
from datetime import datetime, timedelta

# Set your API keys
FINNHUB_API_KEY = 'YOUR_FINNHUB_API_KEY'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

openai.api_key = OPENAI_API_KEY

# Get current time and last 24 hours timestamp
end_time = datetime.now()
start_time = end_time - timedelta(days=1)

# Query Finnhub for the latest stock news
def fetch_latest_news():
    url = f'https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}'
    response = requests.get(url)
    return response.json()

# Analyze news sentiment using ChatGPT
def analyze_news_sentiment(news):
    stocks_trending = {}
    
    for article in news:
        if 'datetime' in article and datetime.fromtimestamp(article['datetime']) >= start_time:
            text = article['title'] + " " + article['summary']
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": f"Analyze the sentiment of the following news article: {text}"}
                ]
            )
            sentiment = response.choices[0].message['content']
            # Assuming sentiment contains stock tickers, you can refine this logic
            for stock in ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]:  # Add more tickers as needed
                if stock in text:
                    stocks_trending[stock] = stocks_trending.get(stock, 0) + 1 if "positive" in sentiment.lower() else 0

    return stocks_trending

# Fetch news and analyze sentiment
latest_news = fetch_latest_news()
stocks_likelihood = analyze_news_sentiment(latest_news)

# Sort stocks by likelihood and get top 25
top_stocks = sorted(stocks_likelihood.items(), key=lambda x: x[1], reverse=True)[:25]

print("Top 25 Stocks Likely to Trend:")
for stock, likelihood in top_stocks:
    print(f"{stock}: {likelihood} trending mentions")

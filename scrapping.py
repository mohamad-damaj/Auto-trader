import yfinance as yf
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
import praw

load_dotenv()

finkey = os.getenv("FINNKEY")
Secret = os.getenv("Secret_Reddit")
Client_ID = os.getenv("Client_ID_Reddit")
User_Agent = os.getenv("user_agent")
def get_reddit(ticker):
    reddit = praw.Reddit(
        client_id=Client_ID,
        client_secret=Secret,
        user_agent=User_Agent
    )
    
    keywords = ["apple", "aapl", "$aapl", "iphone", "tim cook"]

    target_subs = ["stocks", "wallstreetbets", "investing", "StockMarket", "technology", "finance", "business", "news"]
    one_hour_ago = datetime.now() - timedelta(hours=1)
    
    posts = []

    for sub in target_subs:
        for submission in reddit.subreddit(sub).new(limit=50):
            created_utc = datetime.fromtimestamp(submission.created_utc)
            if created_utc > one_hour_ago:
                if any(kw in submission.title.lower() or kw in submission.selftext.lower() for kw in keywords):
                    posts.append({
                        "id": id,
                        "subreddit": sub,
                        "title": submission.title,
                        "created_utc": submission.created_utc,
                        "body": submission.selftext.lower()
                    })

    return posts


def get_news(ticker):
    url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from=2025-06-18&to=2025-06-19&token={finkey}"
    response = requests.get(url)
    data = response.json()

    return [(item['headline'], datetime.fromtimestamp(item['datetime']).strftime('%Y-%m-%d %H:%M:%S'), item['id']) for item in data]

def get_prices(TICKER):
    ticker = yf.Ticker(TICKER)
    df = ticker.history(period="7d", interval="1m")
    return df


if __name__=="__main__":
    news = get_news("AAPL")
    prices = get_prices("AAPL")
    tweets = get_reddit("AAPL")
    print(news[0], tweets)



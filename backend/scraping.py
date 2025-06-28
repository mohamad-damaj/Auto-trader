import yfinance as yf
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
import praw
import pandas as pd

load_dotenv()

finkey = os.getenv("FINNKEY")
Secret = os.getenv("Secret_Reddit")
Client_ID = os.getenv("Client_ID_Reddit")
User_Agent = os.getenv("user_agent")

def get_reddit(ticker, time_prev):
    reddit = praw.Reddit(
        client_id=Client_ID,
        client_secret=Secret,
        user_agent=User_Agent
    )
    
    keywords = ["apple", "aapl", "$aapl", "iphone", "tim cook"]

    target_subs = ["stocks", "wallstreetbets", "investing", "StockMarket", "technology", "finance", "business", "news"]
    one_hour_ago = datetime.now() - timedelta(hours = time_prev)
    
    posts = []

    for sub in target_subs:
        for submission in reddit.subreddit(sub).new(limit=50):
            created_utc = datetime.fromtimestamp(submission.created_utc)
            if True:
                if any(kw in submission.title.lower() or kw in submission.selftext.lower() for kw in keywords):
                    posts.append({
                        "id": submission.id,
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

    return [{
    "id": item["id"],
    "datetime": item["datetime"],
    "headline": item["headline"],
    "summary": item["summary"],
    } for item in data]

def get_prices(TICKER):
    ticker = yf.Ticker(TICKER)
    df = ticker.history(period="7d", interval="1m")
    df = df.reset_index().rename(columns={
    "Datetime": "timestamp",  
    "Open": "open_price",
    "High": "high_price",
    "Low": "low_price",
    "Close": "close_price",
    "Volume": "volume",
    "Dividends": "dividends",
    "Stock Splits": "stock_splits"
    })

    df["timestamp"] = df["timestamp"].astype(str)

    return df.to_dict(orient="records")


if __name__=="__main__":
    news = get_news("AAPL")
    prices = get_prices("AAPL")
    reddit = get_reddit("AAPL", 1)
    print(prices)



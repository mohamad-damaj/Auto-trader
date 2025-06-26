import yfinance as yf
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
import praw

load_dotenv()

finkey = os.getenv("FINNKEY")

def get_reddit(ticker):
    reddit = praw.reddit(
        read_only = True
    )



def get_news(ticker):
    url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from=2025-06-18&to=2025-06-19&token={finkey}"
    response = requests.get(url)
    data = response.json()

    return [(item['headline'], datetime.fromtimestamp(item['datetime']).strftime('%Y-%m-%d %H:%M:%S')) for item in data]

def get_prices(TICKER):
    ticker = yf.Ticker(TICKER)
    df = ticker.history(period="7d", interval="1h")
    return df


if __name__=="__main__":
    news = get_news("AAPL")
    prices = get_prices("AAPL")
    tweets = get_tweets("AAPL")


    print(tweets)
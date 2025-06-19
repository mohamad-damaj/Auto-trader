import twint
import yfinance as yf
from dotenv import load_dotenv
import os
import requests

load_dotenv()

finkey = os.getenv("FINNKEY")

def get_tweets():
    # Configure
    c = twint.Config()
    c.Search = "$TSLA"
    c.Lang = "en"
    c.Limit = 10
    c.Pandas = True

    # Run
    twint.run.Search(c)
    df = twint.storage.panda.Tweets_df

    return df['tweet'].tolist()



def get_news(ticker):
    url = f"https://finnhub.io/api/v1/company-news?symbol={ticker}&from=2025-06-18&to=2025-06-19&token={finkey}"
    response = requests.get(url)
    data = response.json()

    return [item['headline'] for item in data]

def get_prices(TICKER):
    ticker = yf.Ticker(TICKER)
    df = ticker.history(period="5d", interval="1h")
    return df


if __name__=="__main__":
    news = get_news("AAPL")

    print(news)
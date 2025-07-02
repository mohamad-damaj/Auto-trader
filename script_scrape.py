import logging
from .backend.scraping import get_news, get_prices, get_reddit
from .backend.save_to_db import save_to_table
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from .backend.sentiment import finbert_pipeline, vader_pipeline
from .utils.supabase.client import client




logging.basicConfig(
    filename="cron_job.log",
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

def run_cron_job(supabase, date_from, date_to, days= "7d", intervals = "1h", ticker="AAPL", hours_back=1):
    logging.info(f"Starting cron job for {ticker}")
    
    try:
        pipe = pipeline("text-classification", model="ProsusAI/finbert")
        raw_news = get_news(ticker, date_from, date_to)
        if raw_news:
            news_data = finbert_pipeline(pipe, raw_news)
            save_to_table(supabase, news_data, "news")
            logging.info(f"Saved {len(news_data)} news articles")
        else:
            logging.warning("No news data fetched")
    except Exception as e:
        logging.error(f"Error in news processing: {e}")

    try:
        analyzer = SentimentIntensityAnalyzer()
        raw_reddit = get_reddit(ticker, hours_back)
        if raw_reddit:
            reddit_data = vader_pipeline(analyzer, raw_reddit)
            save_to_table(supabase, reddit_data, "reddit")
            logging.info(f"Saved {len(reddit_data)} reddit posts")
        else:
            logging.warning("No reddit data fetched")
    except Exception as e:
        logging.error(f"Error in reddit processing: {e}")
    
    try:
        prices = get_prices(ticker, days=days, interval=intervals)
        if prices:
            save_to_table(supabase, prices, "price")
            logging.info("Saved latest price data")
        else:
            logging.warning("No price data fetched")
    except Exception as e:
        logging.error(f"Error in price processing: {e}")
    
    logging.info(f"Cron job for {ticker} completed successfully\n")

if __name__ == "__main__":
    run_cron_job(date_from="2025-06-29", date_to="2025-07-01", days= "7d", intervals = "1h", ticker="AAPL", hours_back=2160)
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from scrapping import get_news
def finbert_pipeline(pipe, news):
    for article in news:
        text = f"{article['headline']} {article['summary']}"
        score = pipe(text)
        article["score"] = score[0]["score"]
        article["finbert_sentiment"] = score[0]["label"]

    return news


def enrich_posts(analyzer, posts):
    for post in posts:
        text = f"{post['title']} {post['body']}"
        score = analyzer.polarity_scores(text)
        post["vader_sentiment"] = score["compound"]

    return posts

if __name__=="__main__":
    pipe = pipeline("text-classification", model="ProsusAI/finbert")
    print(finbert_pipeline(pipe, get_news("AAPL"))[0])







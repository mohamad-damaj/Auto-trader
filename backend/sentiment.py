from backend.scraping import get_news, get_reddit
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline


def finbert_pipeline(pipe, news):
    for article in news:
        text = f"{article['headline']} {article['summary']}"
        score = pipe(text)
        article["score"] = score[0]["score"]
        article["finbert_sentiment"] = score[0]["label"]

    return news


def vader_pipeline(analyzer, posts):
    for post in posts:
        text = f"{post['title']} {post['body']}"
        vs = analyzer.polarity_scores(text)
        post["vader_sentiment"] = vs["compound"]

    return posts

if __name__=="__main__":
    pipe = pipeline("text-classification", model="ProsusAI/finbert")
    print(finbert_pipeline(pipe, get_news("AAPL"))[0])
    analyzer = SentimentIntensityAnalyzer()
    print(vader_pipeline(analyzer, get_reddit("AAPL", 1))[0])








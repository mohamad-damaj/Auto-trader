import pandas as pd
import numpy as np
import joblib
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from xgboost import XGBClassifier

class RealTimePredictor:
    def __init__(self,
                 db_url: str,
                 model_path: str,
                 scaler_path: str,
                 lookback_hours: int = 3):
        """
        db_url: SQLAlchemy URL for your Postgres (same as your engine)
        model_path: path to saved XGB model (JSON/.bst)
        scaler_path: path to saved StandardScaler (joblib .pkl)
        lookback_hours: at least 3, so you can compute volatility_3h
        """
        self.engine = create_engine(db_url)

        self.model  = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        self.model.load_model(model_path)
        self.scaler = joblib.load(scaler_path)
        self.lookback = lookback_hours

    def _fetch_price(self, start: datetime, end: datetime):
        q = """
        SELECT
          (timestamp::timestamptz AT TIME ZONE 'UTC') AS timestamp,
          open_price,
          high_price,
          low_price,
          close_price,
          volume
        FROM price
        WHERE
          (timestamp::timestamptz AT TIME ZONE 'UTC') >= %(start)s
          AND (timestamp::timestamptz AT TIME ZONE 'UTC') <  %(end)s
        ORDER BY timestamp
        """
        df = pd.read_sql(
            q,
            self.engine,
            params={"start": start, "end": end},
            parse_dates=["timestamp"]
        )
        df = (
            df
            .set_index("timestamp")
            .resample("1h")
            .agg({
                "open_price":  "first",
                "high_price":  "max",
                "low_price":   "min",
                "close_price": "last",
                "volume":      "sum"
            })
            .dropna()
        )
        return df
    def _fetch_news(self, start: datetime, end: datetime):
        start = start.timestamp()
        end = end.timestamp()
        q = """
        SELECT
          datetime,
          score
        FROM news
        WHERE
          (datetime::bigint) > %(start)s
          AND (datetime::bigint) < %(end)s
        """
        df = pd.read_sql(
            q,
            self.engine,
            params={"start": start, "end": end},
        )

        df["datetime"]  = pd.to_datetime(df["datetime"], unit='s')
        # now floor to the hour & aggregate exactly like your notebook
        df["datetime"] = df["datetime"].dt.floor("h")
        df = (
            df
            .groupby("datetime")["score"]
            .mean()
            .to_frame()
            .resample("1h")
            .mean()
            .rename(columns={"score": "news_sentiment"})
        )

        return df

    def _fetch_reddit(self, start: datetime, end: datetime):
        start = start.timestamp()
        end = end.timestamp()
        q = """
        SELECT
          created_utc AS created_utc,
          vader_sentiment
        FROM reddit
        WHERE
          (created_utc::double precision)::bigint >= %(start)s
          AND (created_utc::double precision)::bigint <  %(end)s
        """
        
        df = pd.read_sql(
            q,
            self.engine,
            params={"start": start, "end": end},
        )
        df["created_utc"] = pd.to_datetime(df["created_utc"],  unit='s')
        df = (
            df
            .set_index("created_utc")["vader_sentiment"]
            .resample("1h")
            .mean()
            .to_frame()
            .rename(columns={"vader_sentiment": "reddit_sentiment"})
        )

        return df



    def predict_next(self):

        now   = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        start = now - timedelta(hours=self.lookback)
        end   = now


        price_df  = self._fetch_price(start, end)
        news_df   = self._fetch_news(start, end)
        reddit_df = self._fetch_reddit(start, end)


        df = price_df.join(news_df,   how="left") \
                     .join(reddit_df, how="left")
        df = df[~(df["news_sentiment"].isna() | df["reddit_sentiment"].isna())]


        df["ret_1h"]        = df["close_price"].pct_change()
        df["volatility_3h"] = df["close_price"].rolling(window=3).std()

        df = df.dropna()
        X_last = df.iloc[[-1]]


        feature_cols = [
            "open_price", "high_price", "low_price", "close_price", "volume",
            "ret_1h", "volatility_3h",
            "news_sentiment", "reddit_sentiment"
        ]
        X = X_last[feature_cols].values


        Xs    = self.scaler.transform(X)
        proba = float(self.model.predict_proba(Xs)[0, 1])
        pred  = int(self.model.predict(Xs)[0])
        return {
            "as_of":  X_last.index[0],
            "pred":   pred,       # 1 = up next hour, 0 = not
            "proba":  proba       # probability of up
        }


if __name__ == "__main__":
    import dotenv
    import os
    dotenv.load_dotenv

    dburl = os.getenv("db_url")
    model_path = r"model\trader.json"
    scaler_path = r"model\scaler.pkl"
    predictor = RealTimePredictor(dburl,
                 model_path,
                 scaler_path, lookback_hours=48)
    result = predictor.predict_next()
    
    print(f"prediction is:", result["pred"])
    

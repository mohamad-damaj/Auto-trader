from ..model.predictor import RealTimePredictor
from ..utils.supabase.client import client
from .save_to_db import save_prediction
from .script_scrape import run_cron_job
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import pandas as pd
import os

def update_prediction_task():
    supabase = client()
    db_url = os.getenv("db_url")
    engine = create_engine(db_url)
    model_path = "model/trader.json"
    scaler_path = "model/scaler.pkl"



    date_to = datetime.utcnow()
    date_from = date_to - timedelta(days=1)

    date_to_str = date_to.strftime("%Y-%m-%d")
    date_from_str = date_from.strftime("%Y-%m-%d")

    run_cron_job(
        supabase=supabase,
        date_from=date_from_str,
        date_to=date_to_str,
        days="7d",
        intervals="1h",
        ticker="AAPL",
        hours_back=24  # or 1 if you only want 1 hour of Reddit
    )
    
    prediction = RealTimePredictor(db_url, model_path, scaler_path, lookback_hours=48)
    result = prediction.predict_next()["pred"]

    q = """SELECT MAX(timestamp) AS latest_timestamp FROM price"""
    df = pd.read_sql(q, engine)
    timestamp = df["latest_timestamp"].iloc[0]

    save_prediction(supabase, result, str(timestamp))
    return {"prediction": result, "time": timestamp}

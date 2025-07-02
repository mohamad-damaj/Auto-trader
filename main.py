from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .script_scrape import run_cron_job
from .model.predictor import RealTimePredictor
from .utils.supabase.client import client
from .backend.save_to_db import save_prediction
from sqlalchemy import create_engine
import numpy as np
import pandas as pd
import pytz
import dotenv
import os

dotenv.load_dotenv()

db_url = os.getenv("db_url")

app = FastAPI()

supabase = client()
engine = create_engine(db_url)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/update_pred")
def update_db():
    # try:
    #     run_cron_job(supabase=supabase, date_from="2025-06-29", date_to="2025-07-01", days= "7d", intervals = "1h", ticker="AAPL", hours_back=1)

    # except Exception as e:
    #     print("error:", e)
    #     raise HTTPException(status_code=400, detail="failed to update db")
    
    model_path = r"model\trader.json"
    scaler_path = r"model\scaler.pkl"
    try:

        prediction = RealTimePredictor(db_url,
                    model_path,
                    scaler_path, lookback_hours=48)
        result = prediction.predict_next()["pred"]
        q = """
        SELECT 
        MAX(timestamp) AS latest_timestamp
        FROM
        price
        """

        df = pd.read_sql(
            q,
            engine,
            )
        
        timestamp = df["latest_timestamp"].iloc[0]
        save_prediction(supabase, result, str(timestamp))
        return {"prediction": result, "time": timestamp}
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=400, detail="failed to predict")
    
@app.get("/history/")
def get_history(days: int = 7):
    try:
        q = f"""
        SELECT 
        timestamp,
        close_price AS price,
        prediction
        FROM price
        WHERE (timestamp::timestamptz AT TIME ZONE 'UTC') >= NOW() - INTERVAL '{days} DAYS'
        ORDER BY timestamp
        """
        df = pd.read_sql(q, engine, parse_dates=["timestamp"])
        print(df)
        df.replace({np.nan: None, np.inf: None, -np.inf: None}, inplace=True)
        print("1")
        return {"history": df.to_dict(orient="records")}
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=400, detail="failed to fetch history")



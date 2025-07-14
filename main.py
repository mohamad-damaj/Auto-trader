from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .model.predictor import RealTimePredictor
from .utils.supabase.client import client
from .backend.save_to_db import save_prediction
from .backend.update_pred import update_prediction_task
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
    try:
        return update_prediction_task()
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



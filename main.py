from fastapi import FastAPI
from script_scrape import run_cron_job
app = FastAPI()


run_cron_job("AAPL", hours_back=1)
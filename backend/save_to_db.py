def save_to_table(supabase, data, table):
    response = (
        supabase.table(table)
        .upsert(data)
        .execute()
    )
    return response

def save_prediction(supabase, pred, time):
    response = (
        supabase.table("price")
        .update({"prediction": int(pred)})
        .eq("timestamp", time )
        .execute()
        )
    return response
    


    
if __name__=="__main__":
    from ..utils.supabase.client import client
    from datetime import datetime, timedelta
    import pytz
    supabase = client()
    tz     = pytz.timezone("America/Toronto")
    now_dt = datetime.now(tz).replace(second=0, microsecond=0)
    now_dt = now_dt.replace(minute=30)   

    save_prediction(supabase, 1, str(now_dt))

    print(now_dt)
    
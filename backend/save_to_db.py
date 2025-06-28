
def save_news(supabase, data):
    response = (
        supabase.table("news")
        .insert(data)
        .execute()
    )

def save_reddit(supabase, data):
    response = (
        supabase.table("reddit")
        .insert(data)
        .execute()
    )
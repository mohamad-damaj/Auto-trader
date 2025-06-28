
def save_to_table(supabase, data, table):
    response = (
        supabase.table(table)
        .upsert(data)
        .execute()
    )


    


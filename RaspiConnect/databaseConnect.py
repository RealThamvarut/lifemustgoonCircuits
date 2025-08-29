from supabase import create_client, Client

url: str = "https://iafczodqvfosapepeinj.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlhZmN6b2RxdmZvc2FwZXBlaW5qIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjEzMDQ4MywiZXhwIjoyMDcxNzA2NDgzfQ.HfI10kvj1cUUX-Ilp785J5QXyVnSo_A1P5p1UFA8O6I"

def connectDB():
    supabase: Client = create_client(url, key)
    return supabase

def getUser(supabase: Client, uid: str):
    response = (
        supabase.table("users")
        .select("*")
        .eq("tag_id", uid)
        .execute()
    )

    return response
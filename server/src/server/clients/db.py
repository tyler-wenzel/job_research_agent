import os
from supabase import create_client, Client
from postgrest import APIError
from dotenv import load_dotenv

load_dotenv()

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_SECRET_KEY")
)


class DBClient:
    def __init__(self):
        self.supabase = supabase

    def get_people(self):
        return self.supabase.table("People").select("*").execute()

    def get_person(self, id: int):
        return self.supabase.table("People").select("*").eq("id", id).execute()

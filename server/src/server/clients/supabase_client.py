import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()


class SupabaseClient:
    def __init__(self):
        self.client: Client = create_client(
            os.environ.get("SUPABASE_URL"),
            os.environ.get("SUPABASE_SECRET_KEY"),
        )

    def get_people(self):
        return self.client.table("People").select("*").execute()

    def get_person(self, id: int):
        return self.client.table("People").select("*").eq("id", id).execute()

    def insert_person(self, name: str, email: str, title: str, company: str):
        return (
            self.client.table("People")
            .insert(
                {
                    "name": name,
                    "email": email,
                    "title": title,
                    "company": company,
                    "status": "Created",
                }
            )
            .execute()
        )

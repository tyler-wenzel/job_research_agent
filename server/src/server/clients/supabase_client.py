import os

from dotenv import load_dotenv
from supabase import Client, create_client

from server.models.person import Person

load_dotenv()


class SupabaseClient:
    def __init__(self):
        self.client: Client = create_client(
            os.environ.get("SUPABASE_URL"),
            os.environ.get("SUPABASE_SECRET_KEY"),
        )

    def get_people(self):
        rows = self.client.table("People").select("*").execute().data
        return [Person.model_validate(row) for row in rows]

    def get_person(self, id: int):
        rows = self.client.table("People").select("*").eq("id", id).execute().data
        if not rows:
            return None
        return Person.model_validate(rows[0])

    def get_person_by_email(self, email: str):
        rows = (
            self.client.table("People").select("*").eq("email", email).limit(1).execute()
        ).data
        if not rows:
            return None
        return Person.model_validate(rows[0])

    def insert_person(self, name: str, email: str, title: str, company: str):
        person = Person(name=name, email=email, title=title, company=company)
        saved = (
            self.client.table("People")
            .insert(
                {
                    "name": person.name,
                    "email": person.email,
                    "title": person.title,
                    "company": person.company,
                    "status": person.status,
                }
            )
            .execute()
        )
        return Person.model_validate(saved.data[0])

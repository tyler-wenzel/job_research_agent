from server.clients.greenhouse_client import GreenhouseClient
from server.clients.supabase_client import SupabaseClient


class PeopleService:
    def __init__(self):
        self.greenhouse_client = GreenhouseClient()
        self.supabase_client = SupabaseClient()

    def get_people_from_company(self, company_name: str, limit: int):
        return self.greenhouse_client.get_people_from_company(company_name, limit)

    def get_contacts(self):
        return self.greenhouse_client.get_contacts()

    def query_people(self):
        return self.supabase_client.get_people().data

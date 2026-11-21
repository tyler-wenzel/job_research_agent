from server.clients.greenhouse_client import GreenhouseClient
from server.clients.supabase_client import SupabaseClient
from server.clients.findymail_client import FindymailClient


class PeopleService:
    def __init__(self):
        self.greenhouse_client = GreenhouseClient()
        self.supabase_client = SupabaseClient()
        self.findymail_client = FindymailClient()

    def get_people_from_company(
        self, company_name: str, job_titles: list[str], limit: int
    ):
        employees = self.findymail_client.search_employees(
            website=company_name,
            job_titles=job_titles,
            count=limit,
        )
        return [
            self.findymail_client.find_email(
                name=employee["name"],
                domain=employee.get("companyWebsite") or company_name,
            )
            for employee in employees
        ]

    def get_contacts(self):
        return self.greenhouse_client.get_contacts()

    def query_people(self):
        return self.supabase_client.get_people().data

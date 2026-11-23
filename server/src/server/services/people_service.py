from server.clients.findymail_client import FindymailClient
from server.clients.hunter_client import HunterClient, JobTitle, Seniority
from server.clients.supabase_client import SupabaseClient


class PeopleService:
    def __init__(self):
        self.hunter_client = HunterClient()
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

    def get_contacts(
        self,
        domain: str,
        job_title: JobTitle | None = None,
        seniority: Seniority | None = None,
        limit: int = 5,
        offset: int = 0,
    ):
        return self.hunter_client.domain_search(
            domain=domain,
            job_title=job_title,
            seniority=seniority,
            limit=limit,
            offset=offset,
        )

    def insert_person(self, name: str, email: str, raw_title: str, company: str):
        return self.supabase_client.insert_person(
            name=name,
            email=email,
            title=raw_title,
            company=company,
        ).data

    def query_people(self):
        return self.supabase_client.get_people().data

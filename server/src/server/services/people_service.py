from server.clients.findymail_client import FindymailClient
from server.clients.hunter_client import HunterClient, JobTitle, Seniority
from server.clients.supabase_client import SupabaseClient
from server.models.person import SaveResult


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
        people = self.hunter_client.domain_search(
            domain=domain,
            job_title=job_title,
            seniority=seniority,
            limit=limit,
            offset=offset,
        )
        for person in people:
            person["company"] = domain
        return people

    def save_person(self, name: str, email: str, raw_title: str, company: str):
        existing = self.supabase_client.get_person_by_email(email)
        if existing:
            return SaveResult(saved=False, reason="already_stored", person=existing)

        person = self.supabase_client.insert_person(
            name=name,
            email=email,
            title=raw_title,
            company=company,
        )
        return SaveResult(saved=True, person=person)

    def query_people(self):
        return self.supabase_client.get_people()

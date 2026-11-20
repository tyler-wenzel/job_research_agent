from server.clients.people_client import PeopleClient
from server.clients.db import DBClient


class PeopleService:
    def __init__(self):
        self.people_client = PeopleClient()
        self.db_client = DBClient()

    def get_people_from_company(self, company_name: str, limit: int):
        return self.people_client.get_people_from_company(company_name, limit)

    def get_contacts(self):
        return self.people_client.get_contacts()

    def query_people(self):
        return self.db_client.get_people().data

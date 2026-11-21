import requests


class GreenhouseClient:
    def __init__(self):
        self.base_url = "https://boards-api.greenhouse.io"

    def get_people_from_company(self, company_name: str, limit: int):
        response = requests.get(f"{self.base_url}/v1/boards/greenhouse/jobs/8279752")
        return response.json()

    def get_contacts(self):
        response = requests.get(f"{self.base_url}/v1/boards/greenhouse/contacts")
        return response.json()

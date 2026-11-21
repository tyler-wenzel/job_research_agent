import os

import requests
from dotenv import load_dotenv

load_dotenv()


class FindymailClient:
    def __init__(self):
        self.base_url = "https://app.findymail.com"
        self.headers = {
            "Authorization": f"Bearer {os.environ.get('FINDYMAIL_API_KEY')}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def verify(self, email: str):
        response = requests.post(
            f"{self.base_url}/api/verify",
            headers=self.headers,
            json={"email": email},
        )
        return response.json()

    def find_email(self, name: str, domain: str):
        body = {
            "name": name,
            "domain": domain,
        }

        response = requests.post(
            f"{self.base_url}/api/search/name",
            headers=self.headers,
            json=body,
        )
        return response.json()

    def search_employees(self, website: str, job_titles: list[str], count: int = 1):
        response = requests.post(
            f"{self.base_url}/api/search/employees",
            headers=self.headers,
            json={
                "website": website,
                "job_titles": job_titles,
                "count": count,
            },
        )
        return response.json()

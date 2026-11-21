import os

import requests
from dotenv import load_dotenv

load_dotenv()


class FindymailClient:
    def __init__(self):
        self.base_url = "https://app.findymail.com"
        self.api_key = os.environ.get("FINDYMAIL_API_KEY")

    def verify(self, email: str):
        response = requests.post(
            f"{self.base_url}/api/verify",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={"email": email},
        )
        return response.json()

    def find_email(self, name: str, domain: str, webhook_url: str | None = None):
        body = {"name": name, "domain": domain}
        if webhook_url:
            body["webhook_url"] = webhook_url

        response = requests.post(
            f"{self.base_url}/api/search/name",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=body,
        )
        return response.json()

    def search_employees(self, website: str, job_titles: list[str], count: int = 1):
        response = requests.post(
            f"{self.base_url}/api/search/employees",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json={
                "website": website,
                "job_titles": job_titles,
                "count": count,
            },
        )
        return response.json()

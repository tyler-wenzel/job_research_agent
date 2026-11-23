import os
from enum import StrEnum

import requests
from dotenv import load_dotenv

load_dotenv()


class Seniority(StrEnum):
    JUNIOR = "junior"
    SENIOR = "senior"


class JobTitle(StrEnum):
    SOLUTIONS_ENGINEER = "solutions engineer"
    SOFTWARE_ENGINEER = "software engineer"
    PRODUCT_MANAGER = "product manager"
    FORWARD_DEPLOYED_ENGINEER = "forward deployed engineer"
    SOLUTIONS_ARCHITECT = "solutions architect"
    SALES_ENGINEER = "sales engineer"
    AI_ENGINEER = "ai engineer"


class HunterClient:
    def __init__(self):
        self.base_url = "https://api.hunter.io/v2"
        use_test_key = os.environ.get("HUNTER_USE_TEST_KEY", "").lower() == "true"
        self.api_key = (
            "test-api-key" if use_test_key else os.environ.get("HUNTER_API_KEY")
        )

    def domain_search(
        self,
        domain: str,
        job_title: JobTitle | None = None,
        seniority: Seniority | None = None,
        limit: int = 5,
        offset: int = 0,
    ):
        params = {
            "domain": domain,
            "limit": limit,
            "offset": offset,
            "api_key": self.api_key,
        }
        if job_title:
            params["job_titles"] = job_title
        if seniority:
            params["seniority"] = seniority

        response = requests.get(f"{self.base_url}/domain-search", params=params)
        response.raise_for_status()
        emails = response.json().get("data", {}).get("emails", [])
        return [
            {
                "name": " ".join(
                    part
                    for part in [person.get("first_name"), person.get("last_name")]
                    if part
                ),
                "email": person.get("value"),
                "raw_title": person.get("position_raw"),
            }
            for person in emails
        ]

from langchain.tools import tool
from langchain.chat_models import init_chat_model
from server.clients.hunter_client import JobTitle, Seniority
from server.services.people_service import PeopleService
import json

model = init_chat_model("claude-sonnet-4-6")


@tool
def get_contacts(
    domain: str,
    job_title: JobTitle,
    seniority: Seniority,
    limit: int = 5,
    offset: int = 0,
) -> str:
    """Fetch people at a company by title and seniority, including their emails.

    Args:
        domain: The company domain, such as stripe.com
        job_title: One of solutions engineer, software engineer, product manager, forward deployed engineer, solutions architect, sales engineer, or ai engineer
        seniority: junior or senior
        limit: The number of people to fetch
        offset: The number of matches to skip
    """
    return json.dumps(
        PeopleService().get_contacts(
            domain=domain,
            job_title=job_title,
            seniority=seniority,
            limit=limit,
            offset=offset,
        )
    )


@tool
def insert_person(name: str, email: str, raw_title: str, company: str) -> str:
    """Save a person returned by get_contacts. Status is set to Created.

    Args:
        name: The person's name from get_contacts
        email: The person's email from get_contacts
        raw_title: The person's raw title from get_contacts
        company: The company domain used in the search, such as stripe.com
    """
    return json.dumps(
        PeopleService().insert_person(
            name=name,
            email=email,
            raw_title=raw_title,
            company=company,
        )
    )


@tool
def query_people() -> str:
    """Query the people saved in the database."""
    return json.dumps(PeopleService().query_people())


# Augment the LLM with tools
tools = [get_contacts, insert_person, query_people]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)

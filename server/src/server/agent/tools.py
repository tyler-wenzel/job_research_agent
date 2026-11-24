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
        seniority: junior or senior, default is senior
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
def save_person(name: str, email: str, raw_title: str, company: str) -> str:
    """Save a person returned by get_contacts. Skips a person who is already saved.

    Args:
        name: The person's name from get_contacts
        email: The person's email from get_contacts
        raw_title: The person's raw title from get_contacts
        company: The company on that person, the domain from the search
    """
    return PeopleService().save_person(
        name=name,
        email=email,
        raw_title=raw_title,
        company=company,
    ).model_dump_json()


@tool
def query_people() -> str:
    """Query the people saved in the database."""
    return json.dumps(
        [person.model_dump(mode="json") for person in PeopleService().query_people()]
    )


# Augment the LLM with tools
tools = [get_contacts, save_person, query_people]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)

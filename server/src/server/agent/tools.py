from langchain.tools import tool
from langchain.chat_models import init_chat_model
from server.services.people_service import PeopleService
import json

model = init_chat_model("claude-sonnet-4-6")


@tool
def get_people_from_company(
    company_name: str, job_titles: list[str], limit: int
) -> str:
    """Fetch people with the given job titles at a company, including their emails.

    Args:
        company_name: The company website or name, such as google.com
        job_titles: Job titles to search for
        limit: The number of people to fetch
    """
    return json.dumps(
        PeopleService().get_people_from_company(
            company_name=company_name, job_titles=job_titles, limit=limit
        )
    )


@tool
def query_people() -> str:
    """Query the people saved in the database."""
    return json.dumps(PeopleService().query_people())


# Augment the LLM with tools
tools = [get_people_from_company, query_people]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)

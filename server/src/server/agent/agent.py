from langgraph.graph import StateGraph, START, END
from server.agent.state import MessagesState
from server.agent.model import llm_call
from server.agent.tool_node import tool_node
from server.agent.end_logic import should_continue
from langchain.messages import HumanMessage


agent_builder = StateGraph(MessagesState)

agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)


agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
agent_builder.add_edge("tool_node", "llm_call")


agent = agent_builder.compile()

messages = [
    HumanMessage(
        content="find me 3 people from stripe who are software engineers and save them to the database"
    )
]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()

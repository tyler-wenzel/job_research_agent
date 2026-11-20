from langgraph.graph import StateGraph, START, END
from server.state import MessagesState
from server.model import llm_call
from server.tool_node import tool_node
from server.end_logic import should_continue


agent_builder = StateGraph(MessagesState)

agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)


agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
agent_builder.add_edge("tool_node", "llm_call")


agent = agent_builder.compile()

from langchain.messages import HumanMessage

messages = [HumanMessage(content="Get me a job.")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()

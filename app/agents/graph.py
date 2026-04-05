from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from app.config import settings
from app.agents.tools import query_database, fetch_api

# Simple LLM setup
llm = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0,
    api_key=settings.OPENAI_API_KEY
)

# Bind tools to LLM
tools = [query_database, fetch_api]
llm_with_tools = llm.bind_tools(tools)

# Tool executor
tool_node = ToolNode(tools)

# Agent state
class AgentState(dict):
    messages: Annotated[Sequence[BaseMessage], "add"]

# Agent logic - NO RAG dependency
def agent_node(state: AgentState) -> dict:
    """Call LLM with tools"""
    result = llm_with_tools.invoke(state["messages"])
    return {"messages": [result]}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent", 
    tools_condition, 
    {"tools": "tools", END: END}
)
workflow.add_edge("tools", "agent")

# Compile
agent = workflow.compile()
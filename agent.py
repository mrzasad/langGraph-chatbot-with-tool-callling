from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage

from llm import get_llm
from tools import tools

SYSTEM_PROMPT = """You are a helpful customer support agent for Imtiaz CRM.

**CRITICAL RULE – YOU MUST FOLLOW THIS EXACTLY:**
- When a customer asks about a complaint (e.g., "Check PK-88421", "Was my refund approved?"), you MUST call the `search_complaint_tool` with the order_id. Do not describe the tool – actually call it.
- If the search returns "No complaint found", politely inform the customer and ask if they want to register a new complaint.
- If the customer agrees to register, you MUST call `register_pending_complaint_tool` with the order_id and their complaint text.
- Never output fake function syntax like <function> or {"name": ...}. Always use real tool calls.
- Be concise, professional, and helpful. Match the customer's language.

Now assist the customer using the tools provided."""

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

def build_agent():
    llm = get_llm()
    llm_with_tools = llm.bind_tools(tools)
    tool_node = ToolNode(tools)

    def call_llm(state: AgentState):
        messages = state["messages"]
        # Ensure system prompt is always first
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    graph = StateGraph(AgentState)
    graph.add_node("llm", call_llm)
    graph.add_node("tools", tool_node)
    graph.add_edge(START, "llm")
    graph.add_conditional_edges("llm", tools_condition)
    graph.add_edge("tools", "llm")

    return graph.compile()

# For debugging – run standalone to test
if __name__ == "__main__":
    agent = build_agent()
    print("Agent ready. Enter 'exit' to quit.")
    while True:
        user = input("You: ")
        if user.lower() == "exit":
            break
        result = agent.invoke({"messages": [("user", user)]})
        print("Bot:", result["messages"][-1].content)
import os, getpass, agentops
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_core.messages import SystemMessage, HumanMessage
from IPython.display import Image, display
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
MODEL = os.getenv("MODEL", "gpt-3.5-turbo")

#AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

#agentops.init(AGENTOPS_API_KEY)

print(f"Using model: {MODEL}")
print(f"Using OpenAI API Base: {OPENAI_API_BASE}")
print(f"Using OpenAI API Key: {OPENAI_API_KEY}")

llm = ChatOpenAI(model=MODEL, openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE, temperature=0)

def add(a: int, b: int) -> int:
    """add a and b"""
    return a + b

def multiply(a: int, b: int) -> int:
    """multiply a and b"""
    return a * b


def divide(a: int, b: int) -> float:
    """divide a by b"""
    return a / b

tools = [add,multiply,divide]
llm_with_tools = llm.bind_tools(tools)

sys_msg = SystemMessage(content="You are a helpful math assistant. Use the provided tools to calculate values based on the inputs.")


def assistant(state: MessagesState):     
    return {"messages": [llm_with_tools.invoke([sys_msg]+ state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools",ToolNode(tools))

builder.add_edge(START, "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

react_graph = builder.compile()
#display(Image(react_graph.get_graph(xray=True).draw_mermaid_png()))

messages = [HumanMessage(content="What is the sum of 5 and 3? Multiply the result by 2, then divide by 4.")]
messages = react_graph.invoke({"messages": messages})["messages"]


for m in messages:
    m.pretty_print()
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

llm=ChatOpenAI(model=MODEL, openai_api_key=OPENAI_API_KEY, openai_api_base=OPENAI_API_BASE, temperature=0)

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

messages = [HumanMessage(content="What is the sum of 5 and 3? ")]

messages = react_graph.invoke({"messages": messages})

for msg in messages['messages']:
    msg.pretty_print()


messages = [HumanMessage(content="Multiply the result by 2")]
messages = react_graph.invoke({"messages": messages})
for msg in messages['messages']:
    msg.pretty_print()  

# messages = [HumanMessage(content="Divide the result by 4")]
# messages = react_graph.invoke({"messages": messages})["messages"]
# for msg in messages:
#     msg.pretty_print()  

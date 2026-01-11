import os, getpass, agentops
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage
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

def filter_messages(state: MessagesState):
   #delete all but last 2 messages
   delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
   return {"messages": delete_messages}

def assistant(state: MessagesState):     
    return {"messages": [llm_with_tools.invoke([sys_msg]+ state["messages"])]}


builder = StateGraph(MessagesState)
builder.add_node("filter_messages", filter_messages)
builder.add_node("assistant", assistant)
builder.add_node("tools",ToolNode(tools))

builder.add_edge(START, "filter_messages")
builder.add_edge("filter_messages", "assistant")
builder.add_conditional_edges("assistant", tools_condition)
builder.add_edge("tools", "assistant")

# create a checkpoint memory to save the state
memory = MemorySaver()
#pass the checkpointer to the compile method
react_graph = builder.compile(checkpointer=memory)

#create a thread to store the state
config = {"configurable": {"thread_id": "1"}}

messages = [HumanMessage(content="What is the sum of 5 and 3? ")]

messages = react_graph.invoke({"messages": messages},config)

for msg in messages['messages']:
     msg.pretty_print()
#print(messages)


messages = [HumanMessage(content="Multiply the result by 2")]
messages = react_graph.invoke({"messages": messages},config)
for msg in messages['messages']:
    msg.pretty_print()  

messages = [HumanMessage(content="Divide the result by 4")]
messages = react_graph.invoke({"messages": messages},config)
for msg in messages['messages']:
    msg.pretty_print()  

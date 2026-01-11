import random
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END

class TypeDictState(TypedDict):
    name: str
    mood: Literal['happy', 'sad', 'neutral']


def node_1(state):
    print("--node1--")
    return {"name": state['name'] + " is... "}

def node_2(state):
    print("--node2--")
    mood = {"mood": "happy"}
    return {"mood": mood}

def node_3(state):
    print("--node3--")
    mood = {"mood": "sad"}
    return {"mood": mood}

def node_4(state):
    print("--node4--")
    mood = {"mood": "nuetral"}
    return {"mood": mood}

def decide_mood(state) -> Literal["node_2", "node_3", "node_4"]:
    if random.random() < 0.5:
        return "node_2"
    elif random.random() == 0.5:
        return "node_3"
    else:
        return "node_4"
    

builder = StateGraph(TypeDictState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_node("node_4", node_4)

builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", decide_mood)
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)
builder.add_edge("node_4", END)


graph = builder.compile()

graph.invoke({"name": "Alice", "mood": "neutral"})


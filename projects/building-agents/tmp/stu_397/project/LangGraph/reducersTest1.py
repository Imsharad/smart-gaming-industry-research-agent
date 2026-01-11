from langgraph.graph.message import MessagesState, add_messages
from langchain_core.messages import AIMessage, HumanMessage, RemoveMessage

initial_messages = [AIMessage(content="Hello! How can I assist you today?", name="Model"),
                    HumanMessage(content="Hi! I need help with my homework.", name="User")]

new_message = AIMessage(content="Can you explain the theory of relativity?", name="Model")

print(add_messages(initial_messages,new_message))

#Re-writing
initial_messages = [AIMessage(content="Hello! How can I assist you today?", name="Model", id=1),
                    HumanMessage(content="Hi! I need help with my homework.", name="User", id=2)]

new_message = HumanMessage(content="Can you explain the theory of relativity?", name="Model", id=2)

print(add_messages(initial_messages,new_message))

#Remove Messages

messages = [AIMessage(content="Hello! ", name="Model", id=1)]
messages.append(HumanMessage(content="Hi! ", name="User", id=2))
messages.append(AIMessage(content="How can I assist you today?", name="Model", id=3))
messages.append(HumanMessage(content="I need help with my homework.", name="User", id=4))

delete_message = [RemoveMessage(id=m.id) for m in messages[:-2]]
print(delete_message)

print(add_messages(messages,delete_message))
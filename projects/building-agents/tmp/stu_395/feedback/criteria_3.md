# Criterion 3: Stateful Agent - Review

I really liked your `GameAgent` class implementation. The use of `ShortTermMemory` and the logic to retrieve `previous_messages` from the last run (`last_run.get_final_state()`) is excellent. It shows you understand exactly how to persist state across different execution runs, which is the core of a conversational agent.

However, this criterion is marked as **FAIL** because the submission does not demonstrate the agent handling multiple queries to prove that state is actually maintained.

## What did not work
The notebook only includes a single invocation of the agent:
```python
run1 = agent.invoke(query="Provide me the details of the game  Need for Speed ?")
```
The instructions (in the TODO comments) asked for multiple queries (e.g., about Pokémon Gold, Mario, Mortal Kombat) to demonstrate the agent's capabilities. More importantly, without a follow-up query (e.g., "Who published it?"), there is no visible proof that the agent "remembers" the context from the first turn.

## Why it did not work
State management isn't just about writing the code; it's about verifying that the agent can hold a conversation. If you only ask one question, the "memory" is never accessed or tested. You need to show that the `previous_messages` logic you wrote actually works in practice by running a second and third turn in the same session.

## Why this matters in the real world
Users expect AI assistants to be conversational. If a user asks "What is Super Mario 64?" and then "What console is it on?", the agent must know that "it" refers to Mario 64. Validating this behavior is a critical part of testing conversational AI before deployment.

## Steps to resolve
1.  **Add Follow-up Queries**: In the same cell (or a new one), invoke the agent again using the same `session_id`.
    ```python
    run2 = agent.invoke(query="When was it released?", session_id="project")
    print(run2.get_final_state()["messages"][-1].content)
    ```
2.  **Demonstrate Context**: Ensure the output shows the agent understands the context from the first question.
3.  **Run the provided examples**: The TODO listed specific questions (Pokémon, Mario, etc.). Un-comment or implement those to fully meet the requirements.

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766580604/image.png)

## Resources

**LangGraph StateGraph Guide**
https://medium.com/ai-agents/langgraph-for-beginners-part-4-stategraph-794004555369
This guide is great for understanding how your `StateMachine` (which is very similar to StateGraph) manages the flow of state between steps.

**LangChain: Advanced Memory Patterns**
https://python.langchain.com/docs/how_to/memory/
Review the "ConversationBuffer" concepts here. Your `ShortTermMemory` implementation mirrors this, and seeing how it's used in standard patterns might help you visualize the multi-turn flow.

**OpenAI: Assistants API and State Management**
https://platform.openai.com/docs/assistants/overview
OpenAI's approach to "Threads" is exactly what you are building with your `session_id`. Reading this can give you a high-level view of why persistent threads are efficient.

**LangGraph: Production Agent Workflows**
https://python.langchain.com/docs/langgraph/
Since you are using a graph-based state machine, this documentation will help you see how to extend your agent with more complex state transitions in the future.

**OpenAI Assistants API - Citations**
https://platform.openai.com/docs/assistants/tools/file-search#citations
While your web search returns results, ensure your final agent response properly cites them. This guide shows how to structure citations effectively in a conversational response.

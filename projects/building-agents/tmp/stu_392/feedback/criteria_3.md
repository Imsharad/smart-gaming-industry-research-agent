# Criterion 3: Stateful Agent

Your `Agent` class implementation in `lib/agents.py` is excellent. I specifically liked how you used the `StateMachine` pattern to define the workflow (`message_prep` -> `llm_processor` -> `tool_executor`). The logic for handling `current_tool_calls` and looping back to the LLM processor is exactly how modern agents should operate. The `ShortTermMemory` integration for retrieving previous messages is also correctly implemented to handle context across multiple queries.

## Status: FAIL

### What did not work
Once again, the lack of execution in `Udaplay_02_starter_project.ipynb` prevents me from verifying the agent's behavior. While the code for state management exists, I cannot see it in action. I cannot confirm if the agent actually remembers the context from "Query 1" when answering "Query 2", or if it maintains the conversation history correctly.

### Why it did not work
State management is tricky. Even with correct code, subtle bugs can arise (e.g., token limits being exceeded, history not being appended correctly, or the LLM getting confused by too much context). Without running the notebook and seeing the "Answer" and "Workflow Analysis" outputs, I cannot verify that:
1. The agent maintains the session state across the three test queries.
2. The agent produces structured and well-cited answers as required.
3. The state machine transitions occur as expected (e.g., entering the tool execution loop).

### Why this matters in the real world
In production, "state" is where the complexity lives. A stateless chatbot is easy; a stateful agent that remembers user preferences, previous tool results, and conversation history is hard. Verifying state persistence is critical to ensuring a coherent user experience. If the agent forgets what it did 2 turns ago, the user loses trust. Running the tests is the only way to prove the state machine works.

### Steps to resolve the issue
1. As with the previous criteria, open `Udaplay_02_starter_project.ipynb`.
2. Run the notebook fully.
3. Ensure that for Query 2 and Query 3, the agent's behavior (or your checks) demonstrates that it has access to previous context if applicable.
4. Verify that the final answers include citations as per your system instructions.
5. Save the notebook **with the outputs included**.
6. Resubmit the project.

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766580604/image.png)

## Resources

**LangGraph Overview (Official)**
https://docs.langchain.com/oss/python/langgraph/overview
Your `StateMachine` implementation shares many concepts with LangGraph. This documentation explains the theory behind graph-based agent orchestration, which can help you understand why explicit state transitions are so powerful.

**LangGraph Tutorial (Real Python)**
https://realpython.com/langgraph-python/
This is a great hands-on tutorial that goes deeper into building stateful agents. It covers cyclic graphs and state management patterns that are very similar to what you implemented.

**OpenAI Citations Documentation**
https://platform.openai.com/docs/assistants/tools/file-search#citations
One of the requirements is to provide well-cited answers. This guide shows how OpenAI's Assistants API handles citations, which is a great reference for how to structure your agent's output to include source attribution.

**ReAct: Reasoning and Acting in Language Models**
https://react-lm.github.io/
The pattern you implemented (Reason -> Act -> Observe) is based on the ReAct paper. Reading this will give you the theoretical background on why this interleaving of thought and action is so effective for stateful agents.

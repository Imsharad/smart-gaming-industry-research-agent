# Criterion 3: Stateful Agent

**Status: FAIL**

I was impressed by your use of `StateGraph` and `TypedDict` in the `basicemailassistance.py` file. The logic for routing between "triage" and "response" nodes shows you have a good grasp of how to build stateful applications using LangGraph!

## What did not work
This criterion is marked as **FAIL** because the stateful agent is not implemented for the required domain. The rubric specifically requires an agent that manages conversation state about **video games**, allowing for follow-up questions (e.g., remembering which game was just discussed). Additionally, the agent must properly **cite sources** from the retrieved documents or web search, which is not present in the current submission.

## Why it did not work
While the mechanism for state (LangGraph) is present, the application logic is different. The Udaplay project requires the agent to maintain a "chat history" specifically to answer questions like "What platforms is it on?" after being asked "Tell me about The Witcher 3". The current email agent manages a different kind of state (email triage).

## Why this matters in the real world
In conversational AI, "state" is what makes an interaction feel natural. Users expect the bot to remember what they just said. Furthermore, in RAG applications, **citations** are non-negotiable for trust. Users need to know *where* the information came from (e.g., "Source: GiantBomb Dataset" vs "Source: Tavily Web Search").

## Steps to resolve the issue
1.  **Adapt your StateGraph**: Use the same `StateGraph` pattern you already know, but apply it to the Udaplay agent.
2.  **Track Chat History**: Ensure your `State` object includes a list of messages or conversation history.
3.  **Implement Citations**: Modify your agent's response logic to include the source of the information (e.g., filename or URL) when it provides an answer.
4.  **Handle Follow-ups**: Test that your agent can answer "Who developed it?" immediately after a query about a specific game.

## Resources

Use these resources to adapt your stateful logic to the RAG context:

**LangGraph Tutorial (Real Python)**
[https://realpython.com/langgraph-python/](https://realpython.com/langgraph-python/)
This tutorial is excellent for reinforcing the concepts you're already using, specifically focusing on building stateful LLM applications that can handle complex conversational flows.

**LangGraph Overview (Official)**
[https://docs.langchain.com/oss/python/langgraph/overview](https://docs.langchain.com/oss/python/langgraph/overview)
The official docs provide the definitive reference for managing state updates and persistence, which you'll need to handle the conversation history effectively.

**OpenAI Assistants API - Citations**
[https://platform.openai.com/docs/assistants/tools/file-search#citations](https://platform.openai.com/docs/assistants/tools/file-search#citations)
This guide explains the importance of citations and how to structure them. Even if you aren't using the Assistants API directly, the pattern of extracting and presenting source metadata is the same.

**LangChain RAG Tutorial (Official)**
[https://python.langchain.com/docs/tutorials/rag/](https://python.langchain.com/docs/tutorials/rag/)
Refer back to this for examples of how to pass source documents through your chain so that the final answer can include proper citations.

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766580604/image.png)

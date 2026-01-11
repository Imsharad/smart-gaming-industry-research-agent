# Criterion 2: Agent Development

**Status: FAIL**

I really appreciated how you implemented custom tools in your `basicemailassistance.py` file! Your definition of `write_email`, `schedule_meeting`, and `check_calendar_availability` using the `@tool` decorator demonstrates a solid understanding of how to expose Python functions to an LLM.

## What did not work
This criterion is marked as **FAIL** because the specific tools required for the Udaplay Video Game agent are missing. The rubric requires three specific tools:
1.  A **Retrieval Tool** to query the vector database for game information.
2.  An **Evaluation Tool** to assess if the retrieved information is relevant.
3.  A **Web Search Tool** (like Tavily) to act as a fallback when internal data is insufficient.

Your current submission implements an Email Assistant, which, while functional, does not meet the requirements of the Video Game RAG assignment.

## Why it did not work
The agent needs to be able to access the specific knowledge base (Video Games) created in Criterion 1. Without a retrieval tool, the agent cannot access this data. Without an evaluation tool, it cannot quality-check its own work. Without a web search tool, it has no way to find information not in the database.

## Why this matters in the real world
In professional agent development, "grounding" is essential. We build tools specifically to ground the agent's responses in our proprietary data (the vector DB) and verifying that data (evaluation) is a key pattern to prevent hallucinations. The fallback to web search ensures the agent remains helpful even when local data is missing, increasing its reliability.

## Steps to resolve the issue
1.  **Create a Retrieval Tool**: Implement a tool (e.g., `retrieve_game_info(query: str)`) that searches your ChromaDB collection.
2.  **Create an Evaluation Tool**: Implement a tool (e.g., `evaluate_relevance(query: str, context: str)`) that uses an LLM to check if the context answers the query.
3.  **Integrate Web Search**: Add a tool that uses the Tavily API (or similar) to search the web.
4.  **Update Agent Workflow**: Ensure the agent tries retrieval first, evaluates the result, and falls back to web search if needed.

## Resources

Here are resources to help you build the required tools:

**LangChain Agents Tutorial (Official)**
[https://python.langchain.com/docs/tutorials/agents/](https://python.langchain.com/docs/tutorials/agents/)
This tutorial covers building RAG agents with tools, which is exactly what you need to do here. It shows how to connect your retrieval system as a tool.

**Tavily Search API Documentation**
[https://docs.tavily.com/documentation/api-reference/endpoint/search](https://docs.tavily.com/documentation/api-reference/endpoint/search)
For the fallback capability, you'll need a search tool. Tavily is optimized for agents. This documentation shows how to use their API.

**LlamaIndex Evaluating Module**
[https://developers.llamaindex.ai/python/framework/module_guides/evaluating/](https://developers.llamaindex.ai/python/framework/module_guides/evaluating/)
While this is for LlamaIndex, the concepts of evaluating tool outputs and implementing quality gates are universal and relevant to designing your evaluation tool.

**OpenAI Function Calling Documentation**
[https://platform.openai.com/docs/guides/function-calling](https://platform.openai.com/docs/guides/function-calling)
Since you are using OpenAI models, this guide helps deepen your understanding of how the model decides which tool to call and how to structure the tool definitions.

![1766581438006](image/criteria2/1766581438006.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418224/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418242/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418255/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418267/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418277/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418283/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418321/image.png)

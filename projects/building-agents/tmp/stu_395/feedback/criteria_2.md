# Criterion 2: Agent Development - Review

I really liked how you structured the `GameAgent` class using the `StateMachine`. It's a very clean and modular way to handle the agent's lifecycle (Message Prep -> LLM -> Tool Execution). Your integration of the Tavily web search tool is also excellent—it returns structured, useful data that the agent can easily consume.

However, this criterion is marked as **FAIL** primarily because the `evaluate_retrieval` tool is not implemented correctly.

## What did not work
The `evaluate_retrieval` tool definition contains placeholder code that does not perform any actual evaluation.
```python
@tool
def evaluate_retrieval(game_name:str, collection: str, path: str) -> str:
 retrieve_game("Need For Speed","gamesrepo","gamestoredb")
```
This function ignores its arguments and simply calls `retrieve_game` with hardcoded values. It does not analyze the quality of retrieval, nor does it use an LLM to judge the relevance of documents as required by the docstring and project requirements.

## Why it did not work
The goal of this tool is to act as a **quality gate**. In a sophisticated RAG agent, retrieving documents isn't enough; the agent needs to know if those documents *actually* contain the answer. Your current implementation just re-runs a specific search and returns nothing useful for the agent's reasoning process. Without a working evaluation step, the agent cannot intelligently decide when to fallback to web search based on document quality.

## Why this matters in the real world
In production AI systems, "Guardrails" and "Self-Correction" are essential. An agent that can evaluate its own retrieved context prevents hallucinations and "I don't know" loops. By explicitly grading the retrieval, you ensure that the system only answers when it's confident, or knows exactly when to seek external information (like the web), drastically increasing user trust.

## Steps to resolve
1.  **Implement the Logic**: Rewrite `evaluate_retrieval` to actually judge the content. You should use an LLM to compare the `query` with the `retrieved_docs`.
2.  **Use an LLM Judge**: Inside the tool, create a small prompt for the LLM.
    ```python
    @tool
    def evaluate_retrieval(query: str, retrieved_docs: str) -> str:
        # Pseudo-code example
        eval_prompt = f"Query: {query}\nDocs: {retrieved_docs}\nAre these docs useful to answer the query? Yes/No"
        result = llm.invoke(eval_prompt)
        return result
    ```
3.  **Update Arguments**: Ensure the tool accepts the necessary context (the user's question and the text found by `retrieve_game`) so it can make a comparison.

![1766581438006](image/criteria2/1766581438006.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418224/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418242/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418255/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418267/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418277/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418283/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418321/image.png)

## Resources

**Tool Result Evaluation Strategies**
https://docs.llamaindex.ai/en/stable/module_guides/evaluating/
This guide explains the pattern you are missing: using an "LLM as a judge" to score the relevance of retrieved information before using it.

**Creating Custom Agent Tools**
https://www.llamaindex.ai/blog/agentic-rag-with-llamaindex-2721b8a49ff6
Since you are building a custom evaluation tool, this resource on Agentic RAG gives great examples of how to build tools that allow agents to reason over their own data.

**LangChain Deep Agents Tutorial**
https://python.langchain.com/docs/tutorials/agents/
Refer to the sections on tool integration to see how to properly structure your tool's inputs and outputs so the agent can use them effectively.

**Web Search Integration for AI Agents**
https://docs.tavily.com/documentation/api-reference/endpoint/search
Your Tavily implementation is good, but this doc is useful to ensure you are extracting the most relevant metadata (like citations) to pass to your future evaluation steps.

**Agent Reliability Patterns**
https://docs.llamaindex.ai/en/stable/module_guides/deploying/
Learn about fallback strategies. Your agent correctly fell back to web search, but a proper evaluation tool makes this process robust and deterministic rather than accidental.

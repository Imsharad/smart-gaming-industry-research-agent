# Criterion 2: Agent Development

I was really impressed with how you defined your tools. The `retrieve_game`, `evaluate_retrieval`, and `game_web_search` functions are well-structured, and the docstrings provide excellent context for the LLM to understand how and when to use them. Your system instructions in the `Agent` setup also clearly define the expected workflow (Internal -> Evaluate -> Fallback), which is exactly the kind of logic we look for in robust agents.

## Status: FAIL

### What did not work
Similar to the previous criterion, the `Udaplay_02_starter_project.ipynb` notebook has not been executed. All the output cells are empty (`[]`). While the code for the tools and the agent setup is present, I cannot verify that the agent actually invokes these tools, handles the data correctly, or follows the prescribed workflow.

### Why it did not work
An agent's behavior is non-deterministic and relies heavily on the interaction between the LLM and the tools. Code that "looks" correct in a prompt might not behave as expected in practice (e.g., the agent might skip the evaluation step, or fail to parse the tool output). Without seeing the execution logs (trace), I cannot confirm:
1. That the tools are successfully registered and called by the agent.
2. That the agent follows the "Internal -> Evaluate -> Web" fallback logic.
3. That the API keys (Tavily, OpenAI) are working and configured correctly.

### Why this matters in the real world
In agentic AI development, "prompt engineering" and "tool definition" are only half the battle. The other half is testing and observation. Agents can hallucinate tool usage or get stuck in loops. Running the notebook and inspecting the trace (the step-by-step reasoning and tool calls) is the only way to ensure the agent is reliable and production-ready. It proves that your instructions effectively guide the model's behavior.

### Steps to resolve the issue
1. Open `Udaplay_02_starter_project.ipynb`.
2. Ensure your `.env` file has valid `OPENAI_API_KEY` and `TAVILY_API_KEY`.
3. Run all the cells in the notebook.
4. Check the outputs for the "Detailed Agent Workflow Analysis" section (or equivalent prints) to ensure the agent is calling the tools as expected.
5. Save the notebook **with the outputs included**.
6. Resubmit the project.

![1766581438006](image/criteria2/1766581438006.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418224/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418242/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418255/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418267/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418277/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418283/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418321/image.png)

## Resources

**LangChain Agents Tutorial (Official)**
https://python.langchain.com/docs/tutorials/agents/
This tutorial is the gold standard for understanding how agents works. It explains the loop of "Reason -> Act -> Observe" that you are implementing. Reviewing this can help you debug if your agent isn't calling tools as expected when you run the notebook.

**Tavily Search API Documentation**
https://docs.tavily.com/documentation/api-reference/endpoint/search
You are using Tavily for the web search fallback. This documentation shows the structure of the response you get back, which is crucial for formatting the "Context" you pass back to the LLM.

**OpenAI Function Calling Documentation**
https://platform.openai.com/docs/guides/function-calling
Under the hood, your tools are likely being passed to the model as "functions". Understanding how OpenAI handles these function definitions and the JSON schema can help you write better tool descriptions and arguments.

**LlamaIndex Evaluating Module**
https://developers.llamaindex.ai/python/framework/module_guides/evaluating/
Since you implemented an evaluation tool, this resource is very relevant. It discusses different metrics and methods for evaluating RAG systems, which could give you ideas for making your `evaluate_retrieval` tool even more robust in the future.

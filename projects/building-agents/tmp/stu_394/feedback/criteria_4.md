# Criterion 4: Agent Demonstration and Reporting - Review

I liked how you set up the final agent invocation. The output showing the `ToolMessage` and `AIMessage` sequence provides a clear look into the "brain" of your agent, showing exactly how it decided to call the web search tool after the internal retrieval failed. This visibility is excellent for debugging.

However, this criterion is marked as **FAIL** because the submission does not demonstrate the agent on the required minimum of three example queries.

## What did not work
The notebook only runs a single query: "Provide me the details of the game Need for Speed ?".
The project requirements specify that you must run the agent on **at least three** example queries. The starter code suggested specific questions (Pokémon Gold, Mario 3D, Mortal Kombat) to cover different scenarios, but these were not executed.

## Why it did not work
A single test case is insufficient to prove that an agent is robust. You demonstrated that the "Fallback to Web Search" path works, but you haven't demonstrated:
1.  **Internal Retrieval Success**: A query that *should* be found in your vector DB (to prove RAG works).
2.  **Complex Reasoning**: A query that might require comparing two games or checking a specific detail.
Without these additional tests, we cannot verify that the "Retrieve -> Evaluate -> Web" logic works in all intended scenarios.

## Why this matters in the real world
In AI Engineering, "Evaluation" is as important as "Implementation". You cannot deploy an agent based on one successful chat. You need a test set that covers "Happy Paths" (data found) and "Edge Cases" (data missing). Running multiple queries acts as your integration test suite, proving to stakeholders that the system is reliable.

## Steps to resolve
1.  **Add More Invocations**: Create new cells or expand the current one to call `agent.invoke()` at least two more times.
    ```python
    # Example 2: Should ideally hit the Vector DB (if data exists)
    run2 = agent.invoke(query="Tell me about Super Mario 64")
    print(run2.get_final_state()["messages"][-1].content)

    # Example 3: Another diverse query
    run3 = agent.invoke(query="When was Pokémon Gold released?")
    print(run3.get_final_state()["messages"][-1].content)
    ```
2.  **Verify Outputs**: Ensure that for each query, you print the final response so we can see the answer and any citations.

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766746155/image.png)

## Resources

**LangSmith Evaluation Documentation**
https://docs.langchain.com/langsmith/evaluation
This is the gold standard for how to think about evaluating agents. It moves beyond "print statements" to systematic testing of agent traces.

**Agent Evaluation Cookbook (GitHub)**
https://github.com/langchain-ai/langsmith-cookbook/blob/main/testing-examples/agent_steps/evaluating_agents.ipynb
Use this cookbook to see code examples of how to structure agent tests. It shows how to check if the agent took the expected steps (like calling the right tool).

**LlamaIndex Evaluation Module**
https://developers.llamaindex.ai/python/framework/module_guides/evaluating/
Since your agent uses retrieval, this guide helps you understand how to evaluate the *quality* of the retrieved documents for each of your 3 queries.

**Testing LLMs with LangSmith**
https://medium.com/@andycartel1507/testing-llms-with-langsmith-f9d003ded696
A practical guide on setting up a testing workflow. Even without LangSmith, the *mindset* of "testing inputs and expected outputs" is what you should apply to your notebook demonstrations.

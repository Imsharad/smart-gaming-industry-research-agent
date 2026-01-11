# Criterion 4: Agent Demonstration and Reporting

I noticed that you set up three excellent test queries covering different aspects of the game industry: a specific release date (Pokémon), a genre-defining game (Mario 3D platformer), and a platform availability check (Mortal Kombat X). These are great test cases to stress-test your agent's different tools.

## Status: FAIL

### What did not work
The notebook `Udaplay_02_starter_project.ipynb` has not been executed, and all output cells are empty. This criterion specifically requires you to *demonstrate* the agent's performance. Without the outputs, I cannot see the agent's reasoning process, which tools it selected, or the final answers it generated.

### Why it did not work
The "demonstration" part of this project is about transparency. We need to see the "thought process" of the agent. Did it try to search the vector DB for "Mortal Kombat X"? Did the evaluation tool correctly identify if the information was missing? Did it fall back to the web search? Without the execution logs, these questions remain unanswered. You've built the engine (the code), but you haven't turned the key to show us it runs.

### Why this matters in the real world
In AI engineering, evaluation is everything. An agent might look correct in code but fail in production because of a subtle prompting issue or an API rate limit. Showing the execution traces (reasoning steps, tool inputs/outputs) is standard practice for validating that an agent is behaving safely and correctly. It also proves that the agent is citing sources as requested.

### Steps to resolve the issue
1. Open `Udaplay_02_starter_project.ipynb`.
2. Run all cells, ensuring the agent executes Query 1, Query 2, and Query 3.
3. Verify that the output shows the "Workflow Analysis" or similar debug prints that display the tool usage and reasoning.
4. Check that the final answers are printed and contain citations.
5. Save the notebook **with the outputs included**.
6. Resubmit the project.

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766746155/image.png)

## Resources

**LangSmith Evaluation Documentation**
https://docs.langchain.com/langsmith/evaluation
Evaluating agents is a complex topic. LangSmith is a platform designed specifically for this, allowing you to trace and score your agent's runs. Reading this will give you a professional perspective on how to demonstrate and evaluate agent performance.

**Agent Evaluation Cookbook (GitHub)**
https://github.com/langchain-ai/langsmith-cookbook/blob/main/testing-examples/agent_steps/evaluating_agents.ipynb
This notebook provides practical examples of how to evaluate agents based on their decision-making process. It's a great resource to see how you can systematically test if your agent is choosing the right tools.

**LlamaIndex Evaluation Module**
https://developers.llamaindex.ai/python/framework/module_guides/evaluating/
Since you are using LlamaIndex concepts, this guide on their evaluation framework is very relevant. It discusses metrics like "faithfulness" and "relevancy," which are exactly what your `evaluate_retrieval` tool is trying to measure.

**OpenAI Cookbook: Evaluate RAG**
https://cookbook.openai.com/examples/evaluation/evaluate_rag_with_llamaindex
This cookbook shows how to use LlamaIndex to evaluate RAG systems built with OpenAI models. It connects the dots between the different technologies you are using in this project.

# Criterion 4: Agent Demonstration and Reporting

**Status: FAIL**

I liked that you included test invocations in your script using `agent.invoke`. Testing your agent with concrete inputs like "what is my availability on Friday?" is a great practice to verify functionality immediately.

## What did not work
This criterion is marked as **FAIL** because the demonstration does not cover the required **Video Game RAG** scenarios. To pass, you must submit a notebook (`Udaplay_02_solution_project.ipynb`) that runs the agent on at least **three** specific example queries about video games (e.g., release dates, platforms, developers). The output must clearly show the agent's reasoning process (Thought -> Action -> Observation) and the final answer with citations.

## Why it did not work
The current tests are for the Email Assistant. Without seeing the agent handle specific game queries, I cannot verify that the RAG pipeline (Criterion 1) and the Tools (Criterion 2) are working together correctly to retrieve and answer questions from the game dataset.

## Why this matters in the real world
End-to-end testing with domain-specific queries is the gold standard for validation. In a production environment, we wouldn't ship a "Game Bot" that has only been tested on "Email" tasks. Demonstrating the agent's reasoning trace is also critical for debugging—it lets us see *why* the agent chose a specific tool or answer.

## Steps to resolve the issue
1.  **Create the Notebook**: Start a new notebook `Udaplay_02_solution_project.ipynb`.
2.  **Define Test Queries**: Select at least 3 distinct queries about games in your dataset (e.g., "When was Fallout 4 released?", "Who developed Rocket League?", "What genres is Hades?").
3.  **Run the Agent**: Execute these queries using your Udaplay agent.
4.  **Show the Trace**: Ensure the output displays the agent's "thought process" (using `verbose=True` or printing the intermediate steps) so we can see it deciding to use the `retrieve_game_data` tool.

## Resources

Use these resources to guide your evaluation and demonstration process:

**LangSmith Evaluation Documentation**
[https://docs.langchain.com/langsmith/evaluation](https://docs.langchain.com/langsmith/evaluation)
Since you are using LangChain components, LangSmith is the natural next step for systematic testing. It allows you to trace exactly what your agent is doing during those test queries.

**LlamaIndex Evaluation Module**
[https://developers.llamaindex.ai/python/framework/module_guides/evaluating/](https://developers.llamaindex.ai/python/framework/module_guides/evaluating/)
This resource provides a great framework for thinking about *what* to evaluate (correctness, faithfulness) even if you implement the checks manually or with another tool.

**Weights & Biases: Agent Performance Monitoring**
[https://docs.wandb.ai/guides/prompts](https://docs.wandb.ai/guides/prompts)
W&B provides excellent tools for tracking agent experiments. Looking at their guides can give you ideas on how to structure your reporting and visualizations.

**OpenAI: Prompt Engineering Guide**
[https://platform.openai.com/docs/guides/prompt-engineering](https://platform.openai.com/docs/guides/prompt-engineering)
To get your agent to show its reasoning (Chain-of-Thought), you often need to adjust your system prompts. This guide is the industry standard for learning those techniques.

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766746155/image.png)

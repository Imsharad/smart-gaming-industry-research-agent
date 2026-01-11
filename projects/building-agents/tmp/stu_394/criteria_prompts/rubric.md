<criteria>
1. RAG
Prepare and process a local dataset of video game information for use in a vector database and RAG pipeline
</criteria>

<requirements>
Requirements to Pass:

The submission includes the notebook (Udaplay_01_solution_project.ipynb) that loads, processes, and formats the provided game JSON files.
The processed data is added to a persistent vector database (e.g., ChromaDB) with appropriate embeddings.
The notebook or script demonstrates that the vector database can be queried for semantic search.
</requirements>

<tip>
Reviewer Tip

Confirm that the data loading and processing steps are present and correct.

Check that the vector database is persitently created and populated with the game data.

Ensure that at least one semantic search query is demonstrated and returns relevant results.

Do NOT fail if the student uses a different embedding model or vector DB, as long as the pipeline works.
</tip>

<recommendation>
Look for evidence of successful data loading by checking notebook outputs for confirmation messages, data counts, or sample entries. Verify that the vector database collection shows populated documents and that semantic search queries return meaningful, relevant results with proper document metadata.
</recommendation>

<criteria>
2. Agent Development
Implement agent tools for internal retrieval, evaluation, and web search fallback.
</criteria>

<requirements>
Requirements to Pass:

The submission includes at least three tools:
A tool to retrieve game information from the vector database.
A tool to evaluate the quality of retrieved results.
A tool to perform web search using an API (e.g., Tavily).
Each tool is implemented as a function/class and is integrated into the agent workflow.
The agent: 
first attempts to answer using internal knowledge,
evaluates the result,
and falls back to web search if needed.
</requirements>

<tip>
Reviewer Tip

Check that all three tools are present and functional.

Confirm that the agent workflow uses the tools in the correct order (internal → evaluate → web).

Ensure that the tools are documented and their outputs are used in the agent's reasoning.

Do NOT fail if the student uses a different web search API, as long as the fallback works.
</tip>

<recommendation>
Examine the tool implementations for proper function signatures, docstrings, and error handling. Verify that the evaluation tool provides meaningful assessment of retrieval quality and that the web search tool is properly configured with API credentials and returns structured results.
</recommendation>

<criteria>
3. Build a stateful agent that manages conversation and tool usage.
</criteria>

<requirements>
Requirements to Pass:

The agent is implemented as a class or function that maintains conversation state.
The agent can handle multiple queries in a session, remembering previous context.
The agent's workflow is implemented as a state machine or similar abstraction.
The agent produces clear, structured, and well-cited answers.
</requirements>

<tip>
Reviewer Tip

Confirm that the agent maintains state across multiple queries.

Check that the agent's workflow is modular and uses the tools as nodes or steps.

Ensure that the agent's responses are clear, cite sources, and combine information when needed.

Do NOT fail if the state management is simple, as long as it works and is documented.
</tip>

<recommendation>
Look for evidence of state persistence between queries, such as conversation history, session tracking, or context variables. Verify that the agent's responses include proper source citations and that the workflow demonstrates clear reasoning steps through tool usage.
</recommendation>

<criteria>
4. Demonstrate and report on the agent's performance with example queries.
</criteria>

<requirements>
Requirements to Pass:

The submission includes the notebook (Udaplay_02_solution_project.ipynb) that runs the agent on at least three example queries (e.g., about game release dates, platforms, or publishers).

The output for each query includes the agent's reasoning, tool usage, and final answer.

The report includes at least the response with citation, if any
</requirements>

<tip>
Reviewer Tip

Check that at least three example queries are run and outputs are shown.

Confirm that the agent's reasoning and tool usage are visible in the output.

Ensure that the report contains the final response and the citation, if from web

Do NOT fail if the agent cannot answer every query perfectly, as long as the process is demonstrated.
</tip>

<recommendation>
Review the notebook outputs to ensure each query demonstrates the complete agent workflow, including tool selection reasoning, retrieval attempts, evaluation results, and final responses. Look for clear evidence of the agent's decision-making process and proper citation of information sources.
</recommendation>
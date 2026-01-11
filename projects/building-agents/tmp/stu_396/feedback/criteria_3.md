# Criterion 3: Stateful Agent

You have successfully built a stateful agent that manages its own memory and workflow! I was impressed by your implementation of the `StateMachine` class and how you defined the `AgentState` using `TypedDict`. This structured approach to state management—defining explicit steps like `message_prep`, `query_llm`, and `query_tool`—is exactly how production-grade agents are built today.

Your session management logic is also working correctly. The execution logs show the agent handling a multi-turn conversation about "Need for Speed," where it correctly understood follow-up questions like "Who was the developer?" without the user needing to restate the game's name. This proves that your `ShortTermMemory` and context preservation are functioning as intended.

## Evaluation
**Status: PASS**

Your implementation demonstrates:
- **State Management:** `AgentState` captures the conversation history and tool calls effectively.
- **Workflow:** The state machine correctly transitions between LLM reasoning and tool execution.
- **Context:** The agent remembers previous turns in the session (`session_id="project"`).
- **Response Quality:** The answers are structured and grounded in the tool outputs.

*Suggestion for improvement:* While your agent uses the retrieved information effectively, I noticed the final answers don't always explicitly cite the URLs (e.g., `[Source: wikipedia.org]`). To make your agent "well-cited" for end-users, you could simply update your system instructions string to say: *"Always cite the source URL for every fact you mention."*

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766580604/image.png)

## Additional Resources

To further refine your stateful agent, check out these resources:

**LangGraph: Production Agent Workflows**
[https://python.langchain.com/docs/langgraph/](https://python.langchain.com/docs/langgraph/)
You built a custom state machine, which is great! LangGraph is the industry-standard library that formalizes this pattern. Learning it will let you build even more complex workflows with loops and conditional branching.

**OpenAI Assistants API - Citations**
[https://platform.openai.com/docs/assistants/tools/file-search#citations](https://platform.openai.com/docs/assistants/tools/file-search#citations)
This guide explains how to programmatically extract and format citations. Even if you aren't using the Assistants API directly, the patterns for handling annotations and source attribution are very relevant to your current project.

**LangChain Memory Patterns**
[https://python.langchain.com/docs/how_to/memory/](https://python.langchain.com/docs/how_to/memory/)
Your `ShortTermMemory` is a good start. This documentation covers more advanced memory types, like "ConversationSummaryMemory," which summarizes old messages to save tokens—a crucial technique for long-running agents.

**Anthropic: Claude's Conversation Architecture**
[https://docs.anthropic.com/claude/docs/conversations](https://docs.anthropic.com/claude/docs/conversations)
This is a great read on the theory of conversation management. It explains how to structure "threads" and manage context windows effectively to prevent the agent from getting confused over time.

# Criteria 3: Stateful Agent
**Build a stateful agent that manages conversation and tool usage**

## Setup
```bash
# Set the student directory variable (replace X with actual student number)
STUDENT_DIR="stu_X"  # e.g., stu_51, stu_52, stu_49, etc.
```

## Requirements to Pass:

### 1. The agent is implemented as a class or function that maintains conversation state

**Verification Steps:**

```bash
# Check for agent class definition
grep -n "class.*Agent\|class.*Assistant\|class.*Bot" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "class.*Agent\|class.*Assistant" ${STUDENT_DIR}/lib/*.py 2>/dev/null

# Look for agent initialization with state
grep -n "__init__.*self\|def.*create_agent\|initialize.*agent" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "self.state\|self.memory\|self.history\|self.context" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for state management variables
grep -n "conversation.*history\|chat.*history\|message.*history" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "state.*=.*\|State.*=\|AgentState" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for memory/state storage
grep -n "memory\|Memory\|ConversationBuffer\|ChatMessageHistory" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "session\|Session\|conversation_id" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for state persistence mechanisms
grep -n "save.*state\|load.*state\|persist\|store.*history" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

### 2. The agent can handle multiple queries in a session, remembering previous context

**Verification Steps:**

```bash
# Check for message/query handling loop
grep -n "while\|for.*query\|multiple.*queries" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "invoke.*multiple\|run.*multiple\|test.*queries" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for context preservation
grep -n "append.*history\|add.*message\|update.*context" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "previous.*context\|remember\|recall" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for conversation continuity
grep -n "follow.*up\|previous.*answer\|earlier\|mentioned" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "context.*window\|conversation.*buffer" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify state updates between queries
grep -n "state\[.*\]._=\|update.*state\|modify.*state" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for demonstration of multiple queries
grep -B2 -A5 "query.*1\|first.*question\|Query.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -B2 -A5 "query.*2\|second.*question\|follow.*up" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check if agent references previous interactions
grep -n "as.*mentioned\|previously\|earlier.*response" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

### 3. The agent's workflow is implemented as a state machine or similar abstraction

**Verification Steps:**

```bash
# Check for state machine implementation
grep -n "StateGraph\|state.*machine\|StateMachine" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "LangGraph\|workflow\|WorkflowGraph" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for nodes and edges
grep -n "add_node\|add_edge\|add_conditional" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "START\|END\|node\|edge" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for state transitions
grep -n "transition\|next_state\|move_to\|go_to" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "should_.*\|decide.*next\|route" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify workflow compilation
grep -n "compile\|build.*graph\|create.*workflow" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for workflow visualization (bonus)
grep -n "draw\|visualize\|display.*graph\|mermaid" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for modular workflow steps
grep -n "def.*node\|def.*step\|def.*stage" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

### 4. The agent produces clear, structured, and well-cited answers

**Verification Steps:**

```bash
# Check for citation/source tracking
grep -n "source\|citation\|cite\|reference" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "\[.*\]_\|\\cite\|Source:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for structured response formatting
grep -n "format.*response\|structure.*answer\|response.*template" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "markdown\|\n\n\|bullet\|###" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for answer combination logic
grep -n "combine\|merge\|aggregate.*information" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "synthesize\|summarize\|consolidate" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify clear output formatting
grep -n "print.*response\|display.*answer\|output.*format" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for metadata in responses
grep -n "metadata\|confidence\|relevance.*score" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify web search citation accuracy
grep -B5 -A5 "Information is from.*http\|source.*http" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
echo "VERIFY: Check that web search citations use actual URLs from search results, not generated URLs"
```

## Additional Verification Commands:

```bash
# Check for proper state typing/schema
grep -n "TypedDict\|BaseModel\|dataclass.*State" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "from typing\|Annotated\|State.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify agent invocation pattern
grep -n "agent.invoke\|agent.run\|agent.chat\|agent.query" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for proper error handling in stateful operations
grep -n "try.*state\|except.*state\|handle.*error" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for thread/session safety
grep -n "thread\|session_id\|user_id\|conversation_id" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for state reset/clear functionality
grep -n "reset\|clear.*history\|new.*session" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

## Quick State Management Check:

```bash
# One-liner to verify state management components
echo "=== Checking State Management in ${STUDENT_DIR} ===" && \
echo "Agent class defs: $(grep -c "class.*Agent" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "State variables: $(grep -c "self.state\|self.memory\|self.history" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "State updates: $(grep -c "update.*state\|append.*history" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Workflow refs: $(grep -c "StateGraph\|workflow\|state.*machine" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Multiple queries: $(grep -c "query.*[0-9]_\|Question.*:" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Citations: $(grep -c "source\|citation\|reference" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
```

## Session Continuity Verification:

```bash
# Check for evidence of multi-turn conversations
echo "=== Verifying Session Continuity ===" && \
echo "Checking for multiple test queries:" && \
grep -n "query\|question\|ask" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -10 && \
echo "Checking for context references:" && \
grep -n "previous\|earlier\|mentioned\|follow" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -5
```

## Reviewer Tips:

- **Confirm** that the agent maintains state across multiple queries
- **Check** that the agent's workflow is modular and uses the tools as nodes or steps
- **Ensure** that the agent's responses are clear, cite sources, and combine information when needed
- **IMPORTANT:** Do NOT fail if the state management is simple, as long as it works and is documented

## What to Look For:

- **State persistence:** Evidence of conversation history, session tracking, or context variables
- **Multi-query handling:** Agent can handle follow-up questions and remembers context
- **Workflow structure:** Clear state machine or workflow abstraction
- **Response quality:** Proper source citations and clear reasoning steps
- **Information synthesis:** Agent combines information from multiple sources when appropriate

## Common Issues to Check:

```bash
# No state management
grep -c "state\|memory\|history" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || echo "WARNING: No state management found"

# Single query only
grep -c "multiple\|several\|follow" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || echo "WARNING: May only handle single queries"

# No workflow structure
grep -c "workflow\|graph\|state.*machine" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || echo "WARNING: No workflow abstraction found"

# Missing citations
grep -c "source\|citation\|reference" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || echo "WARNING: No citation mechanism found"

# No state initialization
grep -c "__init__\|initialize\|create.*agent" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || echo "WARNING: No agent initialization found"

# Web search citation accuracy (check if URLs match actual search results)
grep -n "Information is from.*http" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
echo "MANUAL CHECK: Verify that cited URLs match the actual URLs returned by web search tool"
```

## Acceptable Implementation Patterns:

```bash
# Various valid state management approaches
echo "=== Checking for different valid approaches ===" && \
echo "LangChain memory: $(grep -c "ConversationBuffer\|ChatMessageHistory" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "LangGraph states: $(grep -c "StateGraph\|TypedDict.*State" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Custom state dict: $(grep -c "state.*=.*{.*}\|self.state" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Session management: $(grep -c "session\|Session" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
```

## Additional Learning Resources:

### Essential Reading - Stateful Agents and Conversation Memory

**LangGraph State Management and Memory:**
- [LangGraph Memory Management - Overview](https://langchain-ai.github.io/langgraph/concepts/memory/) - Comprehensive guide to short-term and long-term memory in LangGraph
- [LangGraph Tutorial: Building LLM Agents with LangChain's Agent Framework](https://www.getzep.com/ai-agents/langgraph-tutorial/) - Step-by-step tutorial with memory management examples
- [LangGraph Uncovered: Building Stateful Multi-Agent Applications with LLMs](https://dev.to/sreeni5018/langgraph-uncovered-building-stateful-multi-agent-applications-with-llms-part-i-p86) - Deep dive into stateful agent architectures
- [Add memory](https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/) - Practical implementation guide for adding memory to LangGraph agents

**Multi-Turn Conversation and State Persistence:**
- [LangGraph & Redis: Build smarter AI agents with memory & persistence](https://redis.io/blog/langgraph-redis-build-smarter-ai-agents-with-memory-persistence/) - Production-grade memory persistence with Redis
- [Giving Your AI Agents a Memory: Persistence and State in LangGraph](https://krishankantsinghal.medium.com/giving-your-ai-agents-a-memory-persistence-and-state-in-langgraph-407eb9f541d2) - Comprehensive guide to implementing persistent memory
- [Building AI Agents That Actually Remember: A Guide to Stateful Function Tools](https://medium.com/@Micheal-Lanham/building-ai-agents-that-actually-remember-a-guide-to-stateful-function-tools-02b0b1e46937) - Practical patterns for stateful agent implementation
- [Stateful Agents: Conversational Memory That Actually Works](https://toolhouse.ai/blog/stateful-agents-conversational-memory-that-actually-works) - Best practices for conversational memory

**LangChain Conversation Memory and Buffers:**
- [Migrating off ConversationBufferMemory | LangChain](https://python.langchain.com/docs/versions/migrating_memory/conversation_buffer_memory/) - Migration guide from traditional memory to modern approaches
- [A Long-Term Memory Agent | LangChain](https://python.langchain.com/docs/versions/migrating_memory/long_term_memory_agent/) - Implementing agents with long-term memory capabilities
- [How to add memory to chatbots | LangChain](https://python.langchain.com/docs/how_to/chatbots_memory/) - Adding memory to conversational applications
- [Conversational Memory for LLMs with Langchain | Pinecone](https://www.pinecone.io/learn/series/langchain/langchain-conversational-memory/) - Detailed tutorial on implementing conversational memory

**Session Management and Multi-User State Tracking:**
- [Session Management - OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) - Security best practices for session management
- [User Session Management: Best Practices for Secure Access](https://frontegg.com/blog/user-session-management) - Enterprise-grade session management strategies
- [Session management best practices — WorkOS](https://workos.com/blog/session-management-best-practices) - Scalable session management for production systems
- [Session - Agent Development Kit](https://google.github.io/adk-docs/sessions/session/) - Google's approach to agent session management
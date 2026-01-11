# Criteria 2: Agent Development
**Implement agent tools for internal retrieval, evaluation, and web search fallback**

## Setup
```bash
# Set the student directory variable (replace X with actual student number)
STUDENT_DIR="stu_X"  # e.g., stu_51, stu_52, stu_49, etc.
```

## Requirements to Pass:

### 1. The submission includes at least three tools:
- A tool to retrieve game information from the vector database
- A tool to evaluate the quality of retrieved results
- A tool to perform web search using an API (e.g., Tavily)

**Verification Steps:**

```bash
# Check for tool definitions (common patterns)
grep -n "@tool\|def.*tool\|class.*Tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "@tool\|def.*tool\|class.*Tool" ${STUDENT_DIR}/lib/*.py 2>/dev/null

# Look for retrieval tool implementation
grep -n "retrieve\|retrieval\|get_game\|search_game\|query_database" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "collection.query\|similarity_search\|vector.*search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for evaluation tool
grep -n "evaluate\|eval\|quality\|relevance\|score\|assess" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "def evaluate\|class.*Evaluat" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for web search tool
grep -n "tavily\|serper\|google\|bing\|web.*search\|api.*search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "TavilyClient\|requests.get\|api_key" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for tool documentation (docstrings)
grep -B2 -A10 '"""' ${STUDENT_DIR}/Udaplay_02_*project.ipynb | grep -E "tool|retrieve|evaluate|search"

# Count distinct tool functions/classes
grep -c "^def.*tool\|^class.*Tool\|@tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check if tools are in separate module files
ls -la ${STUDENT_DIR}/tools/ 2>/dev/null || ls -la ${STUDENT_DIR}/*/tools/ 2>/dev/null
find ${STUDENT_DIR} -name "*tool*.py" -o -name "*retriev*.py" -o -name "*eval*.py" -o -name "*search*.py"
```

### 2. Each tool is implemented as a function/class and is integrated into the agent workflow

**Verification Steps:**

```bash
# Check for tool integration in agent
grep -n "tools=\[\|tool_list\|available_tools" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "bind_tools\|tool_executor\|execute_tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for LangChain/LlamaIndex tool integration
grep -n "StructuredTool\|Tool\|FunctionTool\|tool_decorator" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "from langchain.*tools\|from llama_index.*tools" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for workflow integration
grep -n "workflow\|StateGraph\|Graph\|pipeline" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "add_node\|add_edge\|compile" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for tool execution in agent
grep -n "tool_calls\|function_call\|use_tool\|invoke.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "if.*tool.*in\|select.*tool\|choose.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for proper function signatures
grep -A3 "def.*retrieve\|def.*evaluate\|def.*search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify tools return structured data
grep -n "return.*{.*\|return.*dict\|return.*json" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

### 3. The agent first attempts to answer using internal knowledge, evaluates the result, and falls back to web search if needed

**Verification Steps:**

```bash
# Check for workflow order implementation
grep -n -A10 "internal.*first\|try.*internal\|attempt.*retriev" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n -A10 "evaluate.*result\|check.*quality\|assess.*retriev" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n -A10 "fallback\|web.*search.*if\|if.*not.*sufficient" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Look for conditional logic (internal → evaluate → web)
grep -n "if.*retriev\|if.*evaluat\|if.*quality" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "else.*web\|fallback.*web\|then.*search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for state transitions
grep -n "next.*state\|transition\|should_.*\|decide_next" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "END\|CONTINUE\|next_step" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify the complete flow in execution
grep -B5 -A10 "invoke\|execute\|run.*agent" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | grep -E "retriev|evaluat|web|search"

# Look for agent reasoning about tool selection
grep -n "reasoning\|thought\|decide\|select.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for proper error handling and fallback
grep -n "try.*except\|if.*error\|handle.*exception" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "fallback\|alternative\|backup" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

## Additional Verification Commands:

```bash
# Check for agent class/function definition
grep -n "class.*Agent\|def.*agent\|create_agent" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify API key configuration
grep -n "api_key\|API_KEY\|getenv\|environ" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
grep -n "TAVILY\|SERPER\|GOOGLE" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for prompt templates that guide tool usage
grep -n "prompt\|template\|system.*message" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -20

# Look for tool descriptions
grep -n "description.*=\|tool_description\|help.*=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check if tools handle edge cases
grep -n "if.*not.*result\|if.*empty\|if.*None" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Verify logging/debugging for tool usage
grep -n "print.*tool\|log.*tool\|debug" ${STUDENT_DIR}/Udaplay_02_*project.ipynb

# Check for tool testing
grep -n "test.*tool\|assert\|example.*query" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
```

## Quick Tool Verification Check:

```bash
# One-liner to verify all three tools and workflow
echo "=== Checking Tools in ${STUDENT_DIR} ===" && \
echo "Retrieval tool refs: $(grep -c "retrieve\|retrieval\|query_database" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Evaluation tool refs: $(grep -c "evaluate\|assess\|quality" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Web search tool refs: $(grep -c "tavily\|web.*search\|api.*search" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Tool decorators: $(grep -c "@tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Workflow refs: $(grep -c "workflow\|StateGraph\|pipeline" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Tool integration: $(grep -c "tools=\[\|bind_tools\|tool_executor" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
```

## Workflow Order Verification:

```bash
# Extract and verify the workflow sequence
echo "=== Verifying Workflow Order ===" && \
echo "1. Internal retrieval attempts:" && \
grep -n "retrieve\|query.*collection\|search.*vector" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -5 && \
echo "2. Evaluation steps:" && \
grep -n "evaluate\|quality\|relevance.*check" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -5 && \
echo "3. Web search fallback:" && \
grep -n "web.*search\|tavily\|fallback" ${STUDENT_DIR}/Udaplay_02_*project.ipynb | head -5
```

## Reviewer Tips:

- **Check** that all three tools are present and functional
- **Confirm** that the agent workflow uses the tools in the correct order (internal → evaluate → web)
- **Ensure** that the tools are documented and their outputs are used in the agent's reasoning
- **IMPORTANT:** Do NOT fail if the student uses a different web search API, as long as the fallback works

## What to Look For:

- **Tool implementations:** Proper function signatures, docstrings, and error handling
- **Evaluation tool:** Provides meaningful assessment of retrieval quality
- **Web search tool:** Properly configured with API credentials and returns structured results
- **Integration:** Tools are properly integrated into the agent workflow
- **Workflow order:** Clear evidence of internal → evaluate → web sequence

## Common Issues to Check:

```bash
# Missing tool definitions
grep -c "@tool\|def.*tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || echo "WARNING: No tool definitions found"

# No API key configuration
grep -c "api_key\|API_KEY" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || echo "WARNING: No API key configuration found"

# Missing workflow structure
grep -c "workflow\|graph\|pipeline" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || echo "WARNING: No workflow structure found"

# Tools not integrated
grep -c "tools=\[\|bind_tools" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || echo "WARNING: Tools may not be integrated"

# No evaluation logic
grep -c "evaluate\|quality\|relevance" ${STUDENT_DIR}/Udaplay_02_*project.ipynb || echo "WARNING: No evaluation logic found"
```

## Tool Implementation Patterns to Accept:

```bash
# Different valid tool implementation patterns
echo "=== Checking for various valid implementations ===" && \
echo "LangChain tools: $(grep -c "langchain.*tool\|StructuredTool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "LlamaIndex tools: $(grep -c "llama.*tool\|FunctionTool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "Custom tools: $(grep -c "class.*Tool\|def.*_tool" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)" && \
echo "OpenAI functions: $(grep -c "function_call\|functions=" ${STUDENT_DIR}/Udaplay_02_*project.ipynb 2>/dev/null)"
```

## Additional Learning Resources:

### Essential Reading - Agent Tools and Function Calling

**LangChain Agent Tools Implementation:**
- [How to create tools | LangChain](https://python.langchain.com/docs/how_to/custom_tools/) - Official guide for creating custom tools using @tool decorator
- [Tool calling | LangChain](https://python.langchain.com/docs/concepts/tool_calling/) - Comprehensive overview of tool calling concepts and patterns
- [How to do tool/function calling | LangChain](https://python.langchain.com/docs/how_to/function_calling/) - Step-by-step implementation guide for function calling
- [Building Custom Tools for LLM Agents | Pinecone](https://www.pinecone.io/learn/series/langchain/langchain-tools/) - Advanced tool creation with practical examples

**LLM Agents with Tools and Web Search:**
- [Building a Web-Searching Agent with LangChain and Llama 3.3 70B](https://www.analyticsvidhya.com/blog/2024/12/building-a-web-searching-agent/) - Complete implementation of web-searching agents
- [Tool Use Agent with RAG + Web Search](https://medium.com/@vsletten/tool-use-agent-with-rag-web-search-8a2696d5eea5) - Combining retrieval and web search in agent workflows
- [LLM Agent Evaluation: Assessing Tool Use, Task Completion, Agentic Reasoning, and More](https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide) - Comprehensive evaluation strategies for agent tools
- [The Ultimate Guide to Web Search APIs for LLMs](https://www.mattcollins.net/web-search-apis-for-llms) - Web search integration best practices

**Agent Workflow Design and Tool Selection:**
- [What Are Agentic Workflows? Patterns, Use Cases, Examples, and More](https://weaviate.io/blog/what-are-agentic-workflows) - Understanding workflow patterns and tool selection
- [AI Agentic Workflows: Tutorial & Best Practices](https://fme.safe.com/guides/ai-agent-architecture/ai-agentic-workflows/) - Best practices for designing agent workflows
- [Advanced LangGraph: Implementing Conditional Edges and Tool-Calling Agents](https://dev.to/jamesli/advanced-langgraph-implementing-conditional-edges-and-tool-calling-agents-3pdn) - Advanced workflow design with conditional logic
- [AI Agent Workflows: A Complete Guide on Whether to Build With LangGraph or LangChain](https://medium.com/data-science/ai-agent-workflows-a-complete-guide-on-whether-to-build-with-langgraph-or-langchain-117025509fa0) - Framework selection guidance

**Function Calling and OpenAI Tools API:**
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling) - Official OpenAI function calling documentation
- [Function calling using LLMs](https://martinfowler.com/articles/function-call-LLM.html) - Comprehensive patterns and implementation strategies
- [An introduction to function calling and tool use](https://www.apideck.com/blog/llm-tool-use-and-function-calling) - Fundamental concepts and practical applications
- [A Guide to Function Calling in OpenAI | Mirascope](https://mirascope.com/blog/openai-function-calling) - Advanced techniques and best practices
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
grep -n "return.*{.*}\|return.*dict\|return.*json" ${STUDENT_DIR}/Udaplay_02_*project.ipynb
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

## External Resources

Add these curated resources at the end when generating the feedback/2.md file:

### Agent Architecture & Tool Integration

**LangChain Deep Agents Tutorial**
https://python.langchain.com/docs/tutorials/agents/
Comprehensive tutorial for building agents with proper tool integration, decision-making frameworks, and workflow orchestration using LangChain's latest patterns.

**Building Reliable Agent Systems**
https://blog.langchain.com/top-5-langgraph-agents-in-production-2024/
LangChain's analysis of production-ready agent patterns, tool selection strategies, and reliable execution approaches from real-world implementations.

**Agent Tool Design Patterns**
https://python.langchain.com/docs/tutorials/agents/
Official LangChain documentation on tool creation, integration patterns, and best practices for agent tool ecosystems.

### Tool Implementation & Web Search

**Creating Custom Agent Tools**
https://www.llamaindex.ai/blog/agentic-rag-with-llamaindex-2721b8a49ff6
LlamaIndex's guide to building custom tools for agentic RAG systems, including retrieval and evaluation tool patterns.

**Web Search Integration for AI Agents**
https://docs.tavily.com/documentation/api-reference/endpoint/search
Tavily's documentation on integrating web search into AI agents, including API usage patterns and result processing.

**Serper API for Agent Search**
https://serper.dev/playground
Alternative web search API with examples of integration into agent workflows. Useful for understanding different search API patterns.

### Agent Evaluation & Quality Control

**Tool Result Evaluation Strategies**
https://docs.llamaindex.ai/en/stable/module_guides/evaluating/
LlamaIndex's comprehensive framework for evaluating tool outputs and implementing quality gates in agent workflows.

**Agent Reliability Patterns**
https://docs.llamaindex.ai/en/stable/module_guides/deploying/
LlamaIndex's guide to building production-ready agents with proper error handling, fallback strategies, and reliability patterns.

### Workflow Orchestration

**Agent State Management**
https://python.langchain.com/docs/langgraph/
Introduction to LangGraph for complex agent workflows with state management, conditional routing, and multi-step reasoning.

**ReAct: Reasoning and Acting in Language Models**
https://react-lm.github.io/
The foundational paper and methodology behind ReAct agents - essential for understanding agent reasoning patterns.

### Multi-Tool Agent Patterns

**Building Multi-Modal Agents**
https://docs.llamaindex.ai/en/stable/module_guides/loading/multi_modal/
LlamaIndex's approach to building agents that can handle multiple types of tools and data sources.

**Agent Toolchain Best Practices**
https://python.langchain.com/docs/use_cases/agent_simulations/
LangChain's collection of agent implementation patterns and toolchain design principles.

## Further Reading

### High-Authority Sources from Leading AI Companies

**OpenAI: Function Calling and Tool Integration**
https://platform.openai.com/docs/guides/function-calling
OpenAI's official guide to function calling with GPT models, covering tool definition, integration patterns, and best practices for building reliable agent systems with external tool access.

**Anthropic: Building Effective AI Agents**
https://www.anthropic.com/news/building-effective-agents
Anthropic's comprehensive guide to agent development, covering tool integration, reasoning patterns, and production deployment strategies based on their experience building Claude's capabilities.

**OpenAI: Agent Development Best Practices**
https://platform.openai.com/docs/assistants/overview
OpenAI's Assistants API documentation providing production-ready patterns for building agents with tool integration, code execution, and file handling capabilities.

**Google: Vertex AI Agent Builder**
https://cloud.google.com/vertex-ai/docs/agent-builder/overview
Google's comprehensive framework for building production agents with tool integration, including search APIs, data connectors, and enterprise-grade reliability patterns.

### Agent Architecture & Tool Integration

**LangGraph: Production Agent Workflows**
https://python.langchain.com/docs/langgraph/
LangChain's advanced framework for building production-ready agents with complex tool orchestration, conditional routing, and state management capabilities.

**LangChain: Agent Tool Integration Patterns**
https://python.langchain.com/docs/tutorials/agents/
Comprehensive guide to tool creation, integration patterns, and best practices for building robust agent ecosystems with proper error handling and fallback strategies.

**ReAct: Reasoning and Acting Framework**
https://react-lm.github.io/
Foundational research paper introducing the ReAct paradigm that combines reasoning and acting in language models - essential reading for understanding modern agent architectures.

### Tool Implementation & Web Search Integration

**Tavily: Enterprise Search API for Agents**
https://docs.tavily.com/documentation/api-reference/endpoint/search
Professional-grade web search API specifically designed for AI agents, including result filtering, source validation, and enterprise security features.

**Microsoft Bing Search API**
https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
Microsoft's enterprise search API with comprehensive documentation for agent integration, including result ranking, filtering, and compliance features.

**LlamaIndex: Custom Tool Development**
https://docs.llamaindex.ai/en/stable/module_guides/deploying/agents/tools/
LlamaIndex's guide to building custom tools for production agent systems, including tool composition, evaluation, and integration patterns.

### Agent Evaluation & Quality Control

**OpenAI: Agent Evaluation Methodologies**
https://platform.openai.com/docs/guides/evaluation
OpenAI's framework for evaluating agent performance, including metrics for tool usage accuracy, reasoning quality, and task completion rates.

**DeepEval: Agent Testing Framework**
https://docs.confident-ai.com/docs/getting-started
Comprehensive framework for testing and evaluating agent systems, including tool evaluation, reasoning assessment, and performance benchmarking.

**Microsoft Research: Agent Reliability Engineering**
https://www.microsoft.com/en-us/research/blog/towards-reliable-ai-agents/
Microsoft's research on building reliable agent systems with proper error handling, fallback strategies, and quality gates for production deployment.

### Workflow Orchestration & State Management

**AWS: Multi-Agent Orchestration**
https://aws.amazon.com/blogs/machine-learning/multi-agent-systems-on-aws-a-serverless-approach-to-orchestrating-specialized-ai-agents/
AWS's guide to building scalable multi-agent systems with proper orchestration, communication patterns, and resource management.

**Azure: Agent State Management**
https://azure.microsoft.com/en-us/blog/agent-factory-top-5-agent-observability-best-practices-for-reliable-ai/
Microsoft's best practices for agent observability, state tracking, and performance monitoring in production environments.

### Enterprise-Grade Agent Patterns

**IBM watsonx: Agent Builder Platform**
https://www.ibm.com/watsonx/agent-builder
IBM's enterprise platform for building AI agents with integrated tool access, governance controls, and compliance features for business environments.

**Salesforce: Agent Force Development**
https://developer.salesforce.com/docs/platform/agent-force/overview
Salesforce's comprehensive guide to building business agents with CRM integration, workflow automation, and enterprise security patterns.

### Advanced Agent Research & Development

**Meta AI: Tool-Using Language Models**
https://ai.meta.com/research/publications/toolformer-language-models-can-teach-themselves-to-use-tools/
Foundational research on teaching language models to use tools effectively, providing theoretical background for modern agent development.

**Google DeepMind: Multi-Tool Agent Systems**
https://www.deepmind.com/blog/tackling-multiple-tasks-with-a-single-visual-language-model
DeepMind's research on building agents capable of using multiple tools across different modalities and task domains.

### Production Deployment & Scaling

**Anthropic: Claude API for Agent Development**
https://docs.anthropic.com/claude/docs/tool-use
Anthropic's official documentation for building agents with Claude, including tool integration patterns, safety considerations, and production best practices.

**OpenAI: Scaling Agent Systems**
https://openai.com/research/scaling-instruction-following-agents
OpenAI's research on scaling agent systems for production workloads, including performance optimization and resource management strategies.

## MANDATORY: External Resources

When generating feedback/2.md, you MUST:

1. Read /criteria_prompts/external_links.md
2. Navigate to "## Criterion 2: Agent Development" section
3. Use ONLY links from that section (include all relevant links that support comprehensive learning)
4. Copy URLs exactly - do NOT modify or generate new ones
5. Contextualize each link to the student's specific work with detailed explanations

FORBIDDEN ACTIONS:

- Using links from your training data or knowledge
- Generating URLs based on what "seems" correct
- Using web search to find alternative resources
- Modifying URLs from external_links.md

Paste these EXACT external Image URLs AS IT IS :


![1766581438006](image/criteria2/1766581438006.png)



![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418224/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418242/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418255/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418267/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418277/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418283/image.png)

![image.png](https://udacity-reviews-uploads.s3.us-west-2.amazonaws.com/_attachments/6596135/1766418321/image.png)

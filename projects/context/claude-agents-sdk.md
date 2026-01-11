
Cognitive Architectures and the Claude Agent SDK: A Technical Treatise on In-Process MCP, Hierarchical Agency, and Procedural Skills
1. The Epistemology of Agentic Systems and the Claude Runtime
The transition from generative artificial intelligence models to autonomous agentic systems represents a fundamental reimagining of software interaction paradigms. Where traditional Large Language Models (LLMs) operate as stateless inference engines—accepting text and returning probabilities—agentic systems function as cognitive runtimes capable of maintaining state, executing reasoning loops, and interacting with deterministic environments. The Claude Agent SDK, developed by Anthropic, serves as a canonical implementation of this shift, providing the necessary infrastructure to operationalize the "Agent Loop"—the recursive process of observation, thought, action, and evaluation.   

This report provides an exhaustive technical analysis of the Claude Agent SDK, specifically focusing on its most sophisticated architectural primitives: In-Process Model Context Protocol (MCP) servers, hierarchical sub-agent orchestration, and the skills.md procedural knowledge framework. These components, when synthesized, allow for the construction of resilient, high-performance systems that transcend the limitations of brittle prompt engineering.

1.1 The Agent Loop as a Runtime Primitive
At the nucleus of the Claude Agent SDK lies the abstraction of the agent loop. In the lower-level Client SDK (e.g., the standard anthropic Python package), the developer is responsible for the manual orchestration of this loop. The model outputs a tool_use stop reason; the developer’s code must catch this, parse the tool name and arguments, execute the corresponding function in the host environment, and inject the result back into the context window. This imperative approach, while flexible, introduces significant boilerplate and cognitive overhead, often leading to fragile implementations of error handling and state management.   

The Agent SDK inverts this control flow. By encapsulating the loop within the query function and the ClaudeSDKClient class, the SDK transforms the agent from a passive responder into an active runtime entity. The SDK manages the "OODA loop" (Observe-Orient-Decide-Act) internally. When a user issues a command, the SDK does not merely send a prompt; it initiates an asynchronous runtime environment built upon anyio in Python or event loops in TypeScript, enabling non-blocking concurrency.   

This runtime environment is responsible for three critical functions:

Context persistence: Managing the sliding window of tokens and conversation history across multiple turns using session identifiers.   

Tool routing: Automatically dispatching model intent to the appropriate execution handler, whether that be a local file system operation or a complex call to an in-process MCP server.

Recursive reasoning: Handling the internal monologue of the agent as it breaks down complex tasks, executes intermediate steps, and self-corrects based on tool feedback.

1.2 The ClaudeAgentOptions Configuration Plane
The behavior of the agent runtime is strictly governed by the ClaudeAgentOptions configuration object. This object acts as the control plane for the agent's cognitive capabilities and environmental constraints. Unlike simple API parameters, ClaudeAgentOptions defines the architectural boundaries of the agent instance.   

The configuration parameters available in ClaudeAgentOptions reveal the depth of the SDK's design:

Parameter	Type	Architectural Implication
model	str	Determines the inference engine (e.g., claude-3-5-sonnet). This selection dictates the reasoning capacity and token cost of the agent.
allowed_tools	list[str]	
Implements the Principle of Least Privilege. By explicitly whitelisting tools, developers prevent "tool injection" where an agent might be tricked into using a dangerous capability like Bash or FileWrite.

system_prompt	str | dict	
Defines the agent's persona and foundational constraints. The SDK supports merging custom prompts with presets like claude_code, allowing for inheritance of Anthropic’s optimized coding behaviors.

mcp_servers	dict	
Configures the connection to Model Context Protocol servers. This is the primary interface for extending the agent's capabilities with custom tools and data sources.

agents	dict	
Defines the registry of available sub-agents. This dictionary maps agent names to AgentDefinition objects, enabling hierarchical delegation of tasks.

setting_sources	list	
Controls the ingestion of environmental configuration, specifically governing whether the agent should scan for CLAUDE.md context files or skills.md definition directories in the user or project scope.

  
The interaction between these parameters is complex. For instance, enabling setting_sources=["project"] without properly configuring allowed_tools to include file system access creates a runtime conflict where the agent knows where to look for settings but lacks the permission to read them. Mastery of ClaudeAgentOptions is therefore the first step in robust agent engineering.

2. The Model Context Protocol: Architecture of In-Process Servers
The Model Context Protocol (MCP) serves as the universal interface layer between the stochastic world of LLMs and the deterministic world of systems and data. While the protocol was initially popularized as a mechanism for connecting agents to external services via standard input/output (stdio) or HTTP/SSE transports, the Claude Agent SDK introduces a radical optimization: In-Process MCP Servers.   

2.1 The Latency and State Problem in Traditional MCP
In a standard "stdio" MCP architecture, the agent and the tool server run as separate processes. Communication occurs via JSON-RPC messages serialized over pipes.   

Serialization Overhead: Every tool call requires serializing arguments to JSON, transmitting them across the process boundary, deserializing them in the tool server, executing the logic, and repeating the serialization process for the result. For high-frequency tool use (e.g., a "grep" tool searching thousands of lines), this latency accumulates.

State Isolation: The tool server and the agent share no memory. If the agent calculates a complex Python object (like a DataFrame or a database connection pool), it cannot pass this object to the tool server. It must pass a reference or serialize the data, which is often impossible for active network connections.

Deployment Complexity: Operations teams must manage the lifecycle of multiple processes. If the agent process dies, the tool process might become an orphan unless rigorous signal handling is implemented.

2.2 In-Process Architecture: Memory Convergence
In-Process MCP servers solve these structural inefficiencies by hosting the MCP server instance directly within the memory space and event loop of the agent application. This is not merely a deployment detail; it changes the fundamental capabilities of the agent.   

In this architecture, the "transport" layer is effectively bypassed. When the agent decides to call a tool, the SDK runtime performs a direct asynchronous function call to the Python or TypeScript method defined in the server.

Key Architectural Advantages:

Zero-Latency Execution: The elimination of IPC (Inter-Process Communication) means tool execution speed is limited only by the execution time of the code itself.

Shared Application State: Tools defined in an in-process server can access global variables, singleton services, and active memory structures of the host application. An agent can receive a user request via an API, pass the active Request object to a tool, and have the tool modify the response directly.   

Simplified Debugging: Developers can set breakpoints within the tool code and step through execution seamlessly from the agent loop, a task that is notoriously difficult with stdio-based external processes.

2.3 Implementing In-Process Servers in Python
The implementation of in-process servers in the Python SDK leverages the create_sdk_mcp_server factory function and the @tool decorator.   

2.3.1 Defining Stateful Tools
The @tool decorator transforms a standard Python async function into an MCP-compliant tool definition. It automatically extracts the function signature to generate the JSON schema required by the LLM to understand the tool's inputs.

Consider a scenario where an agent needs to manipulate a shared data cache that exists only in memory.

Python
from claude_agent_sdk import tool, create_sdk_mcp_server, ClaudeAgentOptions, query
from typing import Any, Dict

# Global application state - inaccessible to external processes
IN_MEMORY_CACHE: Dict[str, Any] = {}

@tool(
    name="cache_store",
    description="Stores a value in the high-speed in-memory application cache.",
    input_schema={
        "key": str,
        "value": str,
        "ttl_seconds": int
    }
)
async def cache_store(args: dict[str, Any]) -> dict[str, Any]:
    """
    Directly manipulates the global dictionary.
    No serialization of the 'store' is required.
    """
    key = args["key"]
    value = args["value"]
    IN_MEMORY_CACHE[key] = value
    
    # Return structure must match MCP ToolResult spec
    return {
        "content":
    }

@tool(
    name="cache_retrieve",
    description="Retrieves a value from the in-memory cache.",
    input_schema={"key": str}
)
async def cache_retrieve(args: dict[str, Any]) -> dict[str, Any]:
    key = args["key"]
    val = IN_MEMORY_CACHE.get(key, "NOT_FOUND")
    return {
        "content": [
            {"type": "text", "text": str(val)}
        ]
    }
2.3.2 Server Initialization and Registration
The create_sdk_mcp_server function aggregates these decorated functions into a cohesive server object. This object handles the internal routing and schema generation.   

Python
# Create the server instance
# This object is a fully compliant MCP server running in RAM
memory_server = create_sdk_mcp_server(
    name="internal-memory-ops",
    version="1.0.0",
    tools=[cache_store, cache_retrieve]
)

# Configuration
options = ClaudeAgentOptions(
    # The key 'memory' becomes the namespace: mcp__memory__cache_store
    mcp_servers={"memory": memory_server},
    allowed_tools=["mcp__memory__cache_store", "mcp__memory__cache_retrieve"]
)
It is crucial to note the naming convention. The SDK typically namespaces tools to avoid collisions. A tool named cache_store inside a server registered under the key memory effectively becomes mcp__memory__cache_store in the allowed_tools list. Failure to use this fully qualified name in the permissions list is a common source of ToolPermissionError.   

2.4 TypeScript Implementation and Routing Challenges
The TypeScript ecosystem for the Claude Agent SDK mirrors the Python approach but relies on the @modelcontextprotocol/sdk for type definitions. However, integration has historically been more complex due to strict separation between the CLI runner and the SDK process.   

In TypeScript, an in-process server is often defined by passing the server instance capability directly.

TypeScript
import { query } from "@anthropic-ai/claude-agent-sdk";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

// Create a standard MCP server instance
const resourceServer = new McpServer({
  name: "LocalResources",
  version: "1.0.0"
});

// Register tool with Zod schema for type safety
resourceServer.tool(
  "get_app_metrics",
  { category: z.string() },
  async ({ category }) => {
    // Direct access to application memory
    return { content: [{ type: "text", text: `Metrics for ${category}: OK` }] };
  }
);

// Integration in Options
// Note: Implementation details vary by SDK version regarding direct object passing
// vs adapter patterns.
const options = {
  mcpServers: {
    "metrics": resourceServer 
  },
  allowedTools: ["mcp__metrics__get_app_metrics"]
};
Addressing Routing Bugs: Research indicates a known issue in certain versions of the TypeScript SDK (specifically on macOS) where in-process MCP servers fail to register correctly with the underlying Claude Code CLI, leading to tools being invisible to the model. This is often due to the IPC bridge between the Node.js process hosting the SDK and the Python-based Claude CLI (if the CLI wrapper is used).   

Mitigation Strategy: To resolve this, developers must ensure that the environment variables identifying the SDK session are correctly propagated. Additionally, using the "Direct SDK" mode (if available in the version) rather than the CLI-wrapper mode ensures that the Node.js process handles the tool execution directly without routing through the external CLI binary.

2.5 Dynamic Tool Registration
A distinct capability of in-process servers is dynamic tool registration. Because the server is a mutable object in memory, the application can add or remove tools at runtime based on the state of the conversation.   

Consider a secure agent that requires authentication. Initially, only a login tool is registered.

Python
async def login(args):
    if verify_creds(args):
        # Dynamically inject the sensitive tool
        admin_server.registry.register_tool(delete_database_tool)
        return "Login successful. Admin tools unlocked."
    return "Login failed."
This pattern of Progressive Tool Disclosure is highly effective for security. It ensures that the model cannot even hallucinate a call to a sensitive tool until the strict logic of the application code has verified the necessary preconditions. This is significantly harder to achieve with external stdio servers, which typically load their tool manifests once at startup.

3. Hierarchical Cognition: Sub-Agent Orchestration
As agentic workflows increase in complexity, the "single agent, many tools" architecture begins to fail. A single context window becomes polluted with irrelevant information, and the system prompt becomes a contradictory mess of instructions. The Claude Agent SDK addresses this through Sub-Agents, a hierarchical architecture that allows a main Orchestrator agent to delegate tasks to specialized Worker agents.   

3.1 The Theoretical Basis of Sub-Agency
The sub-agent pattern is predicated on three principles:

Context Hygiene: A sub-agent starts with a fresh, empty context window (save for its system prompt). It does not need to process the thousands of tokens of conversation history that led to its invocation. This reduces cost and increases focus.   

Specialization of Function: By restricting a sub-agent to a specific domain (e.g., "SQL Expert" vs. "Frontend Designer"), developers can write highly specific system prompts that would be conflicting if combined in a single agent.

Fault Isolation: If a sub-agent gets stuck in a loop or hallucinates, the Orchestrator can terminate the task, receive the failure signal, and decide on a mitigation strategy (e.g., retry with a different prompt) without the main conversation entering an unrecoverable state.

3.2 The Task Tool: The Mechanism of Delegation
The SDK does not introduce a new API call for delegation; instead, it utilizes the Task tool. This built-in tool is the bridge between the Orchestrator and the Sub-Agent.   

When the Orchestrator invokes the Task tool, the SDK runtime:

Suspends the Orchestrator's execution loop.

Instantiates the requested Sub-Agent based on the subagent_type.

Injects the prompt provided by the Orchestrator into the Sub-Agent's context.

Executes the Sub-Agent's loop until completion.

Returns the final output of the Sub-Agent as the result of the tool call to the Orchestrator.

Resumes the Orchestrator.

3.3 Defining Agents with AgentDefinition
The blueprint for a sub-agent is the AgentDefinition class (Python) or interface (TypeScript).   

The Structure of Agency:

Python
@dataclass
class AgentDefinition:
    """
    Defines the cognitive boundaries of a sub-agent.
    """
    description: str  # The "Trigger" for the Orchestrator
    prompt: str       # The "Brain" of the Sub-Agent
    tools: list[str] | None = None  # The "Hands"
    model: Literal["sonnet", "opus", "haiku", "inherit"] | None = None
Description as Router: The description field is arguably the most critical. It is not visible to the Sub-Agent itself; rather, it is injected into the Orchestrator's system prompt. It serves as the semantic router. A description like "Use this agent for all database queries" explicitly instructs the Orchestrator when to reach for this specific tool.   

Model Selection: The model field allows for cost optimization. A "Summarizer" sub-agent might use haiku (fast, cheap), while the "Architect" orchestrator uses opus or sonnet (intelligent, expensive). This allows for Economic Routing within the agent architecture.   

3.4 Implementation Pattern: The recursive Research System
Below is a detailed implementation of a main agent that delegates code analysis to a specialized sub-agent.

Python
from claude_agent_sdk import ClaudeAgentOptions, AgentDefinition, query
import asyncio

# --- Define the Sub-Agent ---
# This agent is specialized: it can ONLY read files and run grep.
# It cannot edit files or run shell commands.
security_auditor = AgentDefinition(
    description="A specialized security auditor. Use this agent when the user asks to check code for vulnerabilities.",
    prompt="""You are a cynical security auditor. 
    You analyze code for: SQL Injection, XSS, and hardcoded credentials.
    You must cite the line numbers of any issues found.
    Be concise.""",
    tools=, # Minimal toolset for safety
    model="claude-3-5-sonnet-20241022"
)

# --- Define the Orchestrator Options ---
options = ClaudeAgentOptions(
    # Register the sub-agent
    agents={"auditor": security_auditor},
    
    # The Orchestrator needs the 'Task' tool to invoke sub-agents.
    # It also needs 'Bash' to perhaps fix the issues later.
    allowed_tools=,
    
    system_prompt="""You are the Lead Developer. 
    You coordinate security reviews but delegate the actual auditing to the 'auditor' agent.
    Once the auditor returns findings, YOU are responsible for fixing them."""
)

async def run_session():
    user_request = "Audit the auth.py file for security holes and fix them."
    
    # Streaming query loop
    async for message in query(user_request, options=options):
        # We can observe the Orchestrator calling the 'Task' tool
        if hasattr(message, 'tool_use') and message.tool_use.name == 'Task':
            print(f"[Orchestrator] Delegating to: {message.tool_use.input['subagent_type']}")
        
        print(message)

if __name__ == "__main__":
    asyncio.run(run_session())
Internal Concurrency and the UH1 Scheduler: Advanced documentation suggests that the Task tool mechanism in Claude Code is supported by an internal concurrency scheduler (referenced as UH1 in architecture diagrams). While the SDK interface appears synchronous (Orchestrator waits for Sub-Agent), the underlying architecture supports parallel execution. If an Orchestrator issues a Task call with multiple sub-tasks (if the API permits a list) or generates multiple Task tool calls in a single turn (parallel tool use), the runtime can spin up multiple Sub-Agent instances concurrently. This is vital for tasks like "Research these 5 companies," where 5 sub-agents can browse the web in parallel, reducing total wall-clock time by 80%.   

4. Procedural Knowledge Engineering: The Skills Framework
While tools provide the capability to act (e.g., run_sql_query), they do not provide the knowledge of how to use those capabilities to solve complex business problems. Traditionally, this knowledge was stuffed into the System Prompt ("To fix a database lock, first run X, then run Y..."). This approach scales poorly.

Anthropic's Skills framework, centered around the SKILL.md file standard, provides a scalable mechanism for injecting Procedural Knowledge into agents.   

4.1 The SKILL.md Specification
A "Skill" is a structured directory containing instructions and resources. The heart of a skill is the SKILL.md file, which must adhere to a strict format.   

Directory Structure: .claude/skills/ └── git-conflict-resolver/ ├── SKILL.md # The instruction set ├── scripts/ # Helper scripts (e.g., specialized git commands) │ └── visual_merge.py └── examples/ # Few-shot examples └── merge_conflict.txt

The SKILL.md Content: The file must begin with YAML frontmatter. This metadata is the linchpin of the discovery mechanism.

name: git-conflict-resolver description: Use this skill when the user encounters a git merge conflict that requires intelligent resolution. allowed-tools:
Git Conflict Resolution Procedure
Prerequisities
Run git status to identify conflicted files.

Resolution Strategy
For each conflicted file:

Read the file markers (<<<<<<<, =======, >>>>>>>).

Analyze the 'ours' vs 'theirs' changes. 3....

4.2 The Mechanism of Progressive Disclosure
The Skills framework solves the context window limitation problem through Progressive Disclosure.   

Discovery (Low Cost): When the agent initializes, it scans the .claude/skills directory. It reads only the YAML frontmatter (name and description). These short strings are added to the system prompt. This might consume only 50-100 tokens per skill, allowing an agent to be aware of hundreds of skills.

Triggering: When the user says, "I have a merge conflict," the agent's reasoning engine matches this intent to the git-conflict-resolver description.

Loading (High Fidelity): The agent decides to "activate" the skill. The SDK runtime then reads the full body of SKILL.md and injects it into the active context window.

Execution: The agent now possesses the detailed runbook and executes the steps.

This architecture mimics human memory: we have a broad index of what we know (Discovery), and we recall the specific details only when the task demands it (Loading).

4.3 Integrating Skills with the SDK
A critical finding in the research is that the SDK does not expose a programmatic add_skill() API. Unlike in-process MCP servers which are added via Python objects, Skills are strictly filesystem-based artifacts.   

To enable skills in the SDK, developers must configure the setting_sources in ClaudeAgentOptions.

Python
options = ClaudeAgentOptions(
    # This instructs the SDK to scan ~/.claude/skills (user) 
    # and./.claude/skills (project)
    setting_sources=["user", "project"],
    
    # The agent needs permission to read the skill files
    allowed_tools= 
)
Implications for Containerization: For agents running in Docker/Kubernetes, this dependency on setting_sources means that skills must be mounted as volumes or COPY'd into the container image at the specific paths expected by the SDK (typically ~/.claude/skills). Dynamic skill injection in a cloud environment therefore requires manipulating the container's file system before the agent process starts, a "Configuration-as-Code" approach distinct from the "Infrastructure-as-Code" approach of MCP.

5. Synthesis: The Enterprise Architect Agent (Case Study)
To demonstrate the power of combining In-Process MCP, Sub-Agents, and Skills, we detail the architecture of a hypothetical "Enterprise Cloud Architect" agent designed to manage AWS infrastructure.

5.1 Architecture Overview
Goal: autonomously identify unencrypted S3 buckets and remediate them.

Components:

Orchestrator Agent: "Cloud Manager".

In-Process MCP Server: "State Tracker" (Maintains a list of scanned accounts in memory).

Sub-Agent: "Auditor" (Specialized in boto3 read operations).

Skill: s3-remediation.md (The standard operating procedure for encryption).

5.2 Implementation Strategy
Step 1: The In-Process State Server This server allows the Orchestrator to track which accounts have been scanned across multiple turns, surviving the statelessness of individual model calls.

Python
# state_server.py
scanned_accounts = set()

@tool("mark_scanned", "Records that an account has been audited", {"account_id": str})
async def mark_scanned(args):
    scanned_accounts.add(args["account_id"])
    return {"content":}

@tool("get_unscanned", "Returns list of pending accounts", {})
async def get_unscanned(args):
    # Logic to diff against a master list
    return {"content": [{"type": "text", "text": "['123456789', '987654321']"}]}
Step 2: The Auditor Sub-Agent We define an agent that has read-only access to AWS. We explicitly deny it the Bash tool to prevent it from executing CLI commands; it must use the AWS_Read MCP tool (assumed to be available).

Python
auditor_def = AgentDefinition(
    description="AWS Auditor. Checks resource configuration.",
    prompt="You are a read-only auditor. Report JSON configurations of S3 buckets.",
    tools= # Only read access
)
Step 3: The Remediation Skill Located at .claude/skills/s3-fix/SKILL.md:

YAML
---
name: s3-encryption-fix
description: Procedure for enabling AES-256 encryption on a bucket.
allowed-tools:
---
# Remediation Steps
1. Verify bucket exists.
2. Apply PutBucketEncryption with Rule: ApplyServerSideEncryptionByDefault...
Step 4: The Orchestration Loop The main agent's loop proceeds as follows:

Call get_unscanned (In-Process MCP) to find target.

Call Task(auditor) to inspect the bucket configuration.

Receive Report: "Bucket X is unencrypted."

Trigger Skill: The Orchestrator matches "unencrypted" to the s3-encryption-fix skill description.

Load Skill: The specific boto3 commands for remediation are loaded.

Execute: The Orchestrator (who has write permissions, unlike the Auditor) executes the fix commands derived from the skill.

Call mark_scanned (In-Process MCP) to close the loop.

This architecture demonstrates Separation of Concerns:

State is handled by Code (MCP).

Discovery is handled by the Sub-Agent (Auditor).

Knowledge is handled by Files (Skills).

Execution is handled by the Orchestrator.

6. Security, Governance, and Production Engineering
Deploying agents with this level of autonomy requires rigorous governance.

6.1 Permission Modes and Guardrails
The ClaudeAgentOptions includes a permission_mode setting.   

ask (Default): The agent halts before every tool use (especially Bash or Edit) to request user confirmation. This is safe but breaks autonomy.

acceptEdits: Allows file modifications without confirmation but prompts for shell commands.

allow: Full autonomy.

Recommendation: For the "Enterprise Architect" agent described above, a hybrid approach is best. The Auditor sub-agent should run in allow mode (read-only tools are safe). The Orchestrator should run in allow mode for MCP tools but ask mode for the final Remediation step, ensuring a human verifies the encryption change before application.

6.2 The Cost of Agency: Token Economics
Developers must account for the Context Tax.

Skills: Each skill adds ~50-100 tokens to the system prompt permanently (for the header). 100 skills = 5,000 to 10,000 tokens of overhead per request.

Sub-Agents: While they prune context, the input to the sub-agent (the prompt passed via Task) and the output (the result string) still consume tokens in the Orchestrator's window.

Optimization: Use the model parameter in AgentDefinition to assign cheaper models (e.g., claude-3-haiku) to verbose sub-tasks like log parsing, reserving opus or sonnet for the high-level orchestration logic.

7. Conclusion
The Claude Agent SDK moves the industry beyond the era of "Chatbots" into the era of "Cognitive Runtimes." By providing a unified substrate for In-Process MCP (Action), Sub-Agents (Delegation), and Skills (Knowledge), it enables the engineering of systems that are stateful, scalable, and secure.

For the architect, the path forward is clear: move logic out of system prompts and into MCP servers; move workflows out of rigid code and into adaptive Skills; and move complexity out of monolithic agents and into hierarchical teams of sub-agents. This modular approach is not merely a convenience—it is the requisite foundation for building the next generation of enterprise AI.


github.com
anthropics/claude-agent-sdk-typescript - GitHub
Opens in a new window

platform.claude.com
Agent SDK overview - Claude Docs
Opens in a new window

platform.claude.com
Agent SDK reference - Python - Claude Docs
Opens in a new window

blog.getbind.co
How to Create Agents with Claude Agents SDK - Bind AI IDE
Opens in a new window

redreamality.com
Claude Agent SDK (Python) Learning Guide
Opens in a new window

blog.gopenai.com
The Claude Developer Guide Agent SDK Reference - GoPenAI
Opens in a new window

github.com
claude-agent-sdk-python/src/claude_agent_sdk/types.py at main - GitHub
Opens in a new window

tessl.io
tessl/pypi-claude-agent-sdk@0.1.x - Registry
Opens in a new window

blog.promptlayer.com
Building Agents with Claude Code's SDK - PromptLayer Blog
Opens in a new window

reddit.com
Claude Agent SDK system prompt best practices : r/ClaudeCode - Reddit
Opens in a new window

platform.claude.com
MCP in the SDK - Claude Docs
Opens in a new window

platform.claude.com
Agent Skills in the SDK - Claude Docs
Opens in a new window

anthropic.com
Introducing the Model Context Protocol - Anthropic
Opens in a new window

hexdocs.pm
MCP Tools Guide — claude_agent_sdk v0.7.3 - Hexdocs
Opens in a new window

github.com
anthropics/claude-agent-sdk-python - GitHub
Opens in a new window

hexdocs.pm
Changelog — claude_agent_sdk v0.6.8 - Hexdocs
Opens in a new window

github.com
[BUG] In-process MCP servers bug in Claude Code TypeScript SDK · Issue #7279 - GitHub
Opens in a new window

github.com
The In Process MCP is not working at all · Issue #147 · anthropics/claude-agent-sdk-python
Opens in a new window

github.com
haasonsaas/agent-harness: Unified harness for hot-swapping between OpenAI Agents SDK and Anthropic Claude Agent SDK with shared tool registry - GitHub
Opens in a new window

anthropic.com
Building agents with the Claude Agent SDK - Anthropic
Opens in a new window

platform.claude.com
Subagents in the SDK - Claude Docs
Opens in a new window

platform.claude.com
Todo Lists - Claude Docs
Opens in a new window

reddit.com
About Claude Code's Task Tool (SubAgent Design) : r/AI_Agents - Reddit
Opens in a new window

pkg.go.dev
claude package - github.com/clsx524/claude-agent-sdk-go - Go Packages
Opens in a new window

eesel.ai
Skills.md vs. Agents.md: What's the difference in 2025? - eesel AI
Opens in a new window

anthropic.com
Equipping agents for the real world with Agent Skills - Anthropic
Opens in a new window

code.claude.com
Agent Skills - Claude Code Docs
Opens in a new window

reddit.com
The Busy Person's Intro to Claude Skills (a feature that might be bigger than MCP) - Reddit
Opens in a new window

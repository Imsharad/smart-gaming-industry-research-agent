<rubric>
    <title>Rubric</title>
    <description>Use this project rubric to understand and assess the project criteria.</description>

    <category name="Data Setup and Knowledge Base Preparation">
        <criterion title="Set up the database and knowledge base infrastructure">
            <summary>Successfully set up the database infrastructure and populate the knowledge base with comprehensive support articles.</summary>
            <requirements>
                <requirement>Successfully run the database management notebook to initialize the databases</requirement>
                <requirement>Database contains the required tables (Account, User, Ticket, TicketMetadata, TicketMessage, Knowledge)</requirement>
                <requirement>Knowledge base includes at least 10 additional support articles beyond the provided 4</requirement>
                <requirement>New articles cover different categories (technical issues, billing, account management, etc.)</requirement>
                <requirement>All database operations complete without errors</requirement>
                <requirement>Can demonstrate successful data retrieval from the database</requirement>
            </requirements>
        </criterion>
    </category>

    <category name="Multi-Agent Architecture with LangGraph">
        <criterion title="Design and document multi-agent architecture">
            <summary>Design and document a comprehensive multi-agent architecture before implementation.</summary>
            <requirements>
                <requirement>Submit a detailed architecture design document in Markdown format</requirement>
                <requirement>Include a visual diagram showing the multi-agent architecture (can use ASCII art, Mermaid, or similar)</requirement>
                <requirement>Document the role and responsibilities of each agent in the system</requirement>
                <requirement>Explain the flow of information and decision-making between agents</requirement>
                <requirement>Describe how the system handles different types of inputs and expected outputs</requirement>
                <requirement>Architecture should be based on one of the standard patterns (Supervisor, Hierarchical, Network, etc.)</requirement>
            </requirements>
        </criterion>
        <criterion title="Implement the designed multi-agent architecture using LangGraph">
            <summary>Implement the designed multi-agent architecture using LangGraph with specialized agents for different tasks.</summary>
            <requirements>
                <requirement>Implementation matches the documented architecture design</requirement>
                <requirement>Project includes at least 4 specialized agents</requirement>
                <requirement>Each agent has a clearly defined role and responsibility as documented</requirement>
                <requirement>Agents are properly connected using LangGraph's graph structure</requirement>
                <requirement>Code demonstrates proper agent state management and message passing</requirement>
            </requirements>
        </criterion>
        <criterion title="Implement task routing and role assignment across agents">
            <summary>Implement intelligent task routing and role assignment across agents based on ticket characteristics.</summary>
            <requirements>
                <requirement>System can classify incoming tickets and route them to appropriate agents</requirement>
                <requirement>Routing logic considers ticket content and metadata (e.g. date, urgency, complexity...)</requirement>
                <requirement>At least one routing decision is made based on ticket classification</requirement>
                <requirement>Code includes routing logic that can be demonstrated with sample tickets</requirement>
                <requirement>Routing follows the architecture design principles</requirement>
            </requirements>
        </criterion>
    </category>

    <category name="Knowledge Retrieval and Tool Usage">
        <criterion title="Implement knowledge-based response system with escalation logic">
            <summary>Implement a knowledge retrieval system that provides responses based on articles and escalates when no relevant knowledge is found.</summary>
            <requirements>
                <requirement>System retrieves relevant knowledge base articles based on ticket content</requirement>
                <requirement>All responses are based on the content of knowledge base articles</requirement>
                <requirement>System can demonstrate retrieval of appropriate articles for different ticket types</requirement>
                <requirement>Implements escalation logic when no relevant knowledge base article is found</requirement>
                <requirement>System includes confidence scoring to determine when to escalate</requirement>
                <requirement>Can demonstrate both successful knowledge retrieval and escalation scenarios</requirement>
            </requirements>
        </criterion>
        <criterion title="Implement support operation tools with database abstraction">
            <summary>Create and implement at least 2 tools that perform support operations with proper database abstraction.</summary>
            <requirements>
                <requirement>Implement at least 2 functional tools for support operations (e.g., account lookup, subscription management, refund processing)</requirement>
                <requirement>Tools abstract the interaction with the CultPass database</requirement>
                <requirement>Tools can be invoked by agents and return structured responses</requirement>
                <requirement>Tools include proper error handling and validation</requirement>
                <requirement>Can demonstrate tool usage with sample operations</requirement>
                <requirement>Tools are properly integrated into the agent workflow</requirement>
            </requirements>
        </criterion>
    </category>

    <category name="Memory and State Management">
        <criterion title="Persist customer interaction history to enable personalized, context-aware support">
            <summary>Implement persistent memory to store and retrieve customer interaction history.</summary>
            <requirements>
                <requirement>System stores conversation history in a persistent database</requirement>
                <requirement>Can retrieve previous interactions for returning customers</requirement>
                <requirement>Uses historical context to provide personalized responses</requirement>
                <requirement>Demonstrates memory retrieval with sample customer interactions</requirement>
            </requirements>
        </criterion>
        <criterion title="Implement state, session and long-term memory in agent workflows">
            <summary>Implement different types of memory in agent workflows.</summary>
            <requirements>
                <requirement>Agents maintain state during multi-step interactions in one execution.</requirement>
                <requirement>Based on the appropriate scope (like thread_id or session_id), it's possible to inspect the workflow (e.g. messages, tool_usage)</requirement>
                <requirement>Short-term memory is used as context to keep conversation running during the same session</requirement>
                <requirement>Long-term memory is used to store resolved issues and customer preferences accross different sessions</requirement>
                <requirement>Memory is properly integrated into agent decision-making</requirement>
            </requirements>
        </criterion>
    </category>

    <category name="Integration and Testing">
        <criterion title="Demonstrate end-to-end ticket processing workflow with proper logging">
            <summary>Demonstrate a complete end-to-end workflow for processing customer support tickets.</summary>
            <requirements>
                <requirement>System can process a ticket from initial submission to resolution/escalation</requirement>
                <requirement>Workflow includes classification, routing, knowledge retrieval, tool usage, resolution attempt, and final action</requirement>
                <requirement>Demonstrates the complete flow with sample tickets</requirement>
                <requirement>Includes proper error handling and edge cases</requirement>
                <requirement>System logs agent decisions, routing choices, tool usage and outcomes</requirement>
                <requirement>All logs are structured and searchable</requirement>
                <requirement>Shows both successful resolution and escalation scenarios</requirement>
                <requirement>Demonstrates tool integration in the workflow</requirement>
            </requirements>
        </criterion>
    </category>

    <suggestions_for_distinction>
        <title>Suggestions to Make Your Project Stand Out</title>
        <suggestion>Advanced Knowledge Retrieval: Implement sophisticated semantic search using embeddings or vector databases for better article matching</suggestion>
        <suggestion>Multi-Channel Support: Extend the system to handle tickets from different channels (email, chat, social media)</suggestion>
        <suggestion>Sentiment Analysis: Add sentiment analysis to prioritize urgent or frustrated customer tickets</suggestion>
        <suggestion>A/B Testing Framework: Implement a framework to test different routing strategies and measure their effectiveness</suggestion>
        <suggestion>MCP: Create specialized tools for common support operations (refunds, account modifications, etc.) using FastMCP</suggestion>
    </suggestions_for_distinction>
</rubric>

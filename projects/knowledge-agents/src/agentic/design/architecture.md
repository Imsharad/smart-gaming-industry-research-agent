# UDA-Hub Multi-Agent Architecture Design

## Overview

UDA-Hub is a Universal Decision Agent designed as an intelligent customer support automation system. The system implements a **Supervisor-based multi-agent architecture** using LangGraph, where specialized agents collaborate to resolve customer support tickets.

## Architecture Pattern

The system follows a **Hierarchical Supervisor Pattern** where:
- A central supervisor orchestrates the workflow.
- Specialized agents handle specific tasks (classification, resolution, escalation).
- Decision points route tickets based on classification, confidence scores, and supervisor decisions.
- A comprehensive memory system maintains both short-term (session) and long-term (persistent) context.

## Visual Architecture Diagram

This diagram illustrates the complete 4-agent workflow as implemented in `enhanced_workflow.py`.

```mermaid
graph TD
    A[Customer Ticket Input] --> B(Initialize Workflow)
    B --> C(Classifier Agent)
    C --> D(Supervisor Agent)
    D --> E{Immediate Escalation?}
    E -->|Yes| F(Escalation Agent)
    E -->|No| G(Retrieve Knowledge)
    G --> H(Execute Tools)
    H --> I(Resolver Agent)
    I --> J{Resolution Confidence < 0.5 OR Escalate Flag?}
    J -->|Yes| F
    J -->|No| K(Finalize & Store History)
    F --> K
    K --> L[Customer Response]

    subgraph "Memory Layer"
        M[Short-term Memory<br/>(LangGraph State)]
        N[Long-term Memory<br/>(Customer History & Preferences DB)]
    end

    subgraph "Data Layer"
        O[(CultPass DB<br/>External)]
        P[(UDA-Hub DB<br/>Core)]
        Q[(Knowledge Base<br/>14 Articles)]
    end

    C -.-> M
    I -.-> M
    K -.-> N
    H -- "Account/Subscription Tools" --> O
    H -- "Knowledge Tool" --> Q
    N -- "Read History" --> B

    style B fill:#e0f7fa,stroke:#00796b
    style D fill:#e1f5fe,stroke:#0277bd
    style F fill:#fff3e0,stroke:#ef6c00
    style I fill:#f1f8e9,stroke:#558b2f
    style L fill:#e8f5e9,stroke:#2e7d32
```

## System Components

### 1. Core Workflow Engine
- **Technology**: LangGraph StateGraph
- **Purpose**: Orchestrates agent interactions and manages state.
- **Location**: `agentic/enhanced_workflow.py` (primary), `agentic/workflow.py` (original 2-agent version for comparison).

### 2. Agent Architecture

#### Implemented Agents (4/4)
1.  **Classifier Agent**
    -   **Role**: Analyzes and classifies incoming support tickets.
    -   **Responsibilities**: Extracts key entities, determines category and priority, suggests tools, and provides a confidence score.
    -   **Location**: `agentic/agents/classifier_agent.py`

2.  **Supervisor Agent**
    -   **Role**: Central coordinator and high-level decision-maker.
    -   **Responsibilities**: Makes initial routing decisions (continue vs. escalate), monitors workflow, and ensures efficient resource allocation.
    -   **Location**: `agentic/agents/supervisor_agent.py`

3.  **Resolver Agent**
    -   **Role**: Generates solutions and customer-facing responses.
    -   **Responsibilities**: Synthesizes information from knowledge base and tools, generates responses, and assesses resolution confidence.
    -   **Location**: `agentic/agents/resolver_agent.py`

4.  **Escalation Agent**
    -   **Role**: Manages cases that require human intervention.
    -   **Responsibilities**: Prepares comprehensive summaries for human agents, analyzes escalation patterns, and generates detailed handoff documentation.
    -   **Location**: `agentic/agents/escalation_agent.py`

### 3. Tool System
- **Account Lookup Tool**: Retrieves customer information from the CultPass database.
- **Subscription Management Tool**: Handles subscription-related operations (pause, cancel, upgrade).
- **Knowledge Retrieval Tool**: Searches the knowledge base for relevant articles.
- **Location**: `agentic/tools/`

### 4. Data Layer
- **External Database**: CultPass customer data (`data/external/cultpass.db`).
- **Core Database**: UDA-Hub application data, including logs and memory (`data/core/udahub.db`).
- **Knowledge Base**: 14 support articles covering diverse categories.

### 5. Memory Management
- **Short-term Memory**: LangGraph `MemorySaver` for session-level state persistence.
- **State Management**: `EnhancedAgentState` TypedDict for passing context through the workflow.
- **Long-term Memory**: A persistent memory system implemented in `agentic/memory_manager.py` that stores customer interaction history and preferences in the core database.

## Information Flow

### Primary Workflow (`enhanced_workflow.py`)
`Ticket Input` → `Initialize` → `Classify` → `Supervise` → `Retrieve Knowledge` → `Execute Tools` → `Resolve` → `Finalize`

### Decision Points
1.  **Supervisor Decision**: After classification, the Supervisor decides whether to proceed with resolution or escalate immediately.
2.  **Resolution Decision**: After the Resolver agent generates a response, the workflow decides whether to finalize the response or escalate to a human based on resolution confidence and agent flags.

## Input/Output Handling

### Supported Input Types
-   Natural language customer tickets.
-   Metadata (e.g., `user_id`, `session_id`).

### Expected Outputs
-   **Successful Resolution**: A structured, helpful response for the customer.
-   **Escalation**: A notification that the ticket has been escalated, along with a detailed summary prepared for a human agent.

---

*This architecture document reflects the final implementation of the UDA-Hub system, ensuring a scalable, intelligent, and reliable ticket resolution process.*

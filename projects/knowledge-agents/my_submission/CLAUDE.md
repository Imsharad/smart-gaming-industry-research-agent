# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

UDA-Hub is a LangGraph-powered multi-agent customer support system with 4 specialized agents (Classifier, Resolver, Supervisor, Escalation) that intelligently handles support tickets for CultPass. The system uses dual databases, comprehensive memory management, and sophisticated workflow orchestration.

## Essential Development Commands

### Environment Setup
```bash
# Install all dependencies with uv
uv sync

# Start Jupyter notebook server with correct environment
uv run jupyter notebook --no-browser --ip=127.0.0.1 --port=8888
```

### Database Setup (Required First Steps)
```bash
# 1. Setup external CultPass database
jupyter nbconvert --execute 01_external_db_setup.ipynb

# 2. Setup core UDA-Hub database  
jupyter nbconvert --execute 02_core_db_setup.ipynb
```

### Running the System
```bash
# Interactive notebook interface (recommended)
# Open 03_agentic_app.ipynb in Jupyter and run cells

# Direct Python execution
python -c "from agentic.enhanced_workflow import orchestrator; from utils import chat_interface; chat_interface(orchestrator, '1')"

# System validation
python test_system.py

# Comprehensive testing (rubric compliance)
python comprehensive_tests.py
```

## Architecture Overview

### Multi-Agent Structure
- **ClassifierAgent**: Categorizes tickets, extracts entities, suggests tools
- **ResolverAgent**: Generates responses, manages confidence-based escalation  
- **SupervisorAgent**: Central coordinator for workflow decisions
- **EscalationAgent**: Handles human handoffs with comprehensive context

### Dual Database Architecture
- **External DB** (`data/external/cultpass.db`): CultPass customer data (users, subscriptions, experiences, reservations)
- **Core DB** (`data/core/udahub.db`): UDA-Hub app data (tickets, knowledge base, interaction history, customer preferences)

### Workflow Engine
LangGraph StateGraph with conditional routing:
```
classify → retrieve_knowledge → execute_tools → resolve → [escalate|end]
```

Escalation triggers:
- Classification confidence < 0.3
- Resolution confidence < 0.5
- Tool execution failures

## Key Components

### Memory Management (`agentic/memory_manager.py`)
- **Short-term**: LangGraph MemorySaver for session persistence
- **Long-term**: Database-backed customer history and preferences
- **Decision Logging**: All agent decisions tracked with confidence scores

### Tools (Database Abstraction Layer)
- **AccountLookupTool**: Customer data retrieval from CultPass DB
- **KnowledgeRetrievalTool**: 15-article knowledge base search
- **SubscriptionManagementTool**: Subscription operations (pause/resume/cancel)

### State Management
`EnhancedAgentState` includes: messages, classification results, customer history, preferences, tool results, and personalized context.

## Development Guidelines

### File Structure Navigation
- **Agents**: `/agentic/agents/` - Individual agent implementations
- **Tools**: `/agentic/tools/` - Database abstraction and external integrations  
- **Workflow**: `/agentic/enhanced_workflow.py` - Main orchestration logic
- **Database Models**: `/data/models/` - SQLAlchemy ORM definitions
- **Design Docs**: `/agentic/design/` - Architecture documentation

### Working with Memory
- Customer preferences stored persistently across sessions
- All agent decisions logged for debugging and analytics
- Use `thread_id` for short-term session memory

### Database Operations
- Always use tools for database access (never direct SQL)
- Both databases must be initialized before development
- Connection pooling handled automatically by tools

### Testing Approach
- **Unit**: Individual agents and tools
- **Integration**: Full workflow scenarios
- **Edge Cases**: Error handling and fallback behaviors
- **Rubric**: All 7 project criteria systematically verified

### Common Patterns
- Confidence thresholds determine escalation paths
- Tools provide clean API over raw database access
- State flows through LangGraph with conditional routing
- Memory manager observes all interactions automatically

### Error Handling
- Graceful degradation with fallback responses
- Comprehensive logging for debugging
- Automatic escalation on component failures
- Timeout management prevents hung workflows
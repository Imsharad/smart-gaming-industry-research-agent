# Solution Directory Structure

```
solution/
│
├── agentic/                          # Core agent system
│   ├── agents/                       # Specialized agents
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── classifier_agent.py       # Ticket categorization agent
│   │   ├── supervisor_agent.py       # Workflow coordination agent
│   │   ├── resolver_agent.py         # Response generation agent
│   │   └── escalation_agent.py       # Human handoff agent
│   │
│   ├── tools/                        # Database abstraction tools
│   │   ├── __init__.py
│   │   ├── README.md
│   │   ├── account_lookup_tool.py    # Customer data retrieval
│   │   ├── knowledge_retrieval_tool.py # KB search
│   │   └── subscription_management_tool.py # Subscription ops
│   │
│   ├── design/                       # Architecture documentation
│   │   ├── README.md                 # Design overview
│   │   └── architecture.md           # Detailed architecture docs
│   │
│   ├── memory_manager.py             # Long-term memory system
│   ├── enhanced_workflow.py          # Main LangGraph orchestration
│   └── workflow.py                   # Base workflow definition
│
├── data/                             # Database and data files
│   ├── core/                         # Core application database
│   │   ├── README.md
│   │   └── udahub.db                 # UDA-Hub app data
│   │
│   ├── external/                     # External CultPass database
│   │   ├── README.md
│   │   ├── cultpass.db               # Customer data
│   │   ├── cultpass_articles.jsonl   # Knowledge base articles
│   │   ├── cultpass_experiences.jsonl # Gym experiences
│   │   └── cultpass_users.jsonl      # User data
│   │
│   └── models/                       # SQLAlchemy ORM models
│       ├── cultpass.py               # CultPass DB models
│       └── udahub.py                 # UDA-Hub DB models
│
├── notebooks/                        # Jupyter notebooks
│   ├── __init__.py
│   ├── 01_external_db_setup_executed.ipynb # External DB setup
│   ├── 02_core_db_setup_executed.ipynb     # Core DB setup
│   └── 03_agentic_app.ipynb                # Interactive interface
│
├── tests/                            # Test suite
│   ├── __init__.py
│   ├── comprehensive_tests.py        # Full rubric compliance tests
│   └── test_system.py                # System validation tests
│
├── utils/                            # Utility functions
│   ├── __init__.py
│   ├── utils.py                      # Database and general utilities
│   └── path_utils.py                 # Path resolution utilities
│
└── .env                              # Environment variables
```

## Directory Descriptions

### agentic/
Contains all agent-related code, tools, and workflow orchestration.

- **agents/**: Four specialized agents (Classifier, Supervisor, Resolver, Escalation)
- **tools/**: Database abstraction layer with three primary tools
- **design/**: Architecture documentation and design decisions
- **memory_manager.py**: Manages short-term and long-term memory
- **enhanced_workflow.py**: LangGraph StateGraph orchestration
- **workflow.py**: Base workflow definitions

### data/
All database files, data sources, and ORM models.

- **core/**: UDA-Hub application database (tickets, knowledge, history)
- **external/**: CultPass customer database (users, subscriptions, experiences)
- **models/**: SQLAlchemy models for both databases

### notebooks/
Jupyter notebooks for setup and interactive usage.

- Setup notebooks (01, 02): Initialize databases
- App notebook (03): Interactive chat interface

### tests/
Comprehensive test suite for system validation.

- **comprehensive_tests.py**: Tests all 7 rubric criteria
- **test_system.py**: Quick system health checks

### utils/
Shared utility functions used across the project.

- **utils.py**: Database helpers, session management
- **path_utils.py**: Path resolution for different environments

## Import Guidelines

### From Tests
```python
from utils.utils import get_session
from agentic.tools import lookup_user_account
from agentic.agents import ClassifierAgent
```

### From Notebooks
```python
from utils.utils import reset_db, get_session
from agentic.enhanced_workflow import orchestrator
```

### From Agents
```python
from agentic.tools import ALL_TOOLS
from agentic.memory_manager import MemoryManager
```

## Running the System

### Setup Databases
```bash
jupyter nbconvert --execute notebooks/01_external_db_setup_executed.ipynb
jupyter nbconvert --execute notebooks/02_core_db_setup_executed.ipynb
```

### Run Tests
```bash
python tests/comprehensive_tests.py
python tests/test_system.py
```

### Interactive Usage
```bash
jupyter notebook notebooks/03_agentic_app.ipynb
```

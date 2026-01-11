# UDA-Hub Tools

This directory contains all the database abstraction tools used by the UDA-Hub agentic system. These tools provide a clean interface for agents to interact with external and internal data sources without needing to know the underlying database schema or implementation details.

## Available Tools

### 1. Account Lookup Tool
- **File:** `account_lookup_tool.py`
- **Purpose:** Retrieves customer account information from the CultPass (external) database.
- **Key Functions:**
    - `lookup_user_account(email_or_id)`: Looks up a user by their email or user ID and returns a summary of their account, subscription, and recent activity.
    - `get_reservation_history(user_id)`: Retrieves a detailed history of a user's event reservations.

### 2. Knowledge Retrieval Tool
- **File:** `knowledge_retrieval_tool.py`
- **Purpose:** Searches and retrieves articles from the UDA-Hub (core) knowledge base.
- **Key Functions:**
    - `search_knowledge_base(query)`: Searches for relevant articles using keyword matching.
    - `get_knowledge_categories()`: Lists all available article categories.
    - `search_knowledge_by_category(category)`: Finds articles within a specific category.
    - `get_full_article(title)`: Retrieves the full content of an article by its title.

### 3. Subscription Management Tool
- **File:** `subscription_management_tool.py`
- **Purpose:** Performs actions related to customer subscriptions in the CultPass database.
- **Key Functions:**
    - `pause_user_subscription(user_id)`: Pauses a user's subscription.
    - `resume_user_subscription(user_id)`: Resumes a paused subscription.
    - `cancel_user_subscription(user_id)`: Cancels a user's subscription.
    - `upgrade_user_subscription(user_id, new_tier)`: Upgrades a user's subscription to a new tier.

## Usage

These tools are designed to be used within the LangGraph workflow. They are typically invoked by the `ResolverAgent` or a dedicated `ToolAgent` based on the classification and suggestions from the `ClassifierAgent`. Each tool is decorated with `@tool` from `langchain_core.tools` to be easily integrated into the agentic framework.
"""
UDA-Hub Support Operation Tools

This package contains database abstraction tools for CultPass customer support operations.
All tools are designed to be used by LangGraph agents and provide structured database access.
"""

from .account_lookup_tool import (
    lookup_user_account,
    get_reservation_history,
    AccountLookupTool
)

from .subscription_management_tool import (
    pause_user_subscription,
    resume_user_subscription,
    cancel_user_subscription,
    upgrade_user_subscription,
    SubscriptionManagementTool
)

from .knowledge_retrieval_tool import (
    search_knowledge_base,
    get_knowledge_categories,
    search_knowledge_by_category,
    get_full_article,
    KnowledgeRetrievalTool
)

# List of all available tools for easy import in agents
ALL_TOOLS = [
    # Account management tools
    lookup_user_account,
    get_reservation_history,
    
    # Subscription management tools
    pause_user_subscription,
    resume_user_subscription,
    cancel_user_subscription,
    upgrade_user_subscription,
    
    # Knowledge base tools
    search_knowledge_base,
    get_knowledge_categories,
    search_knowledge_by_category,
    get_full_article,
]

# Tools grouped by category
ACCOUNT_TOOLS = [
    lookup_user_account,
    get_reservation_history,
]

SUBSCRIPTION_TOOLS = [
    pause_user_subscription,
    resume_user_subscription,
    cancel_user_subscription,
    upgrade_user_subscription,
]

KNOWLEDGE_TOOLS = [
    search_knowledge_base,
    get_knowledge_categories,
    search_knowledge_by_category,
    get_full_article,
]

__all__ = [
    'ALL_TOOLS',
    'ACCOUNT_TOOLS',
    'SUBSCRIPTION_TOOLS', 
    'KNOWLEDGE_TOOLS',
    'lookup_user_account',
    'get_reservation_history',
    'pause_user_subscription',
    'resume_user_subscription',
    'cancel_user_subscription',
    'upgrade_user_subscription',
    'search_knowledge_base',
    'get_knowledge_categories',
    'search_knowledge_by_category',
    'get_full_article',
    'AccountLookupTool',
    'SubscriptionManagementTool',
    'KnowledgeRetrievalTool',
]
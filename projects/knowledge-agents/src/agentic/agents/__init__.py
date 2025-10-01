"""
UDA-Hub Multi-Agent System

This package contains the specialized agents for the Universal Decision Agent system.
Each agent has a specific role in processing customer support tickets.
"""

from .classifier_agent import ClassifierAgent
from .resolver_agent import ResolverAgent
from .supervisor_agent import SupervisorAgent
from .escalation_agent import EscalationAgent

__all__ = [
    'ClassifierAgent',
    'ResolverAgent',
    'SupervisorAgent',
    'EscalationAgent',
]
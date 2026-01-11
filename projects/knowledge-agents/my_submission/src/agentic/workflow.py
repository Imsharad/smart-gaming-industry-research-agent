from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict

# Import our agents and tools
from .agents.classifier_agent import ClassifierAgent
from .agents.resolver_agent import ResolverAgent
from .tools import ALL_TOOLS


class AgentState(TypedDict):
    """State shared between agents in the workflow"""
    messages: List[Any]
    ticket_content: str
    classification: Dict[str, Any]
    knowledge_results: str
    tool_results: str
    final_response: str
    escalate: bool
    confidence: float
    next_actions: List[str]


class UDAHubOrchestrator:
    """Multi-agent orchestrator for UDA-Hub customer support system"""
    
    def __init__(self):
        # Initialize agents
        self.classifier = ClassifierAgent()
        self.resolver = ResolverAgent()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        # Build the workflow graph
        self.graph = self._build_workflow()
        
        # Compile with memory
        self.checkpointer = MemorySaver()
        self.orchestrator = self.graph.compile(checkpointer=self.checkpointer)
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("classify", self._classify_node)
        workflow.add_node("retrieve_knowledge", self._retrieve_knowledge_node) 
        workflow.add_node("execute_tools", self._execute_tools_node)
        workflow.add_node("resolve", self._resolve_node)
        workflow.add_node("escalate", self._escalate_node)
        
        # Define the workflow edges
        workflow.set_entry_point("classify")
        
        # After classification, decide next step
        workflow.add_conditional_edges(
            "classify",
            self._should_escalate_after_classification,
            {
                "escalate": "escalate",
                "continue": "retrieve_knowledge"
            }
        )
        
        # After knowledge retrieval, execute tools if needed
        workflow.add_edge("retrieve_knowledge", "execute_tools")
        
        # After tool execution, resolve
        workflow.add_edge("execute_tools", "resolve")
        
        # After resolution, decide if escalation is needed
        workflow.add_conditional_edges(
            "resolve",
            self._should_escalate_after_resolution,
            {
                "escalate": "escalate",
                "end": END
            }
        )
        
        workflow.add_edge("escalate", END)
        
        return workflow
    
    def _classify_node(self, state: AgentState) -> AgentState:
        """Classification node - analyzes the ticket"""
        # Extract ticket content from messages
        if state["messages"]:
            # Get the last human message
            human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
            if human_messages:
                ticket_content = human_messages[-1].content
            else:
                ticket_content = str(state["messages"][-1].content)
        else:
            ticket_content = ""
        
        # Classify the ticket
        classification = self.classifier.classify_ticket(ticket_content)
        
        # Update state
        state["ticket_content"] = ticket_content
        state["classification"] = classification
        state["escalate"] = classification.get("escalate", False)
        
        return state
    
    def _retrieve_knowledge_node(self, state: AgentState) -> AgentState:
        """Knowledge retrieval node - searches knowledge base"""
        from .tools.knowledge_retrieval_tool import knowledge_tool
        
        # Extract keywords from ticket for knowledge search
        ticket_content = state["ticket_content"]
        classification = state["classification"]
        category = classification.get("category", "")
        
        # Search knowledge base based on content and category
        try:
            # Try category-based search first
            if category:
                category_keywords = category.lower().replace("_", " ").split()
                articles = knowledge_tool.search_articles_by_keywords(category_keywords, max_results=2)
                
                if not articles:
                    # Fall back to content-based search
                    content_keywords = ticket_content.lower().split()[:5]  # Use first 5 words
                    articles = knowledge_tool.search_articles_by_keywords(content_keywords, max_results=2)
                
                if articles:
                    knowledge_results = ""
                    for article in articles:
                        knowledge_results += f"Title: {article['title']}\n"
                        knowledge_results += f"Content: {article['content']}\n\n"
                else:
                    knowledge_results = "No relevant knowledge articles found."
            else:
                knowledge_results = "Classification failed, no knowledge search performed."
                
        except Exception as e:
            knowledge_results = f"Knowledge search error: {str(e)}"
        
        state["knowledge_results"] = knowledge_results
        return state
    
    def _execute_tools_node(self, state: AgentState) -> AgentState:
        """Tool execution node - runs suggested tools"""
        classification = state["classification"]
        suggested_tools = classification.get("suggested_tools", [])
        tool_results = ""
        
        # Map suggested tools to actual tool functions
        tool_map = {
            "lookup_user_account": "lookup_user_account",
            "get_reservation_history": "get_reservation_history", 
            "pause_user_subscription": "pause_user_subscription",
            "search_knowledge_base": "search_knowledge_base"
        }
        
        for suggested_tool in suggested_tools:
            if suggested_tool in tool_map:
                try:
                    # Extract parameters from classification
                    entities = classification.get("key_entities", {})
                    
                    if suggested_tool == "lookup_user_account":
                        email = entities.get("user_email")
                        user_id = entities.get("user_id")
                        if email or user_id:
                            from .tools.account_lookup_tool import lookup_user_account
                            result = lookup_user_account(email or user_id)
                            tool_results += f"Account Lookup: {result}\n\n"
                    
                    elif suggested_tool == "search_knowledge_base":
                        from .tools.knowledge_retrieval_tool import search_knowledge_base
                        query = state["ticket_content"][:100]  # First 100 chars as query
                        result = search_knowledge_base(query)
                        tool_results += f"Knowledge Search: {result}\n\n"
                        
                except Exception as e:
                    tool_results += f"Tool {suggested_tool} error: {str(e)}\n\n"
        
        if not tool_results:
            tool_results = "No tools were executed for this ticket."
        
        state["tool_results"] = tool_results
        return state
    
    def _resolve_node(self, state: AgentState) -> AgentState:
        """Resolution node - generates final response"""
        result = self.resolver.generate_response(
            ticket_content=state["ticket_content"],
            classification=state["classification"],
            knowledge_results=state["knowledge_results"],
            tool_results=state["tool_results"]
        )
        
        state["final_response"] = result["response"]
        state["confidence"] = result["confidence"]
        state["escalate"] = result["escalate"]
        state["next_actions"] = result["next_actions"]
        
        # Add the AI response to messages
        ai_message = AIMessage(content=result["response"])
        state["messages"].append(ai_message)
        
        return state
    
    def _escalate_node(self, state: AgentState) -> AgentState:
        """Escalation node - handles cases requiring human intervention"""
        escalation_summary = self.resolver.generate_escalation_summary(
            ticket_content=state["ticket_content"],
            classification=state["classification"],
            attempts=[],  # Could track resolution attempts
            reason="Automatic escalation based on confidence threshold"
        )
        
        escalation_message = f"""
This ticket has been escalated to a human agent.

Escalation Summary:
{escalation_summary['escalation_summary']}

Priority: {escalation_summary['priority']}
Customer Impact: {escalation_summary['customer_impact']}

A human agent will review this case and provide assistance shortly.
"""
        
        state["final_response"] = escalation_message
        
        # Add escalation message
        ai_message = AIMessage(content=escalation_message)
        state["messages"].append(ai_message)
        
        return state
    
    def _should_escalate_after_classification(self, state: AgentState) -> str:
        """Decision function after classification"""
        classification = state["classification"]
        
        # Escalate immediately if flagged by classifier
        if classification.get("escalate", False):
            return "escalate"
        
        # Escalate if confidence is very low
        if classification.get("confidence", 1.0) < 0.3:
            return "escalate"
        
        # Continue with normal flow
        return "continue"
    
    def _should_escalate_after_resolution(self, state: AgentState) -> str:
        """Decision function after resolution"""
        # Escalate if resolver determined escalation is needed
        if state.get("escalate", False):
            return "escalate"
        
        # Escalate if confidence is too low
        if state.get("confidence", 1.0) < 0.5:
            return "escalate"
        
        # Otherwise end the workflow
        return "end"


# Create the orchestrator instance
uda_hub = UDAHubOrchestrator()
orchestrator = uda_hub.orchestrator
"""
Enhanced UDA-Hub Workflow with 4 Agents, Memory Management, and Structured Logging
This implements the complete multi-agent architecture with all rubric requirements
"""

import time
import uuid
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict

# Import all agents and tools
from .agents.classifier_agent import ClassifierAgent
from .agents.resolver_agent import ResolverAgent
from .agents.supervisor_agent import SupervisorAgent
from .agents.escalation_agent import EscalationAgent
from .memory_manager import MemoryManager
from .tools import ALL_TOOLS


class EnhancedAgentState(TypedDict):
    """Enhanced state shared between agents in the workflow"""
    # Core workflow data
    messages: List[Any]
    ticket_content: str
    session_id: str
    user_id: str
    ticket_id: str
    
    # Agent processing results
    classification: Dict[str, Any]
    supervisor_decision: Dict[str, Any]
    knowledge_results: str
    tool_results: str
    resolution_result: Dict[str, Any]
    escalation_result: Dict[str, Any]
    
    # Final outputs
    final_response: str
    escalate: bool
    confidence: float
    next_actions: List[str]
    
    # Memory and personalization
    customer_history: List[Dict[str, Any]]
    customer_preferences: Dict[str, Any]
    personalized_context: Dict[str, Any]
    
    # Logging and metrics
    agent_logs: List[str]
    processing_times: Dict[str, float]
    errors: List[str]


class EnhancedUDAHubOrchestrator:
    """Enhanced multi-agent orchestrator with complete rubric compliance"""
    
    def __init__(self):
        # Initialize all 4 agents
        self.classifier = ClassifierAgent()
        self.resolver = ResolverAgent()
        self.supervisor = SupervisorAgent()
        self.escalation = EscalationAgent()
        
        # Initialize memory manager
        self.memory_manager = MemoryManager()
        
        # Initialize LLM
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        # Build the enhanced workflow graph
        self.graph = self._build_enhanced_workflow()
        
        # Compile with memory
        self.checkpointer = MemorySaver()
        self.orchestrator = self.graph.compile(checkpointer=self.checkpointer)
    
    def _build_enhanced_workflow(self) -> StateGraph:
        """Build the enhanced LangGraph workflow with 4 agents"""
        workflow = StateGraph(EnhancedAgentState)
        
        # Add nodes for all agents
        workflow.add_node("initialize", self._initialize_node)
        workflow.add_node("classify", self._classify_node)
        workflow.add_node("supervise", self._supervise_node)
        workflow.add_node("retrieve_knowledge", self._retrieve_knowledge_node)
        workflow.add_node("execute_tools", self._execute_tools_node)
        workflow.add_node("resolve", self._resolve_node)
        workflow.add_node("escalate", self._escalate_node)
        workflow.add_node("finalize", self._finalize_node)
        
        # Define the enhanced workflow
        workflow.set_entry_point("initialize")
        
        # Initialize -> Classify
        workflow.add_edge("initialize", "classify")
        
        # Classify -> Supervise
        workflow.add_edge("classify", "supervise")
        
        # Supervise -> Decision
        workflow.add_conditional_edges(
            "supervise",
            self._supervisor_decision,
            {
                "escalate_immediate": "escalate",
                "continue_resolution": "retrieve_knowledge"
            }
        )
        
        # Knowledge -> Tools -> Resolve
        workflow.add_edge("retrieve_knowledge", "execute_tools")
        workflow.add_edge("execute_tools", "resolve")
        
        # Resolve -> Final Decision
        workflow.add_conditional_edges(
            "resolve",
            self._resolution_decision,
            {
                "escalate": "escalate",
                "finalize": "finalize"
            }
        )
        
        # Escalate -> Finalize
        workflow.add_edge("escalate", "finalize")
        
        # Finalize -> END
        workflow.add_edge("finalize", END)
        
        return workflow
    
    def _initialize_node(self, state: EnhancedAgentState) -> EnhancedAgentState:
        """Initialize the workflow with memory retrieval and personalization"""
        start_time = time.time()
        
        try:
            # Extract basic information
            if state["messages"]:
                human_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
                if human_messages:
                    ticket_content = human_messages[-1].content
                else:
                    ticket_content = str(state["messages"][-1].content)
            else:
                ticket_content = ""
            
            # Generate IDs if not present
            session_id = state.get("session_id", str(uuid.uuid4()))
            ticket_id = state.get("ticket_id", str(uuid.uuid4()))
            user_id = state.get("user_id", "unknown_user")
            
            # Retrieve customer history and preferences
            customer_history = self.memory_manager.retrieve_customer_history(user_id) if user_id != "unknown_user" else []
            customer_preferences = self.memory_manager.get_customer_preferences(user_id) if user_id != "unknown_user" else {}
            personalized_context = self.memory_manager.generate_personalized_context(user_id) if user_id != "unknown_user" else {}
            
            # Log initialization
            self.memory_manager.log_agent_decision(
                ticket_id=ticket_id,
                session_id=session_id,
                agent_name="system",
                decision_type="initialization",
                decision_data={
                    "ticket_content_length": len(ticket_content),
                    "customer_history_count": len(customer_history),
                    "has_preferences": bool(customer_preferences)
                },
                processing_time_ms=(time.time() - start_time) * 1000,
                success="success"
            )
            
            # Update state
            state.update({
                "ticket_content": ticket_content,
                "session_id": session_id,
                "ticket_id": ticket_id,
                "user_id": user_id,
                "customer_history": customer_history,
                "customer_preferences": customer_preferences,
                "personalized_context": personalized_context,
                "agent_logs": [f"Initialized workflow for ticket {ticket_id}"],
                "processing_times": {"initialize": (time.time() - start_time) * 1000},
                "errors": []
            })
            
            return state
            
        except Exception as e:
            state["errors"].append(f"Initialization error: {str(e)}")
            self.memory_manager.log_agent_decision(
                ticket_id=state.get("ticket_id", "unknown"),
                session_id=state.get("session_id", "unknown"),
                agent_name="system",
                decision_type="initialization",
                decision_data={},
                processing_time_ms=(time.time() - start_time) * 1000,
                success="failure",
                error_message=str(e)
            )
            return state
    
    def _classify_node(self, state: EnhancedAgentState) -> EnhancedAgentState:
        """Enhanced classification with personalization and logging"""
        start_time = time.time()
        
        try:
            # Include personalized context in classification
            classification_input = {
                "ticket_content": state["ticket_content"],
                "customer_history": state.get("customer_history", []),
                "customer_preferences": state.get("customer_preferences", {})
            }
            
            # Classify the ticket
            classification = self.classifier.classify_ticket(state["ticket_content"])
            
            # Enhance classification with personalized context
            if state.get("personalized_context"):
                patterns = state["personalized_context"].get("patterns", {})
                if patterns.get("most_common_issues"):
                    # Adjust confidence based on historical patterns
                    category = classification.get("category", "").lower()
                    if category in [k.lower() for k in patterns["most_common_issues"].keys()]:
                        classification["confidence"] = min(1.0, classification.get("confidence", 0.5) + 0.1)
                        classification["personalized"] = True
            
            # Log classification decision
            self.memory_manager.log_agent_decision(
                ticket_id=state["ticket_id"],
                session_id=state["session_id"],
                agent_name="classifier",
                decision_type="classification",
                decision_data=classification,
                input_data=classification_input,
                confidence_score=classification.get("confidence", 0),
                processing_time_ms=(time.time() - start_time) * 1000,
                success="success"
            )
            
            # Update state
            state["classification"] = classification
            state["agent_logs"].append(f"Classified ticket as {classification.get('category', 'unknown')} with confidence {classification.get('confidence', 0):.2f}")
            state["processing_times"]["classify"] = (time.time() - start_time) * 1000
            
            return state
            
        except Exception as e:
            error_msg = f"Classification error: {str(e)}"
            state["errors"].append(error_msg)
            state["classification"] = {"category": "error", "confidence": 0, "escalate": True}
            
            self.memory_manager.log_agent_decision(
                ticket_id=state["ticket_id"],
                session_id=state["session_id"],
                agent_name="classifier",
                decision_type="classification",
                decision_data={},
                processing_time_ms=(time.time() - start_time) * 1000,
                success="failure",
                error_message=str(e)
            )
            
            return state
    
    def _supervise_node(self, state: EnhancedAgentState) -> EnhancedAgentState:
        """Supervisor agent coordination and decision making"""
        start_time = time.time()
        
        try:
            # Get supervisor coordination decision
            supervisor_decision = self.supervisor.coordinate_workflow(
                ticket_content=state["ticket_content"],
                classification=state["classification"]
            )
            
            # Log supervisor decision
            self.memory_manager.log_agent_decision(
                ticket_id=state["ticket_id"],
                session_id=state["session_id"],
                agent_name="supervisor",
                decision_type="coordination",
                decision_data=supervisor_decision,
                input_data={
                    "classification": state["classification"],
                    "customer_history_count": len(state.get("customer_history", []))
                },
                confidence_score=supervisor_decision.get("confidence", 0),
                processing_time_ms=(time.time() - start_time) * 1000,
                success="success"
            )
            
            # Update state
            state["supervisor_decision"] = supervisor_decision
            state["agent_logs"].append(f"Supervisor decision: {supervisor_decision.get('reasoning', 'No reasoning provided')}")
            state["processing_times"]["supervise"] = (time.time() - start_time) * 1000
            
            return state
            
        except Exception as e:
            error_msg = f"Supervision error: {str(e)}"
            state["errors"].append(error_msg)
            state["supervisor_decision"] = {"immediate_escalation": True, "reasoning": error_msg}
            
            self.memory_manager.log_agent_decision(
                ticket_id=state["ticket_id"],
                session_id=state["session_id"],
                agent_name="supervisor",
                decision_type="coordination",
                decision_data={},
                processing_time_ms=(time.time() - start_time) * 1000,
                success="failure",
                error_message=str(e)
            )
            
            return state
    
    def _retrieve_knowledge_node(self, state: EnhancedAgentState) -> EnhancedAgentState:
        """Enhanced knowledge retrieval with logging"""
        start_time = time.time()
        
        try:
            from .tools.knowledge_retrieval_tool import knowledge_tool
            
            classification = state["classification"]
            category = classification.get("category", "")
            
            # Search knowledge base with improved keyword extraction
            if category:
                # Create category-specific keywords
                category_map = {
                    "LOGIN_ISSUE": ["login", "password", "access", "account"],
                    "BILLING_PAYMENT": ["billing", "payment", "subscription", "charge"],
                    "RESERVATION_BOOKING": ["reservation", "booking", "event", "spot"],
                    "TECHNICAL_ISSUE": ["technical", "app", "bug", "error"],
                    "ACCOUNT_MANAGEMENT": ["account", "profile", "settings"],
                    "GENERAL_INQUIRY": ["help", "information", "question"],
                    "ESCALATION_REQUIRED": ["complex", "urgent", "escalate"]
                }
                
                # Get category-specific keywords
                category_keywords = category_map.get(category, category.lower().replace("_", " ").split())
                
                # Also extract important keywords from ticket content
                important_words = ["password", "billing", "payment", "cancel", "pause", "reservation", 
                                 "booking", "login", "access", "technical", "error", "problem", "issue",
                                 "subscription", "account", "profile", "help", "question"]
                
                content_keywords = []
                ticket_lower = state["ticket_content"].lower()
                for word in important_words:
                    if word in ticket_lower:
                        content_keywords.append(word)
                
                # Combine category keywords with content keywords
                all_keywords = list(set(category_keywords + content_keywords))
                
                # Try search with combined keywords first
                articles = knowledge_tool.search_articles_by_keywords(all_keywords, max_results=3)
                
                # If no results, try category keywords only
                if not articles and category_keywords:
                    articles = knowledge_tool.search_articles_by_keywords(category_keywords, max_results=3)
                
                if articles:
                    knowledge_results = ""
                    for article in articles:
                        knowledge_results += f"Title: {article['title']}\n"
                        knowledge_results += f"Content: {article['content']}\n\n"
                else:
                    knowledge_results = "No relevant knowledge articles found."
            else:
                knowledge_results = "Classification failed, no knowledge search performed."
            
            # Log knowledge retrieval
            self.memory_manager.log_agent_decision(
                ticket_id=state["ticket_id"],
                session_id=state["session_id"],
                agent_name="knowledge_retrieval",
                decision_type="knowledge_search",
                decision_data={
                    "articles_found": len(articles) if 'articles' in locals() else 0,
                    "category_keywords": category_keywords if 'category_keywords' in locals() else [],
                    "content_keywords": content_keywords if 'content_keywords' in locals() else [],
                    "all_keywords": all_keywords if 'all_keywords' in locals() else []
                },
                processing_time_ms=(time.time() - start_time) * 1000,
                success="success" if knowledge_results != "No relevant knowledge articles found." else "partial"
            )
            
            state["knowledge_results"] = knowledge_results
            state["agent_logs"].append(f"Knowledge retrieval: {'Success' if 'articles found' in knowledge_results.lower() else 'No relevant articles found'}")
            state["processing_times"]["knowledge_retrieval"] = (time.time() - start_time) * 1000
            
            return state
            
        except Exception as e:
            error_msg = f"Knowledge retrieval error: {str(e)}"
            state["errors"].append(error_msg)
            state["knowledge_results"] = f"Knowledge search error: {str(e)}"
            
            self.memory_manager.log_agent_decision(
                ticket_id=state["ticket_id"],
                session_id=state["session_id"],
                agent_name="knowledge_retrieval",
                decision_type="knowledge_search",
                decision_data={},
                processing_time_ms=(time.time() - start_time) * 1000,
                success="failure",
                error_message=str(e)
            )
            
            return state
    
    def _execute_tools_node(self, state: EnhancedAgentState) -> EnhancedAgentState:
        """Enhanced tool execution with comprehensive logging"""
        start_time = time.time()
        
        try:
            classification = state["classification"]
            suggested_tools = classification.get("suggested_tools", [])
            tool_results = ""
            tools_used = []
            
            # Execute suggested tools
            for suggested_tool in suggested_tools:
                tool_start_time = time.time()
                
                try:
                    if suggested_tool == "lookup_user_account":
                        entities = classification.get("key_entities", {})
                        email = entities.get("user_email")
                        user_id = entities.get("user_id") or state.get("user_id")
                        
                        if email or user_id:
                            from .tools.account_lookup_tool import lookup_user_account
                            result = lookup_user_account(email or user_id)
                            tool_results += f"Account Lookup: {result}\n\n"
                            tools_used.append(suggested_tool)
                    
                    elif suggested_tool == "search_knowledge_base":
                        from .tools.knowledge_retrieval_tool import search_knowledge_base
                        query = state["ticket_content"][:100]
                        result = search_knowledge_base(query)
                        tool_results += f"Knowledge Search: {result}\n\n"
                        tools_used.append(suggested_tool)
                    
                    # Log individual tool usage
                    self.memory_manager.log_agent_decision(
                        ticket_id=state["ticket_id"],
                        session_id=state["session_id"],
                        agent_name="tool_executor",
                        decision_type="tool_execution",
                        decision_data={"tool": suggested_tool, "result_length": len(str(result)) if 'result' in locals() else 0},
                        processing_time_ms=(time.time() - tool_start_time) * 1000,
                        success="success"
                    )
                    
                except Exception as tool_error:
                    tool_results += f"Tool {suggested_tool} error: {str(tool_error)}\n\n"
                    self.memory_manager.log_agent_decision(
                        ticket_id=state["ticket_id"],
                        session_id=state["session_id"],
                        agent_name="tool_executor",
                        decision_type="tool_execution",
                        decision_data={"tool": suggested_tool},
                        processing_time_ms=(time.time() - tool_start_time) * 1000,
                        success="failure",
                        error_message=str(tool_error)
                    )
            
            if not tool_results:
                tool_results = "No tools were executed for this ticket."
            
            state["tool_results"] = tool_results
            state["agent_logs"].append(f"Executed {len(tools_used)} tools: {', '.join(tools_used) if tools_used else 'none'}")
            state["processing_times"]["tool_execution"] = (time.time() - start_time) * 1000
            
            return state
            
        except Exception as e:
            error_msg = f"Tool execution error: {str(e)}"
            state["errors"].append(error_msg)
            state["tool_results"] = error_msg
            
            self.memory_manager.log_agent_decision(
                ticket_id=state["ticket_id"],
                session_id=state["session_id"],
                agent_name="tool_executor",
                decision_type="tool_execution",
                decision_data={},
                processing_time_ms=(time.time() - start_time) * 1000,
                success="failure",
                error_message=str(e)
            )
            
            return state
    
    def _resolve_node(self, state: EnhancedAgentState) -> EnhancedAgentState:
        """Enhanced resolution with personalization and logging"""
        start_time = time.time()
        
        try:
            # Include personalized context in resolution
            resolution_result = self.resolver.generate_response(
                ticket_content=state["ticket_content"],
                classification=state["classification"],
                knowledge_results=state["knowledge_results"],
                tool_results=state["tool_results"]
            )
            
            # Adjust response based on customer preferences
            preferences = state.get("customer_preferences", {})
            if "communication" in preferences:
                style_pref = preferences["communication"].get("style", {}).get("value", "standard")
                if style_pref == "detailed":
                    resolution_result["response"] = "Here's a detailed explanation:\n\n" + resolution_result["response"]
                elif style_pref == "brief":
                    resolution_result["response"] = "Brief answer: " + resolution_result["response"][:200] + "..."
            
            # Log resolution attempt
            self.memory_manager.log_agent_decision(
                ticket_id=state["ticket_id"],
                session_id=state["session_id"],
                agent_name="resolver",
                decision_type="resolution",
                decision_data=resolution_result,
                input_data={
                    "classification": state["classification"],
                    "knowledge_available": bool(state["knowledge_results"]),
                    "tools_used": bool(state["tool_results"])
                },
                confidence_score=resolution_result.get("confidence", 0),
                processing_time_ms=(time.time() - start_time) * 1000,
                success="success"
            )
            
            # Update state
            state["resolution_result"] = resolution_result
            state["final_response"] = resolution_result["response"]
            state["confidence"] = resolution_result["confidence"]
            state["escalate"] = resolution_result["escalate"]
            state["next_actions"] = resolution_result["next_actions"]
            
            # Add AI response to messages
            ai_message = AIMessage(content=resolution_result["response"])
            state["messages"].append(ai_message)
            
            state["agent_logs"].append(f"Generated resolution with confidence {resolution_result['confidence']:.2f}")
            state["processing_times"]["resolve"] = (time.time() - start_time) * 1000
            
            return state
            
        except Exception as e:
            error_msg = f"Resolution error: {str(e)}"
            state["errors"].append(error_msg)
            state["escalate"] = True
            state["confidence"] = 0.0
            
            self.memory_manager.log_agent_decision(
                ticket_id=state["ticket_id"],
                session_id=state["session_id"],
                agent_name="resolver",
                decision_type="resolution",
                decision_data={},
                processing_time_ms=(time.time() - start_time) * 1000,
                success="failure",
                error_message=str(e)
            )
            
            return state
    
    def _escalate_node(self, state: EnhancedAgentState) -> EnhancedAgentState:
        """Enhanced escalation with comprehensive analysis and logging"""
        start_time = time.time()
        
        try:
            # Process escalation with full context
            escalation_result = self.escalation.process_escalation(
                ticket_content=state["ticket_content"],
                classification=state["classification"],
                attempts=[],  # Could include resolution attempts
                escalation_reason="Automatic escalation based on confidence threshold or agent decision"
            )
            
            escalation_message = f"""
I apologize, but this issue requires specialized attention. Your ticket has been escalated to a human agent who will be better equipped to assist you.

Escalation Details:
- Escalation ID: {escalation_result.get('escalation_id', 'N/A')}
- Priority: {escalation_result.get('analysis', {}).get('priority', 'Medium')}
- Status: Escalated to human agent

A human agent will review your case and contact you shortly with a personalized solution. Thank you for your patience.
"""
            
            # Log escalation
            self.memory_manager.log_agent_decision(
                ticket_id=state["ticket_id"],
                session_id=state["session_id"],
                agent_name="escalation",
                decision_type="escalation",
                decision_data=escalation_result,
                processing_time_ms=(time.time() - start_time) * 1000,
                success="success"
            )
            
            # Update state
            state["escalation_result"] = escalation_result
            state["final_response"] = escalation_message
            state["escalate"] = True  # Explicitly set escalation flag
            
            # Add escalation message
            ai_message = AIMessage(content=escalation_message)
            state["messages"].append(ai_message)
            
            state["agent_logs"].append(f"Escalated to human agent: {escalation_result['escalation_id']}")
            state["processing_times"]["escalate"] = (time.time() - start_time) * 1000
            
            return state
            
        except Exception as e:
            error_msg = f"Escalation error: {str(e)}"
            state["errors"].append(error_msg)
            
            # Fallback escalation message
            fallback_message = "I apologize, but I'm unable to process your request at this time. Your ticket has been escalated to a human agent who will assist you shortly."
            state["final_response"] = fallback_message
            state["escalate"] = True  # Explicitly set escalation flag even in error case
            
            ai_message = AIMessage(content=fallback_message)
            state["messages"].append(ai_message)
            
            self.memory_manager.log_agent_decision(
                ticket_id=state["ticket_id"],
                session_id=state["session_id"],
                agent_name="escalation",
                decision_type="escalation",
                decision_data={},
                processing_time_ms=(time.time() - start_time) * 1000,
                success="failure",
                error_message=str(e)
            )
            
            return state
    
    def _finalize_node(self, state: EnhancedAgentState) -> EnhancedAgentState:
        """Finalize the workflow and store interaction history"""
        start_time = time.time()
        
        try:
            # Determine final outcome
            outcome = "escalated" if state.get("escalate", False) else "resolved"
            
            # Store interaction history for long-term memory
            interaction_data = {
                "account_id": "cultpass",
                "user_id": state.get("user_id", "unknown"),
                "session_id": state["session_id"],
                "ticket_id": state["ticket_id"],
                "interaction_type": "ticket_resolution",
                "classification_result": state.get("classification", {}),
                "resolution_result": state.get("resolution_result", {}),
                "tools_used": state.get("classification", {}).get("suggested_tools", []),
                "knowledge_articles_used": [],  # Could be extracted from knowledge_results
                "outcome": outcome,
                "confidence_score": state.get("confidence", 0),
                "interaction_summary": f"{outcome.title()} ticket about {state.get('classification', {}).get('category', 'unknown issue')}",
                "full_context": {
                    "ticket_content": state["ticket_content"],
                    "final_response": state.get("final_response", ""),
                    "processing_times": state.get("processing_times", {}),
                    "agent_logs": state.get("agent_logs", []),
                    "errors": state.get("errors", [])
                }
            }
            
            history_id = self.memory_manager.store_interaction_history(interaction_data)
            
            # Log finalization
            self.memory_manager.log_agent_decision(
                ticket_id=state["ticket_id"],
                session_id=state["session_id"],
                agent_name="system",
                decision_type="finalization",
                decision_data={
                    "outcome": outcome,
                    "history_id": history_id,
                    "total_processing_time": sum(state.get("processing_times", {}).values())
                },
                processing_time_ms=(time.time() - start_time) * 1000,
                success="success"
            )
            
            state["agent_logs"].append(f"Workflow completed: {outcome} (History ID: {history_id})")
            state["processing_times"]["finalize"] = (time.time() - start_time) * 1000
            
            return state
            
        except Exception as e:
            error_msg = f"Finalization error: {str(e)}"
            state["errors"].append(error_msg)
            
            self.memory_manager.log_agent_decision(
                ticket_id=state.get("ticket_id", "unknown"),
                session_id=state.get("session_id", "unknown"),
                agent_name="system",
                decision_type="finalization",
                decision_data={},
                processing_time_ms=(time.time() - start_time) * 1000,
                success="failure",
                error_message=str(e)
            )
            
            return state
    
    def _supervisor_decision(self, state: EnhancedAgentState) -> str:
        """Decision function for supervisor routing"""
        supervisor_decision = state.get("supervisor_decision", {})
        
        if supervisor_decision.get("immediate_escalation", False):
            return "escalate_immediate"
        
        return "continue_resolution"
    
    def _resolution_decision(self, state: EnhancedAgentState) -> str:
        """Decision function after resolution"""
        if state.get("escalate", False):
            return "escalate"
        
        if state.get("confidence", 0) < 0.5:
            return "escalate"
        
        return "finalize"


# Create the enhanced orchestrator instance
enhanced_uda_hub = EnhancedUDAHubOrchestrator()
orchestrator = enhanced_uda_hub.orchestrator
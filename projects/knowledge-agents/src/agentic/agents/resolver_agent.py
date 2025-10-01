"""
Resolver Agent - Generates solutions and responses based on retrieved knowledge and tool results
"""
from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate


class ResolverAgent:
    """Agent responsible for generating solutions and customer responses"""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.3)
        
        self.resolution_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
You are a customer support resolver for CultPass, a cultural experiences subscription service.
Your role is to generate helpful, professional, and personalized responses to customer inquiries.

Guidelines:
1. Be empathetic and understanding
2. Provide clear, actionable solutions
3. Use information from knowledge base articles and tool results
4. Maintain a friendly but professional tone
5. Always end with next steps or follow-up actions
6. If unable to fully resolve, suggest escalation appropriately

Response format:
- Start with acknowledgment of the customer's concern
- Provide the solution or information
- Include any relevant steps they need to take
- End with follow-up or next steps

Avoid:
- Generic responses
- Technical jargon
- Making promises you can't keep
- Providing incorrect information
"""),
            HumanMessage(content="""
Original ticket: {ticket_content}

Classification: {classification}

Knowledge base results: {knowledge_results}

Tool execution results: {tool_results}

Generate a helpful response to resolve this customer's issue.

IMPORTANT: If the knowledge base results or ticket content mention specific topics like "password", "billing", "reservation", "cancel", or "pause", make sure to directly address these topics in your response using the same terminology.
""")
        ])
    
    def generate_response(
        self, 
        ticket_content: str,
        classification: Dict[str, Any],
        knowledge_results: str = "",
        tool_results: str = "",
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate a resolution response based on all available information
        
        Args:
            ticket_content: Original customer message
            classification: Results from classifier agent
            knowledge_results: Relevant knowledge base articles
            tool_results: Results from tool executions
            context: Additional context (user history, etc.)
            
        Returns:
            Dictionary containing response and metadata
        """
        try:
            # Prepare the prompt with all available information
            prompt_vars = {
                "ticket_content": ticket_content,
                "classification": str(classification),
                "knowledge_results": knowledge_results or "No relevant knowledge base articles found.",
                "tool_results": tool_results or "No tool results available."
            }
            
            # Generate response
            response = self.llm.invoke(
                self.resolution_prompt.format_messages(**prompt_vars)
            )
            
            # Determine confidence and next actions
            confidence = self._assess_confidence(classification, knowledge_results, tool_results, ticket_content)
            next_actions = self._determine_next_actions(classification, confidence)
            
            result = {
                "response": response.content,
                "confidence": confidence,
                "next_actions": next_actions,
                "resolution_type": self._get_resolution_type(classification, confidence),
                "escalate": confidence < 0.5 or classification.get("escalate", False),
                "generated_at": self._get_timestamp()
            }
            
            # Add context if available
            if context:
                result["context_used"] = True
                result["user_context"] = context
            
            return result
            
        except Exception as e:
            return {
                "response": "I apologize, but I'm experiencing technical difficulties processing your request. Please let me escalate this to a human agent who can assist you better.",
                "confidence": 0.0,
                "next_actions": ["escalate_to_human"],
                "resolution_type": "error",
                "escalate": True,
                "error": str(e),
                "generated_at": self._get_timestamp()
            }
    
    def _assess_confidence(self, classification: Dict[str, Any], knowledge_results: str, tool_results: str, ticket_content: str = "") -> float:
        """Assess confidence in the resolution based on available information"""
        # Start with classification confidence but apply a reduction factor for resolution confidence
        classification_confidence = classification.get("confidence", 0.5)
        
        # Resolution confidence should generally be lower than classification confidence
        # because generating the right response is harder than just categorizing
        base_confidence = classification_confidence * 0.7  # More aggressive reduction factor
        
        # Check for complexity indicators in the ticket content
        ticket_content_lower = ticket_content.lower()
        
        # Major confidence reducers for complex/problematic scenarios
        complexity_indicators = [
            "crashing", "crash", "crashes", "crashed",
            "reinstalled", "multiple times", "three times", "several times",
            "very frustrating", "extremely", "urgent", "immediately", 
            "broken", "not working", "doesn't work", "won't work",
            "premium", "advanced", "complex", "technical issue",
            "something is wrong", "nothing works", "can't figure out"
        ]
        
        complexity_count = sum(1 for indicator in complexity_indicators if indicator in ticket_content_lower)
        if complexity_count > 0:
            base_confidence -= 0.2 * complexity_count  # Reduce confidence significantly for each complexity indicator
        
        # Reduce confidence for vague/unclear requests
        vague_indicators = [
            "something", "somehow", "the thing", "it doesn't work", "not working properly",
            "help with", "need help", "issues", "problems"
        ]
        vague_count = sum(1 for indicator in vague_indicators if indicator in ticket_content_lower)
        if vague_count > 1:  # Multiple vague terms = very unclear request
            base_confidence -= 0.25
        
        # Boost confidence if we have relevant knowledge base results
        if knowledge_results and len(knowledge_results) > 100:
            # Check if knowledge results seem relevant (not just long)
            if any(word in knowledge_results.lower() for word in ["password", "billing", "reservation", "login", "cancel", "pause"]):
                base_confidence += 0.1  # Reduced boost
            else:
                base_confidence += 0.03
        
        # Boost confidence if we have successful tool results
        if tool_results:
            if "successfully" in tool_results.lower() or "found" in tool_results.lower():
                base_confidence += 0.1  # Reduced boost
            elif "error" in tool_results.lower() or "failed" in tool_results.lower():
                base_confidence -= 0.25
        
        # Reduce confidence for complex categories that typically need human intervention
        complex_categories = ["ESCALATION_REQUIRED", "TECHNICAL_ISSUE"]
        if classification.get("category") in complex_categories:
            base_confidence -= 0.35  # More aggressive reduction
        
        # Reduce confidence for frustrated customers
        if classification.get("sentiment") == "frustrated":
            base_confidence -= 0.25  # More aggressive reduction
        
        # High priority issues should have lower confidence unless we have solid tool results
        if classification.get("priority") in ["HIGH", "URGENT"] and not (tool_results and "successfully" in tool_results.lower()):
            base_confidence -= 0.15
        
        # Ensure confidence stays within realistic bounds - lower maximum for complex scenarios
        max_confidence = 0.85 if complexity_count == 0 and vague_count == 0 else 0.6
        return min(max_confidence, max(0.1, base_confidence))
    
    def _determine_next_actions(self, classification: Dict[str, Any], confidence: float) -> List[str]:
        """Determine next actions based on classification and confidence"""
        actions = []
        
        if confidence < 0.5:
            actions.append("escalate_to_human")
        
        category = classification.get("category", "")
        
        if category == "BILLING_PAYMENT":
            actions.extend(["follow_up_payment", "verify_account_status"])
        elif category == "TECHNICAL_ISSUE":
            actions.extend(["check_system_status", "provide_troubleshooting"])
        elif category == "RESERVATION_BOOKING":
            actions.extend(["verify_booking_status", "send_confirmation"])
        
        # Always add general follow-up
        actions.append("schedule_follow_up")
        
        return list(set(actions))  # Remove duplicates
    
    def _get_resolution_type(self, classification: Dict[str, Any], confidence: float) -> str:
        """Determine the type of resolution provided"""
        if confidence >= 0.8:
            return "resolved"
        elif confidence >= 0.6:
            return "partial_resolution"
        elif classification.get("escalate", False):
            return "escalated"
        else:
            return "information_provided"
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def generate_escalation_summary(
        self,
        ticket_content: str,
        classification: Dict[str, Any],
        attempts: List[Dict[str, Any]],
        reason: str = "Unable to resolve automatically"
    ) -> Dict[str, Any]:
        """Generate a comprehensive summary for human escalation"""
        
        escalation_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
Create a comprehensive escalation summary for a human agent.
Include all relevant information, attempted solutions, and recommendations.
Be concise but thorough.
"""),
            HumanMessage(content="""
Ticket: {ticket_content}
Classification: {classification}
Resolution attempts: {attempts}
Escalation reason: {reason}

Create an escalation summary for the human agent.
""")
        ])
        
        try:
            response = self.llm.invoke(
                escalation_prompt.format_messages(
                    ticket_content=ticket_content,
                    classification=str(classification),
                    attempts=str(attempts),
                    reason=reason
                )
            )
            
            return {
                "escalation_summary": response.content,
                "priority": self._get_escalation_priority(classification),
                "category": classification.get("category", "GENERAL"),
                "customer_impact": self._assess_customer_impact(classification),
                "escalated_at": self._get_timestamp(),
                "reason": reason
            }
            
        except Exception as e:
            return {
                "escalation_summary": f"Automatic escalation due to resolution failure. Original ticket: {ticket_content}",
                "priority": "HIGH",
                "category": "SYSTEM_ERROR",
                "customer_impact": "HIGH",
                "escalated_at": self._get_timestamp(),
                "reason": f"System error: {str(e)}"
            }
    
    def _get_escalation_priority(self, classification: Dict[str, Any]) -> str:
        """Determine escalation priority"""
        original_priority = classification.get("priority", "MEDIUM")
        sentiment = classification.get("sentiment", "neutral")
        
        if sentiment == "frustrated" or original_priority == "URGENT":
            return "HIGH"
        elif original_priority == "HIGH":
            return "MEDIUM"
        else:
            return "LOW"
    
    def _assess_customer_impact(self, classification: Dict[str, Any]) -> str:
        """Assess the impact on the customer"""
        category = classification.get("category", "")
        
        high_impact_categories = ["BILLING_PAYMENT", "LOGIN_ISSUE", "ESCALATION_REQUIRED"]
        medium_impact_categories = ["RESERVATION_BOOKING", "TECHNICAL_ISSUE"]
        
        if category in high_impact_categories:
            return "HIGH"
        elif category in medium_impact_categories:
            return "MEDIUM"
        else:
            return "LOW"
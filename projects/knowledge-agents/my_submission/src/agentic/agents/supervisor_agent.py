"""
Supervisor Agent for UDA-Hub System
Central coordinator and decision maker for multi-agent workflows
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


class SupervisorAgent:
    """
    Central supervisor agent that coordinates the entire workflow
    and makes high-level routing and escalation decisions
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.system_prompt = """
        You are the Supervisor Agent for UDA-Hub, a customer support automation system.
        
        Your role is to:
        1. Coordinate the overall workflow and agent interactions
        2. Make high-level routing decisions based on ticket complexity
        3. Monitor workflow progress and intervene when necessary
        4. Make final escalation decisions when agents disagree
        5. Ensure efficient resource allocation across agents
        
        You receive classification results and must decide:
        - Whether to proceed with normal resolution workflow
        - Whether immediate escalation is required
        - Which specialized agents should handle the case
        - How to prioritize multiple concurrent tickets
        
        Always provide structured responses with clear reasoning.
        """
    
    def coordinate_workflow(self, ticket_content: str, classification: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make high-level coordination decisions for the workflow
        
        Args:
            ticket_content: Original customer ticket content
            classification: Results from classifier agent
            
        Returns:
            Dict containing coordination decisions
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""
            Analyze this customer support case and provide coordination decisions:
            
            TICKET CONTENT:
            {ticket_content}
            
            CLASSIFICATION RESULTS:
            Category: {classification.get('category', 'Unknown')}
            Confidence: {classification.get('confidence', 0)}
            Priority: {classification.get('priority', 'MEDIUM')}
            Sentiment: {classification.get('sentiment', 'neutral')}
            Key Entities: {classification.get('key_entities', {})}
            Suggested Tools: {classification.get('suggested_tools', [])}
            Escalate Flag: {classification.get('escalate', False)}
            
            Provide your coordination decisions in this JSON format:
            {{
                "proceed_with_resolution": true/false,
                "immediate_escalation": true/false,
                "priority_level": "low/medium/high/critical",
                "recommended_agents": ["agent1", "agent2"],
                "estimated_complexity": "simple/moderate/complex",
                "resource_allocation": "standard/high_priority",
                "reasoning": "explanation of decisions",
                "special_instructions": "any specific guidance for other agents"
            }}
            """)
        ]
        
        try:
            response = self.llm.invoke(messages)
            
            # Parse structured response (simplified for demo)
            content = response.content.lower()
            
            # Basic decision logic based on classification
            confidence = classification.get('confidence', 0)
            category = classification.get('category', '').lower()
            priority_from_classifier = classification.get('priority', 'MEDIUM').upper()
            sentiment = classification.get('sentiment', 'neutral')
            
            # Check if classifier explicitly flagged for escalation
            escalate_flag = classification.get('escalate', False)
            
            # Check for complexity indicators in ticket content
            ticket_lower = ticket_content.lower()
            complexity_indicators = [
                "crashing", "crash", "crashes", "crashed",
                "reinstalled", "multiple times", "three times", "several times",
                "very frustrating", "extremely", "urgent", "immediately", 
                "broken", "not working", "doesn't work", "won't work",
                "premium", "advanced", "complex", "technical issue",
                "something is wrong", "nothing works", "can't figure out"
            ]
            
            vague_indicators = [
                "something", "somehow", "the thing", "it doesn't work", "not working properly",
                "help with", "need help", "issues", "problems"
            ]
            
            complexity_count = sum(1 for indicator in complexity_indicators if indicator in ticket_lower)
            vague_count = sum(1 for indicator in vague_indicators if indicator in ticket_lower)
            
            # Determine priority based on multiple factors
            if (escalate_flag or priority_from_classifier == 'URGENT' or confidence < 0.2 or 
                sentiment == 'frustrated' or complexity_count >= 2):
                priority = "critical"
                immediate_escalation = True
                proceed_with_resolution = False
            elif (priority_from_classifier == 'HIGH' or confidence < 0.4 or category == 'escalation_required' or
                  category == 'technical_issue' or complexity_count >= 1 or vague_count >= 2):
                priority = "high"
                immediate_escalation = True
                proceed_with_resolution = False
            elif confidence < 0.5:
                priority = "medium"
                immediate_escalation = False
                proceed_with_resolution = True
            elif 'billing' in category or 'payment' in category:
                priority = "medium"
                immediate_escalation = False
                proceed_with_resolution = True
            else:
                priority = "medium"
                immediate_escalation = False
                proceed_with_resolution = True
            
            # Determine complexity
            if len(classification.get('suggested_tools', [])) > 2:
                complexity = "complex"
            elif classification.get('key_entities', {}) and len(classification.get('key_entities', {})) > 3:
                complexity = "moderate"
            else:
                complexity = "simple"
            
            coordination_result = {
                "proceed_with_resolution": proceed_with_resolution,
                "immediate_escalation": immediate_escalation,
                "priority_level": priority,
                "recommended_agents": ["classifier", "resolver"] if proceed_with_resolution else ["escalation"],
                "estimated_complexity": complexity,
                "resource_allocation": "high_priority" if priority in ["high", "critical"] else "standard",
                "reasoning": f"Classification confidence: {confidence:.2f}, Category: {category}, Priority: {priority_from_classifier}, Sentiment: {sentiment}",
                "special_instructions": self._generate_special_instructions(classification, priority),
                "confidence": confidence
            }
            
            return coordination_result
            
        except Exception as e:
            # Fallback coordination decision
            return {
                "proceed_with_resolution": True,
                "immediate_escalation": False,
                "priority_level": "medium",
                "recommended_agents": ["classifier", "resolver"],
                "estimated_complexity": "moderate",
                "resource_allocation": "standard",
                "reasoning": f"Error in supervisor decision making: {str(e)}",
                "special_instructions": "Proceed with standard workflow",
                "confidence": 0.5
            }
    
    def _generate_special_instructions(self, classification: Dict[str, Any], priority: str) -> str:
        """Generate specific instructions based on classification and priority"""
        instructions = []
        
        category = classification.get('category', '').lower()
        confidence = classification.get('confidence', 0)
        
        if confidence < 0.5:
            instructions.append("Use multiple knowledge sources for validation")
        
        if 'billing' in category:
            instructions.append("Verify customer account status before any billing operations")
        
        if 'technical' in category:
            instructions.append("Gather detailed system information before troubleshooting")
        
        if priority == "critical":
            instructions.append("Expedite resolution and prepare escalation summary")
        
        return "; ".join(instructions) if instructions else "Follow standard procedures"
    
    def monitor_progress(self, workflow_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitor ongoing workflow progress and suggest interventions
        
        Args:
            workflow_state: Current state of the workflow
            
        Returns:
            Dict containing monitoring results and recommendations
        """
        try:
            # Analyze current workflow state
            confidence = workflow_state.get('confidence', 0)
            escalate_flag = workflow_state.get('escalate', False)
            tool_results = workflow_state.get('tool_results', '')
            knowledge_results = workflow_state.get('knowledge_results', '')
            
            # Determine if intervention is needed
            intervention_needed = False
            recommendations = []
            
            if confidence < 0.3:
                intervention_needed = True
                recommendations.append("Low confidence detected - consider escalation")
            
            if escalate_flag:
                intervention_needed = True
                recommendations.append("Agent flagged for escalation - prepare handoff")
            
            if 'error' in tool_results.lower():
                intervention_needed = True
                recommendations.append("Tool execution errors detected - retry or escalate")
            
            if 'no relevant' in knowledge_results.lower():
                recommendations.append("Knowledge gap identified - consider alternative sources")
            
            return {
                "intervention_needed": intervention_needed,
                "recommendations": recommendations,
                "continue_workflow": not intervention_needed,
                "supervisor_confidence": confidence if confidence > 0.5 else 0.3,
                "status": "monitoring_active"
            }
            
        except Exception as e:
            return {
                "intervention_needed": True,
                "recommendations": [f"Monitoring error: {str(e)} - manual review required"],
                "continue_workflow": False,
                "supervisor_confidence": 0.2,
                "status": "monitoring_error"
            }
    
    def make_final_decision(self, resolution_result: Dict[str, Any], escalation_input: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make final decision on ticket resolution vs escalation
        
        Args:
            resolution_result: Result from resolver agent
            escalation_input: Optional input from escalation assessment
            
        Returns:
            Dict containing final decision
        """
        try:
            resolution_confidence = resolution_result.get('confidence', 0)
            escalate_flag = resolution_result.get('escalate', False)
            
            # Final decision logic
            if escalate_flag or resolution_confidence < 0.4:
                decision = "escalate"
                reasoning = f"Escalation required: confidence={resolution_confidence:.2f}, flag={escalate_flag}"
            else:
                decision = "resolve"
                reasoning = f"Resolution approved: confidence={resolution_confidence:.2f}"
            
            return {
                "final_decision": decision,
                "reasoning": reasoning,
                "supervisor_confidence": max(resolution_confidence, 0.3),
                "requires_human_review": decision == "escalate",
                "completion_status": "decided"
            }
            
        except Exception as e:
            return {
                "final_decision": "escalate",
                "reasoning": f"Decision error: {str(e)} - defaulting to escalation",
                "supervisor_confidence": 0.2,
                "requires_human_review": True,
                "completion_status": "error_escalation"
            }
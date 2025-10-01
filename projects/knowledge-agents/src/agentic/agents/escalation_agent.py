"""
Escalation Agent for UDA-Hub System
Specialized handling of escalated cases and human handoff preparation
"""

from typing import Dict, Any, List
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


class EscalationAgent:
    """
    Specialized agent for handling escalated cases that require human intervention
    """
    
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.system_prompt = """
        You are the Escalation Agent for UDA-Hub customer support system.
        
        Your role is to:
        1. Handle cases that require human intervention
        2. Prepare comprehensive escalation summaries for human agents
        3. Analyze escalation patterns and provide insights
        4. Generate detailed handoff documentation
        5. Track escalation metrics and success rates
        
        When a case is escalated to you:
        - Analyze all available context and previous attempts
        - Identify the root cause of escalation
        - Prepare structured handoff information
        - Suggest resolution strategies for human agents
        - Document lessons learned for system improvement
        
        Always provide clear, actionable information for human agents.
        """
    
    def process_escalation(self, ticket_content: str, classification: Dict[str, Any], 
                          attempts: List[Dict[str, Any]], escalation_reason: str) -> Dict[str, Any]:
        """
        Process an escalated case and prepare for human handoff
        
        Args:
            ticket_content: Original customer ticket
            classification: Classification results
            attempts: Previous resolution attempts
            escalation_reason: Reason for escalation
            
        Returns:
            Dict containing escalation processing results
        """
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""
            Process this escalated customer support case:
            
            ORIGINAL TICKET:
            {ticket_content}
            
            CLASSIFICATION:
            {classification}
            
            PREVIOUS ATTEMPTS:
            {attempts}
            
            ESCALATION REASON:
            {escalation_reason}
            
            Provide a comprehensive escalation analysis including:
            1. Root cause analysis
            2. Customer impact assessment
            3. Recommended resolution strategies
            4. Priority level and urgency
            5. Required expertise/skills
            6. Expected resolution timeframe
            """)
        ]
        
        try:
            response = self.llm.invoke(messages)
            
            # Generate escalation analysis
            escalation_analysis = self._analyze_escalation(
                ticket_content, classification, attempts, escalation_reason
            )
            
            # Create handoff package
            handoff_package = self._create_handoff_package(
                ticket_content, classification, escalation_analysis
            )
            
            # Track escalation metrics
            metrics = self._track_escalation_metrics(classification, escalation_reason)
            
            return {
                "escalation_id": f"ESC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "analysis": escalation_analysis,
                "handoff_package": handoff_package,
                "metrics": metrics,
                "status": "escalated_to_human",
                "timestamp": datetime.now().isoformat(),
                "estimated_resolution_time": escalation_analysis.get("estimated_time", "2-4 hours")
            }
            
        except Exception as e:
            return self._create_fallback_escalation(ticket_content, escalation_reason, str(e))
    
    def _analyze_escalation(self, ticket_content: str, classification: Dict[str, Any], 
                           attempts: List[Dict[str, Any]], reason: str) -> Dict[str, Any]:
        """Analyze the escalation and determine root cause"""
        
        # Determine escalation category
        escalation_category = self._categorize_escalation(reason, classification)
        
        # Assess customer impact
        impact_level = self._assess_customer_impact(ticket_content, classification)
        
        # Determine priority
        priority = self._determine_escalation_priority(classification, impact_level)
        
        # Analyze root cause
        root_cause = self._identify_root_cause(attempts, reason, classification)
        
        return {
            "escalation_category": escalation_category,
            "root_cause": root_cause,
            "customer_impact": impact_level,
            "priority": priority,
            "complexity": "high" if len(attempts) > 2 else "medium",
            "estimated_time": self._estimate_resolution_time(escalation_category, priority),
            "required_expertise": self._identify_required_expertise(escalation_category, classification)
        }
    
    def _categorize_escalation(self, reason: str, classification: Dict[str, Any]) -> str:
        """Categorize the type of escalation"""
        reason_lower = reason.lower()
        category = classification.get('category', '').lower()
        
        if 'confidence' in reason_lower or 'uncertain' in reason_lower:
            return "low_confidence"
        elif 'complex' in reason_lower or 'multiple' in reason_lower:
            return "complexity"
        elif 'billing' in category or 'payment' in category:
            return "billing_dispute"
        elif 'technical' in category:
            return "technical_complexity"
        elif 'account' in category:
            return "account_security"
        else:
            return "general_escalation"
    
    def _assess_customer_impact(self, ticket_content: str, classification: Dict[str, Any]) -> str:
        """Assess the impact level on the customer"""
        content_lower = ticket_content.lower()
        urgency = classification.get('urgency', 'medium').lower()
        
        # High impact indicators
        high_impact_keywords = ['blocked', 'can\'t access', 'critical', 'urgent', 'losing money']
        medium_impact_keywords = ['slow', 'error', 'problem', 'issue', 'not working']
        
        if urgency == 'critical' or any(keyword in content_lower for keyword in high_impact_keywords):
            return "high"
        elif any(keyword in content_lower for keyword in medium_impact_keywords):
            return "medium"
        else:
            return "low"
    
    def _determine_escalation_priority(self, classification: Dict[str, Any], impact: str) -> str:
        """Determine the priority level for escalation"""
        urgency = classification.get('urgency', 'medium').lower()
        confidence = classification.get('confidence', 0.5)
        
        if urgency == 'critical' or impact == 'high':
            return "P1"  # Highest priority
        elif urgency == 'high' or impact == 'medium':
            return "P2"  # High priority
        elif confidence < 0.3:
            return "P2"  # High priority due to uncertainty
        else:
            return "P3"  # Normal priority
    
    def _identify_root_cause(self, attempts: List[Dict[str, Any]], reason: str, classification: Dict[str, Any]) -> str:
        """Identify the root cause of escalation"""
        if not attempts:
            return f"Direct escalation: {reason}"
        
        # Analyze patterns in failed attempts
        if len(attempts) > 2:
            return "Multiple resolution attempts failed - complex issue requiring specialized expertise"
        elif 'knowledge' in reason.lower():
            return "Knowledge gap - no relevant documentation found"
        elif 'confidence' in reason.lower():
            return "System uncertainty - classification or resolution confidence below threshold"
        else:
            return f"Resolution failure: {reason}"
    
    def _estimate_resolution_time(self, category: str, priority: str) -> str:
        """Estimate resolution time based on escalation type and priority"""
        time_matrix = {
            ("billing_dispute", "P1"): "1-2 hours",
            ("billing_dispute", "P2"): "2-4 hours",
            ("billing_dispute", "P3"): "4-8 hours",
            ("technical_complexity", "P1"): "2-4 hours",
            ("technical_complexity", "P2"): "4-8 hours",
            ("technical_complexity", "P3"): "8-24 hours",
            ("account_security", "P1"): "1-2 hours",
            ("account_security", "P2"): "2-4 hours",
            ("low_confidence", "P1"): "1-2 hours",
            ("low_confidence", "P2"): "2-4 hours",
            ("complexity", "P1"): "4-8 hours",
            ("complexity", "P2"): "8-24 hours"
        }
        
        return time_matrix.get((category, priority), "4-8 hours")
    
    def _identify_required_expertise(self, category: str, classification: Dict[str, Any]) -> List[str]:
        """Identify required expertise for resolution"""
        expertise_map = {
            "billing_dispute": ["billing_specialist", "financial_operations"],
            "technical_complexity": ["technical_support", "engineering"],
            "account_security": ["security_team", "account_management"],
            "low_confidence": ["senior_support", "supervisor"],
            "complexity": ["senior_support", "subject_matter_expert"]
        }
        
        base_expertise = expertise_map.get(category, ["general_support"])
        
        # Add category-specific expertise
        cat = classification.get('category', '').lower()
        if 'subscription' in cat:
            base_expertise.append("subscription_management")
        if 'app' in cat or 'technical' in cat:
            base_expertise.append("technical_support")
        
        return list(set(base_expertise))
    
    def _create_handoff_package(self, ticket_content: str, classification: Dict[str, Any], 
                               analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive handoff package for human agents"""
        
        return {
            "ticket_summary": {
                "original_content": ticket_content,
                "classification": classification,
                "customer_id": classification.get('key_entities', {}).get('user_id', 'Unknown'),
                "category": classification.get('category', 'Unknown')
            },
            "escalation_details": {
                "escalation_reason": analysis.get('root_cause', 'Unknown'),
                "priority": analysis.get('priority', 'P3'),
                "customer_impact": analysis.get('customer_impact', 'medium'),
                "estimated_resolution_time": analysis.get('estimated_time', '4-8 hours')
            },
            "recommended_actions": self._generate_recommended_actions(analysis, classification),
            "context": {
                "previous_attempts": "System attempted automatic resolution",
                "tools_used": classification.get('suggested_tools', []),
                "knowledge_search_results": "Automated knowledge base search completed"
            },
            "resources": {
                "required_expertise": analysis.get('required_expertise', ['general_support']),
                "relevant_documentation": self._identify_relevant_docs(classification),
                "escalation_contacts": self._get_escalation_contacts(analysis.get('escalation_category'))
            }
        }
    
    def _generate_recommended_actions(self, analysis: Dict[str, Any], classification: Dict[str, Any]) -> List[str]:
        """Generate recommended actions for human agents"""
        actions = []
        
        category = analysis.get('escalation_category', '')
        priority = analysis.get('priority', 'P3')
        
        if category == "billing_dispute":
            actions.extend([
                "Verify customer account status and billing history",
                "Review recent transactions and payment methods",
                "Check for any billing system errors or discrepancies"
            ])
        elif category == "technical_complexity":
            actions.extend([
                "Gather detailed system logs and error information",
                "Attempt advanced troubleshooting procedures",
                "Escalate to engineering if needed"
            ])
        elif category == "low_confidence":
            actions.extend([
                "Conduct thorough review of customer request",
                "Consult with subject matter experts",
                "Consider multiple resolution approaches"
            ])
        
        if priority == "P1":
            actions.insert(0, "URGENT: Contact customer immediately to acknowledge escalation")
        
        return actions
    
    def _identify_relevant_docs(self, classification: Dict[str, Any]) -> List[str]:
        """Identify relevant documentation for the case"""
        docs = ["UDA-Hub Operation Manual", "Customer Support Procedures"]
        
        category = classification.get('category', '').lower()
        if 'billing' in category:
            docs.append("Billing and Payments Guide")
        if 'technical' in category:
            docs.append("Technical Troubleshooting Manual")
        if 'account' in category:
            docs.append("Account Management Procedures")
        
        return docs
    
    def _get_escalation_contacts(self, category: str) -> List[str]:
        """Get relevant escalation contacts"""
        contacts = {
            "billing_dispute": ["billing-team@udahub.com", "finance-lead@udahub.com"],
            "technical_complexity": ["tech-support@udahub.com", "engineering@udahub.com"],
            "account_security": ["security@udahub.com", "account-management@udahub.com"],
            "complexity": ["senior-support@udahub.com", "support-manager@udahub.com"]
        }
        
        return contacts.get(category, ["support-manager@udahub.com"])
    
    def _track_escalation_metrics(self, classification: Dict[str, Any], reason: str) -> Dict[str, Any]:
        """Track metrics for this escalation"""
        return {
            "escalation_timestamp": datetime.now().isoformat(),
            "classification_confidence": classification.get('confidence', 0),
            "escalation_reason": reason,
            "category": classification.get('category', 'Unknown'),
            "urgency": classification.get('urgency', 'medium'),
            "automated_attempts": 1  # Could be enhanced to track actual attempts
        }
    
    def _create_fallback_escalation(self, ticket_content: str, reason: str, error: str) -> Dict[str, Any]:
        """Create fallback escalation when processing fails"""
        return {
            "escalation_id": f"ESC_FALLBACK_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "analysis": {
                "escalation_category": "system_error",
                "root_cause": f"Escalation processing error: {error}",
                "customer_impact": "unknown",
                "priority": "P2",
                "complexity": "high",
                "estimated_time": "4-8 hours"
            },
            "handoff_package": {
                "ticket_summary": {"original_content": ticket_content},
                "escalation_details": {"escalation_reason": reason, "priority": "P2"},
                "recommended_actions": ["Manual review required due to system error"],
                "context": {"error": error}
            },
            "status": "escalated_with_error",
            "timestamp": datetime.now().isoformat()
        }
"""
Classifier Agent - Analyzes and classifies incoming support tickets
"""
import json
from datetime import datetime
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate


class ClassifierAgent:
    """Agent responsible for classifying incoming support tickets"""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        
        self.classification_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
You are a support ticket classifier for CultPass, a cultural experiences subscription service.

Analyze the incoming support ticket and classify it into one of these categories:
1. LOGIN_ISSUE - Login problems, password resets, account access
2. BILLING_PAYMENT - Payment issues, billing questions, refunds, subscription changes
3. RESERVATION_BOOKING - Event reservations, booking problems, cancellations
4. TECHNICAL_ISSUE - App crashes, loading problems, technical bugs
5. ACCOUNT_MANAGEMENT - Profile updates, settings, account deletion
6. GENERAL_INQUIRY - General questions about service, experiences, policies
7. ESCALATION_REQUIRED - Complex issues requiring human intervention

Also determine:
- Priority: LOW, MEDIUM, HIGH, URGENT
- Confidence: 0.0 to 1.0 (how confident you are in the classification)
- Key entities: Extract user email, reservation IDs, experience names, etc.
- Suggested tools: Which tools might be needed to resolve this

Confidence Guidelines:
- 0.9-1.0: Very clear, unambiguous requests with specific keywords
- 0.7-0.8: Clear requests but some ambiguity in intent or category
- 0.5-0.6: Somewhat unclear requests requiring interpretation
- 0.3-0.4: Ambiguous requests that could fit multiple categories
- 0.0-0.2: Very unclear or complex requests requiring human review

Respond in this exact JSON format:
{
    "category": "CATEGORY_NAME",
    "priority": "PRIORITY_LEVEL", 
    "confidence": 0.75,
    "reasoning": "Brief explanation of classification and confidence level",
    "key_entities": {
        "user_email": "extracted_email",
        "user_id": "extracted_user_id",
        "reservation_id": "extracted_reservation_id",
        "experience_name": "extracted_experience"
    },
    "suggested_tools": ["tool1", "tool2"],
    "escalate": false,
    "sentiment": "neutral/positive/negative/frustrated"
}
"""),
            HumanMessage(content="Classify this support ticket: {ticket_content}")
        ])
    
    def classify_ticket(self, ticket_content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Classify a support ticket and extract key information
        
        Args:
            ticket_content: The text content of the support ticket
            metadata: Optional metadata about the ticket (channel, timestamp, etc.)
            
        Returns:
            Dictionary containing classification results
        """
        try:
            # Get classification from LLM
            response = self.llm.invoke(
                self.classification_prompt.format_messages(ticket_content=ticket_content)
            )
            
            # Parse the JSON response
            import json
            classification = json.loads(response.content)
            
            # Add metadata if provided
            if metadata:
                classification["metadata"] = metadata
            
            # Add processing timestamp
            classification["classified_at"] = datetime.now().isoformat()
            
            return classification
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "category": "GENERAL_INQUIRY",
                "priority": "MEDIUM",
                "confidence": 0.5,
                "reasoning": "Failed to parse LLM response, using fallback classification",
                "key_entities": {},
                "suggested_tools": ["search_knowledge_base"],
                "escalate": False,
                "sentiment": "neutral",
                "error": "JSON parsing failed",
                "classified_at": datetime.now().isoformat()
            }
        except Exception as e:
            # General error handling
            return {
                "category": "ESCALATION_REQUIRED",
                "priority": "HIGH", 
                "confidence": 0.0,
                "reasoning": f"Classification failed due to error: {str(e)}",
                "key_entities": {},
                "suggested_tools": [],
                "escalate": True,
                "sentiment": "neutral",
                "error": str(e),
                "classified_at": datetime.now().isoformat()
            }
"""
Memory Manager for UDA-Hub System
Handles persistent customer interaction history and long-term memory
"""

import json
import uuid
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.utils import get_session
from data.models.udahub import InteractionHistory, CustomerPreference, AgentDecisionLog
from utils.path_utils import get_core_db_path


class MemoryManager:
    """
    Manages long-term memory for customer interactions and preferences
    """
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = get_core_db_path()
        
        # Ensure we have an absolute path
        db_path = os.path.abspath(db_path)
        self.engine = create_engine(f"sqlite:///{db_path}")
    
    def store_interaction_history(self, interaction_data: Dict[str, Any]) -> str:
        """
        Store customer interaction history for long-term memory
        
        Args:
            interaction_data: Complete interaction context and results
            
        Returns:
            history_id: Unique identifier for the stored interaction
        """
        history_id = str(uuid.uuid4())
        
        try:
            with get_session(self.engine) as session:
                interaction = InteractionHistory(
                    history_id=history_id,
                    account_id=interaction_data.get('account_id', 'cultpass'),
                    user_id=interaction_data.get('user_id'),
                    session_id=interaction_data.get('session_id'),
                    ticket_id=interaction_data.get('ticket_id'),
                    interaction_type=interaction_data.get('interaction_type', 'ticket_resolution'),
                    classification_result=interaction_data.get('classification_result'),
                    resolution_result=interaction_data.get('resolution_result'),
                    tools_used=interaction_data.get('tools_used', []),
                    knowledge_articles_used=interaction_data.get('knowledge_articles_used', []),
                    outcome=interaction_data.get('outcome', 'unknown'),
                    confidence_score=interaction_data.get('confidence_score'),
                    customer_satisfaction=interaction_data.get('customer_satisfaction'),
                    interaction_summary=interaction_data.get('interaction_summary'),
                    full_context=interaction_data.get('full_context')
                )
                session.add(interaction)
                session.commit()
                
            return history_id
            
        except Exception as e:
            print(f"Error storing interaction history: {e}")
            return ""
    
    def retrieve_customer_history(self, user_id: str, account_id: str = "cultpass", 
                                 limit: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve customer's previous interaction history
        
        Args:
            user_id: Customer user ID
            account_id: Account identifier
            limit: Maximum number of interactions to retrieve
            
        Returns:
            List of previous interactions
        """
        try:
            with get_session(self.engine) as session:
                interactions = session.query(InteractionHistory)\
                    .filter_by(user_id=user_id, account_id=account_id)\
                    .order_by(InteractionHistory.created_at.desc())\
                    .limit(limit)\
                    .all()
                
                history = []
                for interaction in interactions:
                    history.append({
                        'history_id': interaction.history_id,
                        'session_id': interaction.session_id,
                        'ticket_id': interaction.ticket_id,
                        'interaction_type': interaction.interaction_type,
                        'classification_result': interaction.classification_result,
                        'resolution_result': interaction.resolution_result,
                        'tools_used': interaction.tools_used,
                        'knowledge_articles_used': interaction.knowledge_articles_used,
                        'outcome': interaction.outcome,
                        'confidence_score': interaction.confidence_score,
                        'interaction_summary': interaction.interaction_summary,
                        'created_at': interaction.created_at.isoformat() if interaction.created_at else None
                    })
                
                return history
                
        except Exception as e:
            print(f"Error retrieving customer history: {e}")
            return []
    
    def store_customer_preference(self, user_id: str, preference_type: str, 
                                 preference_key: str, preference_value: Any,
                                 account_id: str = "cultpass") -> bool:
        """
        Store or update customer preference
        
        Args:
            user_id: Customer user ID
            preference_type: Type of preference (communication, resolution, escalation)
            preference_key: Specific preference key
            preference_value: Preference value
            account_id: Account identifier
            
        Returns:
            Success status
        """
        try:
            preference_id = str(uuid.uuid4())
            
            with get_session(self.engine) as session:
                # Check if preference already exists
                existing = session.query(CustomerPreference)\
                    .filter_by(user_id=user_id, preference_type=preference_type, 
                              preference_key=preference_key)\
                    .first()
                
                if existing:
                    # Update existing preference
                    existing.preference_value = preference_value
                    existing.last_reinforced = datetime.now()
                    existing.times_observed = str(int(existing.times_observed) + 1)
                    existing.updated_at = datetime.now()
                else:
                    # Create new preference
                    preference = CustomerPreference(
                        preference_id=preference_id,
                        account_id=account_id,
                        user_id=user_id,
                        preference_type=preference_type,
                        preference_key=preference_key,
                        preference_value=preference_value,
                        confidence_level=1.0,
                        times_observed="1"
                    )
                    session.add(preference)
                
                session.commit()
                return True
                
        except Exception as e:
            print(f"Error storing customer preference: {e}")
            return False
    
    def get_customer_preferences(self, user_id: str, account_id: str = "cultpass") -> Dict[str, Any]:
        """
        Retrieve customer preferences for personalization
        
        Args:
            user_id: Customer user ID
            account_id: Account identifier
            
        Returns:
            Dictionary of customer preferences
        """
        try:
            with get_session(self.engine) as session:
                preferences = session.query(CustomerPreference)\
                    .filter_by(user_id=user_id, account_id=account_id)\
                    .all()
                
                preference_dict = {}
                for pref in preferences:
                    if pref.preference_type not in preference_dict:
                        preference_dict[pref.preference_type] = {}
                    
                    preference_dict[pref.preference_type][pref.preference_key] = {
                        'value': pref.preference_value,
                        'confidence': pref.confidence_level,
                        'last_reinforced': pref.last_reinforced.isoformat() if pref.last_reinforced else None,
                        'times_observed': pref.times_observed
                    }
                
                return preference_dict
                
        except Exception as e:
            print(f"Error retrieving customer preferences: {e}")
            return {}
    
    def log_agent_decision(self, ticket_id: str, session_id: str, agent_name: str,
                          decision_type: str, decision_data: Dict[str, Any],
                          input_data: Dict[str, Any] = None, confidence_score: float = None,
                          processing_time_ms: float = None, success: str = "success",
                          error_message: str = None) -> str:
        """
        Log agent decision for analysis and debugging
        
        Args:
            ticket_id: Associated ticket ID
            session_id: Session identifier
            agent_name: Name of the agent making the decision
            decision_type: Type of decision (classification, routing, etc.)
            decision_data: The actual decision data
            input_data: Input received by the agent
            confidence_score: Confidence in the decision
            processing_time_ms: Processing time in milliseconds
            success: Success status
            error_message: Error message if failed
            
        Returns:
            log_id: Unique identifier for the log entry
        """
        log_id = str(uuid.uuid4())
        
        try:
            with get_session(self.engine) as session:
                log_entry = AgentDecisionLog(
                    log_id=log_id,
                    ticket_id=ticket_id,
                    session_id=session_id,
                    agent_name=agent_name,
                    decision_type=decision_type,
                    decision_data=decision_data,
                    input_data=input_data,
                    confidence_score=confidence_score,
                    processing_time_ms=processing_time_ms,
                    success=success,
                    error_message=error_message
                )
                session.add(log_entry)
                session.commit()
                
            return log_id
            
        except Exception as e:
            print(f"Error logging agent decision: {e}")
            return ""
    
    def get_agent_logs(self, ticket_id: str = None, agent_name: str = None,
                      limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieve agent decision logs for analysis
        
        Args:
            ticket_id: Filter by specific ticket
            agent_name: Filter by specific agent
            limit: Maximum number of logs to retrieve
            
        Returns:
            List of agent decision logs
        """
        try:
            with get_session(self.engine) as session:
                query = session.query(AgentDecisionLog)
                
                if ticket_id:
                    query = query.filter_by(ticket_id=ticket_id)
                if agent_name:
                    query = query.filter_by(agent_name=agent_name)
                
                logs = query.order_by(AgentDecisionLog.created_at.desc())\
                    .limit(limit)\
                    .all()
                
                log_list = []
                for log in logs:
                    log_list.append({
                        'log_id': log.log_id,
                        'ticket_id': log.ticket_id,
                        'session_id': log.session_id,
                        'agent_name': log.agent_name,
                        'decision_type': log.decision_type,
                        'decision_data': log.decision_data,
                        'input_data': log.input_data,
                        'confidence_score': log.confidence_score,
                        'processing_time_ms': log.processing_time_ms,
                        'success': log.success,
                        'error_message': log.error_message,
                        'created_at': log.created_at.isoformat() if log.created_at else None
                    })
                
                return log_list
                
        except Exception as e:
            print(f"Error retrieving agent logs: {e}")
            return []
    
    def generate_personalized_context(self, user_id: str, account_id: str = "cultpass") -> Dict[str, Any]:
        """
        Generate personalized context based on customer history and preferences
        
        Args:
            user_id: Customer user ID
            account_id: Account identifier
            
        Returns:
            Personalized context for agents to use
        """
        try:
            # Get recent interaction history
            recent_history = self.retrieve_customer_history(user_id, account_id, limit=5)
            
            # Get customer preferences
            preferences = self.get_customer_preferences(user_id, account_id)
            
            # Analyze patterns
            context = {
                'user_id': user_id,
                'account_id': account_id,
                'recent_interactions': len(recent_history),
                'preferences': preferences,
                'patterns': self._analyze_interaction_patterns(recent_history),
                'recommended_approach': self._recommend_approach(recent_history, preferences)
            }
            
            return context
            
        except Exception as e:
            print(f"Error generating personalized context: {e}")
            return {'user_id': user_id, 'account_id': account_id, 'error': str(e)}
    
    def _analyze_interaction_patterns(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in customer interaction history"""
        if not history:
            return {}
        
        patterns = {
            'most_common_issues': {},
            'resolution_success_rate': 0,
            'escalation_rate': 0,
            'average_confidence': 0,
            'preferred_resolution_types': {}
        }
        
        total_interactions = len(history)
        successful_resolutions = 0
        escalations = 0
        confidence_sum = 0
        confidence_count = 0
        
        for interaction in history:
            # Track outcomes
            outcome = interaction.get('outcome', 'unknown')
            if outcome == 'resolved':
                successful_resolutions += 1
            elif outcome == 'escalated':
                escalations += 1
            
            # Track confidence scores
            confidence = interaction.get('confidence_score')
            if confidence is not None:
                confidence_sum += confidence
                confidence_count += 1
            
            # Track issue types
            classification = interaction.get('classification_result', {})
            if isinstance(classification, dict):
                category = classification.get('category', 'unknown')
                patterns['most_common_issues'][category] = patterns['most_common_issues'].get(category, 0) + 1
        
        patterns['resolution_success_rate'] = successful_resolutions / total_interactions if total_interactions > 0 else 0
        patterns['escalation_rate'] = escalations / total_interactions if total_interactions > 0 else 0
        patterns['average_confidence'] = confidence_sum / confidence_count if confidence_count > 0 else 0
        
        return patterns
    
    def _recommend_approach(self, history: List[Dict[str, Any]], preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend approach based on history and preferences"""
        recommendations = {
            'confidence_threshold': 0.5,  # Default
            'preferred_tools': [],
            'communication_style': 'standard',
            'escalation_preference': 'moderate'
        }
        
        # Adjust based on history patterns
        if history:
            patterns = self._analyze_interaction_patterns(history)
            
            # If customer has high escalation rate, be more careful
            if patterns.get('escalation_rate', 0) > 0.3:
                recommendations['confidence_threshold'] = 0.7
                recommendations['escalation_preference'] = 'quick'
            
            # If customer has high success rate, can be more confident
            if patterns.get('resolution_success_rate', 0) > 0.8:
                recommendations['confidence_threshold'] = 0.4
        
        # Incorporate explicit preferences
        if 'communication' in preferences:
            comm_prefs = preferences['communication']
            if 'style' in comm_prefs:
                recommendations['communication_style'] = comm_prefs['style']['value']
        
        if 'escalation' in preferences:
            esc_prefs = preferences['escalation']
            if 'threshold' in esc_prefs:
                recommendations['escalation_preference'] = esc_prefs['threshold']['value']
        
        return recommendations
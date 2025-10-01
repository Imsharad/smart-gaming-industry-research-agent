"""
Account Lookup Tool - Database abstraction for CultPass customer account operations
"""
import os
from typing import Dict, Any, Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_core.tools import tool
import sys

# Add the parent directory to the path to import models
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from data.models.cultpass import User, Subscription, Reservation, Experience
from utils.path_utils import get_external_db_path


class AccountLookupTool:
    """Tool for looking up CultPass customer account information"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = get_external_db_path()
        
        # Ensure we have an absolute path
        db_path = os.path.abspath(db_path)
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.Session = sessionmaker(bind=self.engine)
    
    def lookup_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Look up user account by email address"""
        try:
            with self.Session() as session:
                user = session.query(User).filter(User.email == email).first()
                if not user:
                    return None
                
                # Get subscription info
                subscription = session.query(Subscription).filter(
                    Subscription.user_id == user.user_id
                ).first()
                
                # Get recent reservations
                recent_reservations = session.query(Reservation).filter(
                    Reservation.user_id == user.user_id
                ).order_by(Reservation.created_at.desc()).limit(5).all()
                
                return {
                    "user_id": user.user_id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "is_blocked": user.is_blocked,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "subscription": {
                        "subscription_id": subscription.subscription_id if subscription else None,
                        "status": subscription.status if subscription else "No active subscription",
                        "tier": subscription.tier if subscription else None,
                        "monthly_quota": subscription.monthly_quota if subscription else None,
                        "started_at": subscription.started_at.isoformat() if subscription and subscription.started_at else None,
                        "ended_at": subscription.ended_at.isoformat() if subscription and subscription.ended_at else None,
                    },
                    "recent_reservations_count": len(recent_reservations),
                    "recent_reservations": [
                        {
                            "reservation_id": res.reservation_id,
                            "experience_id": res.experience_id,
                            "status": res.status,
                            "created_at": res.created_at.isoformat() if res.created_at else None
                        } for res in recent_reservations
                    ]
                }
        except Exception as e:
            return {"error": f"Database error: {str(e)}"}
    
    def lookup_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Look up user account by user ID"""
        try:
            with self.Session() as session:
                user = session.query(User).filter(User.user_id == user_id).first()
                if not user:
                    return None
                
                return self.lookup_user_by_email(user.email)
        except Exception as e:
            return {"error": f"Database error: {str(e)}"}
    
    def get_user_reservation_history(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get detailed reservation history for a user"""
        try:
            with self.Session() as session:
                reservations = session.query(Reservation, Experience).join(
                    Experience, Reservation.experience_id == Experience.experience_id
                ).filter(
                    Reservation.user_id == user_id
                ).order_by(Reservation.created_at.desc()).limit(limit).all()
                
                return [
                    {
                        "reservation_id": res.reservation_id,
                        "status": res.status,
                        "created_at": res.created_at.isoformat() if res.created_at else None,
                        "experience": {
                            "experience_id": exp.experience_id,
                            "title": exp.title,
                            "description": exp.description,
                            "location": exp.location,
                            "when": exp.when.isoformat() if exp.when else None,
                            "is_premium": exp.is_premium
                        }
                    } for res, exp in reservations
                ]
        except Exception as e:
            return [{"error": f"Database error: {str(e)}"}]


# Initialize the tool instance
account_tool = AccountLookupTool()


@tool
def lookup_user_account(email_or_id: str) -> str:
    """
    Look up a CultPass user account by email address or user ID.
    
    Args:
        email_or_id: User email address or user ID to look up
        
    Returns:
        JSON string with user account information including subscription status and recent activity
    """
    # Determine if input is email or ID
    if "@" in email_or_id:
        result = account_tool.lookup_user_by_email(email_or_id)
    else:
        result = account_tool.lookup_user_by_id(email_or_id)
    
    if result is None:
        return f"No user found with email/ID: {email_or_id}"
    
    if "error" in result:
        return f"Error looking up user: {result['error']}"
    
    # Format the response for better readability
    response = f"""
User Account Information:
- Name: {result['full_name']}
- Email: {result['email']}
- User ID: {result['user_id']}
- Account Status: {'Blocked' if result['is_blocked'] else 'Active'}
- Member Since: {result['created_at'][:10] if result['created_at'] else 'Unknown'}

Subscription Details:
- Status: {result['subscription']['status']}
- Tier: {result['subscription']['tier'] or 'N/A'}
- Monthly Quota: {result['subscription']['monthly_quota'] or 'N/A'} experiences
- Started: {result['subscription']['started_at'][:10] if result['subscription']['started_at'] else 'N/A'}
- Ends: {result['subscription']['ended_at'][:10] if result['subscription']['ended_at'] else 'Active'}

Activity:
- Recent Reservations: {result['recent_reservations_count']}
"""
    
    if result['recent_reservations']:
        response += "\nRecent Reservations:\n"
        for res in result['recent_reservations'][:3]:  # Show top 3
            response += f"  - {res['reservation_id']} ({res['status']}) on {res['created_at'][:10]}\n"
    
    return response


@tool
def get_reservation_history(user_id: str, limit: str = "5") -> str:
    """
    Get detailed reservation history for a user.
    
    Args:
        user_id: The user ID to get reservation history for
        limit: Number of reservations to return (default: 5, max: 20)
        
    Returns:
        Formatted string with detailed reservation history
    """
    try:
        limit_int = min(int(limit), 20)  # Cap at 20 for performance
    except ValueError:
        limit_int = 5
    
    reservations = account_tool.get_user_reservation_history(user_id, limit_int)
    
    if not reservations:
        return f"No reservations found for user ID: {user_id}"
    
    if reservations and "error" in reservations[0]:
        return f"Error retrieving reservations: {reservations[0]['error']}"
    
    response = f"Reservation History for User {user_id}:\n\n"
    
    for i, res in enumerate(reservations, 1):
        exp = res['experience']
        response += f"{i}. {exp['title']}\n"
        response += f"   Location: {exp['location']}\n"
        response += f"   When: {exp['when'][:16] if exp['when'] else 'TBD'}\n"
        response += f"   Status: {res['status']}\n"
        response += f"   Reserved: {res['created_at'][:10] if res['created_at'] else 'Unknown'}\n"
        response += f"   Premium: {'Yes' if exp['is_premium'] else 'No'}\n\n"
    
    return response
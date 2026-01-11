"""
Subscription Management Tool - Database abstraction for CultPass subscription operations
"""
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from langchain_core.tools import tool
import sys

# Add the parent directory to the path to import models
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from data.models.cultpass import User, Subscription


class SubscriptionManagementTool:
    """Tool for managing CultPass subscription operations"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            from utils.path_utils import get_external_db_path
            db_path = get_external_db_path()
        
        # Ensure we have an absolute path
        db_path = os.path.abspath(db_path)
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        self.Session = sessionmaker(bind=self.engine)
    
    def pause_subscription(self, user_id: str, reason: str = "User requested") -> Dict[str, Any]:
        """Pause a user's subscription"""
        try:
            with self.Session() as session:
                # Find the user and subscription
                user = session.query(User).filter(User.user_id == user_id).first()
                if not user:
                    return {"success": False, "error": f"User not found: {user_id}"}
                
                subscription = session.query(Subscription).filter(
                    Subscription.user_id == user_id
                ).first()
                
                if not subscription:
                    return {"success": False, "error": f"No subscription found for user: {user_id}"}
                
                if subscription.status == "paused":
                    return {"success": False, "error": "Subscription is already paused"}
                
                if subscription.status == "cancelled":
                    return {"success": False, "error": "Cannot pause a cancelled subscription"}
                
                # Update subscription status
                subscription.status = "paused"
                subscription.updated_at = datetime.now()
                
                session.commit()
                
                return {
                    "success": True,
                    "message": f"Subscription {subscription.subscription_id} has been paused",
                    "subscription_id": subscription.subscription_id,
                    "previous_status": "active",
                    "new_status": "paused",
                    "reason": reason,
                    "user_name": user.full_name,
                    "user_email": user.email
                }
        except Exception as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    def resume_subscription(self, user_id: str) -> Dict[str, Any]:
        """Resume a paused subscription"""
        try:
            with self.Session() as session:
                # Find the user and subscription
                user = session.query(User).filter(User.user_id == user_id).first()
                if not user:
                    return {"success": False, "error": f"User not found: {user_id}"}
                
                subscription = session.query(Subscription).filter(
                    Subscription.user_id == user_id
                ).first()
                
                if not subscription:
                    return {"success": False, "error": f"No subscription found for user: {user_id}"}
                
                if subscription.status != "paused":
                    return {"success": False, "error": f"Subscription is not paused (current status: {subscription.status})"}
                
                # Update subscription status
                subscription.status = "active"
                subscription.updated_at = datetime.now()
                
                session.commit()
                
                return {
                    "success": True,
                    "message": f"Subscription {subscription.subscription_id} has been resumed",
                    "subscription_id": subscription.subscription_id,
                    "previous_status": "paused",
                    "new_status": "active",
                    "user_name": user.full_name,
                    "user_email": user.email,
                    "monthly_quota": subscription.monthly_quota
                }
        except Exception as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    def cancel_subscription(self, user_id: str, reason: str = "User requested") -> Dict[str, Any]:
        """Cancel a user's subscription"""
        try:
            with self.Session() as session:
                # Find the user and subscription
                user = session.query(User).filter(User.user_id == user_id).first()
                if not user:
                    return {"success": False, "error": f"User not found: {user_id}"}
                
                subscription = session.query(Subscription).filter(
                    Subscription.user_id == user_id
                ).first()
                
                if not subscription:
                    return {"success": False, "error": f"No subscription found for user: {user_id}"}
                
                if subscription.status == "cancelled":
                    return {"success": False, "error": "Subscription is already cancelled"}
                
                # Set end date to end of current billing cycle (30 days from now)
                end_date = datetime.now() + timedelta(days=30)
                
                # Update subscription
                subscription.status = "cancelled"
                subscription.ended_at = end_date
                subscription.updated_at = datetime.now()
                
                session.commit()
                
                return {
                    "success": True,
                    "message": f"Subscription {subscription.subscription_id} has been cancelled",
                    "subscription_id": subscription.subscription_id,
                    "previous_status": "active",
                    "new_status": "cancelled",
                    "end_date": end_date.isoformat(),
                    "reason": reason,
                    "user_name": user.full_name,
                    "user_email": user.email,
                    "note": "Subscription will remain active until the end of the billing cycle"
                }
        except Exception as e:
            return {"success": False, "error": f"Database error: {str(e)}"}
    
    def upgrade_subscription(self, user_id: str, new_tier: str) -> Dict[str, Any]:
        """Upgrade a user's subscription tier"""
        valid_tiers = {"basic": 4, "premium": 8, "unlimited": 999}
        
        if new_tier.lower() not in valid_tiers:
            return {"success": False, "error": f"Invalid tier: {new_tier}. Valid tiers: {list(valid_tiers.keys())}"}
        
        try:
            with self.Session() as session:
                # Find the user and subscription
                user = session.query(User).filter(User.user_id == user_id).first()
                if not user:
                    return {"success": False, "error": f"User not found: {user_id}"}
                
                subscription = session.query(Subscription).filter(
                    Subscription.user_id == user_id
                ).first()
                
                if not subscription:
                    return {"success": False, "error": f"No subscription found for user: {user_id}"}
                
                if subscription.status not in ["active", "paused"]:
                    return {"success": False, "error": f"Cannot upgrade {subscription.status} subscription"}
                
                old_tier = subscription.tier
                old_quota = subscription.monthly_quota
                
                # Update subscription
                subscription.tier = new_tier.lower()
                subscription.monthly_quota = valid_tiers[new_tier.lower()]
                subscription.updated_at = datetime.now()
                
                session.commit()
                
                return {
                    "success": True,
                    "message": f"Subscription upgraded from {old_tier} to {new_tier}",
                    "subscription_id": subscription.subscription_id,
                    "previous_tier": old_tier,
                    "new_tier": new_tier.lower(),
                    "previous_quota": old_quota,
                    "new_quota": subscription.monthly_quota,
                    "user_name": user.full_name,
                    "user_email": user.email
                }
        except Exception as e:
            return {"success": False, "error": f"Database error: {str(e)}"}


# Initialize the tool instance
subscription_tool = SubscriptionManagementTool()


@tool
def pause_user_subscription(user_id: str, reason: str = "Customer request") -> str:
    """
    Pause a user's CultPass subscription.
    
    Args:
        user_id: The user ID whose subscription to pause
        reason: Reason for pausing (optional)
        
    Returns:
        Status message about the pause operation
    """
    result = subscription_tool.pause_subscription(user_id, reason)
    
    if result["success"]:
        return f"""
Subscription Successfully Paused:
- User: {result['user_name']} ({result['user_email']})
- Subscription ID: {result['subscription_id']}
- Status: {result['previous_status']} → {result['new_status']}
- Reason: {result['reason']}

The subscription is now paused and will not be charged. User can resume anytime through their account or by contacting support.
"""
    else:
        return f"Failed to pause subscription: {result['error']}"


@tool
def resume_user_subscription(user_id: str) -> str:
    """
    Resume a paused CultPass subscription.
    
    Args:
        user_id: The user ID whose subscription to resume
        
    Returns:
        Status message about the resume operation
    """
    result = subscription_tool.resume_subscription(user_id)
    
    if result["success"]:
        return f"""
Subscription Successfully Resumed:
- User: {result['user_name']} ({result['user_email']})
- Subscription ID: {result['subscription_id']}
- Status: {result['previous_status']} → {result['new_status']}
- Monthly Quota: {result['monthly_quota']} experiences

The subscription is now active and the user can start making reservations again.
"""
    else:
        return f"Failed to resume subscription: {result['error']}"


@tool
def cancel_user_subscription(user_id: str, reason: str = "Customer request") -> str:
    """
    Cancel a user's CultPass subscription.
    
    Args:
        user_id: The user ID whose subscription to cancel
        reason: Reason for cancellation (optional)
        
    Returns:
        Status message about the cancellation
    """
    result = subscription_tool.cancel_subscription(user_id, reason)
    
    if result["success"]:
        return f"""
Subscription Successfully Cancelled:
- User: {result['user_name']} ({result['user_email']})
- Subscription ID: {result['subscription_id']}
- Status: {result['previous_status']} → {result['new_status']}
- End Date: {result['end_date'][:10]}
- Reason: {result['reason']}

{result['note']}
"""
    else:
        return f"Failed to cancel subscription: {result['error']}"


@tool
def upgrade_user_subscription(user_id: str, new_tier: str) -> str:
    """
    Upgrade a user's CultPass subscription tier.
    
    Args:
        user_id: The user ID whose subscription to upgrade
        new_tier: New tier (basic, premium, unlimited)
        
    Returns:
        Status message about the upgrade
    """
    result = subscription_tool.upgrade_subscription(user_id, new_tier)
    
    if result["success"]:
        return f"""
Subscription Successfully Upgraded:
- User: {result['user_name']} ({result['user_email']})
- Subscription ID: {result['subscription_id']}
- Tier: {result['previous_tier']} → {result['new_tier']}
- Monthly Quota: {result['previous_quota']} → {result['new_quota']} experiences

The upgrade is effective immediately. User can now access {result['new_quota']} experiences per month.
"""
    else:
        return f"Failed to upgrade subscription: {result['error']}"
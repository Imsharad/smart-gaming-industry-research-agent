import enum
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Enum,
    ForeignKey,
    UniqueConstraint,
    JSON,
    Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.decl_api import DeclarativeBase
from sqlalchemy.sql import func


Base:DeclarativeBase = declarative_base()

class Account(Base):
    __tablename__ = 'accounts'
    account_id = Column(String, primary_key=True)
    account_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    users = relationship("User", back_populates="account")
    tickets = relationship("Ticket", back_populates="account")
    knowledge_articles = relationship("Knowledge", back_populates="account")

    def __repr__(self):
        return f"<Account(account_id='{self.account_id}', account_name='{self.account_name}')>"


class User(Base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey('accounts.account_id'), nullable=False)
    external_user_id = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    account = relationship("Account", back_populates="users")
    tickets = relationship("Ticket", back_populates="user")

    __table_args__ = (
        UniqueConstraint('account_id', 'external_user_id', name='uq_user_external_per_account'),
    )

    def __repr__(self):
        return f"<User(user_id='{self.user_id}', user_name='{self.user_name}', external_user_id='{self.external_user_id}')>"



class Ticket(Base):
    __tablename__ = 'tickets'
    ticket_id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey('accounts.account_id'), nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    channel = Column(String)
    created_at = Column(DateTime, default=func.now())

    account = relationship("Account", back_populates="tickets")
    user = relationship("User", back_populates="tickets")
    ticket_metadata = relationship("TicketMetadata", uselist=False, back_populates="ticket")
    messages = relationship("TicketMessage", back_populates="ticket")

    def __repr__(self):
        return f"<Ticket(ticket_id='{self.ticket_id}', channel='{self.channel}', created_at='{self.created_at}')>"


class TicketMetadata(Base):
    __tablename__ = 'ticket_metadata'
    ticket_id = Column(String, ForeignKey('tickets.ticket_id'), primary_key=True)
    status = Column(String, nullable=False)
    main_issue_type = Column(String)
    tags = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    ticket = relationship("Ticket", back_populates="ticket_metadata")

    def __repr__(self):
        return f"<TicketMetadata(ticket_id='{self.ticket_id}', status='{self.status}', issue_type='{self.main_issue_type}')>"


class RoleEnum(enum.Enum):
    user = "user"
    agent = "agent"
    ai = "ai"
    system = "system"


class TicketMessage(Base):
    __tablename__ = 'ticket_messages'
    message_id = Column(String, primary_key=True)
    ticket_id = Column(String, ForeignKey('tickets.ticket_id'), nullable=False)
    role = Column(Enum(RoleEnum, name="role_enum"), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())

    ticket = relationship("Ticket", back_populates="messages")

    def __repr__(self):
        short_content = (self.content[:30] + "...") if self.content and len(self.content) > 30 else self.content
        return f"<TicketMessage(message_id='{self.message_id}', role='{self.role.name}', content='{short_content}')>"


class Knowledge(Base):
    __tablename__ = 'knowledge'
    article_id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey('accounts.account_id'), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    account = relationship("Account", back_populates="knowledge_articles")

    def __repr__(self):
        return f"<Knowledge(article_id='{self.article_id}', title='{self.title}')>"


class InteractionHistory(Base):
    """Persistent storage for customer interaction history across sessions"""
    __tablename__ = 'interaction_history'
    
    history_id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey('accounts.account_id'), nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    session_id = Column(String, nullable=False)
    ticket_id = Column(String, ForeignKey('tickets.ticket_id'), nullable=True)
    
    interaction_type = Column(String, nullable=False)  # 'ticket_resolution', 'escalation', 'tool_usage'
    classification_result = Column(JSON)  # Store classification data
    resolution_result = Column(JSON)     # Store resolution data
    tools_used = Column(JSON)            # List of tools used
    knowledge_articles_used = Column(JSON)  # List of articles referenced
    
    outcome = Column(String, nullable=False)  # 'resolved', 'escalated', 'partial'
    confidence_score = Column(Float)
    customer_satisfaction = Column(Float, nullable=True)  # If available
    
    interaction_summary = Column(Text)    # Brief summary for quick reference
    full_context = Column(JSON)          # Complete interaction context
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    account = relationship("Account")
    user = relationship("User")
    ticket = relationship("Ticket")
    
    def __repr__(self):
        return f"<InteractionHistory(history_id='{self.history_id}', user_id='{self.user_id}', outcome='{self.outcome}')>"


class CustomerPreference(Base):
    """Long-term memory for customer preferences and behavioral patterns"""
    __tablename__ = 'customer_preferences'
    
    preference_id = Column(String, primary_key=True)
    account_id = Column(String, ForeignKey('accounts.account_id'), nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    
    preference_type = Column(String, nullable=False)  # 'communication', 'resolution', 'escalation'
    preference_key = Column(String, nullable=False)   # 'preferred_channel', 'escalation_threshold'
    preference_value = Column(JSON, nullable=False)   # Flexible storage for preference data
    
    confidence_level = Column(Float, default=1.0)    # How confident we are in this preference
    last_reinforced = Column(DateTime, default=func.now())  # When this preference was last observed
    times_observed = Column(String, default="1")     # How many times we've seen this pattern
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    account = relationship("Account")
    user = relationship("User")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'preference_type', 'preference_key', 
                        name='uq_customer_preference'),
    )
    
    def __repr__(self):
        return f"<CustomerPreference(user_id='{self.user_id}', type='{self.preference_type}', key='{self.preference_key}')>"


class AgentDecisionLog(Base):
    """Structured logging for agent decisions and actions"""
    __tablename__ = 'agent_decision_log'
    
    log_id = Column(String, primary_key=True)
    ticket_id = Column(String, ForeignKey('tickets.ticket_id'), nullable=False)
    session_id = Column(String, nullable=False)
    
    agent_name = Column(String, nullable=False)      # 'classifier', 'resolver', 'supervisor', 'escalation'
    decision_type = Column(String, nullable=False)   # 'classification', 'routing', 'escalation', 'resolution'
    decision_data = Column(JSON, nullable=False)     # The actual decision/output
    
    input_data = Column(JSON)                        # What the agent received as input
    confidence_score = Column(Float)                 # Agent's confidence in the decision
    processing_time_ms = Column(Float)               # How long the decision took
    
    success = Column(String, nullable=False)         # 'success', 'partial', 'failure'
    error_message = Column(Text, nullable=True)      # If there was an error
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    ticket = relationship("Ticket")
    
    def __repr__(self):
        return f"<AgentDecisionLog(agent='{self.agent_name}', decision='{self.decision_type}', success='{self.success}')>"

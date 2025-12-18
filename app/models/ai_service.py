"""
AI/LLM service models
For explanations, recommendations, and chat interactions
"""
from sqlalchemy import Column, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class AIConversation(BaseModel):
    """AI conversation thread"""
    __tablename__ = "ai_conversations"
    
    title = Column(String(200))
    context_type = Column(String(50))  # e.g., "geofence", "asset", "zone", "general"
    context_id = Column(String(36))  # UUID of related entity
    
    # Relationships
    messages = relationship("AIMessage", back_populates="conversation", cascade="all, delete-orphan", order_by="AIMessage.created_at")
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    def __repr__(self):
        return f"<AIConversation {self.title}>"


class AIMessage(BaseModel):
    """Individual AI message in a conversation"""
    __tablename__ = "ai_messages"
    
    conversation_id = Column(ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    message_metadata = Column(JSON)  # Additional metadata (model used, tokens, etc.)
    
    # Relationships
    conversation = relationship("AIConversation", back_populates="messages")
    
    def __repr__(self):
        return f"<AIMessage {self.role} in {self.conversation_id}>"


class AIRecommendation(BaseModel):
    """AI-generated recommendations"""
    __tablename__ = "ai_recommendations"
    
    recommendation_type = Column(String(50), nullable=False)  # e.g., "geofence_optimization", "security_alert"
    entity_type = Column(String(50))  # e.g., "geofence", "asset"
    entity_id = Column(String(36))  # UUID of related entity
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    confidence_score = Column(String(20))  # 0.0-1.0
    status = Column(String(20), default="pending")  # pending, accepted, rejected, implemented
    recommendation_metadata = Column(JSON)
    
    def __repr__(self):
        return f"<AIRecommendation {self.title}>"


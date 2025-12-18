"""
AI/LLM service schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class AIMessageCreate(BaseModel):
    """AI message creation"""
    conversation_id: Optional[str] = None
    content: str = Field(..., min_length=1, description="Message content")
    context_type: Optional[str] = Field(None, description="Context: geofence, asset, zone, general")
    context_id: Optional[str] = Field(None, description="ID of related entity")
    metadata: Optional[Dict[str, Any]] = None


class AIMessageResponse(BaseModel):
    """AI message response"""
    id: str
    conversation_id: str
    role: str
    content: str
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True


class AIConversationResponse(BaseModel):
    """AI conversation response"""
    id: str
    title: Optional[str]
    context_type: Optional[str]
    context_id: Optional[str]
    user_id: str
    messages: List[AIMessageResponse] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AIRecommendationResponse(BaseModel):
    """AI recommendation response"""
    id: str
    recommendation_type: str
    entity_type: Optional[str]
    entity_id: Optional[str]
    title: str
    description: str
    confidence_score: Optional[str]
    status: str
    recommendation_metadata: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


"""
AI/LLM Service Router
REST-compliant endpoints for AI interactions
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.core.database import get_db
from app.core.dependencies import AuthDependency, require_read, require_write
from app.models.user import User
from app.schemas.ai_service import AIMessageCreate, AIMessageResponse, AIConversationResponse, AIRecommendationResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/ai", tags=["AI Service"])


def _message_to_response(message) -> AIMessageResponse:
    """Convert message model to response schema"""
    return AIMessageResponse(
        id=str(message.id),
        conversation_id=str(message.conversation_id),
        role=message.role,
        content=message.content,
        message_metadata=message.message_metadata,
        created_at=message.created_at
    )


@router.post("/chat", response_model=dict)
async def send_ai_message(
    message_data: AIMessageCreate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Send a message to AI and get response"""
    user_msg, ai_msg = AIService.send_message(db, message_data, current_user.id)
    return {
        "user_message": _message_to_response(user_msg),
        "ai_message": _message_to_response(ai_msg),
        "conversation_id": str(user_msg.conversation_id)
    }


@router.get("/conversations", response_model=list[AIConversationResponse])
async def list_conversations(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    current_user: User = Depends(require_read),
    db: Session = Depends(get_db)
):
    """List user's AI conversations"""
    skip = (page - 1) * per_page
    conversations, total = AIService.list_conversations(db, current_user.id, skip, per_page)
    
    result = []
    for conv in conversations:
        messages = [_message_to_response(m) for m in conv.messages]
        result.append(AIConversationResponse(
            id=str(conv.id),
            title=conv.title,
            context_type=conv.context_type,
            context_id=conv.context_id,
            user_id=str(conv.user_id),
            messages=messages,
            created_at=conv.created_at,
            updated_at=conv.updated_at
        ))
    
    return result


@router.get("/conversations/{conversation_id}", response_model=AIConversationResponse)
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(require_read),
    db: Session = Depends(get_db)
):
    """Get conversation with messages"""
    conversation = AIService.get_conversation(db, UUID(conversation_id))
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if str(conversation.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    messages = [_message_to_response(m) for m in conversation.messages]
    return AIConversationResponse(
        id=str(conversation.id),
        title=conversation.title,
        context_type=conversation.context_type,
        context_id=conversation.context_id,
        user_id=str(conversation.user_id),
        messages=messages,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at
    )


@router.post("/recommendations", response_model=AIRecommendationResponse)
async def generate_recommendation(
    entity_type: str = Query(...),
    entity_id: str = Query(...),
    recommendation_type: str = Query(...),
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Generate AI recommendation for an entity"""
    recommendation = AIService.generate_recommendation(
        db, entity_type, entity_id, recommendation_type, {}
    )
    
    return AIRecommendationResponse(
        id=str(recommendation.id),
        recommendation_type=recommendation.recommendation_type,
        entity_type=recommendation.entity_type,
        entity_id=recommendation.entity_id,
        title=recommendation.title,
        description=recommendation.description,
        confidence_score=recommendation.confidence_score,
        status=recommendation.status,
        recommendation_metadata=recommendation.recommendation_metadata,
        created_at=recommendation.created_at,
        updated_at=recommendation.updated_at
    )


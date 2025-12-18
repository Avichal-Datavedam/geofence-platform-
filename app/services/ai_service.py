"""
AI/LLM Service
Single Responsibility: Handle AI interactions, explanations, and recommendations
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from uuid import UUID
import openai
from app.models.ai_service import AIConversation, AIMessage, AIRecommendation
from app.schemas.ai_service import AIMessageCreate
from app.core.config import get_settings

settings = get_settings()

if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY


class AIService:
    """Service for AI/LLM operations"""
    
    @staticmethod
    def create_conversation(
        db: Session,
        user_id: UUID,
        context_type: Optional[str] = None,
        context_id: Optional[str] = None,
        title: Optional[str] = None
    ) -> AIConversation:
        """Create a new AI conversation"""
        conversation = AIConversation(
            title=title or "New Conversation",
            context_type=context_type,
            context_id=str(context_id) if context_id else None,
            user_id=user_id
        )
        
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    
    @staticmethod
    def send_message(
        db: Session,
        message_data: AIMessageCreate,
        user_id: UUID
    ) -> tuple[AIMessage, AIMessage]:
        """Send a message to AI and get response"""
        # Get or create conversation
        if message_data.conversation_id:
            conversation = db.query(AIConversation).filter(
                AIConversation.id == UUID(message_data.conversation_id)
            ).first()
        else:
            conversation = AIService.create_conversation(
                db,
                user_id,
                message_data.context_type,
                message_data.context_id
            )
        
        if not conversation:
            raise ValueError("Conversation not found")
        
        # Save user message
        user_message = AIMessage(
            conversation_id=conversation.id,
            role="user",
            content=message_data.content,
            message_metadata=message_data.metadata
        )
        db.add(user_message)
        db.flush()
        
        # Get AI response
        if settings.AI_SERVICE_ENABLED and settings.OPENAI_API_KEY:
            ai_response_content = AIService._get_ai_response(
                db,
                conversation,
                message_data.content
            )
        else:
            ai_response_content = "AI service is currently unavailable."
        
        # Save AI message
        ai_message = AIMessage(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response_content,
            message_metadata={"model": settings.AI_MODEL}
        )
        db.add(ai_message)
        db.commit()
        db.refresh(user_message)
        db.refresh(ai_message)
        
        return user_message, ai_message
    
    @staticmethod
    def _get_ai_response(
        db: Session,
        conversation: AIConversation,
        user_message: str
    ) -> str:
        """Get AI response using OpenAI API"""
        # Get conversation history
        messages = db.query(AIMessage).filter(
            AIMessage.conversation_id == conversation.id
        ).order_by(AIMessage.created_at).all()
        
        # Build context
        system_prompt = "You are an AI assistant for a geo-fencing platform. Help users understand geofences, zones, assets, and provide recommendations."
        
        if conversation.context_type:
            system_prompt += f"\n\nContext: {conversation.context_type}"
            if conversation.context_id:
                system_prompt += f" (ID: {conversation.context_id})"
        
        message_history = [{"role": "system", "content": system_prompt}]
        
        for msg in messages:
            message_history.append({
                "role": msg.role,
                "content": msg.content
            })
        
        message_history.append({"role": "user", "content": user_message})
        
        try:
            response = openai.ChatCompletion.create(
                model=settings.AI_MODEL,
                messages=message_history,
                temperature=settings.AI_TEMPERATURE
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating AI response: {str(e)}"
    
    @staticmethod
    def generate_recommendation(
        db: Session,
        entity_type: str,
        entity_id: str,
        recommendation_type: str,
        context: Dict[str, Any]
    ) -> AIRecommendation:
        """Generate AI recommendation for an entity"""
        # Build prompt for recommendation
        prompt = f"Analyze this {entity_type} and provide recommendations for {recommendation_type}."
        prompt += f"\n\nContext: {context}"
        
        if settings.AI_SERVICE_ENABLED and settings.OPENAI_API_KEY:
            try:
                response = openai.ChatCompletion.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are an expert system analyst providing actionable recommendations."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5
                )
                ai_content = response.choices[0].message.content
            except Exception as e:
                ai_content = f"Recommendation generation failed: {str(e)}"
        else:
            ai_content = "AI service unavailable for recommendations."
        
        recommendation = AIRecommendation(
            recommendation_type=recommendation_type,
            entity_type=entity_type,
            entity_id=entity_id,
            title=f"Recommendation for {entity_type}",
            description=ai_content,
            confidence_score="0.7",
            recommendation_metadata=context
        )
        
        db.add(recommendation)
        db.commit()
        db.refresh(recommendation)
        return recommendation
    
    @staticmethod
    def get_conversation(db: Session, conversation_id: UUID) -> Optional[AIConversation]:
        """Get conversation with messages"""
        return db.query(AIConversation).filter(AIConversation.id == conversation_id).first()
    
    @staticmethod
    def list_conversations(
        db: Session,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> tuple[List[AIConversation], int]:
        """List user's conversations"""
        query = db.query(AIConversation).filter(AIConversation.user_id == user_id)
        total = query.count()
        conversations = query.order_by(AIConversation.updated_at.desc()).offset(skip).limit(limit).all()
        return conversations, total


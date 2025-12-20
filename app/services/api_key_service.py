"""
API Key Service
Business logic for API key management
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import UUID
from typing import List, Optional, Tuple
from datetime import datetime, timedelta

from app.models.api_key import APIKey, APIKeyScope
from app.schemas.api_key import APIKeyCreate, APIKeyUpdate, APIKeyPreset


class APIKeyService:
    """Service for managing API keys"""
    
    @staticmethod
    def get_scopes_for_preset(preset: APIKeyPreset, custom_scopes: Optional[List[str]] = None) -> List[str]:
        """Get scope list based on preset"""
        if preset == APIKeyPreset.READ_ONLY:
            return APIKeyScope.read_only()
        elif preset == APIKeyPreset.STANDARD:
            return APIKeyScope.standard()
        elif preset == APIKeyPreset.FULL_ACCESS:
            return APIKeyScope.full_access()
        elif preset == APIKeyPreset.ADMIN:
            return APIKeyScope.admin()
        elif preset == APIKeyPreset.CUSTOM and custom_scopes:
            return custom_scopes
        return APIKeyScope.read_only()
    
    @staticmethod
    def create_api_key(
        db: Session,
        data: APIKeyCreate,
        organization_id: UUID,
        created_by_id: UUID
    ) -> Tuple[APIKey, str]:
        """Create a new API key. Returns (api_key_model, full_key_string)"""
        # Generate the key
        full_key, prefix, key_hash = APIKey.generate_key()
        
        # Get scopes based on preset
        scopes = APIKeyService.get_scopes_for_preset(data.preset, data.custom_scopes)
        
        # Calculate expiration
        expires_at = None
        if data.expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=data.expires_in_days)
        
        api_key = APIKey(
            name=data.name,
            description=data.description,
            key_prefix=prefix,
            key_hash=key_hash,
            organization_id=organization_id,
            created_by_id=created_by_id,
            scopes=scopes,
            rate_limit_per_minute=str(data.rate_limit_per_minute),
            rate_limit_per_day=str(data.rate_limit_per_day),
            expires_at=expires_at,
            allowed_ips=data.allowed_ips
        )
        
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
        
        return api_key, full_key
    
    @staticmethod
    def validate_api_key(db: Session, key: str) -> Optional[APIKey]:
        """Validate an API key and return the model if valid"""
        if not key or not key.startswith("gfp_"):
            return None
        
        key_hash = APIKey.hash_key(key)
        api_key = db.query(APIKey).filter(APIKey.key_hash == key_hash).first()
        
        if not api_key or not api_key.is_valid():
            return None
        
        # Update last used timestamp
        api_key.last_used_at = datetime.utcnow()
        api_key.usage_count = str(int(api_key.usage_count or 0) + 1)
        db.commit()
        
        return api_key
    
    @staticmethod
    def get_api_key(db: Session, key_id: UUID) -> Optional[APIKey]:
        """Get API key by ID"""
        return db.query(APIKey).filter(APIKey.id == key_id).first()
    
    @staticmethod
    def list_api_keys(
        db: Session,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 20,
        include_inactive: bool = False
    ) -> Tuple[List[APIKey], int]:
        """List API keys for an organization"""
        query = db.query(APIKey).filter(APIKey.organization_id == organization_id)
        
        if not include_inactive:
            query = query.filter(APIKey.is_active == True)
        
        total = query.count()
        keys = query.order_by(APIKey.created_at.desc()).offset(skip).limit(limit).all()
        
        return keys, total
    
    @staticmethod
    def update_api_key(
        db: Session,
        key_id: UUID,
        organization_id: UUID,
        data: APIKeyUpdate
    ) -> Optional[APIKey]:
        """Update an API key"""
        api_key = db.query(APIKey).filter(
            and_(APIKey.id == key_id, APIKey.organization_id == organization_id)
        ).first()
        
        if not api_key:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "rate_limit_per_minute" or field == "rate_limit_per_day":
                value = str(value)
            setattr(api_key, field, value)
        
        db.commit()
        db.refresh(api_key)
        return api_key
    
    @staticmethod
    def revoke_api_key(db: Session, key_id: UUID, organization_id: UUID) -> bool:
        """Revoke (deactivate) an API key"""
        api_key = db.query(APIKey).filter(
            and_(APIKey.id == key_id, APIKey.organization_id == organization_id)
        ).first()
        
        if not api_key:
            return False
        
        api_key.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def delete_api_key(db: Session, key_id: UUID, organization_id: UUID) -> bool:
        """Permanently delete an API key"""
        api_key = db.query(APIKey).filter(
            and_(APIKey.id == key_id, APIKey.organization_id == organization_id)
        ).first()
        
        if not api_key:
            return False
        
        db.delete(api_key)
        db.commit()
        return True
    
    @staticmethod
    def check_scope(api_key: APIKey, required_scope: str) -> bool:
        """Check if API key has the required scope"""
        return api_key.has_scope(required_scope)
    
    @staticmethod
    def check_any_scope(api_key: APIKey, required_scopes: List[str]) -> bool:
        """Check if API key has any of the required scopes"""
        return api_key.has_any_scope(required_scopes)

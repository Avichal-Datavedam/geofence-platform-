"""
API Key Authentication Middleware
Supports both JWT tokens and API keys for multi-tenant access
"""
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from typing import Optional, List

from app.core.database import get_db
from app.services.api_key_service import APIKeyService
from app.models.api_key import APIKey, APIKeyScope


# API Key header scheme
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def get_api_key(
    api_key: Optional[str] = Depends(api_key_header),
    db: Session = Depends(get_db)
) -> Optional[APIKey]:
    """
    Validate API key from header and return the APIKey model.
    Returns None if no API key provided (allows fallback to JWT).
    """
    if not api_key:
        return None
    
    key = APIKeyService.validate_api_key(db, api_key)
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key",
            headers={"WWW-Authenticate": "API-Key"}
        )
    
    return key


def require_scope(required_scope: str):
    """
    Dependency that requires a specific scope.
    Use with API key authentication.
    """
    async def scope_checker(
        api_key: Optional[APIKey] = Depends(get_api_key)
    ):
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key required",
                headers={"WWW-Authenticate": "API-Key"}
            )
        
        if not api_key.has_scope(required_scope):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"API key missing required scope: {required_scope}"
            )
        
        return api_key
    
    return scope_checker


def require_any_scope(required_scopes: List[str]):
    """
    Dependency that requires any of the specified scopes.
    """
    async def scope_checker(
        api_key: Optional[APIKey] = Depends(get_api_key)
    ):
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API key required",
                headers={"WWW-Authenticate": "API-Key"}
            )
        
        if not api_key.has_any_scope(required_scopes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"API key missing required scopes. Need one of: {required_scopes}"
            )
        
        return api_key
    
    return scope_checker


# Pre-defined scope requirements
require_geofences_read = require_scope(APIKeyScope.READ_GEOFENCES)
require_geofences_write = require_scope(APIKeyScope.WRITE_GEOFENCES)
require_assets_read = require_scope(APIKeyScope.READ_ASSETS)
require_assets_write = require_scope(APIKeyScope.WRITE_ASSETS)
require_zones_read = require_scope(APIKeyScope.READ_ZONES)
require_zones_write = require_scope(APIKeyScope.WRITE_ZONES)
require_notifications_read = require_scope(APIKeyScope.READ_NOTIFICATIONS)
require_notifications_write = require_scope(APIKeyScope.WRITE_NOTIFICATIONS)
require_realtime_tracking = require_scope(APIKeyScope.REALTIME_TRACKING)
require_ai_access = require_scope(APIKeyScope.AI_ASSISTANT)
require_admin_users = require_scope(APIKeyScope.ADMIN_USERS)
require_admin_org = require_scope(APIKeyScope.ADMIN_ORGANIZATION)
require_admin_keys = require_scope(APIKeyScope.ADMIN_API_KEYS)


class APIKeyOrJWT:
    """
    Combined authentication that accepts either API key or JWT token.
    API key takes precedence if both are provided.
    """
    def __init__(self, required_scopes: Optional[List[str]] = None):
        self.required_scopes = required_scopes
    
    async def __call__(
        self,
        request: Request,
        api_key: Optional[APIKey] = Depends(get_api_key),
        db: Session = Depends(get_db)
    ):
        # If API key is provided and valid, use it
        if api_key:
            if self.required_scopes and not api_key.has_any_scope(self.required_scopes):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"API key missing required scopes"
                )
            return {
                "type": "api_key",
                "api_key": api_key,
                "organization_id": api_key.organization_id
            }
        
        # Fall back to JWT authentication
        from app.core.dependencies import get_current_user
        try:
            user = await get_current_user(request, db)
            return {
                "type": "jwt",
                "user": user,
                "organization_id": None  # User might have multiple orgs
            }
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Valid API key or JWT token required",
                headers={"WWW-Authenticate": "Bearer, API-Key"}
            )

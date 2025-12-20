"""
API Keys Router
Endpoints for managing API keys (multi-tenant)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from app.core.database import get_db
from app.core.dependencies import require_write, require_delete
from app.models.user import User
from app.models.api_key import APIKeyScope
from app.schemas.api_key import (
    APIKeyCreate,
    APIKeyUpdate,
    APIKeyResponse,
    APIKeyCreatedResponse,
    APIKeyListResponse,
    APIKeyValidation
)
from app.services.api_key_service import APIKeyService

router = APIRouter(prefix="/api-keys", tags=["API Keys"])


def _key_to_response(api_key) -> APIKeyResponse:
    """Convert API key model to response schema"""
    return APIKeyResponse(
        id=str(api_key.id),
        name=api_key.name,
        description=api_key.description,
        key_prefix=api_key.key_prefix,
        organization_id=str(api_key.organization_id),
        scopes=api_key.scopes or [],
        rate_limit_per_minute=int(api_key.rate_limit_per_minute or 100),
        rate_limit_per_day=int(api_key.rate_limit_per_day or 10000),
        is_active=api_key.is_active,
        expires_at=api_key.expires_at,
        last_used_at=api_key.last_used_at,
        usage_count=int(api_key.usage_count or 0),
        allowed_ips=api_key.allowed_ips,
        created_at=api_key.created_at,
        updated_at=api_key.updated_at
    )


@router.post("", response_model=APIKeyCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    data: APIKeyCreate,
    organization_id: str = Query(..., description="Organization ID to create key for"),
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """
    Create a new API key for an organization.
    
    **Important**: The full API key is only shown once in this response. Save it securely!
    
    **Presets**:
    - `read_only`: Can only read geofences, assets, zones, notifications
    - `standard`: Read + write for geofences, assets, zones
    - `full_access`: All read/write + realtime tracking, AI, webhooks
    - `admin`: Full access + user/org/key management
    - `custom`: Specify your own scopes
    """
    api_key, full_key = APIKeyService.create_api_key(
        db,
        data=data,
        organization_id=UUID(organization_id),
        created_by_id=current_user.id
    )
    
    response = _key_to_response(api_key)
    return APIKeyCreatedResponse(
        **response.model_dump(),
        api_key=full_key
    )


@router.get("", response_model=APIKeyListResponse)
async def list_api_keys(
    organization_id: str = Query(..., description="Organization ID"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    include_inactive: bool = Query(False),
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """List all API keys for an organization"""
    skip = (page - 1) * per_page
    keys, total = APIKeyService.list_api_keys(
        db,
        organization_id=UUID(organization_id),
        skip=skip,
        limit=per_page,
        include_inactive=include_inactive
    )
    
    return APIKeyListResponse(
        items=[_key_to_response(k) for k in keys],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/scopes", response_model=dict)
async def list_available_scopes():
    """List all available API key scopes and presets"""
    return {
        "scopes": {
            "read": {
                "geofences:read": "Read geofence data",
                "assets:read": "Read asset data",
                "zones:read": "Read zone data",
                "notifications:read": "Read notifications",
                "analytics:read": "Read analytics data"
            },
            "write": {
                "geofences:write": "Create/update/delete geofences",
                "assets:write": "Create/update/delete assets",
                "zones:write": "Create/update/delete zones",
                "notifications:write": "Manage notifications"
            },
            "admin": {
                "users:admin": "Manage users",
                "organization:admin": "Manage organization settings",
                "api_keys:admin": "Manage API keys"
            },
            "special": {
                "tracking:realtime": "Access realtime tracking WebSocket",
                "ai:access": "Use AI assistant features",
                "webhooks:manage": "Manage webhooks"
            }
        },
        "presets": {
            "read_only": APIKeyScope.read_only(),
            "standard": APIKeyScope.standard(),
            "full_access": APIKeyScope.full_access(),
            "admin": APIKeyScope.admin()
        }
    }


@router.get("/{key_id}", response_model=APIKeyResponse)
async def get_api_key(
    key_id: str,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Get details of a specific API key"""
    api_key = APIKeyService.get_api_key(db, UUID(key_id))
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    return _key_to_response(api_key)


@router.patch("/{key_id}", response_model=APIKeyResponse)
async def update_api_key(
    key_id: str,
    data: APIKeyUpdate,
    organization_id: str = Query(..., description="Organization ID"),
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Update an API key's settings"""
    api_key = APIKeyService.update_api_key(
        db,
        key_id=UUID(key_id),
        organization_id=UUID(organization_id),
        data=data
    )
    if not api_key:
        raise HTTPException(status_code=404, detail="API key not found")
    return _key_to_response(api_key)


@router.post("/{key_id}/revoke", status_code=status.HTTP_200_OK)
async def revoke_api_key(
    key_id: str,
    organization_id: str = Query(..., description="Organization ID"),
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Revoke (deactivate) an API key"""
    success = APIKeyService.revoke_api_key(db, UUID(key_id), UUID(organization_id))
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")
    return {"message": "API key revoked successfully"}


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    key_id: str,
    organization_id: str = Query(..., description="Organization ID"),
    current_user: User = Depends(require_delete),
    db: Session = Depends(get_db)
):
    """Permanently delete an API key"""
    success = APIKeyService.delete_api_key(db, UUID(key_id), UUID(organization_id))
    if not success:
        raise HTTPException(status_code=404, detail="API key not found")


@router.post("/validate", response_model=APIKeyValidation)
async def validate_api_key(
    api_key: str = Query(..., description="The API key to validate"),
    db: Session = Depends(get_db)
):
    """Validate an API key and return its details (for testing)"""
    key = APIKeyService.validate_api_key(db, api_key)
    
    if not key:
        return APIKeyValidation(
            valid=False,
            error="Invalid or expired API key"
        )
    
    return APIKeyValidation(
        valid=True,
        key_id=str(key.id),
        organization_id=str(key.organization_id),
        scopes=key.scopes
    )

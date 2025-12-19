"""
Geofence Access Router
Endpoints for managing who has access to geofences
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.core.dependencies import require_write, require_delete
from app.models.user import User
from app.schemas.geofence_access import (
    GeofenceAccessCreate,
    GeofenceAccessUpdate,
    GeofenceAccessResponse,
    GeofenceAccessListResponse,
    UserGeofenceAccessResponse,
    BulkAccessCreate,
    AccessLevel
)
from app.services.geofence_access_service import GeofenceAccessService
from app.services.geofence_service import GeofenceService

router = APIRouter(prefix="/geofences/{geofence_id}/access", tags=["Geofence Access"])


def _access_to_response(access, db: Session) -> GeofenceAccessResponse:
    """Convert access model to response schema"""
    user = db.query(User).filter(User.id == access.user_id).first()
    granted_by = db.query(User).filter(User.id == access.granted_by_id).first() if access.granted_by_id else None
    
    return GeofenceAccessResponse(
        id=str(access.id),
        geofence_id=str(access.geofence_id),
        user_id=str(access.user_id),
        username=user.username if user else None,
        email=user.email if user else None,
        access_level=access.access_level,
        granted_by_id=str(access.granted_by_id) if access.granted_by_id else None,
        granted_by_username=granted_by.username if granted_by else None,
        created_at=access.created_at,
        updated_at=access.updated_at
    )


@router.get("", response_model=GeofenceAccessListResponse)
async def list_geofence_access(
    geofence_id: str,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """List all users with access to a geofence"""
    # Verify geofence exists
    geofence = GeofenceService.get_geofence(db, UUID(geofence_id))
    if not geofence:
        raise HTTPException(status_code=404, detail="Geofence not found")
    
    access_list = GeofenceAccessService.get_geofence_access_list(db, UUID(geofence_id))
    
    return GeofenceAccessListResponse(
        items=[_access_to_response(a, db) for a in access_list],
        total=len(access_list)
    )


@router.post("", response_model=GeofenceAccessResponse, status_code=status.HTTP_201_CREATED)
async def grant_access(
    geofence_id: str,
    access_data: GeofenceAccessCreate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Grant access to a user for this geofence"""
    # Verify geofence exists
    geofence = GeofenceService.get_geofence(db, UUID(geofence_id))
    if not geofence:
        raise HTTPException(status_code=404, detail="Geofence not found")
    
    # Verify target user exists
    target_user = db.query(User).filter(User.id == UUID(access_data.user_id)).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    access = GeofenceAccessService.grant_access(
        db,
        geofence_id=UUID(geofence_id),
        user_id=UUID(access_data.user_id),
        access_level=access_data.access_level.value,
        granted_by_id=current_user.id
    )
    
    return _access_to_response(access, db)


@router.post("/bulk", response_model=List[GeofenceAccessResponse], status_code=status.HTTP_201_CREATED)
async def bulk_grant_access(
    geofence_id: str,
    bulk_data: BulkAccessCreate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Grant access to multiple users at once"""
    # Verify geofence exists
    geofence = GeofenceService.get_geofence(db, UUID(geofence_id))
    if not geofence:
        raise HTTPException(status_code=404, detail="Geofence not found")
    
    user_ids = [UUID(uid) for uid in bulk_data.user_ids]
    
    access_list = GeofenceAccessService.bulk_grant_access(
        db,
        geofence_id=UUID(geofence_id),
        user_ids=user_ids,
        access_level=bulk_data.access_level.value,
        granted_by_id=current_user.id
    )
    
    return [_access_to_response(a, db) for a in access_list]


@router.get("/{user_id}", response_model=GeofenceAccessResponse)
async def get_user_access(
    geofence_id: str,
    user_id: str,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Get a specific user's access level for this geofence"""
    access = GeofenceAccessService.get_user_access(db, UUID(geofence_id), UUID(user_id))
    if not access:
        raise HTTPException(status_code=404, detail="Access record not found")
    
    return _access_to_response(access, db)


@router.patch("/{user_id}", response_model=GeofenceAccessResponse)
async def update_user_access(
    geofence_id: str,
    user_id: str,
    access_data: GeofenceAccessUpdate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Update a user's access level"""
    access = GeofenceAccessService.update_access(
        db,
        geofence_id=UUID(geofence_id),
        user_id=UUID(user_id),
        access_level=access_data.access_level.value
    )
    
    if not access:
        raise HTTPException(status_code=404, detail="Access record not found")
    
    return _access_to_response(access, db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_access(
    geofence_id: str,
    user_id: str,
    current_user: User = Depends(require_delete),
    db: Session = Depends(get_db)
):
    """Revoke a user's access to this geofence"""
    success = GeofenceAccessService.revoke_access(db, UUID(geofence_id), UUID(user_id))
    if not success:
        raise HTTPException(status_code=404, detail="Access record not found")


# Additional router for user-centric access view
user_access_router = APIRouter(prefix="/users/me/geofence-access", tags=["User Geofence Access"])


@user_access_router.get("", response_model=List[UserGeofenceAccessResponse])
async def get_my_geofence_access(
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Get all geofences the current user has access to"""
    access_list = GeofenceAccessService.get_user_geofences(db, current_user.id)
    
    return [
        UserGeofenceAccessResponse(
            geofence_id=str(geofence.id),
            geofence_name=geofence.name,
            access_level=access.access_level,
            granted_at=access.created_at
        )
        for access, geofence in access_list
    ]

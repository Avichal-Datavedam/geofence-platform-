"""
Geofence Access schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class AccessLevel(str, Enum):
    """Permission levels for geofence access"""
    VIEWER = "viewer"
    EDITOR = "editor"
    ADMIN = "admin"
    OWNER = "owner"


class GeofenceAccessCreate(BaseModel):
    """Schema for granting access to a geofence"""
    user_id: str = Field(..., description="User ID to grant access to")
    access_level: AccessLevel = Field(AccessLevel.VIEWER, description="Permission level")


class GeofenceAccessUpdate(BaseModel):
    """Schema for updating access level"""
    access_level: AccessLevel = Field(..., description="New permission level")


class GeofenceAccessResponse(BaseModel):
    """Schema for geofence access response"""
    id: str
    geofence_id: str
    user_id: str
    username: Optional[str] = None
    email: Optional[str] = None
    access_level: AccessLevel
    granted_by_id: Optional[str] = None
    granted_by_username: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GeofenceAccessListResponse(BaseModel):
    """List of users with access to a geofence"""
    items: List[GeofenceAccessResponse]
    total: int


class UserGeofenceAccessResponse(BaseModel):
    """Schema showing which geofences a user has access to"""
    geofence_id: str
    geofence_name: str
    access_level: AccessLevel
    granted_at: datetime


class BulkAccessCreate(BaseModel):
    """Schema for granting access to multiple users"""
    user_ids: List[str] = Field(..., min_length=1, description="List of user IDs")
    access_level: AccessLevel = Field(AccessLevel.VIEWER, description="Permission level for all users")

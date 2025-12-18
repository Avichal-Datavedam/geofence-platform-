"""
Notification schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.geofence import Point


class NotificationCreate(BaseModel):
    """Notification creation schema"""
    notification_type: str = Field(..., description="Type: proximity, breach, alert, etc.")
    severity: str = Field(..., pattern="^(critical|high|medium|low|info)$")
    title: str = Field(..., min_length=1, max_length=200)
    message: Optional[str] = None
    location: Point
    distance_meters: Optional[float] = Field(None, ge=0)
    geofence_id: Optional[str] = None
    zone_id: Optional[str] = None
    asset_id: Optional[str] = None


class NotificationUpdate(BaseModel):
    """Notification update schema"""
    status: Optional[str] = Field(None, pattern="^(active|acknowledged|resolved|dismissed)$")
    is_read: Optional[bool] = None


class NotificationResponse(BaseModel):
    """Notification response schema"""
    id: str
    notification_type: str
    severity: str
    title: str
    message: Optional[str]
    location: Point
    distance_meters: Optional[float]
    status: str
    is_read: bool
    acknowledged_at: Optional[datetime]
    resolved_at: Optional[datetime]
    geofence_id: Optional[str]
    zone_id: Optional[str]
    asset_id: Optional[str]
    user_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


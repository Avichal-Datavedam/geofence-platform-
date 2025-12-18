"""
Notification Router
REST-compliant endpoints for notifications and proximity detection
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.core.database import get_db
from app.core.dependencies import AuthDependency, require_read, require_write
from app.models.user import User
from app.schemas.notification import NotificationCreate, NotificationUpdate, NotificationResponse
from app.services.notification_service import NotificationService
from geoalchemy2.shape import to_shape

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def _notification_to_response(notification) -> NotificationResponse:
    """Convert notification model to response schema"""
    location_shape = to_shape(notification.location)
    
    return NotificationResponse(
        id=str(notification.id),
        notification_type=notification.notification_type,
        severity=notification.severity,
        title=notification.title,
        message=notification.message,
        location={
            "latitude": location_shape.y,
            "longitude": location_shape.x
        },
        distance_meters=notification.distance_meters,
        status=notification.status,
        is_read=notification.is_read,
        acknowledged_at=notification.acknowledged_at,
        resolved_at=notification.resolved_at,
        geofence_id=str(notification.geofence_id) if notification.geofence_id else None,
        zone_id=str(notification.zone_id) if notification.zone_id else None,
        asset_id=str(notification.asset_id) if notification.asset_id else None,
        user_id=str(notification.user_id) if notification.user_id else None,
        created_at=notification.created_at,
        updated_at=notification.updated_at
    )


@router.get("", response_model=list[NotificationResponse])
async def list_notifications(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    is_read: Optional[bool] = Query(None),
    current_user: User = Depends(require_read),
    db: Session = Depends(get_db)
):
    """List notifications"""
    skip = (page - 1) * per_page
    notifications, total = NotificationService.list_notifications(
        db, skip=skip, limit=per_page, status=status, severity=severity, is_read=is_read
    )
    return [_notification_to_response(n) for n in notifications]


@router.post("", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Create a new notification"""
    notification = NotificationService.create_notification(db, notification_data, current_user.id)
    return _notification_to_response(notification)


@router.post("/check-proximity/{asset_id}", response_model=list[NotificationResponse])
async def check_proximity(
    asset_id: str,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Check asset proximity to geofences and create notifications"""
    notifications = NotificationService.check_proximity(db, UUID(asset_id), latitude, longitude)
    return [_notification_to_response(n) for n in notifications]


@router.patch("/{notification_id}/acknowledge", response_model=NotificationResponse)
async def acknowledge_notification(
    notification_id: str,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Acknowledge a notification"""
    notification = NotificationService.acknowledge_notification(db, UUID(notification_id), current_user.id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return _notification_to_response(notification)


"""
Notification Service
Single Responsibility: Manage notifications and proximity detection
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.shape import from_shape
from shapely.geometry import Point as ShapelyPoint
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.models.notification import Notification
from app.models.geofence import Geofence
from app.schemas.notification import NotificationCreate, NotificationUpdate


class NotificationService:
    """Service for notification operations"""
    
    @staticmethod
    def create_notification(db: Session, notification_data: NotificationCreate, user_id: UUID) -> Notification:
        """Create a new notification"""
        point = ShapelyPoint(
            notification_data.location.longitude,
            notification_data.location.latitude
        )
        location_wkb = from_shape(point, srid=4326)
        
        notification = Notification(
            notification_type=notification_data.notification_type,
            severity=notification_data.severity,
            title=notification_data.title,
            message=notification_data.message,
            location=location_wkb,
            distance_meters=notification_data.distance_meters,
            geofence_id=UUID(notification_data.geofence_id) if notification_data.geofence_id else None,
            zone_id=UUID(notification_data.zone_id) if notification_data.zone_id else None,
            asset_id=UUID(notification_data.asset_id) if notification_data.asset_id else None,
            user_id=user_id
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification
    
    @staticmethod
    def check_proximity(
        db: Session,
        asset_id: UUID,
        latitude: float,
        longitude: float
    ) -> List[Notification]:
        """Check if asset is in proximity to any geofence and create notifications"""
        point = ShapelyPoint(longitude, latitude)
        point_wkb = from_shape(point, srid=4326)
        
        # Find intersecting geofences
        geofences = db.query(Geofence).filter(
            func.ST_Intersects(Geofence.geometry, point_wkb),
            Geofence.status == "active"
        ).all()
        
        notifications = []
        for geofence in geofences:
            # Calculate distance to boundary
            distance = db.scalar(
                func.ST_Distance(geofence.geometry, point_wkb)
            )
            
            notification = Notification(
                notification_type="proximity",
                severity="medium" if distance < 100 else "low",
                title=f"Asset in proximity to {geofence.name}",
                message=f"Distance: {distance:.2f} meters",
                location=point_wkb,
                distance_meters=distance,
                geofence_id=geofence.id,
                asset_id=asset_id
            )
            notifications.append(notification)
        
        if notifications:
            db.add_all(notifications)
            db.commit()
        
        return notifications
    
    @staticmethod
    def list_notifications(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        is_read: Optional[bool] = None
    ) -> tuple[List[Notification], int]:
        """List notifications with pagination"""
        query = db.query(Notification)
        
        if status:
            query = query.filter(Notification.status == status)
        if severity:
            query = query.filter(Notification.severity == severity)
        if is_read is not None:
            query = query.filter(Notification.is_read == is_read)
        
        total = query.count()
        notifications = query.order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
        
        return notifications, total
    
    @staticmethod
    def acknowledge_notification(db: Session, notification_id: UUID, user_id: UUID) -> Optional[Notification]:
        """Acknowledge a notification"""
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            return None
        
        notification.status = "acknowledged"
        notification.is_read = True
        notification.acknowledged_at = datetime.utcnow()
        notification.user_id = user_id
        
        db.commit()
        db.refresh(notification)
        return notification


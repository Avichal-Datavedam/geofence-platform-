"""
Notification and proximity detection model
"""
from sqlalchemy import Column, String, Text, ForeignKey, Float, DateTime, Boolean, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.geometry_utils import GeometryColumn, USE_SQLITE
from app.core.config import get_settings

settings = get_settings()


class Notification(BaseModel):
    """Notification model for alerts and proximity detection"""
    __tablename__ = "notifications"
    
    notification_type = Column(String(50), nullable=False, index=True)  # e.g., "proximity", "breach", "alert"
    severity = Column(String(20), nullable=False, index=True)  # critical, high, medium, low, info
    title = Column(String(200), nullable=False)
    message = Column(Text)
    
    # Location where notification was triggered
    location = GeometryColumn("POINT", srid=settings.DEFAULT_SRID, index=True)
    distance_meters = Column(Float)  # Distance to geofence/zone boundary
    
    # Status
    status = Column(String(20), default="active", index=True)  # active, acknowledged, resolved, dismissed
    is_read = Column(Boolean, default=False, index=True)
    acknowledged_at = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))
    
    # Relationships
    geofence_id = Column(ForeignKey("geofences.id", ondelete="SET NULL"), index=True)
    zone_id = Column(ForeignKey("zones.id", ondelete="SET NULL"), index=True)
    asset_id = Column(ForeignKey("assets.id", ondelete="SET NULL"), index=True)
    user_id = Column(ForeignKey("users.id", ondelete="SET NULL"), index=True)  # User who triggered/acknowledged
    
    geofence = relationship("Geofence", back_populates="notifications")
    
    # Spatial index (only for PostgreSQL)
    __table_args__ = (
        (Index("idx_notification_location", "location", postgresql_using="gist"),)
        if not USE_SQLITE else ()
    )
    
    def __repr__(self):
        return f"<Notification {self.title} ({self.notification_type})>"


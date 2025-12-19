"""
Geofence Access model
Controls who has access to a geofence and their permission level
"""
from sqlalchemy import Column, String, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import enum


class AccessLevel(str, enum.Enum):
    """Permission levels for geofence access"""
    VIEWER = "viewer"        # Can view geofence details
    EDITOR = "editor"        # Can edit geofence properties
    ADMIN = "admin"          # Can manage access and edit
    OWNER = "owner"          # Full control including delete


class GeofenceAccess(BaseModel):
    """Geofence access control model"""
    __tablename__ = "geofence_access"
    
    # Foreign keys
    geofence_id = Column(ForeignKey("geofences.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Access level
    access_level = Column(
        String(20),
        nullable=False,
        default=AccessLevel.VIEWER.value,
        index=True
    )
    
    # Optional: who granted this access
    granted_by_id = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    geofence = relationship("Geofence", back_populates="access_list")
    user = relationship("User", foreign_keys=[user_id], back_populates="geofence_access")
    granted_by = relationship("User", foreign_keys=[granted_by_id])
    
    # Ensure unique user-geofence combination
    __table_args__ = (
        UniqueConstraint('geofence_id', 'user_id', name='uq_geofence_user_access'),
    )
    
    def __repr__(self):
        return f"<GeofenceAccess {self.user_id} -> {self.geofence_id}: {self.access_level}>"

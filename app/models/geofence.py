"""
Geofence model
Geometric boundaries with altitude support
"""
from sqlalchemy import Column, String, Float, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.geometry_utils import GeometryColumn, USE_SQLITE
from app.core.config import get_settings

settings = get_settings()


class Geofence(BaseModel):
    """Geofence model - geometric boundaries"""
    __tablename__ = "geofences"
    
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    
    # Geometry - PostGIS Geography type (Text for SQLite)
    geometry = GeometryColumn("GEOMETRY", srid=settings.DEFAULT_SRID, nullable=False, index=True)
    
    # Center point for quick distance calculations
    center_point = GeometryColumn("POINT", srid=settings.DEFAULT_SRID, nullable=False, index=True)
    
    # Altitude constraints
    altitude_min_meters = Column(Float, default=0.0)
    altitude_max_meters = Column(Float, default=500.0)
    
    # Metadata
    status = Column(String(20), default="active", index=True)  # active, inactive, monitoring
    priority = Column(String(20), default=1)  # 1-5
    
    # Relationships
    organization_id = Column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    created_by_id = Column(ForeignKey("users.id", ondelete="SET NULL"))
    
    zones = relationship("Zone", back_populates="geofence", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="geofence", lazy="dynamic")
    
    # Spatial indexes (only for PostgreSQL)
    __table_args__ = (
        (Index("idx_geofence_geometry", "geometry", postgresql_using="gist"),
         Index("idx_geofence_center", "center_point", postgresql_using="gist"),)
        if not USE_SQLITE else ()
    )
    
    def __repr__(self):
        return f"<Geofence {self.name}>"


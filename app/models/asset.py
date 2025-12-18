"""
Asset model
Trackable entities (devices, vehicles, etc.)
"""
from sqlalchemy import Column, String, Text, ForeignKey, Float, DateTime, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.geometry_utils import GeometryColumn, USE_SQLITE
from app.core.config import get_settings

settings = get_settings()


class Asset(BaseModel):
    """Asset model - trackable entities"""
    __tablename__ = "assets"
    
    name = Column(String(100), nullable=False, index=True)
    asset_type = Column(String(50), nullable=False)  # e.g., "drone", "vehicle", "device"
    identifier = Column(String(100), unique=True, nullable=False, index=True)  # Unique identifier
    
    # Current location
    current_location = GeometryColumn("POINT", srid=settings.DEFAULT_SRID, index=True)
    altitude_meters = Column(Float)
    heading_degrees = Column(Float)  # 0-360
    speed_mps = Column(Float)  # meters per second
    
    # Status
    status = Column(String(20), default="active", index=True)  # active, inactive, offline
    last_seen = Column(DateTime(timezone=True), index=True)
    
    # Relationships
    owner_id = Column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    organization_id = Column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    owner = relationship("User", back_populates="assets")
    
    # Trajectory history
    trajectories = relationship("AssetTrajectory", back_populates="asset", cascade="all, delete-orphan")
    
    # Spatial index (only for PostgreSQL)
    __table_args__ = (
        (Index("idx_asset_location", "current_location", postgresql_using="gist"),)
        if not USE_SQLITE else ()
    )
    
    def __repr__(self):
        return f"<Asset {self.name} ({self.identifier})>"


class AssetTrajectory(BaseModel):
    """Asset trajectory history"""
    __tablename__ = "asset_trajectories"
    
    asset_id = Column(ForeignKey("assets.id", ondelete="CASCADE"), nullable=False, index=True)
    location = GeometryColumn("POINT", srid=settings.DEFAULT_SRID, nullable=False, index=True)
    altitude_meters = Column(Float)
    heading_degrees = Column(Float)
    speed_mps = Column(Float)
    recorded_at = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Relationships
    asset = relationship("Asset", back_populates="trajectories")
    
    # Spatial index (only for PostgreSQL)
    __table_args__ = (
        (Index("idx_trajectory_location", "location", postgresql_using="gist"),
         Index("idx_trajectory_time", "recorded_at"),)
        if not USE_SQLITE else (Index("idx_trajectory_time", "recorded_at"),)
    )


"""
Organization model
Multi-tenant support
"""
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.geometry_utils import GeometryColumn
from app.core.config import get_settings

settings = get_settings()


class Organization(BaseModel):
    """Organization model for multi-tenant support"""
    __tablename__ = "organizations"
    
    name = Column(String(100), unique=True, nullable=False, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    description = Column(Text)
    
    # Headquarters location
    headquarters_location = GeometryColumn("POINT", srid=settings.DEFAULT_SRID, index=True)
    
    # Relationships
    geofences = relationship("Geofence", backref="organization", lazy="dynamic")
    assets = relationship("Asset", backref="organization", lazy="dynamic")
    
    def __repr__(self):
        return f"<Organization {self.name}>"


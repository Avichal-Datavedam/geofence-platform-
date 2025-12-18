"""
Zone model
Logical areas within geofences
"""
from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Zone(BaseModel):
    """Zone model - logical areas within geofences"""
    __tablename__ = "zones"
    
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    zone_type = Column(String(50), nullable=False)  # e.g., "restricted", "monitoring", "safe"
    priority = Column(String(20), default=1)  # 1-5
    
    # Relationships
    geofence_id = Column(ForeignKey("geofences.id", ondelete="CASCADE"), nullable=False, index=True)
    geofence = relationship("Geofence", back_populates="zones")
    
    # Zone rules/metadata (stored as JSON in description or separate table)
    rules = Column(Text)  # JSON string with zone-specific rules
    
    def __repr__(self):
        return f"<Zone {self.name} in Geofence {self.geofence_id}>"


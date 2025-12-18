"""
Zone schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ZoneCreate(BaseModel):
    """Zone creation schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    zone_type: str = Field(..., description="Zone type: restricted, monitoring, safe, etc.")
    priority: int = Field(1, ge=1, le=5)
    geofence_id: str = Field(..., description="Parent geofence ID")
    rules: Optional[Dict[str, Any]] = Field(None, description="Zone-specific rules as JSON")


class ZoneUpdate(BaseModel):
    """Zone update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    zone_type: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    rules: Optional[Dict[str, Any]] = None


class ZoneResponse(BaseModel):
    """Zone response schema"""
    id: str
    name: str
    description: Optional[str]
    zone_type: str
    priority: int
    geofence_id: str
    rules: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


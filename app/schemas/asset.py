"""
Asset schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.geofence import Point


class AssetCreate(BaseModel):
    """Asset creation schema"""
    name: str = Field(..., min_length=1, max_length=100)
    asset_type: str = Field(..., description="Asset type: drone, vehicle, device, etc.")
    identifier: str = Field(..., min_length=1, max_length=100, description="Unique identifier")
    current_location: Optional[Point] = None
    altitude_meters: Optional[float] = Field(None, ge=0)
    heading_degrees: Optional[float] = Field(None, ge=0, lt=360)
    speed_mps: Optional[float] = Field(None, ge=0)
    organization_id: Optional[str] = None


class AssetUpdate(BaseModel):
    """Asset update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    asset_type: Optional[str] = None
    current_location: Optional[Point] = None
    altitude_meters: Optional[float] = Field(None, ge=0)
    heading_degrees: Optional[float] = Field(None, ge=0, lt=360)
    speed_mps: Optional[float] = Field(None, ge=0)
    status: Optional[str] = Field(None, pattern="^(active|inactive|offline)$")


class AssetResponse(BaseModel):
    """Asset response schema"""
    id: str
    name: str
    asset_type: str
    identifier: str
    current_location: Optional[Point]
    altitude_meters: Optional[float]
    heading_degrees: Optional[float]
    speed_mps: Optional[float]
    status: str
    last_seen: Optional[datetime]
    owner_id: Optional[str]
    organization_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AssetTrajectoryCreate(BaseModel):
    """Asset trajectory point creation"""
    asset_id: str
    location: Point
    altitude_meters: Optional[float] = Field(None, ge=0)
    heading_degrees: Optional[float] = Field(None, ge=0, lt=360)
    speed_mps: Optional[float] = Field(None, ge=0)


class AssetTrajectoryResponse(BaseModel):
    """Asset trajectory response"""
    id: str
    asset_id: str
    location: Point
    altitude_meters: Optional[float]
    heading_degrees: Optional[float]
    speed_mps: Optional[float]
    recorded_at: datetime
    
    class Config:
        from_attributes = True


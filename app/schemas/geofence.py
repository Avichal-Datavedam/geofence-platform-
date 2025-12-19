"""
Geofence schemas
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime


class Point(BaseModel):
    """Geographic point"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    altitude: Optional[float] = Field(None, ge=0, description="Altitude in meters")


class GeometryCreate(BaseModel):
    """Geometry creation schema (GeoJSON format)"""
    type: str = Field(..., description="Geometry type: Point, Polygon, LineString, etc.")
    coordinates: list = Field(..., description="Coordinates array following GeoJSON spec")


class GeofenceCreate(BaseModel):
    """Geofence creation schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    geometry: GeometryCreate = Field(..., description="GeoJSON geometry object")
    center_point: Point = Field(..., description="Center point for quick calculations")
    altitude_min_meters: float = Field(0.0, ge=0)
    altitude_max_meters: float = Field(500.0, ge=0)
    status: str = Field("active", pattern="^(active|inactive|monitoring)$")
    priority: int = Field(1, ge=1, le=5)
    organization_id: Optional[str] = None


class GeofenceUpdate(BaseModel):
    """Geofence update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    geometry: Optional[GeometryCreate] = None
    center_point: Optional[Point] = None
    altitude_min_meters: Optional[float] = Field(None, ge=0)
    altitude_max_meters: Optional[float] = Field(None, ge=0)
    status: Optional[str] = Field(None, pattern="^(active|inactive|monitoring)$")
    priority: Optional[int] = Field(None, ge=1, le=5)


class AccessInfo(BaseModel):
    """Brief access info for geofence response"""
    user_id: str
    username: Optional[str] = None
    access_level: str


class GeofenceResponse(BaseModel):
    """Geofence response schema"""
    id: str
    name: str
    description: Optional[str]
    geometry: Dict[str, Any]  # GeoJSON
    center_point: Point
    altitude_min_meters: float
    altitude_max_meters: float
    status: str
    priority: int
    organization_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    access_list: Optional[List[AccessInfo]] = None
    
    class Config:
        from_attributes = True


class GeofenceListResponse(BaseModel):
    """Paginated geofence list response"""
    items: list[GeofenceResponse]
    total: int
    page: int
    per_page: int
    pages: int


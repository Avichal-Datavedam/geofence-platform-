"""
Zone Router
REST-compliant endpoints for zone management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import json
from app.core.database import get_db
from app.core.dependencies import AuthDependency, require_read, require_write, require_delete
from app.models.user import User
from app.schemas.zone import ZoneCreate, ZoneUpdate, ZoneResponse
from app.services.zone_service import ZoneService

router = APIRouter(prefix="/zones", tags=["Zones"])


def _zone_to_response(zone) -> ZoneResponse:
    """Convert zone model to response schema"""
    return ZoneResponse(
        id=str(zone.id),
        name=zone.name,
        description=zone.description,
        zone_type=zone.zone_type,
        priority=zone.priority,
        geofence_id=str(zone.geofence_id),
        rules=json.loads(zone.rules) if zone.rules else None,
        created_at=zone.created_at,
        updated_at=zone.updated_at
    )


@router.get("", response_model=list[ZoneResponse])
async def list_zones(
    geofence_id: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_read),
    db: Session = Depends(get_db)
):
    """List zones"""
    skip = (page - 1) * per_page
    gf_id = UUID(geofence_id) if geofence_id else None
    
    zones, total = ZoneService.list_zones(db, geofence_id=gf_id, skip=skip, limit=per_page)
    return [_zone_to_response(z) for z in zones]


@router.post("", response_model=ZoneResponse, status_code=status.HTTP_201_CREATED)
async def create_zone(
    zone_data: ZoneCreate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Create a new zone"""
    zone = ZoneService.create_zone(db, zone_data)
    return _zone_to_response(zone)


@router.get("/{zone_id}", response_model=ZoneResponse)
async def get_zone(
    zone_id: str,
    current_user: User = Depends(require_read),
    db: Session = Depends(get_db)
):
    """Get zone by ID"""
    zone = ZoneService.get_zone(db, UUID(zone_id))
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return _zone_to_response(zone)


@router.put("/{zone_id}", response_model=ZoneResponse)
async def update_zone(
    zone_id: str,
    zone_data: ZoneUpdate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Update zone (full update)"""
    zone = ZoneService.update_zone(db, UUID(zone_id), zone_data)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return _zone_to_response(zone)


@router.patch("/{zone_id}", response_model=ZoneResponse)
async def patch_zone(
    zone_id: str,
    zone_data: ZoneUpdate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Partially update zone"""
    zone = ZoneService.update_zone(db, UUID(zone_id), zone_data)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return _zone_to_response(zone)


@router.delete("/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_zone(
    zone_id: str,
    current_user: User = Depends(require_delete),
    db: Session = Depends(get_db)
):
    """Delete zone"""
    success = ZoneService.delete_zone(db, UUID(zone_id))
    if not success:
        raise HTTPException(status_code=404, detail="Zone not found")


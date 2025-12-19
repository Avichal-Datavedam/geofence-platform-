"""
Geofence Router
REST-compliant endpoints for geofence management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from app.core.database import get_db
from app.core.dependencies import AuthDependency, require_read, require_write, require_delete
from app.models.user import User
from app.schemas.geofence import GeofenceCreate, GeofenceUpdate, GeofenceResponse, GeofenceListResponse, AccessInfo
from app.services.geofence_service import GeofenceService
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping

router = APIRouter(prefix="/geofences", tags=["Geofences"])


def _geofence_to_response(geofence, include_access: bool = False) -> GeofenceResponse:
    """Convert geofence model to response schema"""
    geometry_shape = to_shape(geofence.geometry)
    center_shape = to_shape(geofence.center_point)
    
    from app.schemas.geofence import Point
    
    # Build access list if requested and available
    access_list = None
    if include_access and hasattr(geofence, 'access_list') and geofence.access_list:
        access_list = [
            AccessInfo(
                user_id=str(access.user_id),
                username=access.user.username if access.user else None,
                access_level=access.access_level
            )
            for access in geofence.access_list
        ]
    
    return GeofenceResponse(
        id=str(geofence.id),
        name=geofence.name,
        description=geofence.description,
        geometry=mapping(geometry_shape),
        center_point=Point(
            latitude=center_shape.y,
            longitude=center_shape.x
        ),
        altitude_min_meters=geofence.altitude_min_meters,
        altitude_max_meters=geofence.altitude_max_meters,
        status=geofence.status,
        priority=geofence.priority,
        organization_id=str(geofence.organization_id) if geofence.organization_id else None,
        created_at=geofence.created_at,
        updated_at=geofence.updated_at,
        access_list=access_list
    )


@router.get("", response_model=GeofenceListResponse)
async def list_geofences(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    organization_id: Optional[str] = Query(None),
    current_user: User = Depends(require_read),
    db: Session = Depends(get_db)
):
    """List geofences with pagination"""
    skip = (page - 1) * per_page
    org_id = UUID(organization_id) if organization_id else None
    
    geofences, total = GeofenceService.list_geofences(
        db, skip=skip, limit=per_page, status=status, organization_id=org_id
    )
    
    return GeofenceListResponse(
        items=[_geofence_to_response(g) for g in geofences],
        total=total,
        page=page,
        per_page=per_page,
        pages=(total + per_page - 1) // per_page
    )


@router.post("", response_model=GeofenceResponse, status_code=status.HTTP_201_CREATED)
async def create_geofence(
    geofence_data: GeofenceCreate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Create a new geofence"""
    geofence = GeofenceService.create_geofence(db, geofence_data, current_user.id)
    return _geofence_to_response(geofence)


@router.get("/{geofence_id}", response_model=GeofenceResponse)
async def get_geofence(
    geofence_id: str,
    include_access: bool = Query(False, description="Include access list in response"),
    current_user: User = Depends(require_read),
    db: Session = Depends(get_db)
):
    """Get geofence by ID"""
    geofence = GeofenceService.get_geofence(db, UUID(geofence_id))
    if not geofence:
        raise HTTPException(status_code=404, detail="Geofence not found")
    return _geofence_to_response(geofence, include_access=include_access)


@router.put("/{geofence_id}", response_model=GeofenceResponse)
async def update_geofence(
    geofence_id: str,
    geofence_data: GeofenceUpdate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Update geofence (full update)"""
    geofence = GeofenceService.update_geofence(db, UUID(geofence_id), geofence_data)
    if not geofence:
        raise HTTPException(status_code=404, detail="Geofence not found")
    return _geofence_to_response(geofence)


@router.patch("/{geofence_id}", response_model=GeofenceResponse)
async def patch_geofence(
    geofence_id: str,
    geofence_data: GeofenceUpdate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Partially update geofence"""
    geofence = GeofenceService.update_geofence(db, UUID(geofence_id), geofence_data)
    if not geofence:
        raise HTTPException(status_code=404, detail="Geofence not found")
    return _geofence_to_response(geofence)


@router.delete("/{geofence_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_geofence(
    geofence_id: str,
    current_user: User = Depends(require_delete),
    db: Session = Depends(get_db)
):
    """Delete geofence"""
    success = GeofenceService.delete_geofence(db, UUID(geofence_id))
    if not success:
        raise HTTPException(status_code=404, detail="Geofence not found")


@router.get("/nearby/search", response_model=GeofenceListResponse)
async def find_nearby_geofences(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_meters: float = Query(5000, ge=0),
    current_user: User = Depends(require_read),
    db: Session = Depends(get_db)
):
    """Find geofences near a point"""
    geofences = GeofenceService.find_nearby_geofences(db, latitude, longitude, radius_meters)
    
    return GeofenceListResponse(
        items=[_geofence_to_response(g) for g in geofences],
        total=len(geofences),
        page=1,
        per_page=len(geofences),
        pages=1
    )


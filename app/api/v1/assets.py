"""
Asset Router
REST-compliant endpoints for asset management
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.core.database import get_db
from app.core.dependencies import AuthDependency, require_read, require_write
from app.models.user import User
from app.schemas.asset import AssetCreate, AssetUpdate, AssetResponse, AssetTrajectoryCreate, AssetTrajectoryResponse
from app.services.asset_service import AssetService
from geoalchemy2.shape import to_shape

router = APIRouter(prefix="/assets", tags=["Assets"])


def _asset_to_response(asset) -> AssetResponse:
    """Convert asset model to response schema"""
    location = None
    if asset.current_location:
        location_shape = to_shape(asset.current_location)
        location = {
            "latitude": location_shape.y,
            "longitude": location_shape.x
        }
    
    return AssetResponse(
        id=str(asset.id),
        name=asset.name,
        asset_type=asset.asset_type,
        identifier=asset.identifier,
        current_location=location,
        altitude_meters=asset.altitude_meters,
        heading_degrees=asset.heading_degrees,
        speed_mps=asset.speed_mps,
        status=asset.status,
        last_seen=asset.last_seen,
        owner_id=str(asset.owner_id) if asset.owner_id else None,
        organization_id=str(asset.organization_id) if asset.organization_id else None,
        created_at=asset.created_at,
        updated_at=asset.updated_at
    )


@router.get("", response_model=list[AssetResponse])
async def list_assets(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    asset_type: Optional[str] = Query(None),
    current_user: User = Depends(require_read),
    db: Session = Depends(get_db)
):
    """List assets"""
    skip = (page - 1) * per_page
    assets, total = AssetService.list_assets(db, skip=skip, limit=per_page, status=status, asset_type=asset_type)
    return [_asset_to_response(a) for a in assets]


@router.post("", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset_data: AssetCreate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Create a new asset"""
    asset = AssetService.create_asset(db, asset_data, current_user.id)
    return _asset_to_response(asset)


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: str,
    current_user: User = Depends(require_read),
    db: Session = Depends(get_db)
):
    """Get asset by ID"""
    asset = AssetService.get_asset(db, UUID(asset_id))
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return _asset_to_response(asset)


@router.put("/{asset_id}/location", response_model=AssetResponse)
async def update_asset_location(
    asset_id: str,
    location_data: AssetTrajectoryCreate,
    current_user: User = Depends(require_write),
    db: Session = Depends(get_db)
):
    """Update asset location and create trajectory point"""
    asset = AssetService.update_asset_location(db, UUID(asset_id), location_data)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return _asset_to_response(asset)


@router.get("/{asset_id}/trajectory", response_model=list[AssetTrajectoryResponse])
async def get_asset_trajectory(
    asset_id: str,
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    limit: int = Query(1000, le=10000),
    current_user: User = Depends(require_read),
    db: Session = Depends(get_db)
):
    """Get asset trajectory history"""
    trajectories = AssetService.get_asset_trajectory(
        db, UUID(asset_id), start_time, end_time, limit
    )
    
    result = []
    for traj in trajectories:
        location_shape = to_shape(traj.location)
        result.append(AssetTrajectoryResponse(
            id=str(traj.id),
            asset_id=str(traj.asset_id),
            location={
                "latitude": location_shape.y,
                "longitude": location_shape.x
            },
            altitude_meters=traj.altitude_meters,
            heading_degrees=traj.heading_degrees,
            speed_mps=traj.speed_mps,
            recorded_at=traj.recorded_at
        ))
    
    return result


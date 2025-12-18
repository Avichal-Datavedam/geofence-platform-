"""
Asset Service
Single Responsibility: Manage asset operations and tracking
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.shape import from_shape
from shapely.geometry import Point as ShapelyPoint
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.models.asset import Asset, AssetTrajectory
from app.schemas.asset import AssetCreate, AssetUpdate, AssetTrajectoryCreate


class AssetService:
    """Service for asset operations"""
    
    @staticmethod
    def create_asset(db: Session, asset_data: AssetCreate, user_id: UUID) -> Asset:
        """Create a new asset"""
        location_wkb = None
        if asset_data.current_location:
            point = ShapelyPoint(
                asset_data.current_location.longitude,
                asset_data.current_location.latitude
            )
            location_wkb = from_shape(point, srid=4326)
        
        asset = Asset(
            name=asset_data.name,
            asset_type=asset_data.asset_type,
            identifier=asset_data.identifier,
            current_location=location_wkb,
            altitude_meters=asset_data.altitude_meters,
            heading_degrees=asset_data.heading_degrees,
            speed_mps=asset_data.speed_mps,
            owner_id=user_id,
            organization_id=UUID(asset_data.organization_id) if asset_data.organization_id else None,
            last_seen=datetime.utcnow()
        )
        
        db.add(asset)
        db.commit()
        db.refresh(asset)
        return asset
    
    @staticmethod
    def get_asset(db: Session, asset_id: UUID) -> Optional[Asset]:
        """Get asset by ID"""
        return db.query(Asset).filter(Asset.id == asset_id).first()
    
    @staticmethod
    def update_asset_location(
        db: Session,
        asset_id: UUID,
        location_data: AssetTrajectoryCreate
    ) -> Optional[Asset]:
        """Update asset location and create trajectory point"""
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            return None
        
        # Update current location
        point = ShapelyPoint(
            location_data.location.longitude,
            location_data.location.latitude
        )
        location_wkb = from_shape(point, srid=4326)
        
        asset.current_location = location_wkb
        asset.altitude_meters = location_data.altitude_meters
        asset.heading_degrees = location_data.heading_degrees
        asset.speed_mps = location_data.speed_mps
        asset.last_seen = datetime.utcnow()
        
        # Create trajectory point
        trajectory = AssetTrajectory(
            asset_id=asset_id,
            location=location_wkb,
            altitude_meters=location_data.altitude_meters,
            heading_degrees=location_data.heading_degrees,
            speed_mps=location_data.speed_mps,
            recorded_at=datetime.utcnow()
        )
        db.add(trajectory)
        
        db.commit()
        db.refresh(asset)
        return asset
    
    @staticmethod
    def list_assets(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        asset_type: Optional[str] = None
    ) -> tuple[List[Asset], int]:
        """List assets with pagination"""
        query = db.query(Asset)
        
        if status:
            query = query.filter(Asset.status == status)
        if asset_type:
            query = query.filter(Asset.asset_type == asset_type)
        
        total = query.count()
        assets = query.offset(skip).limit(limit).all()
        
        return assets, total
    
    @staticmethod
    def get_asset_trajectory(
        db: Session,
        asset_id: UUID,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 1000
    ) -> List[AssetTrajectory]:
        """Get asset trajectory history"""
        query = db.query(AssetTrajectory).filter(AssetTrajectory.asset_id == asset_id)
        
        if start_time:
            query = query.filter(AssetTrajectory.recorded_at >= start_time)
        if end_time:
            query = query.filter(AssetTrajectory.recorded_at <= end_time)
        
        return query.order_by(AssetTrajectory.recorded_at.desc()).limit(limit).all()


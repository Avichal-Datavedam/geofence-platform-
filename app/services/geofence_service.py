"""
Geofence Service
Single Responsibility: Manage geofence operations
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from geoalchemy2.shape import from_shape
from shapely.geometry import shape, Point as ShapelyPoint
from typing import List, Optional
from uuid import UUID
from app.models.geofence import Geofence
from app.schemas.geofence import GeofenceCreate, GeofenceUpdate
from app.core.config import get_settings

settings = get_settings()


class GeofenceService:
    """Service for geofence operations"""
    
    @staticmethod
    def create_geofence(db: Session, geofence_data: GeofenceCreate, user_id: UUID) -> Geofence:
        """Create a new geofence"""
        # Convert GeoJSON to PostGIS geometry
        geometry_shape = shape(geofence_data.geometry.dict())
        geometry_wkb = from_shape(geometry_shape, srid=settings.DEFAULT_SRID)
        
        # Convert center point
        center_shape = ShapelyPoint(
            geofence_data.center_point.longitude,
            geofence_data.center_point.latitude
        )
        center_wkb = from_shape(center_shape, srid=settings.DEFAULT_SRID)
        
        geofence = Geofence(
            name=geofence_data.name,
            description=geofence_data.description,
            geometry=geometry_wkb,
            center_point=center_wkb,
            altitude_min_meters=geofence_data.altitude_min_meters,
            altitude_max_meters=geofence_data.altitude_max_meters,
            status=geofence_data.status,
            priority=geofence_data.priority,
            organization_id=UUID(geofence_data.organization_id) if geofence_data.organization_id else None,
            created_by_id=user_id
        )
        
        db.add(geofence)
        db.commit()
        db.refresh(geofence)
        return geofence
    
    @staticmethod
    def get_geofence(db: Session, geofence_id: UUID) -> Optional[Geofence]:
        """Get geofence by ID"""
        return db.query(Geofence).filter(Geofence.id == geofence_id).first()
    
    @staticmethod
    def list_geofences(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        organization_id: Optional[UUID] = None
    ) -> tuple[List[Geofence], int]:
        """List geofences with pagination"""
        query = db.query(Geofence)
        
        if status:
            query = query.filter(Geofence.status == status)
        if organization_id:
            query = query.filter(Geofence.organization_id == organization_id)
        
        total = query.count()
        geofences = query.offset(skip).limit(limit).all()
        
        return geofences, total
    
    @staticmethod
    def update_geofence(
        db: Session,
        geofence_id: UUID,
        geofence_data: GeofenceUpdate
    ) -> Optional[Geofence]:
        """Update geofence"""
        geofence = db.query(Geofence).filter(Geofence.id == geofence_id).first()
        if not geofence:
            return None
        
        if geofence_data.name is not None:
            geofence.name = geofence_data.name
        if geofence_data.description is not None:
            geofence.description = geofence_data.description
        if geofence_data.geometry is not None:
            geometry_shape = shape(geofence_data.geometry.dict())
            geofence.geometry = from_shape(geometry_shape, srid=settings.DEFAULT_SRID)
        if geofence_data.center_point is not None:
            center_shape = ShapelyPoint(
                geofence_data.center_point.longitude,
                geofence_data.center_point.latitude
            )
            geofence.center_point = from_shape(center_shape, srid=settings.DEFAULT_SRID)
        if geofence_data.altitude_min_meters is not None:
            geofence.altitude_min_meters = geofence_data.altitude_min_meters
        if geofence_data.altitude_max_meters is not None:
            geofence.altitude_max_meters = geofence_data.altitude_max_meters
        if geofence_data.status is not None:
            geofence.status = geofence_data.status
        if geofence_data.priority is not None:
            geofence.priority = geofence_data.priority
        
        db.commit()
        db.refresh(geofence)
        return geofence
    
    @staticmethod
    def delete_geofence(db: Session, geofence_id: UUID) -> bool:
        """Delete geofence"""
        geofence = db.query(Geofence).filter(Geofence.id == geofence_id).first()
        if not geofence:
            return False
        
        db.delete(geofence)
        db.commit()
        return True
    
    @staticmethod
    def find_nearby_geofences(
        db: Session,
        latitude: float,
        longitude: float,
        radius_meters: float = 5000
    ) -> List[Geofence]:
        """Find geofences near a point"""
        point = ShapelyPoint(longitude, latitude)
        point_wkb = from_shape(point, srid=settings.DEFAULT_SRID)
        
        geofences = db.query(Geofence).filter(
            func.ST_DWithin(
                Geofence.center_point,
                point_wkb,
                radius_meters
            )
        ).all()
        
        return geofences


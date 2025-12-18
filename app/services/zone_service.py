"""
Zone Service
Single Responsibility: Manage zone operations
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import json
from app.models.zone import Zone
from app.schemas.zone import ZoneCreate, ZoneUpdate


class ZoneService:
    """Service for zone operations"""
    
    @staticmethod
    def create_zone(db: Session, zone_data: ZoneCreate) -> Zone:
        """Create a new zone"""
        zone = Zone(
            name=zone_data.name,
            description=zone_data.description,
            zone_type=zone_data.zone_type,
            priority=zone_data.priority,
            geofence_id=UUID(zone_data.geofence_id),
            rules=json.dumps(zone_data.rules) if zone_data.rules else None
        )
        
        db.add(zone)
        db.commit()
        db.refresh(zone)
        return zone
    
    @staticmethod
    def get_zone(db: Session, zone_id: UUID) -> Optional[Zone]:
        """Get zone by ID"""
        return db.query(Zone).filter(Zone.id == zone_id).first()
    
    @staticmethod
    def list_zones(
        db: Session,
        geofence_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> tuple[List[Zone], int]:
        """List zones with pagination"""
        query = db.query(Zone)
        
        if geofence_id:
            query = query.filter(Zone.geofence_id == geofence_id)
        
        total = query.count()
        zones = query.offset(skip).limit(limit).all()
        
        return zones, total
    
    @staticmethod
    def update_zone(
        db: Session,
        zone_id: UUID,
        zone_data: ZoneUpdate
    ) -> Optional[Zone]:
        """Update zone"""
        zone = db.query(Zone).filter(Zone.id == zone_id).first()
        if not zone:
            return None
        
        if zone_data.name is not None:
            zone.name = zone_data.name
        if zone_data.description is not None:
            zone.description = zone_data.description
        if zone_data.zone_type is not None:
            zone.zone_type = zone_data.zone_type
        if zone_data.priority is not None:
            zone.priority = zone_data.priority
        if zone_data.rules is not None:
            zone.rules = json.dumps(zone_data.rules)
        
        db.commit()
        db.refresh(zone)
        return zone
    
    @staticmethod
    def delete_zone(db: Session, zone_id: UUID) -> bool:
        """Delete zone"""
        zone = db.query(Zone).filter(Zone.id == zone_id).first()
        if not zone:
            return False
        
        db.delete(zone)
        db.commit()
        return True


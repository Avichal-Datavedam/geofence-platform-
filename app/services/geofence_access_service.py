"""
Geofence Access Service
Business logic for managing geofence access control
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import UUID
from typing import List, Optional, Tuple

from app.models.geofence_access import GeofenceAccess, AccessLevel
from app.models.geofence import Geofence
from app.models.user import User


class GeofenceAccessService:
    """Service for managing geofence access"""
    
    @staticmethod
    def grant_access(
        db: Session,
        geofence_id: UUID,
        user_id: UUID,
        access_level: str,
        granted_by_id: UUID
    ) -> GeofenceAccess:
        """Grant access to a user for a geofence"""
        # Check if access already exists
        existing = db.query(GeofenceAccess).filter(
            and_(
                GeofenceAccess.geofence_id == geofence_id,
                GeofenceAccess.user_id == user_id
            )
        ).first()
        
        if existing:
            # Update existing access
            existing.access_level = access_level
            existing.granted_by_id = granted_by_id
            db.commit()
            db.refresh(existing)
            return existing
        
        # Create new access
        access = GeofenceAccess(
            geofence_id=geofence_id,
            user_id=user_id,
            access_level=access_level,
            granted_by_id=granted_by_id
        )
        db.add(access)
        db.commit()
        db.refresh(access)
        return access
    
    @staticmethod
    def update_access(
        db: Session,
        geofence_id: UUID,
        user_id: UUID,
        access_level: str
    ) -> Optional[GeofenceAccess]:
        """Update access level for a user"""
        access = db.query(GeofenceAccess).filter(
            and_(
                GeofenceAccess.geofence_id == geofence_id,
                GeofenceAccess.user_id == user_id
            )
        ).first()
        
        if not access:
            return None
        
        access.access_level = access_level
        db.commit()
        db.refresh(access)
        return access
    
    @staticmethod
    def revoke_access(
        db: Session,
        geofence_id: UUID,
        user_id: UUID
    ) -> bool:
        """Revoke user's access to a geofence"""
        access = db.query(GeofenceAccess).filter(
            and_(
                GeofenceAccess.geofence_id == geofence_id,
                GeofenceAccess.user_id == user_id
            )
        ).first()
        
        if not access:
            return False
        
        db.delete(access)
        db.commit()
        return True
    
    @staticmethod
    def get_geofence_access_list(
        db: Session,
        geofence_id: UUID
    ) -> List[GeofenceAccess]:
        """Get all users with access to a geofence"""
        return db.query(GeofenceAccess).filter(
            GeofenceAccess.geofence_id == geofence_id
        ).all()
    
    @staticmethod
    def get_user_access(
        db: Session,
        geofence_id: UUID,
        user_id: UUID
    ) -> Optional[GeofenceAccess]:
        """Get a specific user's access to a geofence"""
        return db.query(GeofenceAccess).filter(
            and_(
                GeofenceAccess.geofence_id == geofence_id,
                GeofenceAccess.user_id == user_id
            )
        ).first()
    
    @staticmethod
    def get_user_geofences(
        db: Session,
        user_id: UUID
    ) -> List[Tuple[GeofenceAccess, Geofence]]:
        """Get all geofences a user has access to"""
        return db.query(GeofenceAccess, Geofence).join(
            Geofence, GeofenceAccess.geofence_id == Geofence.id
        ).filter(
            GeofenceAccess.user_id == user_id
        ).all()
    
    @staticmethod
    def check_access(
        db: Session,
        geofence_id: UUID,
        user_id: UUID,
        required_level: str
    ) -> bool:
        """Check if user has required access level or higher"""
        access = db.query(GeofenceAccess).filter(
            and_(
                GeofenceAccess.geofence_id == geofence_id,
                GeofenceAccess.user_id == user_id
            )
        ).first()
        
        if not access:
            return False
        
        # Define access hierarchy
        hierarchy = {
            AccessLevel.VIEWER.value: 1,
            AccessLevel.EDITOR.value: 2,
            AccessLevel.ADMIN.value: 3,
            AccessLevel.OWNER.value: 4
        }
        
        user_level = hierarchy.get(access.access_level, 0)
        required = hierarchy.get(required_level, 0)
        
        return user_level >= required
    
    @staticmethod
    def bulk_grant_access(
        db: Session,
        geofence_id: UUID,
        user_ids: List[UUID],
        access_level: str,
        granted_by_id: UUID
    ) -> List[GeofenceAccess]:
        """Grant access to multiple users at once"""
        results = []
        for user_id in user_ids:
            access = GeofenceAccessService.grant_access(
                db, geofence_id, user_id, access_level, granted_by_id
            )
            results.append(access)
        return results

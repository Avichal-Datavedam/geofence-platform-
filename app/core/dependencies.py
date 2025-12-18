"""
FastAPI dependencies for authentication, authorization, and common operations
Zero-trust dependency injection
"""
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from app.core.database import get_db
from app.core.security import SecurityManager
from app.models.user import User
from app.models.rbac import Role, Permission, UserRole
from app.schemas.auth import TokenData

security = HTTPBearer()


class AuthDependency:
    """Authentication dependency manager"""
    
    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: Session = Depends(get_db)
    ) -> User:
        """Get current authenticated user from JWT token"""
        token = credentials.credentials
        payload = SecurityManager.decode_token(token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id: Optional[str] = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Convert string user_id to UUID for database query
        try:
            user_uuid = UUID(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID format",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = db.query(User).filter(User.id == user_uuid).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        
        return user


class PermissionChecker:
    """RBAC permission checker"""
    
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions
    
    async def __call__(
        self,
        current_user: User = Depends(AuthDependency.get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        """Check if user has required permissions"""
        # Get user roles
        user_roles = db.query(UserRole).filter(UserRole.user_id == current_user.id).all()
        role_ids = [ur.role_id for ur in user_roles]
        
        if not role_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no assigned roles"
            )
        
        # Get permissions for user's roles
        permissions = db.query(Permission).join(Role.permissions).filter(
            Role.id.in_(role_ids)
        ).all()
        
        user_permissions = {perm.name for perm in permissions}
        
        # Check if user has all required permissions
        missing_permissions = set(self.required_permissions) - user_permissions
        if missing_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permissions: {', '.join(missing_permissions)}"
            )
        
        return current_user


class RoleChecker:
    """RBAC role checker"""
    
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles
    
    async def __call__(
        self,
        current_user: User = Depends(AuthDependency.get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        """Check if user has required role"""
        user_roles = db.query(UserRole).join(Role).filter(
            UserRole.user_id == current_user.id,
            Role.name.in_(self.allowed_roles)
        ).first()
        
        if not user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required roles: {', '.join(self.allowed_roles)}"
            )
        
        return current_user


# Common permission checkers
require_read = PermissionChecker(["read"])
require_write = PermissionChecker(["write"])
require_delete = PermissionChecker(["delete"])
require_admin = PermissionChecker(["admin"])

# Common role checkers
require_admin_role = RoleChecker(["admin"])
require_operator_role = RoleChecker(["operator", "admin"])


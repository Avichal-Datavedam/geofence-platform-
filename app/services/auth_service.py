"""
Auth Service
Single Responsibility: Handle authentication operations
"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.rbac import Role, Permission, UserRole
from app.core.security import SecurityManager
from app.schemas.auth import UserRegister
from datetime import datetime


class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def _ensure_default_role(db: Session) -> Role:
        """Ensure default 'user' role exists with basic permissions"""
        # Check if role exists
        role = db.query(Role).filter(Role.name == "user").first()
        if role:
            return role
        
        # Create default permissions
        permissions_data = [
            {"name": "read", "resource": "all", "action": "read", "description": "Read access"},
            {"name": "write", "resource": "all", "action": "write", "description": "Write access"},
            {"name": "delete", "resource": "own", "action": "delete", "description": "Delete own resources"},
        ]
        
        permissions = []
        for perm_data in permissions_data:
            perm = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
            if not perm:
                perm = Permission(**perm_data)
                db.add(perm)
            permissions.append(perm)
        
        # Create user role
        role = Role(
            name="user",
            description="Default user role with basic permissions",
            is_system="true"
        )
        role.permissions = permissions
        db.add(role)
        db.commit()
        db.refresh(role)
        return role
    
    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> User:
        """Register a new user"""
        # Check if user exists
        existing_user = db.query(User).filter(
            (User.username == user_data.username) | (User.email == user_data.email)
        ).first()
        
        if existing_user:
            raise ValueError("Username or email already exists")
        
        # Create user
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=SecurityManager.get_password_hash(user_data.password),
            full_name=user_data.full_name
        )
        
        db.add(user)
        db.flush()  # Get user.id before commit
        
        # Assign default role
        default_role = AuthService._ensure_default_role(db)
        user_role = UserRole(user_id=user.id, role_id=default_role.id)
        db.add(user_role)
        
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User | None:
        """Authenticate user by username and password"""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        
        if not SecurityManager.verify_password(password, user.password_hash):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        return user


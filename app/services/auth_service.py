"""
Auth Service
Single Responsibility: Handle authentication operations
"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import SecurityManager
from app.schemas.auth import UserRegister
from datetime import datetime


class AuthService:
    """Service for authentication operations"""
    
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


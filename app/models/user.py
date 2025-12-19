"""
User model
Device-independent user management
"""
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class User(BaseModel):
    """User model for authentication and authorization"""
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    assets = relationship("Asset", back_populates="owner", lazy="dynamic")
    geofence_access = relationship("GeofenceAccess", foreign_keys="GeofenceAccess.user_id", back_populates="user", lazy="dynamic")
    
    def __repr__(self):
        return f"<User {self.username}>"


"""
RBAC (Role-Based Access Control) models
Modular, device-independent permission system
"""
from sqlalchemy import Column, String, Text, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

# Many-to-many relationship between roles and permissions
role_permission = Table(
    "role_permission",
    BaseModel.metadata,
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
)


class Role(BaseModel):
    """Role model - groups of permissions"""
    __tablename__ = "roles"
    
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text)
    is_system = Column(String(20), default=False)  # System roles cannot be deleted
    
    # Relationships
    permissions = relationship("Permission", secondary=role_permission, back_populates="roles")
    users = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Role {self.name}>"


class Permission(BaseModel):
    """Permission model - granular access controls"""
    __tablename__ = "permissions"
    
    name = Column(String(100), unique=True, nullable=False, index=True)
    resource = Column(String(50), nullable=False, index=True)  # e.g., "geofence", "asset", "zone"
    action = Column(String(50), nullable=False)  # e.g., "read", "write", "delete", "admin"
    description = Column(Text)
    
    # Relationships
    roles = relationship("Role", secondary=role_permission, back_populates="permissions")
    
    def __repr__(self):
        return f"<Permission {self.resource}:{self.action}>"


class UserRole(BaseModel):
    """User-Role association - many-to-many"""
    __tablename__ = "user_roles"
    
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")
    
    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )
    
    def __repr__(self):
        return f"<UserRole user_id={self.user_id} role_id={self.role_id}>"


class Policy(BaseModel):
    """Policy model - fine-grained access control rules"""
    __tablename__ = "policies"
    
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    resource_type = Column(String(50), nullable=False)  # e.g., "geofence", "asset"
    conditions = Column(Text)  # JSON string with policy conditions
    effect = Column(String(10), nullable=False, default="allow")  # "allow" or "deny"
    priority = Column(String(20), default=100)  # Lower number = higher priority
    
    # Relationships
    role_policies = relationship("RolePolicy", back_populates="policy", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Policy {self.name}>"


class RolePolicy(BaseModel):
    """Role-Policy association"""
    __tablename__ = "role_policies"
    
    role_id = Column(ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True)
    policy_id = Column(ForeignKey("policies.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Relationships
    role = relationship("Role")
    policy = relationship("Policy", back_populates="role_policies")
    
    __table_args__ = (
        UniqueConstraint("role_id", "policy_id", name="uq_role_policy"),
    )


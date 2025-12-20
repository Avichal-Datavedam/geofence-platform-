"""
API Key model
Multi-tenant API key management with different access scopes
"""
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
import secrets
import hashlib
from datetime import datetime, timedelta


class APIKeyScope:
    """Available API key scopes/permissions"""
    # Read scopes
    READ_GEOFENCES = "geofences:read"
    READ_ASSETS = "assets:read"
    READ_ZONES = "zones:read"
    READ_NOTIFICATIONS = "notifications:read"
    READ_ANALYTICS = "analytics:read"
    
    # Write scopes
    WRITE_GEOFENCES = "geofences:write"
    WRITE_ASSETS = "assets:write"
    WRITE_ZONES = "zones:write"
    WRITE_NOTIFICATIONS = "notifications:write"
    
    # Admin scopes
    ADMIN_USERS = "users:admin"
    ADMIN_ORGANIZATION = "organization:admin"
    ADMIN_API_KEYS = "api_keys:admin"
    
    # Special scopes
    REALTIME_TRACKING = "tracking:realtime"
    AI_ASSISTANT = "ai:access"
    WEBHOOKS = "webhooks:manage"
    
    # Preset bundles
    @classmethod
    def read_only(cls):
        return [cls.READ_GEOFENCES, cls.READ_ASSETS, cls.READ_ZONES, cls.READ_NOTIFICATIONS]
    
    @classmethod
    def standard(cls):
        return cls.read_only() + [cls.WRITE_GEOFENCES, cls.WRITE_ASSETS, cls.WRITE_ZONES]
    
    @classmethod
    def full_access(cls):
        return [
            cls.READ_GEOFENCES, cls.READ_ASSETS, cls.READ_ZONES, cls.READ_NOTIFICATIONS, cls.READ_ANALYTICS,
            cls.WRITE_GEOFENCES, cls.WRITE_ASSETS, cls.WRITE_ZONES, cls.WRITE_NOTIFICATIONS,
            cls.REALTIME_TRACKING, cls.AI_ASSISTANT, cls.WEBHOOKS
        ]
    
    @classmethod
    def admin(cls):
        return cls.full_access() + [cls.ADMIN_USERS, cls.ADMIN_ORGANIZATION, cls.ADMIN_API_KEYS]


class APIKey(BaseModel):
    """API Key for multi-tenant access"""
    __tablename__ = "api_keys"
    
    # Key identification
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    key_prefix = Column(String(8), nullable=False, index=True)  # First 8 chars for identification
    key_hash = Column(String(64), nullable=False, unique=True)  # SHA-256 hash of full key
    
    # Ownership - multi-tenant
    organization_id = Column(ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    created_by_id = Column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    
    # Permissions
    scopes = Column(JSON, nullable=False, default=list)  # List of scope strings
    
    # Rate limiting
    rate_limit_per_minute = Column(String(20), default=100)
    rate_limit_per_day = Column(String(20), default=10000)
    
    # Status and validity
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    usage_count = Column(String(20), default=0)
    
    # IP restrictions (optional)
    allowed_ips = Column(JSON, nullable=True)  # List of allowed IP addresses/ranges
    
    # Relationships
    organization = relationship("Organization", backref="api_keys")
    created_by = relationship("User", backref="created_api_keys")
    
    def __repr__(self):
        return f"<APIKey {self.name} ({self.key_prefix}...)>"
    
    @staticmethod
    def generate_key() -> tuple:
        """Generate a new API key and return (full_key, prefix, hash)"""
        # Generate a 32-byte random key, encode as hex (64 chars)
        full_key = f"gfp_{secrets.token_hex(32)}"  # gfp = geofence platform
        prefix = full_key[:12]  # gfp_ + 8 chars
        key_hash = hashlib.sha256(full_key.encode()).hexdigest()
        return full_key, prefix, key_hash
    
    @staticmethod
    def hash_key(key: str) -> str:
        """Hash an API key for comparison"""
        return hashlib.sha256(key.encode()).hexdigest()
    
    def has_scope(self, scope: str) -> bool:
        """Check if this API key has a specific scope"""
        return scope in (self.scopes or [])
    
    def has_any_scope(self, scopes: list) -> bool:
        """Check if this API key has any of the specified scopes"""
        return any(s in (self.scopes or []) for s in scopes)
    
    def is_valid(self) -> bool:
        """Check if API key is valid (active and not expired)"""
        if not self.is_active:
            return False
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return True

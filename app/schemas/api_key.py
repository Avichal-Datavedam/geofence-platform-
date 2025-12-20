"""
API Key schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class APIKeyScopeEnum(str, Enum):
    """Available API key scopes"""
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


class APIKeyPreset(str, Enum):
    """Preset scope bundles"""
    READ_ONLY = "read_only"
    STANDARD = "standard"
    FULL_ACCESS = "full_access"
    ADMIN = "admin"
    CUSTOM = "custom"


class APIKeyCreate(BaseModel):
    """Schema for creating an API key"""
    name: str = Field(..., min_length=1, max_length=100, description="Name for the API key")
    description: Optional[str] = Field(None, description="Description of what this key is used for")
    preset: APIKeyPreset = Field(APIKeyPreset.STANDARD, description="Preset scope bundle")
    custom_scopes: Optional[List[str]] = Field(None, description="Custom scopes (only if preset is CUSTOM)")
    expires_in_days: Optional[int] = Field(None, ge=1, le=365, description="Days until expiration (null = never)")
    rate_limit_per_minute: int = Field(100, ge=1, le=10000)
    rate_limit_per_day: int = Field(10000, ge=1, le=1000000)
    allowed_ips: Optional[List[str]] = Field(None, description="List of allowed IP addresses")


class APIKeyResponse(BaseModel):
    """Schema for API key response (without the actual key)"""
    id: str
    name: str
    description: Optional[str]
    key_prefix: str
    organization_id: str
    scopes: List[str]
    rate_limit_per_minute: int
    rate_limit_per_day: int
    is_active: bool
    expires_at: Optional[datetime]
    last_used_at: Optional[datetime]
    usage_count: int
    allowed_ips: Optional[List[str]]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class APIKeyCreatedResponse(APIKeyResponse):
    """Response when creating a new API key - includes the full key (shown only once)"""
    api_key: str = Field(..., description="The full API key - save this, it won't be shown again!")


class APIKeyUpdate(BaseModel):
    """Schema for updating an API key"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    scopes: Optional[List[str]] = None
    rate_limit_per_minute: Optional[int] = Field(None, ge=1, le=10000)
    rate_limit_per_day: Optional[int] = Field(None, ge=1, le=1000000)
    is_active: Optional[bool] = None
    allowed_ips: Optional[List[str]] = None


class APIKeyListResponse(BaseModel):
    """Paginated list of API keys"""
    items: List[APIKeyResponse]
    total: int
    page: int
    per_page: int


class APIKeyValidation(BaseModel):
    """Response for API key validation"""
    valid: bool
    key_id: Optional[str] = None
    organization_id: Optional[str] = None
    scopes: Optional[List[str]] = None
    error: Optional[str] = None

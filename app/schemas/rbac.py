"""
RBAC schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PermissionResponse(BaseModel):
    """Permission response schema"""
    id: str
    name: str
    resource: str
    action: str
    description: Optional[str]
    
    class Config:
        from_attributes = True


class RoleCreate(BaseModel):
    """Role creation schema"""
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    permission_ids: Optional[List[str]] = Field(default_factory=list)


class RoleResponse(BaseModel):
    """Role response schema"""
    id: str
    name: str
    description: Optional[str]
    is_system: bool
    permissions: List[PermissionResponse] = []
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserRoleAssign(BaseModel):
    """User role assignment schema"""
    user_id: str
    role_ids: List[str] = Field(..., min_items=1)


class PolicyCreate(BaseModel):
    """Policy creation schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    resource_type: str
    conditions: Optional[dict] = None
    effect: str = Field("allow", pattern="^(allow|deny)$")
    priority: int = Field(100, ge=0)


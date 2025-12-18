"""
Custom exceptions for the application
"""
from fastapi import HTTPException, status


class GeofenceNotFoundError(HTTPException):
    """Geofence not found exception"""
    def __init__(self, geofence_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Geofence with ID {geofence_id} not found"
        )


class AssetNotFoundError(HTTPException):
    """Asset not found exception"""
    def __init__(self, asset_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Asset with ID {asset_id} not found"
        )


class ZoneNotFoundError(HTTPException):
    """Zone not found exception"""
    def __init__(self, zone_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Zone with ID {zone_id} not found"
        )


class PermissionDeniedError(HTTPException):
    """Permission denied exception"""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )


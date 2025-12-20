"""API v1 routers"""
from fastapi import APIRouter
from app.api.v1 import auth, geofences, zones, assets, notifications, ai, geofence_access, api_keys

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(geofences.router)
api_router.include_router(geofence_access.router)
api_router.include_router(geofence_access.user_access_router)
api_router.include_router(zones.router)
api_router.include_router(assets.router)
api_router.include_router(notifications.router)
api_router.include_router(ai.router)
api_router.include_router(api_keys.router)

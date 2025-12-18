"""
Main FastAPI Application
Production-grade geo-fencing platform backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import get_settings
from app.api.v1 import api_router
from app.core.database import Base, engine, DB_AVAILABLE
from app.models import ai_service, asset, geofence, notification, organization, rbac, user, zone
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

# Create database tables (only if database is available)
from app.core.database import engine, DB_AVAILABLE
if engine and DB_AVAILABLE:
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("SUCCESS: Database tables created successfully")
    except Exception as e:
        logger.warning(f"WARNING: Could not create database tables: {e}")
        logger.info("INFO: App will run in limited mode without database")
else:
    logger.warning("WARNING: Database not available - API endpoints requiring database will not work")
    logger.info("TIP: To enable database features, set up PostgreSQL or use USE_SQLITE=true")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-grade geo-fencing platform with AI-first, zero-trust architecture",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.get_cors_methods(),
    allow_headers=settings.get_cors_headers(),
)

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Geo-fencing Platform API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from app.core.database import DB_AVAILABLE
    return {
        "status": "healthy" if DB_AVAILABLE else "limited",
        "version": settings.APP_VERSION,
        "database": "connected" if DB_AVAILABLE else "not available"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(exc)
            }
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )


"""
Database configuration and session management
PostgreSQL with PostGIS support, with SQLite fallback
"""
from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool, StaticPool
from typing import Generator, Optional
from app.core.config import get_settings
import os

settings = get_settings()

# Try to use PostgreSQL, with graceful error handling
database_url = settings.DATABASE_URL
engine = None
use_sqlite = False

# Check if we should use SQLite fallback
if "sqlite" in database_url.lower() or os.getenv("USE_SQLITE", "").lower() == "true":
    use_sqlite = True
    print("WARNING: Using SQLite - Geospatial features will be limited")
    database_url = "sqlite:///./geofence_dev.db"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
else:
    try:
        # Try PostgreSQL with PostGIS
        engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_MAX_OVERFLOW,
            pool_pre_ping=settings.DB_POOL_PRE_PING,
            echo=settings.DEBUG
        )
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        # Enable PostGIS extension on connection (only for PostgreSQL)
        @event.listens_for(engine, "connect")
        def set_postgis_extension(dbapi_conn, connection_record):
            """Enable PostGIS extension on each connection"""
            try:
                with dbapi_conn.cursor() as cursor:
                    cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")
                    cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis_topology")
            except Exception:
                # If PostGIS is not available, continue without it
                pass
        
        print("SUCCESS: Connected to PostgreSQL database")
    except Exception as e:
        print(f"WARNING: Could not connect to PostgreSQL: {e}")
        print("INFO: The app will start but database features will be unavailable.")
        print("TIP: To enable full features, set up PostgreSQL or use: USE_SQLITE=true")
        # Create a dummy engine that will fail gracefully
        engine = None

if engine:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    SessionLocal = None

Base = declarative_base()

# Store database availability
DB_AVAILABLE = engine is not None

def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency
    Yields a database session and ensures cleanup
    """
    if not engine or not SessionLocal:
        raise Exception("Database is not available. Please set up PostgreSQL or use USE_SQLITE=true")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


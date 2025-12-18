"""
Geometry column utility for SQLite/PostgreSQL compatibility
"""
from sqlalchemy import Column, Text
from app.core.config import get_settings
import os

settings = get_settings()

# Detect if using SQLite
USE_SQLITE = "sqlite" in settings.DATABASE_URL.lower() or os.getenv("USE_SQLITE", "").lower() == "true"

def GeometryColumn(geometry_type: str, srid: int = None, nullable: bool = True, index: bool = False):
    """
    Returns appropriate column type based on database.
    For SQLite: returns Text column (stores WKT/GeoJSON as string)
    For PostgreSQL: returns GeoAlchemy2 Geometry column
    """
    if USE_SQLITE:
        # SQLite: store geometry as Text (WKT or GeoJSON string)
        return Column(Text, nullable=nullable)
    else:
        # PostgreSQL with PostGIS
        from geoalchemy2 import Geometry
        return Column(
            Geometry(geometry_type, srid=srid or settings.DEFAULT_SRID),
            nullable=nullable,
            index=index
        )

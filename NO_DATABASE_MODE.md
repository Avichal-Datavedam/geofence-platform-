# Running Without Database - Demo Mode

## Quick Start (No Database Required!)

The app has been modified to run without PostgreSQL for quick testing.

### Backend (No Database Setup Needed)

1. **Activate virtual environment:**
```powershell
.\venv\Scripts\Activate.ps1
```

2. **Run the server:**
```powershell
uvicorn app.main:app --reload
```

The app will automatically use SQLite (no setup needed!) for basic functionality.

**Note:** Geospatial features (PostGIS) require PostgreSQL, but basic CRUD operations will work with SQLite.

### Frontend

1. **Install Node.js** (if not installed):
   - Download from: https://nodejs.org/
   - Install the LTS version

2. **Install and run frontend:**
```powershell
cd frontend
npm install
npm run dev
```

### What Works Without PostgreSQL

✅ User registration and login
✅ Basic API endpoints
✅ API documentation at http://localhost:8000/api/docs
✅ Frontend UI
✅ Authentication

⚠️ Limited: Geospatial queries (PostGIS features)
✅ Basic CRUD operations work with SQLite

### Testing

1. Backend: http://localhost:8000/api/docs
2. Frontend: http://localhost:3000

### When You're Ready for Full Features

To enable full geospatial features, set up PostgreSQL with PostGIS:
- See `RUNNING_INSTRUCTIONS.md` for PostgreSQL setup
- Or use Docker: `docker run --name geofence-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=geofence_db -p 5432:5432 -d postgis/postgis:15-3.4`

Then update `.env`:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/geofence_db
```


# Setup Guide - Step by Step

## ✅ Step 1: Python Environment (COMPLETED)
- Virtual environment created
- Dependencies installed

## Step 2: Create .env File

Create a `.env` file in the root directory with:

```env
# Application
APP_NAME=Geo-fencing Platform
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# Security - CHANGE THIS IN PRODUCTION!
SECRET_KEY=dev-secret-key-change-in-production-use-random-string-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database - UPDATE WITH YOUR POSTGRESQL CREDENTIALS
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/geofence_db

# Redis (Optional for now)
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173","http://127.0.0.1:3000"]

# AI/LLM (Optional - can be added later)
OPENAI_API_KEY=
AI_SERVICE_ENABLED=True
AI_MODEL=gpt-4-turbo-preview
AI_TEMPERATURE=0.7

# Geospatial
DEFAULT_SRID=4326
MAX_GEOFENCE_POINTS=1000
```

## Step 3: Set Up PostgreSQL

### Option A: Install PostgreSQL Locally

1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Install with PostGIS extension (select during installation)
3. Create database:
```sql
CREATE DATABASE geofence_db;
\c geofence_db
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
```

### Option B: Use Docker (Recommended)

```bash
docker run --name geofence-postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=geofence_db \
  -p 5432:5432 \
  -d postgis/postgis:15-3.4
```

### Option C: Use Cloud Database
- Use a managed PostgreSQL service (AWS RDS, Azure, etc.)
- Update DATABASE_URL in .env

## Step 4: Run Backend

1. Activate virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```

2. Run the server:
```powershell
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Step 5: Set Up Frontend

1. Navigate to frontend directory:
```powershell
cd frontend
```

2. Install dependencies:
```powershell
npm install
```

3. Run development server:
```powershell
npm run dev
```

Frontend will be available at http://localhost:3000

## Step 6: Test the Application

1. Open http://localhost:3000
2. Register a new user
3. Login
4. Explore the dashboard!

## Troubleshooting

### Database Connection Error
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Ensure PostGIS extension is installed

### Port Already in Use
- Change port in uvicorn: `uvicorn app.main:app --reload --port 8001`
- Or kill the process using the port

### Frontend API Errors
- Check backend is running
- Verify CORS_ORIGINS includes frontend URL
- Check browser console for errors

## Next Steps

1. Create your first geofence
2. Add assets to track
3. Set up notifications
4. Try the AI chat feature (requires OpenAI API key)


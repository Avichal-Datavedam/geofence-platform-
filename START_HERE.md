# 🚀 Quick Start - Run Without Database!

## Backend (No Database Setup Needed!)

### Step 1: Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### Step 2: Run Backend
```powershell
uvicorn app.main:app --reload
```

**That's it!** The app will start even without a database.

- ✅ API will be available at: http://localhost:8000
- ✅ API Docs at: http://localhost:8000/api/docs
- ⚠️ Database endpoints will show errors (expected without DB)

## Frontend

### Step 1: Install Node.js (if not installed)
Download from: https://nodejs.org/ (install LTS version)

### Step 2: Install and Run
```powershell
cd frontend
npm install
npm run dev
```

- ✅ Frontend at: http://localhost:3000

## What Works

✅ Backend API server runs
✅ API documentation works
✅ Frontend UI loads
✅ Authentication endpoints (will need DB for actual auth)
✅ All endpoints are accessible

⚠️ Database operations will fail (expected - no DB setup)

## To Enable Full Features

### Option 1: Use SQLite (Quick)
Set environment variable:
```powershell
$env:USE_SQLITE="true"
uvicorn app.main:app --reload
```

### Option 2: Use PostgreSQL (Full Features)
1. Install PostgreSQL with PostGIS
2. Create database
3. Update `.env` with `DATABASE_URL=postgresql://user:pass@localhost:5432/geofence_db`
4. Restart server

See `RUNNING_INSTRUCTIONS.md` for details.

## Test It Now!

1. Start backend: `uvicorn app.main:app --reload`
2. Visit: http://localhost:8000/api/docs
3. Start frontend: `cd frontend && npm run dev`
4. Visit: http://localhost:3000

Enjoy! 🎉


# 🚀 Quick Start - Run Without Database!

## ✅ Backend is Ready!

The app has been configured to run **without a database** for quick testing.

### Start Backend:

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run server
uvicorn app.main:app --reload
```

**That's it!** The server will start on http://localhost:8000

- ✅ API Docs: http://localhost:8000/api/docs
- ✅ Health Check: http://localhost:8000/health

**Note:** Database endpoints will show errors (expected without DB), but the API server runs fine!

## Frontend

### Step 1: Install Node.js
Download from: https://nodejs.org/ (LTS version)

### Step 2: Install & Run
```powershell
cd frontend
npm install
npm run dev
```

Frontend will be at: http://localhost:3000

## What Works

✅ Backend API server
✅ API documentation
✅ Frontend UI
✅ All endpoints accessible
⚠️ Database operations will fail (expected)

## To Enable Database Features Later

See `RUNNING_INSTRUCTIONS.md` for PostgreSQL setup.

For now, you can explore:
- API documentation at http://localhost:8000/api/docs
- Frontend UI at http://localhost:3000

Enjoy! 🎉


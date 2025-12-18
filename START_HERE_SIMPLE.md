# 🚀 Simple Guide - Run Both Services

## Step 1: Fix Node.js PATH (If Needed)

If `node --version` doesn't work:

1. **Close PowerShell completely**
2. **Reopen PowerShell**
3. Try: `node --version`

If still not working:
- Restart your computer (Node.js installer adds to PATH on restart)
- Or manually add Node.js to PATH (see below)

## Step 2: Run Backend

Open PowerShell in the project folder and run:

```powershell
# Make sure you're in: c:\Users\asus\Downloads\geofence-platform
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

**OR use the script:**
```powershell
.\start-backend.ps1
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

✅ Backend running at: http://localhost:8000

## Step 3: Run Frontend (In a NEW PowerShell Window)

Open a **NEW PowerShell window** and run:

```powershell
# Make sure you're in: c:\Users\asus\Downloads\geofence-platform
cd frontend
npm install
npm run dev
```

**OR use the script:**
```powershell
.\start-frontend.ps1
```

You should see:
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:3000/
```

✅ Frontend running at: http://localhost:3000

## Step 4: Open in Browser

- **Frontend:** http://localhost:3000
- **Backend API Docs:** http://localhost:8000/api/docs

## Quick Script to Start Both

```powershell
.\start-both.ps1
```

This opens both in separate windows!

## Troubleshooting

### Backend: "Module not found"
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend: "node not recognized"
1. Install Node.js: https://nodejs.org/
2. **RESTART PowerShell** (important!)
3. Try again

### Frontend: "npm install" fails
```powershell
cd frontend
npm install --legacy-peer-deps
```

### Port Already in Use
- Backend: Change port to 8001 in the command
- Frontend: Change port in `frontend/vite.config.ts`

## What You Need

✅ Python 3.11+ (you have this)
✅ Node.js 18+ (install from nodejs.org)
✅ Virtual environment activated for backend
✅ Dependencies installed (npm install in frontend folder)

## Current Status

- ✅ Backend code ready
- ✅ Frontend code ready  
- ⚠️ Need Node.js in PATH (restart PowerShell/computer)
- ⚠️ Need to install frontend dependencies (npm install)


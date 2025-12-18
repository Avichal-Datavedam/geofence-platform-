# How to Run Both Backend and Frontend

## Quick Start (Easiest Way)

### Option 1: Use the Startup Scripts

I've created PowerShell scripts to make it easy:

**Start Both at Once:**
```powershell
.\start-both.ps1
```

This will open two separate windows - one for backend, one for frontend.

**Or Start Separately:**

**Backend:**
```powershell
.\start-backend.ps1
```

**Frontend:**
```powershell
.\start-frontend.ps1
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```powershell
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
npm run dev
```

## Troubleshooting

### Backend Issues

**"Module not found" errors:**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**"Port 8000 already in use":**
- Change port: `uvicorn app.main:app --reload --port 8001`
- Or kill the process using port 8000

### Frontend Issues

**"node is not recognized":**
1. Install Node.js from https://nodejs.org/
2. **RESTART PowerShell completely**
3. Verify: `node --version`

**"npm install" fails:**
```powershell
cd frontend
npm install --legacy-peer-deps
```

**"Port 3000 already in use":**
- Change port in `frontend/vite.config.ts`
- Or use: `npm run dev -- --port 3001`

### Node.js PATH Issue

If Node.js is installed but not recognized:

1. Find Node.js installation path (usually `C:\Program Files\nodejs\`)
2. Add to PATH:
   - Right-click "This PC" → Properties
   - Advanced System Settings → Environment Variables
   - Edit "Path" → Add Node.js path
   - Restart PowerShell

Or simply restart your computer after installing Node.js.

## Verify Everything Works

1. **Backend:** http://localhost:8000/api/docs
2. **Frontend:** http://localhost:3000
3. **Health Check:** http://localhost:8000/health

## What You Should See

**Backend Terminal:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Frontend Terminal:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
```

## Need Help?

- Check `FRONTEND_SETUP.md` for frontend setup
- Check `RUNNING_INSTRUCTIONS.md` for detailed setup
- Check `QUICK_START.md` for quick reference


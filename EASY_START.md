# 🚀 EASY START - Run Both Services

## Quick Setup (Run Once)

```powershell
.\setup-and-run.ps1
```

This will:
- ✅ Check Python
- ✅ Setup backend dependencies
- ✅ Check Node.js
- ✅ Setup frontend dependencies

## Then Start Services

### Option 1: Start Both at Once (Easiest!)

```powershell
.\start-both.ps1
```

This opens two windows - one for backend, one for frontend.

### Option 2: Start Separately

**Terminal 1 - Backend:**
```powershell
.\start-backend.ps1
```

**Terminal 2 - Frontend:**
```powershell
.\start-frontend.ps1
```

### Option 3: Manual Start

**Backend:**
```powershell
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```powershell
cd frontend
npm run dev
```

## Access the Application

- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/api/docs

## Troubleshooting

### Backend won't start
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend: "node not recognized"
1. Install Node.js: https://nodejs.org/
2. **RESTART PowerShell** (very important!)
3. Try again

### Frontend: "npm install" fails
```powershell
cd frontend
npm install --legacy-peer-deps
```

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

- Backend issues: Check `RUNNING_INSTRUCTIONS.md`
- Frontend issues: Check `FRONTEND_SETUP.md`
- Node.js PATH: Check `FIX_NODEJS_PATH.md`


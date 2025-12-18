# 🎯 START HERE - Run Backend and Frontend

## ✅ Backend is Ready!

The backend is configured and ready to run.

## 🚀 Quick Start

### Step 1: Start Backend

Open PowerShell in the project folder and run:

```powershell
.\start-backend.ps1
```

**OR manually:**
```powershell
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

✅ Backend will run at: **http://localhost:8000**
✅ API Docs at: **http://localhost:8000/api/docs**

### Step 2: Start Frontend

**If Node.js is installed and working:**

Open a **NEW PowerShell window** and run:

```powershell
.\start-frontend.ps1
```

**OR manually:**
```powershell
cd frontend
npm install
npm run dev
```

✅ Frontend will run at: **http://localhost:3000**

### Step 3: Or Start Both at Once

```powershell
.\start-both.ps1
```

This opens both services in separate windows!

## ⚠️ If Node.js is Not Working

If `node --version` doesn't work:

1. **Close ALL PowerShell windows**
2. **Restart your computer** (this fixes PATH issues)
3. Open PowerShell again
4. Try: `node --version`

If still not working, see `FIX_NODEJS_PATH.md` for detailed instructions.

## 📋 What You Need

- ✅ Python 3.11+ (you have this)
- ✅ Virtual environment (already created)
- ✅ Backend dependencies (already installed)
- ⚠️ Node.js 18+ (install from https://nodejs.org/)
- ⚠️ Frontend dependencies (run `npm install` in frontend folder)

## 🎯 Current Status

- ✅ **Backend:** Ready to run!
- ⚠️ **Frontend:** Need Node.js in PATH (restart computer after installing)

## 📚 More Help

- **Backend setup:** `RUNNING_INSTRUCTIONS.md`
- **Frontend setup:** `FRONTEND_SETUP.md`
- **Node.js PATH fix:** `FIX_NODEJS_PATH.md`
- **Complete guide:** `EASY_START.md`

## 🎉 Once Both Are Running

- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs

Enjoy your geo-fencing platform! 🚀


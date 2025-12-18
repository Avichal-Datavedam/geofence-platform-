# Fix Blank Page Issue

## The Problem

You're seeing a blank white page because:
1. **Backend is not running** - Frontend needs backend API
2. **JavaScript errors** - Check browser console (F12)
3. **Missing Tailwind CSS** - Styles not loading

## Quick Fix Steps

### Step 1: Start Backend

Open a **NEW PowerShell window** and run:

```powershell
cd c:\Users\asus\Downloads\geofence-platform
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --port 8000
```

Wait until you see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 2: Check Browser Console

1. **Press F12** in your browser
2. Click **Console** tab
3. Look for **red error messages**
4. Share the errors with me

### Step 3: Restart Frontend

In the frontend terminal:
1. Press **Ctrl+C** to stop
2. Run again: `npm run dev`

### Step 4: Clear Browser Cache

1. Press **Ctrl+Shift+R** (hard refresh)
2. Or **Ctrl+F5**

## Common Errors & Fixes

### Error: "Failed to fetch" or Network errors
- **Fix:** Backend is not running - start it!

### Error: "Cannot find module"
- **Fix:** Run `npm install` in frontend folder

### Error: "Tailwind CSS" errors
- **Fix:** Already fixed in postcss.config.js

### Blank page with no errors
- **Fix:** Check if React is rendering - look for `<div id="root">` in page source

## Verify Everything

1. ✅ Backend running: http://localhost:8000/health
2. ✅ Frontend running: http://localhost:3000
3. ✅ No console errors (F12)
4. ✅ Backend terminal shows "Uvicorn running"

## Still Blank?

1. **Open browser console (F12)**
2. **Copy all red error messages**
3. **Check Network tab** - are files loading?
4. **Try different browser** (Edge, Firefox)

Let me know what errors you see in the console!


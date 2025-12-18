# Frontend Setup Guide

## Step 1: Install Node.js

Node.js is required to run the frontend. 

### Download and Install:
1. Go to: https://nodejs.org/
2. Download the **LTS version** (recommended)
3. Run the installer
4. **Important:** Make sure to check "Add to PATH" during installation
5. Restart your terminal/PowerShell after installation

### Verify Installation:
```powershell
node --version
npm --version
```

You should see version numbers (e.g., v20.x.x and 10.x.x)

## Step 2: Install Frontend Dependencies

Once Node.js is installed:

```powershell
cd frontend
npm install
```

This will install all required packages (React, Vite, Leaflet, etc.)

## Step 3: Run Frontend

```powershell
npm run dev
```

The frontend will start on: **http://localhost:3000**

## Troubleshooting

### "node is not recognized"
- Node.js is not installed or not in PATH
- Restart terminal after installation
- Reinstall Node.js and check "Add to PATH"

### "npm install" fails
- Check internet connection
- Try: `npm install --legacy-peer-deps`
- Delete `node_modules` folder and `package-lock.json`, then try again

### Port 3000 already in use
- Change port in `vite.config.ts` or use: `npm run dev -- --port 3001`

### Frontend can't connect to backend
- Make sure backend is running on http://localhost:8000
- Check `vite.config.ts` proxy settings
- Check CORS settings in backend `.env` file

## Quick Start (After Node.js Installation)

```powershell
# Navigate to frontend
cd frontend

# Install dependencies (first time only)
npm install

# Run development server
npm run dev
```

Then open: http://localhost:3000


# Install Node.js - Step by Step

## Why You Need Node.js

Node.js is required to run the frontend React application. It includes `npm` (Node Package Manager) which installs frontend dependencies.

## Installation Steps

### 1. Download Node.js

**Option A: Official Website (Recommended)**
- Go to: https://nodejs.org/
- Click "Download Node.js (LTS)" - this is the Long Term Support version
- The file will be something like: `node-v20.x.x-x64.msi`

**Option B: Direct Download**
- Windows 64-bit: https://nodejs.org/dist/v20.11.0/node-v20.11.0-x64.msi
- Choose the LTS version (even number like v20, v18, etc.)

### 2. Install Node.js

1. Run the downloaded `.msi` installer
2. Click "Next" through the setup wizard
3. **IMPORTANT:** Accept the license agreement
4. **IMPORTANT:** On "Custom Setup" page, make sure "Add to PATH" is checked (it should be by default)
5. Click "Install"
6. Wait for installation to complete
7. Click "Finish"

### 3. Verify Installation

**Close and reopen PowerShell**, then run:

```powershell
node --version
npm --version
```

You should see:
```
v20.11.0  (or similar version)
10.2.4    (or similar version)
```

If you see "command not found", restart your computer or check PATH settings.

### 4. Install Frontend Dependencies

Once Node.js is installed:

```powershell
cd frontend
npm install
```

This will take a few minutes to download all packages.

### 5. Run Frontend

```powershell
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

Open http://localhost:3000 in your browser!

## Troubleshooting

### "node is not recognized"
- **Solution 1:** Restart PowerShell/terminal completely
- **Solution 2:** Restart your computer
- **Solution 3:** Reinstall Node.js and make sure "Add to PATH" is checked

### "npm install" is slow or fails
- Check your internet connection
- Try: `npm install --legacy-peer-deps`
- If it fails, delete `node_modules` folder and try again

### Port 3000 already in use
- Change port in `vite.config.ts`
- Or kill the process using port 3000

## Quick Checklist

- [ ] Download Node.js LTS from nodejs.org
- [ ] Install Node.js (check "Add to PATH")
- [ ] Restart PowerShell
- [ ] Verify: `node --version` works
- [ ] Navigate to `frontend` folder
- [ ] Run: `npm install`
- [ ] Run: `npm run dev`
- [ ] Open http://localhost:3000

## Alternative: Use nvm (Node Version Manager)

If you want to manage multiple Node.js versions:

1. Install nvm-windows: https://github.com/coreybutler/nvm-windows/releases
2. Then: `nvm install lts`
3. Then: `nvm use lts`

But for now, just install Node.js directly - it's simpler!


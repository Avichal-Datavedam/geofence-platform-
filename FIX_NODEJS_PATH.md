# Fix Node.js PATH Issue

If you installed Node.js but `node --version` doesn't work, here's how to fix it:

## Method 1: Restart (Easiest)

1. **Close ALL PowerShell/Command Prompt windows**
2. **Restart your computer**
3. Open PowerShell again
4. Try: `node --version`

This usually fixes it because the Node.js installer updates PATH on restart.

## Method 2: Manual PATH Fix

### Step 1: Find Node.js Installation

Node.js is usually installed at:
- `C:\Program Files\nodejs\`
- `C:\Program Files (x86)\nodejs\`
- Or check: `C:\Users\YourName\AppData\Roaming\npm`

### Step 2: Add to PATH

1. Press `Win + X` → **System**
2. Click **Advanced system settings**
3. Click **Environment Variables**
4. Under **User variables**, find **Path** and click **Edit**
5. Click **New**
6. Add: `C:\Program Files\nodejs\` (or wherever Node.js is)
7. Click **OK** on all windows
8. **Close and reopen PowerShell**

### Step 3: Verify

```powershell
node --version
npm --version
```

## Method 3: Use Full Path (Temporary)

If you need to run it now without fixing PATH:

```powershell
# Find where Node.js is installed, then use full path:
& "C:\Program Files\nodejs\node.exe" --version
& "C:\Program Files\nodejs\npm.cmd" --version
```

## Method 4: Reinstall Node.js

1. Uninstall Node.js from Control Panel
2. Download fresh from https://nodejs.org/
3. Install again
4. **Make sure "Add to PATH" is checked during installation**
5. Restart computer

## Quick Test

After fixing PATH, test with:

```powershell
node --version
npm --version
cd frontend
npm install
npm run dev
```

If all commands work, you're good to go! 🎉


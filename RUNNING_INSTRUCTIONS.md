# Running Instructions - Quick Start

## ✅ What's Already Done

1. ✅ Python virtual environment created
2. ✅ All Python dependencies installed
3. ✅ Backend code structure verified
4. ✅ App imports successfully

## 🔧 What You Need to Do

### 1. Create .env File

Create a file named `.env` in the root directory (`c:\Users\asus\Downloads\geofence-platform\.env`) with this content:

```env
SECRET_KEY=dev-secret-key-change-in-production-12345
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/geofence_db
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
DEBUG=True
ENVIRONMENT=development
```

**Important:** Update `DATABASE_URL` with your PostgreSQL credentials!

### 2. Set Up PostgreSQL Database

You have 3 options:

#### Option A: Install PostgreSQL Locally
1. Download from: https://www.postgresql.org/download/windows/
2. During installation, make sure to install PostGIS extension
3. After installation, open pgAdmin or psql and run:
```sql
CREATE DATABASE geofence_db;
\c geofence_db
CREATE EXTENSION IF NOT EXISTS postgis;
```

#### Option B: Use Docker (Easiest)
If you have Docker installed:
```powershell
docker run --name geofence-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=geofence_db -p 5432:5432 -d postgis/postgis:15-3.4
```

#### Option C: Use SQLite for Testing (Quick Start)
For quick testing without PostgreSQL, you can modify the code to use SQLite, but PostGIS features won't work.

### 3. Run the Backend

Open PowerShell in the project directory and run:

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the server
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Then visit:
- API Docs: http://localhost:8000/api/docs
- API: http://localhost:8000

### 4. Set Up Frontend (Optional)

If you want to run the frontend:

1. **Install Node.js** (if not installed):
   - Download from: https://nodejs.org/
   - Install the LTS version

2. **Install frontend dependencies:**
```powershell
cd frontend
npm install
```

3. **Run frontend:**
```powershell
npm run dev
```

Frontend will be at: http://localhost:3000

## 🚀 Quick Test

Once backend is running, test it:

1. **Register a user:**
```powershell
curl -X POST http://localhost:8000/api/v1/auth/register -H "Content-Type: application/json" -d '{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"Test1234!\",\"full_name\":\"Test User\"}'
```

2. **Login:**
```powershell
curl -X POST http://localhost:8000/api/v1/auth/login -H "Content-Type: application/json" -d '{\"username\":\"testuser\",\"password\":\"Test1234!\"}'
```

3. **Or use the API docs:** Visit http://localhost:8000/api/docs and test directly in the browser!

## 📝 Common Issues

### "Database connection failed"
- Make sure PostgreSQL is running
- Check DATABASE_URL in .env matches your PostgreSQL setup
- Verify PostGIS extension is installed

### "Module not found"
- Make sure virtual environment is activated: `.\venv\Scripts\Activate.ps1`
- Reinstall: `pip install -r requirements.txt`

### "Port 8000 already in use"
- Change port: `uvicorn app.main:app --reload --port 8001`
- Or kill the process using port 8000

## 🎯 Next Steps After Running

1. Create your first geofence via API
2. Add assets to track
3. Test proximity detection
4. Try AI chat (needs OpenAI API key in .env)

## 📚 Documentation

- Full setup: See `SETUP_GUIDE.md`
- Architecture: See `ARCHITECTURE.md`
- Quick start: See `QUICKSTART.md`


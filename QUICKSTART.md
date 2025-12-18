# Quick Start Guide

## Prerequisites

- Python 3.11+
- PostgreSQL 15+ with PostGIS extension
- Node.js 18+ and npm
- Redis (optional, for caching)

## Backend Setup

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL with PostGIS:**
```sql
-- Connect to PostgreSQL
CREATE DATABASE geofence_db;
\c geofence_db
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

5. **Run the server:**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/api/docs`

## Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Run development server:**
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## First Steps

1. **Register a user:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "SecurePass123!",
    "full_name": "Admin User"
  }'
```

2. **Login:**
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "SecurePass123!"
  }'
```

3. **Create a geofence:**
```bash
curl -X POST http://localhost:8000/api/v1/geofences \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Geofence",
    "description": "A test geofence",
    "geometry": {
      "type": "Polygon",
      "coordinates": [[
        [77.2, 28.6],
        [77.3, 28.6],
        [77.3, 28.7],
        [77.2, 28.7],
        [77.2, 28.6]
      ]]
    },
    "center_point": {
      "latitude": 28.65,
      "longitude": 77.25
    },
    "altitude_min_meters": 0,
    "altitude_max_meters": 500
  }'
```

## Testing the AI Service

1. **Send a message to AI:**
```bash
curl -X POST http://localhost:8000/api/v1/ai/chat \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What is a geofence?",
    "context_type": "general"
  }'
```

## Frontend Usage

1. Open `http://localhost:3000` in your browser
2. Login with your credentials
3. Explore:
   - **Dashboard**: Overview with stats and AI chat
   - **Map View**: Interactive map with geofences and assets
   - **Geofences**: Manage geographic boundaries
   - **Assets**: Track entities
   - **Notifications**: View alerts

## Common Issues

### PostGIS not found
```bash
# Ubuntu/Debian
sudo apt-get install postgresql-postgis

# macOS
brew install postgis
```

### Database connection error
- Check PostgreSQL is running
- Verify DATABASE_URL in .env
- Ensure PostGIS extension is installed

### Frontend API errors
- Check backend is running on port 8000
- Verify CORS_ORIGINS includes frontend URL
- Check browser console for errors

## Next Steps

- Set up RBAC roles and permissions
- Configure AI service with OpenAI API key
- Add more geofences and assets
- Customize the dashboard
- Set up production deployment


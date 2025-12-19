# Geo-fencing Platform

FastAPI backend + React frontend for geo-fencing with map-based UI, asset tracking, and notifications.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, JWT Auth, PostgreSQL/SQLite
- **Frontend**: React 18, TypeScript, Vite, TailwindCSS, Leaflet Maps

---

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+

---

### Windows (PowerShell)

```powershell
# Clone & setup
git clone https://github.com/Avichal-Datavedam/geofence-platform-.git
cd geofence-platform-

# Backend setup
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt

# Create .env file
@"
SECRET_KEY=your-secret-key-change-in-production
USE_SQLITE=true
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
"@ | Out-File -FilePath .env -Encoding utf8

# Start backend (Terminal 1)
python -m uvicorn app.main:app --reload --port 8000

# Start frontend (Terminal 2)
cd frontend
npm install
npm run dev
```

### macOS / Linux

```bash
# Clone & setup
git clone https://github.com/Avichal-Datavedam/geofence-platform-.git
cd geofence-platform-

# Backend setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
SECRET_KEY=your-secret-key-change-in-production
USE_SQLITE=true
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
EOF

# Start backend (Terminal 1)
uvicorn app.main:app --reload --port 8000

# Start frontend (Terminal 2)
cd frontend
npm install
npm run dev
```

---

## URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## Project Structure

```
├── app/                 # Backend (FastAPI)
│   ├── api/v1/          # API routes
│   ├── core/            # Config, security
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   └── services/        # Business logic
├── frontend/            # Frontend (React)
│   └── src/
│       ├── components/  # UI components
│       ├── pages/       # Page views
│       └── services/    # API client
└── requirements.txt
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/login` | Login |
| GET | `/api/v1/geofences` | List geofences |
| POST | `/api/v1/geofences` | Create geofence |
| GET | `/api/v1/assets` | List assets |
| GET | `/api/v1/notifications` | List notifications |

Full API documentation at http://localhost:8000/docs

---

## License

MIT


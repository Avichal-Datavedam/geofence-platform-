# Geo-fencing Platform

Production-grade FastAPI backend with React frontend for a geo-fencing platform with AI-first, zero-trust architecture.

## Features

- **AI-first Architecture**: Integrated AI/LLM service for explanations and recommendations
- **Zero-trust Security**: JWT authentication, RBAC, and strict access controls
- **Modular RBAC**: Device-independent role-based access control system
- **REST-compliant API**: Full CRUD operations with proper HTTP methods
- **Geospatial Support**: PostgreSQL with PostGIS for advanced geospatial operations
- **Real-time Tracking**: Asset tracking with trajectory history
- **Proximity Detection**: Automatic notification generation for geofence breaches
- **Modern Frontend**: React with map-based UI and AI chat integration
- **Map Drawing Tools**: Lasso, Polygon, Rectangle, and Circle tools for creating geofences

---

## Quick Start

### Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **npm** or **yarn**

---

## Running Locally

### Windows (PowerShell)

```powershell
# 1. Clone the repository
git clone https://github.com/Avichal-Datavedam/geofence-platform-.git
cd geofence-platform-

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Create .env file
@"
SECRET_KEY=your-secret-key-change-in-production
USE_SQLITE=true
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
"@ | Out-File -FilePath .env -Encoding utf8

# 5. Start backend server (Terminal 1)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 6. Open a new terminal, then install and run frontend (Terminal 2)
cd frontend
npm install
npm run dev
```

### macOS / Linux (Terminal)

```bash
# 1. Clone the repository
git clone https://github.com/Avichal-Datavedam/geofence-platform-.git
cd geofence-platform-

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Create .env file
cat > .env << EOF
SECRET_KEY=your-secret-key-change-in-production
USE_SQLITE=true
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
EOF

# 5. Start backend server (Terminal 1)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 6. Open a new terminal, then install and run frontend (Terminal 2)
cd frontend
npm install
npm run dev
```

---

## Access the Application

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |
| **API Docs (ReDoc)** | http://localhost:8000/redoc |
| **Health Check** | http://localhost:8000/health |

---

## Architecture

### Backend Structure

```
app/
├── api/v1/          # API routers (REST endpoints)
├── core/            # Configuration, security, dependencies
├── models/          # SQLAlchemy database models
├── schemas/         # Pydantic validation schemas
├── services/        # Business logic (Single Responsibility)
└── main.py         # FastAPI application entry point
```

### Frontend Structure

```
frontend/
├── src/
│   ├── components/  # Reusable React components
│   ├── contexts/    # React contexts (Auth, etc.)
│   ├── pages/       # Page components
│   ├── services/    # API client services
│   └── App.tsx      # Main application
```

## Modules

1. **Assets**: Trackable entities (drones, vehicles, devices)
2. **Geofences**: Geometric boundaries with altitude support
3. **Zones**: Logical areas within geofences
4. **Notifications**: Proximity detection and alerting
5. **AI/LLM Service**: Explanations, recommendations, and chat

## Setup

### Backend

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (create `.env`):
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/geofence_db
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=your-openai-api-key  # Optional
CORS_ORIGINS=["http://localhost:3000"]
```

3. Initialize database:
```bash
# Make sure PostgreSQL with PostGIS is running
# The app will create tables automatically on startup
```

4. Run the server:
```bash
uvicorn app.main:app --reload
```

### Frontend

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run development server:
```bash
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get tokens
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/refresh` - Refresh access token

### Geofences
- `GET /api/v1/geofences` - List geofences
- `POST /api/v1/geofences` - Create geofence
- `GET /api/v1/geofences/{id}` - Get geofence
- `PUT /api/v1/geofences/{id}` - Update geofence
- `PATCH /api/v1/geofences/{id}` - Partial update
- `DELETE /api/v1/geofences/{id}` - Delete geofence
- `GET /api/v1/geofences/nearby/search` - Find nearby geofences

### Assets
- `GET /api/v1/assets` - List assets
- `POST /api/v1/assets` - Create asset
- `GET /api/v1/assets/{id}` - Get asset
- `PUT /api/v1/assets/{id}/location` - Update asset location
- `GET /api/v1/assets/{id}/trajectory` - Get trajectory history

### Zones
- `GET /api/v1/zones` - List zones
- `POST /api/v1/zones` - Create zone
- `GET /api/v1/zones/{id}` - Get zone
- `PUT /api/v1/zones/{id}` - Update zone
- `DELETE /api/v1/zones/{id}` - Delete zone

### Notifications
- `GET /api/v1/notifications` - List notifications
- `POST /api/v1/notifications` - Create notification
- `POST /api/v1/notifications/check-proximity/{asset_id}` - Check proximity
- `PATCH /api/v1/notifications/{id}/acknowledge` - Acknowledge notification

### AI Service
- `POST /api/v1/ai/chat` - Send message to AI
- `GET /api/v1/ai/conversations` - List conversations
- `GET /api/v1/ai/conversations/{id}` - Get conversation
- `POST /api/v1/ai/recommendations` - Generate recommendation

## RBAC System

The platform uses a modular RBAC system with:
- **Roles**: Groups of permissions (e.g., admin, operator, viewer)
- **Permissions**: Granular access controls (resource:action format)
- **Policies**: Fine-grained rules for specific resources

Example permissions:
- `geofence:read`
- `geofence:write`
- `geofence:delete`
- `asset:read`
- `asset:write`

## Database Schema

Key tables:
- `users` - User accounts
- `roles`, `permissions`, `user_roles` - RBAC system
- `geofences` - Geographic boundaries
- `zones` - Logical areas
- `assets` - Trackable entities
- `asset_trajectories` - Location history
- `notifications` - Alerts and proximity events
- `ai_conversations`, `ai_messages` - AI chat history
- `ai_recommendations` - AI-generated recommendations

## Security Features

- JWT-based authentication with refresh tokens
- Password hashing with bcrypt
- Zero-trust architecture (verify everything)
- CORS protection
- Input validation with Pydantic
- SQL injection prevention via ORM

## Frontend Features

- **Dashboard**: Overview with stats, charts, and AI chat widget
- **Map View**: Interactive map with geofences and assets
- **Geofences**: Manage geographic boundaries
- **Assets**: Track and manage assets
- **Notifications**: View and acknowledge alerts
- **AI Chat**: Integrated AI assistant for explanations and recommendations

## Development

### Running Tests
```bash
pytest
```

### Database Migrations
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Production Deployment

1. Set `ENVIRONMENT=production` in `.env`
2. Configure proper CORS origins
3. Use production-grade database (PostgreSQL with PostGIS)
4. Set up Redis for caching
5. Configure reverse proxy (Nginx)
6. Enable HTTPS/TLS
7. Set up monitoring and logging

## License

MIT


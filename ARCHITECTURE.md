# Architecture Overview

## Design Principles

### 1. AI-First Architecture
- AI/LLM service integrated at the core
- AI chat assistant for user interactions
- AI-generated recommendations for geofences, assets, and zones
- Context-aware AI responses based on user's current view

### 2. Zero-Trust Security
- Every request is authenticated and authorized
- JWT tokens with short expiration (15 minutes)
- Token rotation on refresh
- RBAC with granular permissions
- No implicit trust - verify everything

### 3. Single Responsibility Principle
- Each service class has one clear purpose
- Services are independent and testable
- Clear separation: Router → Service → Model
- No monolithic classes

### 4. REST-Compliant API
- Proper HTTP methods: GET, POST, PUT, PATCH, DELETE
- Resource-based URLs
- Standard status codes
- Consistent response formats

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │Dashboard │  │ Map View │  │Geofences  │  │  AI Chat ││
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘│
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/REST
┌─────────────────────▼────────────────────────────────────┐
│              FastAPI Backend (Port 8000)                 │
│  ┌────────────────────────────────────────────────────┐  │
│  │              API Routers (v1)                     │  │
│  │  /auth  /geofences  /zones  /assets  /notifications│ │
│  └──────────────────┬───────────────────────────────┘  │
│                      │                                   │
│  ┌───────────────────▼───────────────────────────────┐  │
│  │            Service Layer                           │  │
│  │  GeofenceService  ZoneService  AssetService        │  │
│  │  NotificationService  AIService  AuthService      │  │
│  └───────────────────┬───────────────────────────────┘  │
│                      │                                   │
│  ┌───────────────────▼───────────────────────────────┐  │
│  │         Dependency Injection                      │  │
│  │  AuthDependency  PermissionChecker  RoleChecker   │  │
│  └───────────────────┬───────────────────────────────┘  │
│                      │                                   │
│  ┌───────────────────▼───────────────────────────────┐  │
│  │            Database Models (SQLAlchemy)            │  │
│  └───────────────────┬───────────────────────────────┘  │
└──────────────────────┼──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌─────▼─────┐ ┌─────▼─────┐
│ PostgreSQL   │ │   Redis   │ │  OpenAI   │
│  + PostGIS    │ │  (Cache)  │ │   API     │
└──────────────┘ └───────────┘ └───────────┘
```

## Module Breakdown

### 1. Assets Module
**Purpose**: Track and manage trackable entities (drones, vehicles, devices)

**Components**:
- `Asset` model: Core entity with location, status, metadata
- `AssetTrajectory` model: Historical location data
- `AssetService`: Business logic for asset operations
- `AssetRouter`: REST endpoints

**Key Features**:
- Real-time location tracking
- Trajectory history
- Status management
- Organization association

### 2. Geofences Module
**Purpose**: Define geographic boundaries with altitude constraints

**Components**:
- `Geofence` model: PostGIS geometry, altitude bounds
- `GeofenceService`: CRUD operations, spatial queries
- `GeofenceRouter`: REST endpoints

**Key Features**:
- Polygon, circle, rectangle support
- Altitude min/max constraints
- Spatial indexing for performance
- Proximity detection

### 3. Zones Module
**Purpose**: Logical areas within geofences

**Components**:
- `Zone` model: Zone type, rules, priority
- `ZoneService`: Zone management
- `ZoneRouter`: REST endpoints

**Key Features**:
- Zone types (restricted, monitoring, safe)
- Custom rules per zone
- Priority levels
- Geofence association

### 4. Notifications Module
**Purpose**: Alert system for proximity detection and breaches

**Components**:
- `Notification` model: Alert data, severity, status
- `NotificationService`: Alert generation, proximity checks
- `NotificationRouter`: REST endpoints

**Key Features**:
- Automatic proximity detection
- Severity levels (critical, high, medium, low, info)
- Acknowledgment workflow
- Location-based alerts

### 5. AI/LLM Service Module
**Purpose**: AI-powered explanations, recommendations, and chat

**Components**:
- `AIConversation` model: Chat threads
- `AIMessage` model: Individual messages
- `AIRecommendation` model: Generated recommendations
- `AIService`: OpenAI integration, context management
- `AIRouter`: REST endpoints

**Key Features**:
- Context-aware conversations
- Entity-specific recommendations
- Conversation history
- Multi-turn dialogues

## RBAC System

### Structure
```
User
  └── UserRole (many-to-many)
       └── Role
            └── RolePermission (many-to-many)
                 └── Permission (resource:action)
```

### Permission Format
- `{resource}:{action}`
- Examples: `geofence:read`, `asset:write`, `zone:delete`

### Roles
- **Admin**: Full system access
- **Operator**: Operational access (write geofences, assets)
- **Analyst**: Read access with analytics
- **Viewer**: Read-only access

### Policies
- Fine-grained rules for specific resources
- Conditions-based access control
- Priority-based evaluation

## Database Design

### Key Tables
1. **users**: User accounts and authentication
2. **roles, permissions, user_roles**: RBAC system
3. **geofences**: Geographic boundaries (PostGIS)
4. **zones**: Logical areas
5. **assets**: Trackable entities
6. **asset_trajectories**: Location history
7. **notifications**: Alerts and events
8. **ai_conversations, ai_messages**: AI chat
9. **ai_recommendations**: AI suggestions

### Spatial Features
- PostGIS Geography type for accurate calculations
- Spatial indexes (GIST) for performance
- Functions: ST_Intersects, ST_Distance, ST_DWithin

## API Design

### Versioning
- URL-based: `/api/v1/`
- Header-based for minor versions

### Response Format
```json
{
  "success": true,
  "data": {...},
  "meta": {
    "timestamp": "2025-12-03T18:36:12Z",
    "request_id": "uuid"
  },
  "pagination": {...}
}
```

### Error Format
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {...}
  }
}
```

## Frontend Architecture

### Component Structure
```
src/
├── components/     # Reusable components
│   ├── Layout.tsx
│   ├── AIChatWidget.tsx
│   └── ProtectedRoute.tsx
├── pages/          # Page components
│   ├── Dashboard.tsx
│   ├── MapView.tsx
│   ├── Geofences.tsx
│   ├── Assets.tsx
│   └── Notifications.tsx
├── contexts/       # React contexts
│   └── AuthContext.tsx
└── services/      # API clients
    └── api.ts
```

### State Management
- React Query for server state
- Context API for auth state
- Local state for UI state

### Map Integration
- Leaflet for map rendering
- React-Leaflet for React integration
- GeoJSON for geofence rendering
- Real-time asset markers

## Security Measures

1. **Authentication**
   - JWT tokens
   - Refresh token rotation
   - Password hashing (bcrypt)

2. **Authorization**
   - RBAC with permissions
   - Policy-based access control
   - Dependency injection for checks

3. **Data Protection**
   - Input validation (Pydantic)
   - SQL injection prevention (ORM)
   - CORS configuration
   - Rate limiting

4. **Audit**
   - Request logging
   - User action tracking
   - Error logging

## Performance Optimizations

1. **Database**
   - Spatial indexes
   - Connection pooling
   - Query optimization

2. **Caching**
   - Redis for frequently accessed data
   - TTL-based expiration
   - Multi-layer caching

3. **Frontend**
   - Code splitting
   - Lazy loading
   - Optimistic updates

## Deployment Considerations

1. **Backend**
   - Gunicorn/Uvicorn workers
   - Nginx reverse proxy
   - PostgreSQL with read replicas
   - Redis cluster

2. **Frontend**
   - Static file serving (CDN)
   - Environment-based config
   - Build optimization

3. **Monitoring**
   - Health checks
   - Metrics collection
   - Log aggregation
   - Error tracking

## Scalability

- Horizontal scaling of API servers
- Database read replicas
- Redis cluster for distributed caching
- Message queue for async tasks
- CDN for static assets

## Future Enhancements

1. WebSocket support for real-time updates
2. Advanced analytics and reporting
3. Multi-tenant isolation
4. Mobile app support
5. Advanced AI features (predictive analytics)
6. Integration with external systems
7. Advanced geospatial operations
8. Batch operations API


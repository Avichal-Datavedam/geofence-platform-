# Deploy to Render

## Quick Deploy Steps

### 1. Push to GitHub
First, push your code to a GitHub repository:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/geofence-platform.git
git push -u origin main
```

### 2. Deploy Backend on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `geofence-api`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables:
   - `USE_SQLITE` = `true`
   - `SECRET_KEY` = (generate a random string)
   - `DEBUG` = `false`
   - `CORS_ORIGINS` = `https://YOUR-FRONTEND-URL.onrender.com`
6. Click **Create Web Service**

### 3. Deploy Frontend on Render

1. Click **New +** → **Static Site**
2. Connect the same GitHub repository
3. Configure:
   - **Name**: `geofence-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
4. Add Environment Variable:
   - `VITE_API_URL` = `https://geofence-api.onrender.com/api/v1`
5. Add Redirect/Rewrite Rule:
   - Source: `/*`
   - Destination: `/index.html`
   - Type: Rewrite
6. Click **Create Static Site**

### 4. Update CORS (After Both Deploy)

Once both are deployed, update the backend's `CORS_ORIGINS` environment variable with your actual frontend URL.

## Environment Variables Reference

### Backend
| Variable | Description | Example |
|----------|-------------|---------|
| `USE_SQLITE` | Use SQLite database | `true` |
| `SECRET_KEY` | JWT secret key | Random 32+ char string |
| `DEBUG` | Debug mode | `false` |
| `CORS_ORIGINS` | Allowed origins | `https://geofence-frontend.onrender.com` |

### Frontend
| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://geofence-api.onrender.com/api/v1` |

## Test Your Deployment

1. Visit your frontend URL: `https://geofence-frontend.onrender.com`
2. Register a new user
3. Login and explore the dashboard

## Troubleshooting

- **CORS errors**: Ensure `CORS_ORIGINS` includes your frontend URL
- **API not found**: Check `VITE_API_URL` is correct
- **Database errors**: Verify `USE_SQLITE=true` is set

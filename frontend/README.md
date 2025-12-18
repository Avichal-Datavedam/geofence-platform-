# Frontend - Geo-fencing Platform

React + TypeScript + Vite frontend for the geo-fencing platform.

## Prerequisites

- Node.js 18+ (download from https://nodejs.org/)
- npm (comes with Node.js)

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at: http://localhost:3000

## Project Structure

```
src/
├── components/     # Reusable components
├── pages/          # Page components
├── contexts/       # React contexts (Auth)
├── services/       # API client
└── App.tsx        # Main app component
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Features

- 🗺️ Interactive map with Leaflet
- 📊 Dashboard with charts
- 🤖 AI chat assistant
- 🔐 Authentication
- 📱 Responsive design

## Backend Connection

The frontend connects to the backend API at `http://localhost:8000` via proxy configured in `vite.config.ts`.

Make sure the backend is running before using the frontend!


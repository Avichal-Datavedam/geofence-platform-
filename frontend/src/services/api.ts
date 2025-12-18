import axios from 'axios'

// Use environment variable for API URL in production, fallback to relative path for local dev
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response.data,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle token refresh or redirect to login
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authApi = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }),
  register: (data: any) => api.post('/auth/register', data),
  getCurrentUser: () => api.get('/auth/me'),
  refreshToken: (refreshToken: string) =>
    api.post('/auth/refresh', { refresh_token: refreshToken }),
}

export const geofenceApi = {
  list: (params?: any) => api.get('/geofences', { params }),
  get: (id: string) => api.get(`/geofences/${id}`),
  create: (data: any) => api.post('/geofences', data),
  update: (id: string, data: any) => api.put(`/geofences/${id}`, data),
  delete: (id: string) => api.delete(`/geofences/${id}`),
  findNearby: (lat: number, lon: number, radius: number) =>
    api.get('/geofences/nearby/search', {
      params: { latitude: lat, longitude: lon, radius_meters: radius },
    }),
}

export const assetApi = {
  list: (params?: any) => api.get('/assets', { params }),
  get: (id: string) => api.get(`/assets/${id}`),
  create: (data: any) => api.post('/assets', data),
  updateLocation: (id: string, data: any) =>
    api.put(`/assets/${id}/location`, data),
  getTrajectory: (id: string, params?: any) =>
    api.get(`/assets/${id}/trajectory`, { params }),
}

export const notificationApi = {
  list: (params?: any) => api.get('/notifications', { params }),
  create: (data: any) => api.post('/notifications', data),
  acknowledge: (id: string) => api.patch(`/notifications/${id}/acknowledge`),
  checkProximity: (assetId: string, lat: number, lon: number) =>
    api.post(`/notifications/check-proximity/${assetId}`, null, {
      params: { latitude: lat, longitude: lon },
    }),
}

export const aiApi = {
  sendMessage: (data: any) => api.post('/ai/chat', data),
  getConversations: (params?: any) => api.get('/ai/conversations', { params }),
  getConversation: (id: string) => api.get(`/ai/conversations/${id}`),
  generateRecommendation: (params: any) =>
    api.post('/ai/recommendations', null, { params }),
}

export default api


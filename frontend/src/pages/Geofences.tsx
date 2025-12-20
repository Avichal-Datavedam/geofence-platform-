import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { geofenceApi } from '../services/api'
import { Hexagon, MapPin, AlertCircle, Plus, X, Trash2, Edit, Eye, Map } from 'lucide-react'
import GeofenceMap from '../components/GeofenceMap'

interface CreateGeofenceForm {
  name: string
  description: string
  geofence_type: string
  latitude: string
  longitude: string
  radius: string
  altitude_min: string
  altitude_max: string
  priority: string
  geometry: any
}

const Geofences = () => {
  const queryClient = useQueryClient()
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [useMapDrawing, setUseMapDrawing] = useState(true)
  const [formData, setFormData] = useState<CreateGeofenceForm>({
    name: '',
    description: '',
    geofence_type: 'polygon',
    latitude: '',
    longitude: '',
    radius: '100',
    altitude_min: '0',
    altitude_max: '1000',
    priority: '5',
    geometry: null,
  })
  const [error, setError] = useState('')

  const { data, isLoading } = useQuery({
    queryKey: ['geofences'],
    queryFn: () => geofenceApi.list({ per_page: 100 }),
  })

  const createMutation = useMutation({
    mutationFn: (data: any) => geofenceApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['geofences'] })
      setShowCreateModal(false)
      resetForm()
    },
    onError: (err: any) => {
      setError(err.response?.data?.detail || 'Failed to create geofence')
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => geofenceApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['geofences'] })
    },
  })

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      geofence_type: 'polygon',
      latitude: '',
      longitude: '',
      radius: '100',
      altitude_min: '0',
      altitude_max: '1000',
      priority: '5',
      geometry: null,
    })
    setError('')
    setUseMapDrawing(true)
  }

  const handleGeometryCreated = (geometry: any, center: { lat: number; lng: number }) => {
    setFormData({
      ...formData,
      geometry,
      latitude: center.lat.toString(),
      longitude: center.lng.toString(),
      geofence_type: geometry.type === 'Circle' ? 'circular' : 'polygon',
      radius: geometry.radius?.toString() || '100',
    })
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    const lat = parseFloat(formData.latitude)
    const lng = parseFloat(formData.longitude)
    const radius = parseFloat(formData.radius)

    if (isNaN(lat) || isNaN(lng)) {
      setError('Please enter valid latitude and longitude')
      return
    }

    const geofenceData = {
      name: formData.name,
      description: formData.description,
      geofence_type: formData.geofence_type,
      geometry: {
        type: 'Point',
        coordinates: [lng, lat],
      },
      center_point: {
        latitude: lat,
        longitude: lng,
      },
      radius_meters: radius,
      altitude_min_meters: parseFloat(formData.altitude_min),
      altitude_max_meters: parseFloat(formData.altitude_max),
      priority: parseInt(formData.priority),
      status: 'active',
    }

    createMutation.mutate(geofenceData)
  }

  if (isLoading) {
    return (
      <div className="p-8">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8 bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
      {/* Header */}
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent">
            Geofences
          </h1>
          <p className="mt-2 text-gray-600">Manage your geographic boundaries and zones</p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-xl hover:from-primary-700 hover:to-primary-800 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5"
        >
          <Plus className="h-5 w-5" />
          Create Geofence
        </button>
      </div>

      {/* Stats Bar */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Hexagon className="h-5 w-5 text-blue-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">{data?.items?.length || 0}</p>
              <p className="text-sm text-gray-500">Total Geofences</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-100 rounded-lg">
              <Eye className="h-5 w-5 text-green-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {data?.items?.filter((g: any) => g.status === 'active').length || 0}
              </p>
              <p className="text-sm text-gray-500">Active</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-100 rounded-lg">
              <MapPin className="h-5 w-5 text-purple-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {data?.items?.filter((g: any) => g.geofence_type === 'circular').length || 0}
              </p>
              <p className="text-sm text-gray-500">Circular</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-100 rounded-lg">
              <AlertCircle className="h-5 w-5 text-orange-600" />
            </div>
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {data?.items?.filter((g: any) => g.priority >= 8).length || 0}
              </p>
              <p className="text-sm text-gray-500">High Priority</p>
            </div>
          </div>
        </div>
      </div>

      {/* Geofences Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data?.items?.map((geofence: any) => (
          <div
            key={geofence.id}
            className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 hover:shadow-lg transition-all duration-200 hover:-translate-y-1 group"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-br from-primary-100 to-primary-200 rounded-xl">
                  <Hexagon className="h-6 w-6 text-primary-600" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{geofence.name}</h3>
                  <span className="text-xs text-gray-500 capitalize">{geofence.geofence_type}</span>
                </div>
              </div>
              <span
                className={`px-3 py-1 text-xs font-semibold rounded-full ${
                  geofence.status === 'active'
                    ? 'bg-green-100 text-green-700 ring-1 ring-green-200'
                    : 'bg-gray-100 text-gray-600 ring-1 ring-gray-200'
                }`}
              >
                {geofence.status}
              </span>
            </div>

            {geofence.description && (
              <p className="text-sm text-gray-600 mb-4 line-clamp-2">{geofence.description}</p>
            )}

            <div className="space-y-3 text-sm">
              <div className="flex items-center text-gray-600 bg-gray-50 rounded-lg p-2">
                <MapPin className="h-4 w-4 mr-2 text-primary-500" />
                <span className="font-mono text-xs">
                  {geofence.center_point?.latitude?.toFixed(4)},{' '}
                  {geofence.center_point?.longitude?.toFixed(4)}
                </span>
              </div>
              <div className="flex items-center justify-between text-gray-600">
                <div className="flex items-center">
                  <AlertCircle className="h-4 w-4 mr-2 text-orange-500" />
                  <span className="text-xs">
                    Alt: {geofence.altitude_min_meters}m - {geofence.altitude_max_meters}m
                  </span>
                </div>
                <span className={`text-xs font-medium px-2 py-1 rounded ${
                  geofence.priority >= 8 ? 'bg-red-100 text-red-700' :
                  geofence.priority >= 5 ? 'bg-yellow-100 text-yellow-700' :
                  'bg-blue-100 text-blue-700'
                }`}>
                  P{geofence.priority}
                </span>
              </div>
            </div>

            {/* Action buttons */}
            <div className="mt-4 pt-4 border-t border-gray-100 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button className="flex-1 flex items-center justify-center gap-1 px-3 py-2 text-xs font-medium text-primary-600 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors">
                <Edit className="h-3 w-3" />
                Edit
              </button>
              <button
                onClick={() => deleteMutation.mutate(geofence.id)}
                className="flex items-center justify-center gap-1 px-3 py-2 text-xs font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors"
              >
                <Trash2 className="h-3 w-3" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {(!data?.items || data.items.length === 0) && (
        <div className="text-center py-16 bg-white rounded-2xl border-2 border-dashed border-gray-200">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
            <Hexagon className="h-8 w-8 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No geofences yet</h3>
          <p className="text-gray-500 mb-4">Create your first geofence to get started</p>
          <button
            onClick={() => setShowCreateModal(true)}
            className="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <Plus className="h-4 w-4" />
            Create Geofence
          </button>
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[95vh] overflow-y-auto">
            <div className="flex items-center justify-between p-6 border-b border-gray-100">
              <div>
                <h2 className="text-xl font-bold text-gray-900">Create New Geofence</h2>
                <p className="text-sm text-gray-500 mt-1">Draw your geofence on the map or enter coordinates manually</p>
              </div>
              <button
                onClick={() => { setShowCreateModal(false); resetForm(); }}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <X className="h-5 w-5 text-gray-500" />
              </button>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
              {/* Map Section */}
              <div className="flex flex-col">
                <div className="flex items-center justify-between mb-3">
                  <label className="block text-sm font-medium text-gray-700">
                    <Map className="inline h-4 w-4 mr-1" />
                    Draw on Map
                  </label>
                  <button
                    type="button"
                    onClick={() => setUseMapDrawing(!useMapDrawing)}
                    className={`text-xs px-3 py-1 rounded-full transition-colors ${
                      useMapDrawing 
                        ? 'bg-primary-100 text-primary-700' 
                        : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {useMapDrawing ? 'Map Mode' : 'Manual Mode'}
                  </button>
                </div>
                
                {useMapDrawing ? (
                  <div className="relative" style={{ height: '400px', minHeight: '400px' }}>
                    <GeofenceMap
                      onGeometryCreated={handleGeometryCreated}
                      existingGeofences={data?.items || []}
                      height="400px"
                    />
                  </div>
                ) : (
                  <div className="h-[400px] bg-gray-100 rounded-xl flex items-center justify-center border-2 border-dashed border-gray-300">
                    <div className="text-center text-gray-500">
                      <Map className="h-12 w-12 mx-auto mb-2 opacity-50" />
                      <p>Map drawing disabled</p>
                      <p className="text-xs">Enter coordinates manually</p>
                    </div>
                  </div>
                )}

                {formData.geometry && (
                  <div className="mt-3 p-3 bg-green-50 border border-green-200 rounded-lg">
                    <p className="text-sm text-green-700 font-medium">✓ Geometry captured</p>
                    <p className="text-xs text-green-600">
                      Type: {formData.geometry.type} | Center: {formData.latitude}, {formData.longitude}
                    </p>
                  </div>
                )}
              </div>

              {/* Form Section */}
              <form onSubmit={handleSubmit} className="space-y-4">
                {error && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                    {error}
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    placeholder="e.g., Office Building Zone"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    rows={2}
                    placeholder="Optional description..."
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Latitude</label>
                    <input
                      type="number"
                      step="any"
                      value={formData.latitude}
                      onChange={(e) => setFormData({ ...formData, latitude: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors bg-gray-50"
                      placeholder="From map"
                      readOnly={useMapDrawing && !!formData.geometry}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Longitude</label>
                    <input
                      type="number"
                      step="any"
                      value={formData.longitude}
                      onChange={(e) => setFormData({ ...formData, longitude: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors bg-gray-50"
                      placeholder="From map"
                      readOnly={useMapDrawing && !!formData.geometry}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Min Altitude (m)</label>
                    <input
                      type="number"
                      value={formData.altitude_min}
                      onChange={(e) => setFormData({ ...formData, altitude_min: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Max Altitude (m)</label>
                    <input
                      type="number"
                      value={formData.altitude_max}
                      onChange={(e) => setFormData({ ...formData, altitude_max: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Priority (1-10)</label>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>Low</span>
                    <span className="font-medium text-primary-600">Priority: {formData.priority}</span>
                    <span>High</span>
                  </div>
                </div>

                <div className="flex gap-3 pt-4">
                  <button
                    type="button"
                    onClick={() => { setShowCreateModal(false); resetForm(); }}
                    className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={createMutation.isPending || (!formData.geometry && !formData.latitude)}
                    className="flex-1 px-4 py-2 bg-gradient-to-r from-primary-600 to-primary-700 text-white rounded-lg hover:from-primary-700 hover:to-primary-800 transition-colors disabled:opacity-50"
                  >
                    {createMutation.isPending ? 'Creating...' : 'Create Geofence'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Geofences


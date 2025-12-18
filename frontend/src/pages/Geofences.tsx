import { useQuery } from '@tanstack/react-query'
import { geofenceApi } from '../services/api'
import { Hexagon, MapPin, AlertCircle } from 'lucide-react'

const Geofences = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['geofences'],
    queryFn: () => geofenceApi.list({ per_page: 100 }),
  })

  if (isLoading) {
    return (
      <div className="p-8">
        <div className="animate-pulse">Loading geofences...</div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <div className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Geofences</h1>
          <p className="mt-2 text-gray-600">Manage your geographic boundaries</p>
        </div>
        <button className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
          Create Geofence
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data?.items?.map((geofence: any) => (
          <div
            key={geofence.id}
            className="bg-white rounded-lg shadow border border-gray-200 p-6 hover:shadow-lg transition-shadow"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <Hexagon className="h-5 w-5 text-primary-600 mr-2" />
                <h3 className="text-lg font-semibold text-gray-900">{geofence.name}</h3>
              </div>
              <span
                className={`px-2 py-1 text-xs font-medium rounded ${
                  geofence.status === 'active'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {geofence.status}
              </span>
            </div>

            {geofence.description && (
              <p className="text-sm text-gray-600 mb-4">{geofence.description}</p>
            )}

            <div className="space-y-2 text-sm">
              <div className="flex items-center text-gray-600">
                <MapPin className="h-4 w-4 mr-2" />
                <span>
                  {geofence.center_point?.latitude?.toFixed(4)},{' '}
                  {geofence.center_point?.longitude?.toFixed(4)}
                </span>
              </div>
              <div className="flex items-center text-gray-600">
                <AlertCircle className="h-4 w-4 mr-2" />
                <span>
                  Altitude: {geofence.altitude_min_meters}m - {geofence.altitude_max_meters}m
                </span>
              </div>
              <div className="pt-2 border-t border-gray-200">
                <span className="text-xs text-gray-500">
                  Priority: {geofence.priority}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {(!data?.items || data.items.length === 0) && (
        <div className="text-center py-12">
          <Hexagon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No geofences found</p>
        </div>
      )}
    </div>
  )
}

export default Geofences


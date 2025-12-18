import { MapContainer, TileLayer, Polygon, Marker, Popup, useMap } from 'react-leaflet'
import { useQuery } from '@tanstack/react-query'
import { geofenceApi, assetApi } from '../services/api'
import { LatLngExpression } from 'leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix for default marker icon
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

const MapView = () => {
  const { data: geofences } = useQuery({
    queryKey: ['geofences'],
    queryFn: () => geofenceApi.list({ per_page: 100 }),
  })

  const { data: assets } = useQuery({
    queryKey: ['assets'],
    queryFn: () => assetApi.list({ per_page: 100 }),
  })

  const defaultCenter: LatLngExpression = [28.6139, 77.2090] // Default to Delhi
  const defaultZoom = 10

  const getPolygonCoordinates = (geometry: any): LatLngExpression[] => {
    if (geometry.type === 'Polygon' && geometry.coordinates) {
      return geometry.coordinates[0].map((coord: number[]) => [coord[1], coord[0]] as LatLngExpression)
    }
    return []
  }

  return (
    <div className="h-screen w-full relative">
      <div className="absolute top-4 left-4 z-[1000] bg-white rounded-lg shadow-lg p-4">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">Map View</h2>
        <div className="space-y-1 text-sm text-gray-600">
          <p>Geofences: {geofences?.total || 0}</p>
          <p>Active Assets: {assets?.length || 0}</p>
        </div>
      </div>

      <MapContainer
        center={defaultCenter}
        zoom={defaultZoom}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Render Geofences */}
        {geofences?.items?.map((geofence: any) => {
          const coordinates = getPolygonCoordinates(geofence.geometry)
          if (coordinates.length === 0) return null

          return (
            <Polygon
              key={geofence.id}
              positions={coordinates}
              pathOptions={{
                color: geofence.status === 'active' ? '#3b82f6' : '#9ca3af',
                fillColor: geofence.status === 'active' ? '#3b82f6' : '#9ca3af',
                fillOpacity: 0.2,
                weight: 2,
              }}
            >
              <Popup>
                <div>
                  <h3 className="font-semibold">{geofence.name}</h3>
                  <p className="text-sm text-gray-600">{geofence.description}</p>
                  <p className="text-xs mt-1">
                    Status: <span className="font-medium">{geofence.status}</span>
                  </p>
                  <p className="text-xs">
                    Altitude: {geofence.altitude_min_meters}m - {geofence.altitude_max_meters}m
                  </p>
                </div>
              </Popup>
            </Polygon>
          )
        })}

        {/* Render Assets */}
        {assets?.map((asset: any) => {
          if (!asset.current_location) return null

          return (
            <Marker
              key={asset.id}
              position={[asset.current_location.latitude, asset.current_location.longitude]}
            >
              <Popup>
                <div>
                  <h3 className="font-semibold">{asset.name}</h3>
                  <p className="text-sm text-gray-600">{asset.asset_type}</p>
                  <p className="text-xs mt-1">
                    Status: <span className="font-medium">{asset.status}</span>
                  </p>
                  {asset.altitude_meters && (
                    <p className="text-xs">Altitude: {asset.altitude_meters.toFixed(1)}m</p>
                  )}
                </div>
              </Popup>
            </Marker>
          )
        })}
      </MapContainer>
    </div>
  )
}

export default MapView


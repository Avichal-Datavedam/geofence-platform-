import { useState, useEffect, useRef } from 'react'
import { MapContainer, TileLayer, Polygon, Marker, Popup, useMap, Circle, ZoomControl, ScaleControl } from 'react-leaflet'
import { useQuery } from '@tanstack/react-query'
import { geofenceApi, assetApi } from '../services/api'
import { LatLngExpression } from 'leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'
import MapSearchControl from '../components/MapSearchControl'
import { 
  Layers, Navigation, Maximize2, Minimize2, RefreshCw, 
  Eye, EyeOff, Crosshair, Map as MapIcon, Satellite, Mountain,
  List, MapPin, ChevronRight, X, Play, Pause
} from 'lucide-react'

// Fix for default marker icon
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

// Asset type icons as SVG paths
const assetTypeIcons: Record<string, string> = {
  vehicle: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/></svg>`,
  drone: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M22 11h-2V9h-2v2h-2V9h-2v2h-2V9H10v2H8V9H6v2H4V9H2v2h2v2H2v2h2v-2h2v2h2v-2h2v2h2v-2h2v2h2v-2h2v2h2v-2h-2v-2h2zm-10 2H8v-2h4v2z"/></svg>`,
  device: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/></svg>`,
  tracker: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm8.94 3c-.46-4.17-3.77-7.48-7.94-7.94V1h-2v2.06C6.83 3.52 3.52 6.83 3.06 11H1v2h2.06c.46 4.17 3.77 7.48 7.94 7.94V23h2v-2.06c4.17-.46 7.48-3.77 7.94-7.94H23v-2h-2.06zM12 19c-3.87 0-7-3.13-7-7s3.13-7 7-7 7 3.13 7 7-3.13 7-7 7z"/></svg>`,
}

// Custom marker icons
const createCustomIcon = (color: string, type: 'asset' | 'search' = 'asset') => {
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="
      background: ${color};
      width: ${type === 'search' ? '20px' : '14px'};
      height: ${type === 'search' ? '20px' : '14px'};
      border-radius: 50%;
      border: 3px solid white;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    "></div>`,
    iconSize: [type === 'search' ? 20 : 14, type === 'search' ? 20 : 14],
    iconAnchor: [type === 'search' ? 10 : 7, type === 'search' ? 10 : 7],
  })
}

// Create asset icon based on type
const createAssetIcon = (assetType: string, isActive: boolean) => {
  const bgColor = isActive ? '#22c55e' : '#9ca3af'
  const iconSvg = assetTypeIcons[assetType] || assetTypeIcons.tracker
  
  return L.divIcon({
    className: 'custom-asset-marker',
    html: `<div style="
      background: ${bgColor};
      width: 36px;
      height: 36px;
      border-radius: 50%;
      border: 3px solid white;
      box-shadow: 0 3px 10px rgba(0,0,0,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    ">
      <div style="width: 20px; height: 20px; display: flex; align-items: center; justify-content: center;">
        ${iconSvg}
      </div>
    </div>`,
    iconSize: [36, 36],
    iconAnchor: [18, 18],
  })
}

// Map controller component for programmatic control
const MapController = ({ center, zoom, onMouseMove }: { 
  center?: [number, number], 
  zoom?: number,
  onMouseMove?: (lat: number, lng: number) => void 
}) => {
  const map = useMap()
  
  useEffect(() => {
    if (center) {
      map.flyTo(center, zoom || map.getZoom(), { duration: 1.5 })
    }
  }, [center, zoom, map])

  useEffect(() => {
    if (onMouseMove) {
      const handleMouseMove = (e: L.LeafletMouseEvent) => {
        onMouseMove(e.latlng.lat, e.latlng.lng)
      }
      map.on('mousemove', handleMouseMove)
      return () => {
        map.off('mousemove', handleMouseMove)
      }
    }
  }, [map, onMouseMove])
  
  return null
}

// Tile layer options
const tileLayers = {
  street: {
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '© OpenStreetMap contributors',
    name: 'Street Map'
  },
  satellite: {
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: '© Esri',
    name: 'Satellite'
  },
  terrain: {
    url: 'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    attribution: '© OpenTopoMap',
    name: 'Terrain'
  }
}

const MapView = () => {
  const [mapCenter, setMapCenter] = useState<[number, number] | undefined>(undefined)
  const [mapZoom, setMapZoom] = useState<number | undefined>(undefined)
  const [searchMarker, setSearchMarker] = useState<{ lat: number, lng: number, name: string } | null>(null)
  const [currentLayer, setCurrentLayer] = useState<'street' | 'satellite' | 'terrain'>('street')
  const [showGeofences, setShowGeofences] = useState(true)
  const [showAssets, setShowAssets] = useState(true)
  const [isFullscreen, setIsFullscreen] = useState(false)
  const [currentLocation, setCurrentLocation] = useState<[number, number] | null>(null)
  const [showLayerPanel, setShowLayerPanel] = useState(false)
  const [showZonesList, setShowZonesList] = useState(true)
  const [mouseCoords, setMouseCoords] = useState<{ lat: number, lng: number } | null>(null)
  const [placeNames, setPlaceNames] = useState<Record<string, string>>({})
  const [isSimulating, setIsSimulating] = useState(false)
  const [simulatedPositions, setSimulatedPositions] = useState<Record<string, { lat: number, lng: number, heading: number }>>({})
  const mapContainerRef = useRef<HTMLDivElement>(null)

  const { data: geofences, refetch: refetchGeofences } = useQuery({
    queryKey: ['geofences'],
    queryFn: () => geofenceApi.list({ per_page: 100 }),
  })

  const { data: assets, refetch: refetchAssets } = useQuery({
    queryKey: ['assets'],
    queryFn: () => assetApi.list({ per_page: 100 }),
  })

  const defaultCenter: LatLngExpression = [20.5937, 78.9629] // India center
  const defaultZoom = 5

  // Fetch place names for geofences using reverse geocoding
  useEffect(() => {
    const fetchPlaceNames = async () => {
      const items = (geofences as any)?.items || []
      for (const geofence of items) {
        if (placeNames[geofence.id]) continue // Skip if already fetched
        
        let lat: number | null = null
        let lng: number | null = null
        
        if (geofence.center_point) {
          lat = geofence.center_point.latitude
          lng = geofence.center_point.longitude
        } else if (geofence.geometry?.type === 'Point') {
          lng = geofence.geometry.coordinates[0]
          lat = geofence.geometry.coordinates[1]
        }
        
        if (lat && lng) {
          try {
            const response = await fetch(
              `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=14`
            )
            const data = await response.json()
            const placeName = data.address?.city || data.address?.town || data.address?.village || 
                              data.address?.suburb || data.address?.county || data.address?.state || 'Unknown'
            setPlaceNames(prev => ({ ...prev, [geofence.id]: placeName }))
          } catch (error) {
            console.error('Error fetching place name:', error)
            setPlaceNames(prev => ({ ...prev, [geofence.id]: 'Unknown' }))
          }
        }
      }
    }
    
    if ((geofences as any)?.items?.length > 0) {
      fetchPlaceNames()
    }
  }, [(geofences as any)?.items])

  // Initialize simulated positions from actual asset positions
  useEffect(() => {
    const assetList = ((assets as any)?.items || assets as any) || []
    if (Array.isArray(assetList) && assetList.length > 0) {
      const initialPositions: Record<string, { lat: number, lng: number, heading: number }> = {}
      assetList.forEach((asset: any) => {
        if (asset.current_location && !simulatedPositions[asset.id]) {
          initialPositions[asset.id] = {
            lat: asset.current_location.latitude,
            lng: asset.current_location.longitude,
            heading: Math.random() * 360
          }
        }
      })
      if (Object.keys(initialPositions).length > 0) {
        setSimulatedPositions(prev => ({ ...prev, ...initialPositions }))
      }
    }
  }, [assets])

  // Simulation interval - move assets randomly
  useEffect(() => {
    if (!isSimulating) return

    const interval = setInterval(() => {
      setSimulatedPositions(prev => {
        const updated = { ...prev }
        Object.keys(updated).forEach(id => {
          const pos = updated[id]
          // Random movement - adjust heading slightly and move forward
          const headingChange = (Math.random() - 0.5) * 30 // -15 to +15 degrees
          const newHeading = (pos.heading + headingChange + 360) % 360
          const speed = 0.0005 + Math.random() * 0.001 // Random speed
          
          // Calculate new position based on heading
          const radians = (newHeading * Math.PI) / 180
          const newLat = pos.lat + Math.cos(radians) * speed
          const newLng = pos.lng + Math.sin(radians) * speed
          
          updated[id] = { lat: newLat, lng: newLng, heading: newHeading }
        })
        return updated
      })
    }, 500) // Update every 500ms

    return () => clearInterval(interval)
  }, [isSimulating])

  const getPolygonCoordinates = (geometry: any): LatLngExpression[] => {
    if (geometry.type === 'Polygon' && geometry.coordinates) {
      return geometry.coordinates[0].map((coord: number[]) => [coord[1], coord[0]] as LatLngExpression)
    }
    return []
  }

  const getPointCoordinates = (geometry: any): [number, number] | null => {
    if (geometry.type === 'Point' && geometry.coordinates) {
      return [geometry.coordinates[1], geometry.coordinates[0]]
    }
    return null
  }

  const isPointGeometry = (geometry: any): boolean => {
    return geometry?.type === 'Point'
  }

  // Handle location search
  const handleLocationSelect = (lat: number, lng: number, name: string) => {
    setSearchMarker({ lat, lng, name })
    setMapCenter([lat, lng])
    setMapZoom(15)
  }

  // Get current location
  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const { latitude, longitude } = position.coords
          setCurrentLocation([latitude, longitude])
          setMapCenter([latitude, longitude])
          setMapZoom(16)
        },
        (error) => {
          console.error('Error getting location:', error)
          alert('Unable to get your location. Please enable location services.')
        },
        { enableHighAccuracy: true }
      )
    }
  }

  // Toggle fullscreen
  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      mapContainerRef.current?.requestFullscreen()
      setIsFullscreen(true)
    } else {
      document.exitFullscreen()
      setIsFullscreen(false)
    }
  }

  // Refresh data
  const refreshData = () => {
    refetchGeofences()
    refetchAssets()
  }

  // Get status color
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return '#22c55e'
      case 'inactive': return '#9ca3af'
      case 'monitoring': return '#f59e0b'
      default: return '#6366f1'
    }
  }

  return (
    <div ref={mapContainerRef} className="h-[calc(100vh-4rem)] w-full relative bg-gray-100">
      {/* Top Search Bar */}
      <div className="absolute top-4 left-1/2 -translate-x-1/2 z-[1000] w-full max-w-xl px-4">
        <MapSearchControl 
          onLocationSelect={handleLocationSelect}
          onGetCurrentLocation={getCurrentLocation}
        />
      </div>

      {/* Stats Panel */}
      <div className="absolute top-20 left-4 z-[1000] bg-white/95 backdrop-blur-sm rounded-xl shadow-lg p-4 min-w-[200px]">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-sm font-semibold text-gray-900">Overview</h2>
          <button 
            onClick={refreshData}
            className="p-1.5 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
            title="Refresh data"
          >
            <RefreshCw className="h-4 w-4" />
          </button>
        </div>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Geofences</span>
            <span className="text-sm font-semibold text-primary-600">{(geofences as any)?.total || (geofences as any)?.items?.length || 0}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">Active Assets</span>
            <span className="text-sm font-semibold text-green-600">{(assets as any)?.items?.length || (assets as any)?.length || 0}</span>
          </div>
        </div>

        {/* Visibility Toggles */}
        <div className="mt-4 pt-3 border-t border-gray-100">
          <p className="text-xs font-medium text-gray-500 uppercase mb-2">Visibility</p>
          <div className="space-y-1">
            <button
              onClick={() => setShowGeofences(!showGeofences)}
              className={`w-full flex items-center gap-2 px-2 py-1.5 rounded-lg text-sm transition-colors ${
                showGeofences ? 'bg-primary-50 text-primary-700' : 'text-gray-500 hover:bg-gray-50'
              }`}
            >
              {showGeofences ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
              Geofences
            </button>
            <button
              onClick={() => setShowAssets(!showAssets)}
              className={`w-full flex items-center gap-2 px-2 py-1.5 rounded-lg text-sm transition-colors ${
                showAssets ? 'bg-green-50 text-green-700' : 'text-gray-500 hover:bg-gray-50'
              }`}
            >
              {showAssets ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
              Assets
            </button>
          </div>
        </div>

        {/* Simulation Control */}
        <div className="mt-4 pt-3 border-t border-gray-100">
          <p className="text-xs font-medium text-gray-500 uppercase mb-2">Simulation</p>
          <button
            onClick={() => setIsSimulating(!isSimulating)}
            className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
              isSimulating 
                ? 'bg-orange-500 text-white shadow-md' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {isSimulating ? (
              <>
                <Pause className="h-4 w-4" />
                Stop Simulation
              </>
            ) : (
              <>
                <Play className="h-4 w-4" />
                Start Simulation
              </>
            )}
          </button>
          {isSimulating && (
            <p className="text-xs text-orange-600 mt-2 flex items-center gap-1">
              <span className="w-2 h-2 bg-orange-500 rounded-full animate-pulse"></span>
              Assets are moving...
            </p>
          )}
        </div>
      </div>

      {/* Layer Switcher */}
      <div className="absolute top-20 right-4 z-[1000] flex gap-2">
        {/* Zones List Toggle */}
        <button
          onClick={() => setShowZonesList(!showZonesList)}
          className={`bg-white/95 backdrop-blur-sm rounded-xl shadow-lg p-3 hover:bg-gray-50 transition-colors ${
            showZonesList ? 'ring-2 ring-primary-500' : ''
          }`}
          title="Toggle zones list"
        >
          <List className="h-5 w-5 text-gray-700" />
        </button>

        <div className="relative">
          <button
            onClick={() => setShowLayerPanel(!showLayerPanel)}
            className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg p-3 hover:bg-gray-50 transition-colors"
            title="Change map style"
          >
            <Layers className="h-5 w-5 text-gray-700" />
          </button>
          
          {showLayerPanel && (
            <div className="absolute top-full right-0 mt-2 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden w-40">
              <button
                onClick={() => { setCurrentLayer('street'); setShowLayerPanel(false) }}
                className={`w-full flex items-center gap-3 px-4 py-3 text-sm transition-colors ${
                  currentLayer === 'street' ? 'bg-primary-50 text-primary-700' : 'hover:bg-gray-50'
                }`}
              >
                <MapIcon className="h-4 w-4" />
                Street
              </button>
              <button
                onClick={() => { setCurrentLayer('satellite'); setShowLayerPanel(false) }}
                className={`w-full flex items-center gap-3 px-4 py-3 text-sm transition-colors ${
                  currentLayer === 'satellite' ? 'bg-primary-50 text-primary-700' : 'hover:bg-gray-50'
                }`}
              >
                <Satellite className="h-4 w-4" />
                Satellite
              </button>
              <button
                onClick={() => { setCurrentLayer('terrain'); setShowLayerPanel(false) }}
                className={`w-full flex items-center gap-3 px-4 py-3 text-sm transition-colors ${
                  currentLayer === 'terrain' ? 'bg-primary-50 text-primary-700' : 'hover:bg-gray-50'
                }`}
              >
                <Mountain className="h-4 w-4" />
                Terrain
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Zones List Panel */}
      {showZonesList && (
        <div className="absolute top-36 right-4 z-[1000] bg-white/95 backdrop-blur-sm rounded-xl shadow-lg w-72 max-h-[calc(100vh-220px)] flex flex-col">
          <div className="flex items-center justify-between p-3 border-b border-gray-100">
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4 text-primary-600" />
              <h3 className="font-semibold text-sm text-gray-900">Zones</h3>
              <span className="bg-primary-100 text-primary-700 text-xs px-2 py-0.5 rounded-full font-medium">
                {(geofences as any)?.items?.length || 0}
              </span>
            </div>
            <button
              onClick={() => setShowZonesList(false)}
              className="p-1 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <X className="h-4 w-4 text-gray-400" />
            </button>
          </div>
          
          <div className="overflow-y-auto flex-1 p-2">
            {(geofences as any)?.items?.length > 0 ? (
              <div className="space-y-1">
                {(geofences as any)?.items?.map((geofence: any) => {
                  const color = getStatusColor(geofence.status)
                  return (
                    <button
                      key={geofence.id}
                      onClick={() => {
                        if (geofence.center_point) {
                          setMapCenter([geofence.center_point.latitude, geofence.center_point.longitude])
                          setMapZoom(15)
                        } else if (geofence.geometry) {
                          const coords = isPointGeometry(geofence.geometry) 
                            ? getPointCoordinates(geofence.geometry)
                            : null
                          if (coords) {
                            setMapCenter(coords)
                            setMapZoom(15)
                          }
                        }
                      }}
                      className="w-full flex items-center gap-3 p-2.5 rounded-lg hover:bg-gray-50 transition-colors text-left group"
                    >
                      <div 
                        className="w-3 h-3 rounded-full flex-shrink-0 shadow-sm"
                        style={{ backgroundColor: color, boxShadow: `0 0 0 3px ${color}30` }}
                      />
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">{geofence.name}</p>
                        <p className="text-xs text-gray-500 truncate">
                          {placeNames[geofence.id] ? (
                            <span className="text-primary-600">{placeNames[geofence.id]}</span>
                          ) : (
                            <span className="text-gray-400">Loading...</span>
                          )}
                          {' • '}<span className="capitalize">{geofence.status}</span>
                        </p>
                      </div>
                      <ChevronRight className="h-4 w-4 text-gray-300 group-hover:text-gray-500 transition-colors flex-shrink-0" />
                    </button>
                  )
                })}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <MapPin className="h-8 w-8 mx-auto mb-2 text-gray-300" />
                <p className="text-sm">No zones created yet</p>
                <p className="text-xs mt-1">Create geofences to see them here</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Map Controls */}
      <div className="absolute bottom-8 right-4 z-[1000] flex flex-col gap-2">
        <button
          onClick={getCurrentLocation}
          className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg p-3 hover:bg-gray-50 transition-colors"
          title="Go to my location"
        >
          <Navigation className="h-5 w-5 text-gray-700" />
        </button>
        <button
          onClick={toggleFullscreen}
          className="bg-white/95 backdrop-blur-sm rounded-xl shadow-lg p-3 hover:bg-gray-50 transition-colors"
          title={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'}
        >
          {isFullscreen ? (
            <Minimize2 className="h-5 w-5 text-gray-700" />
          ) : (
            <Maximize2 className="h-5 w-5 text-gray-700" />
          )}
        </button>
      </div>

      {/* Coordinates Display */}
      {mouseCoords && (
        <div className="absolute bottom-8 left-4 z-[1000] bg-white/95 backdrop-blur-sm rounded-lg shadow-lg px-3 py-2">
          <div className="flex items-center gap-2 text-xs text-gray-600">
            <Crosshair className="h-3 w-3" />
            <span>Lat: {mouseCoords.lat.toFixed(6)}</span>
            <span className="text-gray-300">|</span>
            <span>Lng: {mouseCoords.lng.toFixed(6)}</span>
          </div>
        </div>
      )}

      {/* Map Container */}
      <MapContainer
        center={defaultCenter}
        zoom={defaultZoom}
        style={{ height: '100%', width: '100%' }}
        zoomControl={false}
        className="rounded-none"
      >
        <MapController 
          center={mapCenter} 
          zoom={mapZoom} 
          onMouseMove={(lat, lng) => setMouseCoords({ lat, lng })}
        />
        <ZoomControl position="bottomright" />
        <ScaleControl position="bottomleft" metric={true} imperial={false} />
        
        <TileLayer
          attribution={tileLayers[currentLayer].attribution}
          url={tileLayers[currentLayer].url}
        />

        {/* Search Result Marker */}
        {searchMarker && (
          <>
            <Marker 
              position={[searchMarker.lat, searchMarker.lng]}
              icon={createCustomIcon('#ef4444', 'search')}
            >
              <Popup>
                <div className="p-1">
                  <h3 className="font-semibold text-sm">{searchMarker.name.split(',')[0]}</h3>
                  <p className="text-xs text-gray-500 mt-1">
                    {searchMarker.lat.toFixed(6)}, {searchMarker.lng.toFixed(6)}
                  </p>
                </div>
              </Popup>
            </Marker>
            <Circle
              center={[searchMarker.lat, searchMarker.lng]}
              radius={100}
              pathOptions={{
                color: '#ef4444',
                fillColor: '#ef4444',
                fillOpacity: 0.1,
                weight: 2,
                dashArray: '5, 5'
              }}
            />
          </>
        )}

        {/* Current Location Marker */}
        {currentLocation && (
          <>
            <Marker 
              position={currentLocation}
              icon={createCustomIcon('#3b82f6', 'search')}
            >
              <Popup>
                <div className="p-1">
                  <h3 className="font-semibold text-sm">Your Location</h3>
                  <p className="text-xs text-gray-500 mt-1">
                    {currentLocation[0].toFixed(6)}, {currentLocation[1].toFixed(6)}
                  </p>
                </div>
              </Popup>
            </Marker>
            <Circle
              center={currentLocation}
              radius={50}
              pathOptions={{
                color: '#3b82f6',
                fillColor: '#3b82f6',
                fillOpacity: 0.15,
                weight: 2
              }}
            />
          </>
        )}

        {/* Render Geofences */}
        {showGeofences && (geofences as any)?.items?.map((geofence: any) => {
          const color = getStatusColor(geofence.status)
          
          // Check if it's a Point geometry
          if (isPointGeometry(geofence.geometry)) {
            const pointCoords = getPointCoordinates(geofence.geometry)
            if (!pointCoords) return null
            
            return (
              <Circle
                key={geofence.id}
                center={pointCoords}
                radius={500}
                pathOptions={{
                  color: color,
                  fillColor: color,
                  fillOpacity: 0.25,
                  weight: 3,
                }}
              >
                <Popup>
                  <div className="p-1 min-w-[180px]">
                    <div className="flex items-center gap-2 mb-2">
                      <div className="w-3 h-3 rounded-full" style={{ backgroundColor: color }}></div>
                      <h3 className="font-semibold text-sm">{geofence.name}</h3>
                    </div>
                    {geofence.description && (
                      <p className="text-xs text-gray-600 mb-2">{geofence.description}</p>
                    )}
                    <div className="space-y-1 text-xs">
                      <div className="flex justify-between">
                        <span className="text-gray-500">Status</span>
                        <span className="font-medium capitalize">{geofence.status}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-500">Priority</span>
                        <span className="font-medium">{geofence.priority}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-500">Altitude</span>
                        <span className="font-medium">{geofence.altitude_min_meters}m - {geofence.altitude_max_meters}m</span>
                      </div>
                    </div>
                  </div>
                </Popup>
              </Circle>
            )
          }
          
          // Handle Polygon geometry
          const coordinates = getPolygonCoordinates(geofence.geometry)
          if (coordinates.length === 0) return null

          return (
            <Polygon
              key={geofence.id}
              positions={coordinates}
              pathOptions={{
                color: color,
                fillColor: color,
                fillOpacity: 0.2,
                weight: 3,
              }}
            >
              <Popup>
                <div className="p-1 min-w-[180px]">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: color }}></div>
                    <h3 className="font-semibold text-sm">{geofence.name}</h3>
                  </div>
                  {geofence.description && (
                    <p className="text-xs text-gray-600 mb-2">{geofence.description}</p>
                  )}
                  <div className="space-y-1 text-xs">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Status</span>
                      <span className="font-medium capitalize">{geofence.status}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Priority</span>
                      <span className="font-medium">{geofence.priority}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Altitude</span>
                      <span className="font-medium">{geofence.altitude_min_meters}m - {geofence.altitude_max_meters}m</span>
                    </div>
                  </div>
                </div>
              </Popup>
            </Polygon>
          )
        })}

        {/* Render Assets */}
        {showAssets && ((assets as any)?.items || assets as any)?.map?.((asset: any) => {
          // Get position - use simulated position if simulation is running
          const simPos = simulatedPositions[asset.id]
          const position = isSimulating && simPos 
            ? [simPos.lat, simPos.lng] as [number, number]
            : asset.current_location 
              ? [asset.current_location.latitude, asset.current_location.longitude] as [number, number]
              : null
          
          if (!position) return null

          const isActive = asset.status === 'active'

          return (
            <Marker
              key={asset.id}
              position={position}
              icon={createAssetIcon(asset.asset_type, isActive)}
            >
              <Popup>
                <div className="p-1 min-w-[160px]">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="w-3 h-3 rounded-full" style={{ backgroundColor: isActive ? '#22c55e' : '#9ca3af' }}></div>
                    <h3 className="font-semibold text-sm">{asset.name}</h3>
                  </div>
                  <div className="space-y-1 text-xs">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Type</span>
                      <span className="font-medium">{asset.asset_type}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Status</span>
                      <span className="font-medium capitalize">{asset.status}</span>
                    </div>
                    {asset.altitude_meters && (
                      <div className="flex justify-between">
                        <span className="text-gray-500">Altitude</span>
                        <span className="font-medium">{asset.altitude_meters.toFixed(1)}m</span>
                      </div>
                    )}
                  </div>
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


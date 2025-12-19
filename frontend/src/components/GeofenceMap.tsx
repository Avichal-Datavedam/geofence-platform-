import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-draw'
import 'leaflet-draw/dist/leaflet.draw.css'
import { Lasso, Pentagon, Square, Circle, Trash2 } from 'lucide-react'

// Fix for default marker icons
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

interface GeofenceMapProps {
  onGeometryCreated: (geometry: any, center: { lat: number; lng: number }) => void
  existingGeofences?: any[]
  height?: string
}

type DrawingMode = 'none' | 'lasso' | 'polygon' | 'rectangle' | 'circle'

const GeofenceMap = ({ onGeometryCreated, existingGeofences = [], height = '400px' }: GeofenceMapProps) => {
  const mapRef = useRef<HTMLDivElement>(null)
  const mapInstanceRef = useRef<L.Map | null>(null)
  const drawnItemsRef = useRef<L.FeatureGroup | null>(null)
  const [drawingMode, setDrawingMode] = useState<DrawingMode>('none')
  const drawingModeRef = useRef<DrawingMode>('none')
  const isDrawingRef = useRef(false)
  const lassoPointsRef = useRef<L.LatLng[]>([])
  const lassoPolylineRef = useRef<L.Polyline | null>(null)
  const drawHandlersRef = useRef<any>({})
  const onGeometryCreatedRef = useRef(onGeometryCreated)
  
  // Keep refs in sync with state/props
  useEffect(() => {
    drawingModeRef.current = drawingMode
  }, [drawingMode])
  
  useEffect(() => {
    onGeometryCreatedRef.current = onGeometryCreated
  }, [onGeometryCreated])

  // Process geometry and call callback
  const processGeometry = (layer: any, layerType: string) => {
    const drawnItems = drawnItemsRef.current
    if (!drawnItems) return

    drawnItems.clearLayers()
    drawnItems.addLayer(layer)

    let geometry: any = null
    let center: { lat: number; lng: number } = { lat: 0, lng: 0 }

    if (layerType === 'polygon' || layerType === 'rectangle' || layerType === 'lasso') {
      const latlngs = layer.getLatLngs()[0] as L.LatLng[]
      const coordinates = latlngs.map((ll: L.LatLng) => [ll.lng, ll.lat])
      coordinates.push(coordinates[0]) // Close the polygon
      
      geometry = {
        type: 'Polygon',
        coordinates: [coordinates]
      }

      const bounds = layer.getBounds()
      const c = bounds.getCenter()
      center = { lat: c.lat, lng: c.lng }

    } else if (layerType === 'circle') {
      const c = layer.getLatLng()
      const radius = layer.getRadius()
      
      geometry = {
        type: 'Circle',
        center: [c.lng, c.lat],
        radius: radius
      }
      center = { lat: c.lat, lng: c.lng }
    }

    if (geometry) {
      onGeometryCreated(geometry, center)
    }
  }

  // Clear drawn items
  const clearDrawing = () => {
    if (drawnItemsRef.current) {
      drawnItemsRef.current.clearLayers()
    }
    if (lassoPolylineRef.current && mapInstanceRef.current) {
      mapInstanceRef.current.removeLayer(lassoPolylineRef.current)
      lassoPolylineRef.current = null
    }
    lassoPointsRef.current = []
    setDrawingMode('none')
    onGeometryCreated(null, { lat: 0, lng: 0 })
  }

  // Start specific drawing mode
  const startDrawing = (mode: DrawingMode) => {
    const map = mapInstanceRef.current
    if (!map) return

    // Cancel any existing drawing
    if (lassoPolylineRef.current) {
      map.removeLayer(lassoPolylineRef.current)
      lassoPolylineRef.current = null
    }
    lassoPointsRef.current = []

    setDrawingMode(mode)

    if (mode === 'lasso') {
      // Enable lasso mode - we'll handle this with mouse events
      map.dragging.disable()
      isDrawingRef.current = false
    } else if (mode === 'polygon' && drawHandlersRef.current.polygon) {
      drawHandlersRef.current.polygon.enable()
    } else if (mode === 'rectangle' && drawHandlersRef.current.rectangle) {
      drawHandlersRef.current.rectangle.enable()
    } else if (mode === 'circle' && drawHandlersRef.current.circle) {
      drawHandlersRef.current.circle.enable()
    }
  }

  useEffect(() => {
    if (!mapRef.current || mapInstanceRef.current) return

    // Initialize map
    const map = L.map(mapRef.current).setView([20.5937, 78.9629], 5)

    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map)

    // Initialize feature group for drawn items
    const drawnItems = new L.FeatureGroup()
    map.addLayer(drawnItems)
    drawnItemsRef.current = drawnItems

    // Create draw handlers (without adding control)
    const shapeOptions = {
      color: '#6366f1',
      fillColor: '#6366f1',
      fillOpacity: 0.3,
      weight: 2
    }

    drawHandlersRef.current = {
      polygon: new (L.Draw as any).Polygon(map, { shapeOptions, allowIntersection: false }),
      rectangle: new (L.Draw as any).Rectangle(map, { shapeOptions }),
      circle: new (L.Draw as any).Circle(map, { shapeOptions })
    }

    // Handle draw events from leaflet-draw handlers
    map.on(L.Draw.Event.CREATED, (e: any) => {
      processGeometry(e.layer, e.layerType)
      setDrawingMode('none')
    })

    // Lasso drawing with mouse events
    map.on('mousedown', (e: L.LeafletMouseEvent) => {
      if (drawingModeRef.current !== 'lasso') return
      isDrawingRef.current = true
      lassoPointsRef.current = [e.latlng]
      
      if (lassoPolylineRef.current) {
        map.removeLayer(lassoPolylineRef.current)
      }
      lassoPolylineRef.current = L.polyline([e.latlng], {
        color: '#6366f1',
        weight: 2,
        dashArray: '5, 5'
      }).addTo(map)
    })

    map.on('mousemove', (e: L.LeafletMouseEvent) => {
      if (!isDrawingRef.current || drawingModeRef.current !== 'lasso') return
      
      lassoPointsRef.current.push(e.latlng)
      if (lassoPolylineRef.current) {
        lassoPolylineRef.current.addLatLng(e.latlng)
      }
    })

    map.on('mouseup', () => {
      if (!isDrawingRef.current || drawingModeRef.current !== 'lasso') return
      isDrawingRef.current = false
      map.dragging.enable()

      const points = lassoPointsRef.current
      if (points.length > 2) {
        // Simplify points to reduce complexity
        const simplified = simplifyPoints(points, 0.0001)
        
        // Create polygon from lasso points
        const polygon = L.polygon(simplified, {
          color: '#6366f1',
          fillColor: '#6366f1',
          fillOpacity: 0.3,
          weight: 2
        })

        // Remove the temporary polyline
        if (lassoPolylineRef.current) {
          map.removeLayer(lassoPolylineRef.current)
          lassoPolylineRef.current = null
        }

        processGeometry(polygon, 'lasso')
      }
      
      lassoPointsRef.current = []
      setDrawingMode('none')
    })

    mapInstanceRef.current = map

    // Add existing geofences
    existingGeofences.forEach((geofence) => {
      if (geofence.center_point) {
        const { latitude, longitude } = geofence.center_point
        L.circle([latitude, longitude], {
          radius: geofence.radius_meters || 100,
          color: geofence.status === 'active' ? '#22c55e' : '#9ca3af',
          fillColor: geofence.status === 'active' ? '#22c55e' : '#9ca3af',
          fillOpacity: 0.2,
          weight: 2
        })
          .bindPopup(`<b>${geofence.name}</b><br>${geofence.description || ''}`)
          .addTo(map)
      }
    })

    return () => {
      map.remove()
      mapInstanceRef.current = null
    }
  }, [])

  // Simplify points using Douglas-Peucker algorithm
  const simplifyPoints = (points: L.LatLng[], tolerance: number): L.LatLng[] => {
    if (points.length <= 2) return points

    let maxDist = 0
    let maxIndex = 0
    const first = points[0]
    const last = points[points.length - 1]

    for (let i = 1; i < points.length - 1; i++) {
      const dist = perpendicularDistance(points[i], first, last)
      if (dist > maxDist) {
        maxDist = dist
        maxIndex = i
      }
    }

    if (maxDist > tolerance) {
      const left = simplifyPoints(points.slice(0, maxIndex + 1), tolerance)
      const right = simplifyPoints(points.slice(maxIndex), tolerance)
      return [...left.slice(0, -1), ...right]
    }

    return [first, last]
  }

  const perpendicularDistance = (point: L.LatLng, lineStart: L.LatLng, lineEnd: L.LatLng): number => {
    const dx = lineEnd.lng - lineStart.lng
    const dy = lineEnd.lat - lineStart.lat
    const mag = Math.sqrt(dx * dx + dy * dy)
    if (mag === 0) return 0

    const u = ((point.lng - lineStart.lng) * dx + (point.lat - lineStart.lat) * dy) / (mag * mag)
    const closestX = lineStart.lng + u * dx
    const closestY = lineStart.lat + u * dy

    return Math.sqrt(Math.pow(point.lng - closestX, 2) + Math.pow(point.lat - closestY, 2))
  }

  // Update lasso event handlers when drawingMode changes
  useEffect(() => {
    const map = mapInstanceRef.current
    if (!map) return

    if (drawingMode === 'lasso') {
      map.dragging.disable()
    } else {
      map.dragging.enable()
    }
  }, [drawingMode])

  const tools = [
    { mode: 'lasso' as DrawingMode, icon: Lasso, label: 'Lasso (Freehand)', desc: 'Click and drag to draw freely' },
    { mode: 'polygon' as DrawingMode, icon: Pentagon, label: 'Polygon', desc: 'Click points to create shape' },
    { mode: 'rectangle' as DrawingMode, icon: Square, label: 'Rectangle', desc: 'Click and drag' },
    { mode: 'circle' as DrawingMode, icon: Circle, label: 'Circle', desc: 'Click center, drag radius' },
  ]

  return (
    <div className="relative">
      <div 
        ref={mapRef} 
        style={{ height, width: '100%' }}
        className={`rounded-xl overflow-hidden border-2 shadow-sm transition-colors ${
          drawingMode === 'lasso' ? 'border-primary-500 cursor-crosshair' : 'border-gray-200'
        }`}
      />
      
      {/* Custom Drawing Toolbar */}
      <div className="absolute top-3 left-3 bg-white rounded-xl shadow-lg p-2 z-[1000]">
        <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide px-2 mb-2">Draw Tools</p>
        <div className="space-y-1">
          {tools.map(({ mode, icon: Icon, label }) => (
            <button
              key={mode}
              onClick={() => startDrawing(mode)}
              className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                drawingMode === mode
                  ? 'bg-primary-500 text-white shadow-md'
                  : 'text-gray-700 hover:bg-gray-100'
              }`}
            >
              <Icon className="h-4 w-4" />
              {label}
            </button>
          ))}
          <hr className="my-2 border-gray-200" />
          <button
            onClick={clearDrawing}
            className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-red-600 hover:bg-red-50 transition-all"
          >
            <Trash2 className="h-4 w-4" />
            Clear
          </button>
        </div>
      </div>

      {/* Status indicator */}
      {drawingMode !== 'none' && (
        <div className="absolute top-3 right-3 bg-primary-500 text-white px-4 py-2 rounded-lg shadow-lg z-[1000] flex items-center gap-2">
          <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
          <span className="text-sm font-medium">
            {drawingMode === 'lasso' ? 'Click and drag to draw' : `Drawing ${drawingMode}...`}
          </span>
        </div>
      )}

      {/* Instructions */}
      <div className="absolute bottom-3 left-3 bg-white/95 backdrop-blur-sm rounded-lg shadow-lg px-3 py-2 z-[1000] max-w-xs">
        <p className="text-xs text-gray-600">
          {drawingMode === 'lasso' 
            ? '🖱️ Click and drag to draw a freehand shape. Release to complete.'
            : drawingMode === 'polygon'
            ? '🖱️ Click on map to add points. Double-click to finish.'
            : drawingMode === 'rectangle'
            ? '🖱️ Click and drag to draw rectangle.'
            : drawingMode === 'circle'
            ? '🖱️ Click center point, drag for radius.'
            : '👆 Select a drawing tool from the left panel to start.'}
        </p>
      </div>
    </div>
  )
}

export default GeofenceMap

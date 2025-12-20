import { useState, useRef, useEffect } from 'react'
import { Search, MapPin, Loader2, X, Navigation } from 'lucide-react'

interface SearchResult {
  display_name: string
  lat: string
  lon: string
  type: string
  importance: number
}

interface MapSearchControlProps {
  onLocationSelect: (lat: number, lng: number, name: string) => void
  onGetCurrentLocation?: () => void
}

const MapSearchControl = ({ onLocationSelect, onGetCurrentLocation }: MapSearchControlProps) => {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isOpen, setIsOpen] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const searchRef = useRef<HTMLDivElement>(null)
  const debounceRef = useRef<NodeJS.Timeout | null>(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  // Debounced search using Nominatim (OpenStreetMap)
  const searchLocation = async (searchQuery: string) => {
    if (!searchQuery.trim() || searchQuery.length < 3) {
      setResults([])
      setIsOpen(false)
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(searchQuery)}&limit=8&addressdetails=1`,
        {
          headers: {
            'Accept-Language': 'en',
            'User-Agent': 'GeofencePlatform/1.0'
          }
        }
      )

      if (!response.ok) throw new Error('Search failed')

      const data: SearchResult[] = await response.json()
      setResults(data)
      setIsOpen(data.length > 0)
    } catch (err) {
      setError('Failed to search. Please try again.')
      setResults([])
    } finally {
      setIsLoading(false)
    }
  }

  // Handle input change with debounce
  const handleInputChange = (value: string) => {
    setQuery(value)
    
    if (debounceRef.current) {
      clearTimeout(debounceRef.current)
    }

    debounceRef.current = setTimeout(() => {
      searchLocation(value)
    }, 400)
  }

  // Handle result selection
  const handleSelect = (result: SearchResult) => {
    const lat = parseFloat(result.lat)
    const lng = parseFloat(result.lon)
    onLocationSelect(lat, lng, result.display_name)
    setQuery(result.display_name.split(',')[0])
    setIsOpen(false)
    setResults([])
  }

  // Clear search
  const handleClear = () => {
    setQuery('')
    setResults([])
    setIsOpen(false)
  }

  // Get location type icon/label
  const getTypeLabel = (type: string): string => {
    const types: Record<string, string> = {
      city: '🏙️ City',
      town: '🏘️ Town',
      village: '🏡 Village',
      suburb: '🏠 Suburb',
      county: '📍 County',
      state: '🗺️ State',
      country: '🌍 Country',
      road: '🛣️ Road',
      building: '🏢 Building',
      amenity: '📌 Place',
      boundary: '📍 Area'
    }
    return types[type] || '📍 Location'
  }

  return (
    <div ref={searchRef} className="relative w-full max-w-md">
      {/* Search Input */}
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          {isLoading ? (
            <Loader2 className="h-5 w-5 text-gray-400 animate-spin" />
          ) : (
            <Search className="h-5 w-5 text-gray-400" />
          )}
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => handleInputChange(e.target.value)}
          onFocus={() => results.length > 0 && setIsOpen(true)}
          placeholder="Search for a location..."
          className="block w-full pl-10 pr-20 py-3 border border-gray-200 rounded-xl bg-white shadow-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm transition-all"
        />
        <div className="absolute inset-y-0 right-0 flex items-center gap-1 pr-2">
          {query && (
            <button
              onClick={handleClear}
              className="p-1.5 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <X className="h-4 w-4" />
            </button>
          )}
          {onGetCurrentLocation && (
            <button
              onClick={onGetCurrentLocation}
              className="p-1.5 text-primary-500 hover:text-primary-600 rounded-lg hover:bg-primary-50 transition-colors"
              title="Use my location"
            >
              <Navigation className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="absolute top-full mt-2 w-full bg-red-50 border border-red-200 rounded-lg px-3 py-2 text-sm text-red-600">
          {error}
        </div>
      )}

      {/* Search Results Dropdown */}
      {isOpen && results.length > 0 && (
        <div className="absolute top-full mt-2 w-full bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden z-50 max-h-80 overflow-y-auto">
          {results.map((result, index) => (
            <button
              key={index}
              onClick={() => handleSelect(result)}
              className="w-full px-4 py-3 text-left hover:bg-gray-50 transition-colors border-b border-gray-50 last:border-0 flex items-start gap-3"
            >
              <MapPin className="h-5 w-5 text-primary-500 mt-0.5 flex-shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {result.display_name.split(',')[0]}
                </p>
                <p className="text-xs text-gray-500 truncate mt-0.5">
                  {result.display_name.split(',').slice(1, 4).join(',')}
                </p>
                <span className="inline-block mt-1 text-xs text-gray-400">
                  {getTypeLabel(result.type)}
                </span>
              </div>
            </button>
          ))}
        </div>
      )}

      {/* No results message */}
      {isOpen && query.length >= 3 && results.length === 0 && !isLoading && (
        <div className="absolute top-full mt-2 w-full bg-white rounded-xl shadow-xl border border-gray-100 px-4 py-6 text-center">
          <MapPin className="h-8 w-8 text-gray-300 mx-auto mb-2" />
          <p className="text-sm text-gray-500">No locations found</p>
          <p className="text-xs text-gray-400 mt-1">Try a different search term</p>
        </div>
      )}
    </div>
  )
}

export default MapSearchControl

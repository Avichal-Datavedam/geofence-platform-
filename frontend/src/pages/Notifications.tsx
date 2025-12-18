import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { notificationApi } from '../services/api'
import { Bell, CheckCircle, AlertTriangle, Info, XCircle } from 'lucide-react'

const Notifications = () => {
  const queryClient = useQueryClient()

  const { data, isLoading } = useQuery({
    queryKey: ['notifications'],
    queryFn: () => notificationApi.list({ per_page: 100 }),
  })

  const acknowledgeMutation = useMutation({
    mutationFn: (id: string) => notificationApi.acknowledge(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] })
    },
  })

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <XCircle className="h-5 w-5 text-red-600" />
      case 'high':
        return <AlertTriangle className="h-5 w-5 text-orange-600" />
      case 'medium':
        return <Info className="h-5 w-5 text-yellow-600" />
      default:
        return <Bell className="h-5 w-5 text-blue-600" />
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-50 border-red-200'
      case 'high':
        return 'bg-orange-50 border-orange-200'
      case 'medium':
        return 'bg-yellow-50 border-yellow-200'
      default:
        return 'bg-blue-50 border-blue-200'
    }
  }

  if (isLoading) {
    return (
      <div className="p-8">
        <div className="animate-pulse">Loading notifications...</div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Notifications</h1>
        <p className="mt-2 text-gray-600">View and manage your alerts</p>
      </div>

      <div className="space-y-4">
        {data?.map((notification: any) => (
          <div
            key={notification.id}
            className={`bg-white rounded-lg shadow border-2 p-6 ${getSeverityColor(
              notification.severity
            )}`}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start flex-1">
                <div className="mr-4">{getSeverityIcon(notification.severity)}</div>
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {notification.title}
                    </h3>
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded ${
                        notification.severity === 'critical'
                          ? 'bg-red-100 text-red-800'
                          : notification.severity === 'high'
                          ? 'bg-orange-100 text-orange-800'
                          : 'bg-yellow-100 text-yellow-800'
                      }`}
                    >
                      {notification.severity}
                    </span>
                    {notification.status === 'acknowledged' && (
                      <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded">
                        Acknowledged
                      </span>
                    )}
                  </div>
                  {notification.message && (
                    <p className="text-sm text-gray-600 mb-3">{notification.message}</p>
                  )}
                  <div className="flex items-center space-x-4 text-xs text-gray-500">
                    <span>
                      Location: {notification.location?.latitude?.toFixed(4)},{' '}
                      {notification.location?.longitude?.toFixed(4)}
                    </span>
                    {notification.distance_meters && (
                      <span>Distance: {notification.distance_meters.toFixed(2)}m</span>
                    )}
                    <span>
                      {new Date(notification.created_at).toLocaleString()}
                    </span>
                  </div>
                </div>
              </div>
              {notification.status === 'active' && (
                <button
                  onClick={() => acknowledgeMutation.mutate(notification.id)}
                  disabled={acknowledgeMutation.isPending}
                  className="ml-4 px-4 py-2 bg-primary-600 text-white text-sm rounded-lg hover:bg-primary-700 disabled:opacity-50 flex items-center"
                >
                  <CheckCircle className="h-4 w-4 mr-2" />
                  Acknowledge
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {(!data || data.length === 0) && (
        <div className="text-center py-12">
          <Bell className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No notifications found</p>
        </div>
      )}
    </div>
  )
}

export default Notifications


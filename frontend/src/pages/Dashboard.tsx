import { useQuery } from '@tanstack/react-query'
import { geofenceApi, assetApi, notificationApi } from '../services/api'
import {
  Hexagon,
  Package,
  Bell,
  AlertTriangle,
  TrendingUp,
  MapPin,
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import AIChatWidget from '../components/AIChatWidget'

const Dashboard = () => {
  const { data: geofences } = useQuery({
    queryKey: ['geofences'],
    queryFn: () => geofenceApi.list({ per_page: 100 }),
  })

  const { data: assets } = useQuery({
    queryKey: ['assets'],
    queryFn: () => assetApi.list({ per_page: 100 }),
  })

  const { data: notifications } = useQuery({
    queryKey: ['notifications'],
    queryFn: () => notificationApi.list({ per_page: 50, status: 'active' }),
  })

  const stats = [
    {
      name: 'Active Geofences',
      value: geofences?.total || 0,
      icon: Hexagon,
      color: 'bg-blue-500',
      change: '+12%',
    },
    {
      name: 'Tracked Assets',
      value: assets?.length || 0,
      icon: Package,
      color: 'bg-green-500',
      change: '+5%',
    },
    {
      name: 'Active Alerts',
      value: notifications?.length || 0,
      icon: Bell,
      color: 'bg-red-500',
      change: '-3%',
    },
    {
      name: 'Critical Alerts',
      value: notifications?.filter((n: any) => n.severity === 'critical').length || 0,
      icon: AlertTriangle,
      color: 'bg-orange-500',
      change: '+2%',
    },
  ]

  // Mock chart data
  const chartData = [
    { name: 'Mon', alerts: 12, assets: 45 },
    { name: 'Tue', alerts: 19, assets: 52 },
    { name: 'Wed', alerts: 15, assets: 48 },
    { name: 'Thu', alerts: 22, assets: 55 },
    { name: 'Fri', alerts: 18, assets: 50 },
    { name: 'Sat', alerts: 10, assets: 42 },
    { name: 'Sun', alerts: 8, assets: 40 },
  ]

  const severityData = [
    { name: 'Critical', value: 5, color: '#ef4444' },
    { name: 'High', value: 12, color: '#f97316' },
    { name: 'Medium', value: 18, color: '#eab308' },
    { name: 'Low', value: 25, color: '#3b82f6' },
  ]

  return (
    <div className="p-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">Overview of your geo-fencing platform</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div
              key={stat.name}
              className="bg-white rounded-lg shadow p-6 border border-gray-200"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="mt-2 text-3xl font-bold text-gray-900">{stat.value}</p>
                  <p className="mt-1 text-sm text-green-600 flex items-center">
                    <TrendingUp className="h-4 w-4 mr-1" />
                    {stat.change}
                  </p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Charts and AI Chat */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Activity Chart */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow p-6 border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Activity Overview</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="alerts"
                stroke="#ef4444"
                strokeWidth={2}
                name="Alerts"
              />
              <Line
                type="monotone"
                dataKey="assets"
                stroke="#3b82f6"
                strokeWidth={2}
                name="Active Assets"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Severity Distribution */}
        <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Alert Severity</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={severityData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {severityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Notifications and AI Chat */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        {/* Recent Notifications */}
        <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Notifications</h2>
          <div className="space-y-4">
            {notifications?.slice(0, 5).map((notification: any) => (
              <div
                key={notification.id}
                className="flex items-start p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className={`p-2 rounded ${
                  notification.severity === 'critical' ? 'bg-red-100' :
                  notification.severity === 'high' ? 'bg-orange-100' :
                  'bg-yellow-100'
                }`}>
                  <Bell className={`h-4 w-4 ${
                    notification.severity === 'critical' ? 'text-red-600' :
                    notification.severity === 'high' ? 'text-orange-600' :
                    'text-yellow-600'
                  }`} />
                </div>
                <div className="ml-3 flex-1">
                  <p className="text-sm font-medium text-gray-900">{notification.title}</p>
                  <p className="text-xs text-gray-500 mt-1">{notification.message}</p>
                  <div className="flex items-center mt-2 text-xs text-gray-400">
                    <MapPin className="h-3 w-3 mr-1" />
                    {notification.location?.latitude?.toFixed(4)}, {notification.location?.longitude?.toFixed(4)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Chat Widget */}
        <AIChatWidget />
      </div>
    </div>
  )
}

export default Dashboard


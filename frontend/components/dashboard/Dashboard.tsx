'use client'

import { useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import Sidebar from './Sidebar'
import Organizations from './Organizations'
import Employees from './Employees'
import ShiftPatterns from './ShiftPatterns'
import Schedules from './Schedules'
import Leaves from './Leaves'

type TabType = 'organizations' | 'employees' | 'shift-patterns' | 'schedules' | 'leaves'

export default function Dashboard() {
  const { user, logout } = useAuth()
  const [activeTab, setActiveTab] = useState<TabType>('organizations')
  const [selectedOrganization, setSelectedOrganization] = useState<number | null>(null)

  const renderContent = () => {
    switch (activeTab) {
      case 'organizations':
        return <Organizations onSelect={setSelectedOrganization} />
      case 'employees':
        return selectedOrganization ? (
          <Employees organizationId={selectedOrganization} />
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">Please select an organization first</p>
          </div>
        )
      case 'shift-patterns':
        return selectedOrganization ? (
          <ShiftPatterns organizationId={selectedOrganization} />
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">Please select an organization first</p>
          </div>
        )
      case 'schedules':
        return selectedOrganization ? (
          <Schedules organizationId={selectedOrganization} />
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">Please select an organization first</p>
          </div>
        )
      case 'leaves':
        return selectedOrganization ? (
          <Leaves organizationId={selectedOrganization} />
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">Please select an organization first</p>
          </div>
        )
      default:
        return <Organizations onSelect={setSelectedOrganization} />
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Shift Planner</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">
                Welcome, {user?.full_name || user?.email}
              </span>
              <button
                onClick={logout}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <Sidebar activeTab={activeTab} onTabChange={(tab: TabType) => setActiveTab(tab)} />

        {/* Main content */}
        <main className="flex-1 p-6">
          <div className="max-w-7xl mx-auto">
            {renderContent()}
          </div>
        </main>
      </div>
    </div>
  )
} 
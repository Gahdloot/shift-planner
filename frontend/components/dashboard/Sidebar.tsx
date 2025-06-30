'use client'

import { 
  BuildingOfficeIcon, 
  UsersIcon, 
  ClockIcon, 
  CalendarIcon, 
  CalendarDaysIcon 
} from '@heroicons/react/24/outline'

type TabType = 'organizations' | 'employees' | 'shift-patterns' | 'schedules' | 'leaves'

interface SidebarProps {
  activeTab: TabType
  onTabChange: (tab: TabType) => void
}

const navigation = [
  { name: 'Organizations', href: 'organizations' as TabType, icon: BuildingOfficeIcon },
  { name: 'Employees', href: 'employees' as TabType, icon: UsersIcon },
  { name: 'Shift Patterns', href: 'shift-patterns' as TabType, icon: ClockIcon },
  { name: 'Schedules', href: 'schedules' as TabType, icon: CalendarIcon },
  { name: 'Leave Management', href: 'leaves' as TabType, icon: CalendarDaysIcon },
]

export default function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  return (
    <div className="w-64 bg-white shadow-lg">
      <nav className="mt-5 px-2">
        <div className="space-y-1">
          {navigation.map((item) => {
            const isActive = activeTab === item.href
            return (
              <button
                key={item.name}
                onClick={() => onTabChange(item.href)}
                className={`${
                  isActive
                    ? 'bg-primary-100 border-primary-500 text-primary-700'
                    : 'border-transparent text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                } group w-full flex items-center px-3 py-2 text-sm font-medium border-l-4 transition-colors`}
              >
                <item.icon
                  className={`${
                    isActive ? 'text-primary-500' : 'text-gray-400 group-hover:text-gray-500'
                  } mr-3 flex-shrink-0 h-6 w-6`}
                  aria-hidden="true"
                />
                {item.name}
              </button>
            )
          })}
        </div>
      </nav>
    </div>
  )
} 
'use client'

interface SchedulesProps {
  organizationId: number
}

export default function Schedules({ organizationId }: SchedulesProps) {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Schedules</h2>
        <button className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md">
          Generate Schedule
        </button>
      </div>
      
      <div className="bg-white p-8 rounded-lg shadow text-center">
        <p className="text-gray-500">Schedule management coming soon...</p>
        <p className="text-sm text-gray-400 mt-2">Organization ID: {organizationId}</p>
      </div>
    </div>
  )
} 
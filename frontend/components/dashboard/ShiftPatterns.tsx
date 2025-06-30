'use client'

interface ShiftPatternsProps {
  organizationId: number
}

export default function ShiftPatterns({ organizationId }: ShiftPatternsProps) {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Shift Patterns</h2>
        <button className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md">
          Add Shift Pattern
        </button>
      </div>
      
      <div className="bg-white p-8 rounded-lg shadow text-center">
        <p className="text-gray-500">Shift pattern management coming soon...</p>
        <p className="text-sm text-gray-400 mt-2">Organization ID: {organizationId}</p>
      </div>
    </div>
  )
} 
'use client'

interface EmployeesProps {
  organizationId: number
}

export default function Employees({ organizationId }: EmployeesProps) {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Employees</h2>
        <button className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md">
          Add Employee
        </button>
      </div>
      
      <div className="bg-white p-8 rounded-lg shadow text-center">
        <p className="text-gray-500">Employee management coming soon...</p>
        <p className="text-sm text-gray-400 mt-2">Organization ID: {organizationId}</p>
      </div>
    </div>
  )
} 
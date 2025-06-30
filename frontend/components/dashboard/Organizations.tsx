'use client'

import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import axios from 'axios'
import toast from 'react-hot-toast'
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline'

const organizationSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  description: z.string().optional(),
})

type OrganizationFormData = z.infer<typeof organizationSchema>

interface Organization {
  id: number
  name: string
  description?: string
  is_active: boolean
  created_at: string
}

interface OrganizationsProps {
  onSelect: (organizationId: number) => void
}

export default function Organizations({ onSelect }: OrganizationsProps) {
  const [organizations, setOrganizations] = useState<Organization[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editingOrg, setEditingOrg] = useState<Organization | null>(null)

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<OrganizationFormData>({
    resolver: zodResolver(organizationSchema),
  })

  useEffect(() => {
    fetchOrganizations()
  }, [])

  const fetchOrganizations = async () => {
    try {
      const response = await axios.get('/api/organizations')
      setOrganizations(response.data)
    } catch (error) {
      toast.error('Failed to fetch organizations')
    } finally {
      setIsLoading(false)
    }
  }

  const onSubmit = async (data: OrganizationFormData) => {
    try {
      if (editingOrg) {
        await axios.put(`/api/organizations/${editingOrg.id}`, data)
        toast.success('Organization updated successfully')
      } else {
        await axios.post('/api/organizations', data)
        toast.success('Organization created successfully')
      }
      fetchOrganizations()
      setShowForm(false)
      setEditingOrg(null)
      reset()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Operation failed')
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this organization?')) return
    
    try {
      await axios.delete(`/api/organizations/${id}`)
      toast.success('Organization deleted successfully')
      fetchOrganizations()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to delete organization')
    }
  }

  const handleEdit = (org: Organization) => {
    setEditingOrg(org)
    reset({ name: org.name, description: org.description })
    setShowForm(true)
  }

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Organizations</h2>
        <button
          onClick={() => {
            setShowForm(true)
            setEditingOrg(null)
            reset()
          }}
          className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md flex items-center space-x-2"
        >
          <PlusIcon className="h-5 w-5" />
          <span>Add Organization</span>
        </button>
      </div>

      {showForm && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-lg font-medium mb-4">
            {editingOrg ? 'Edit Organization' : 'Create Organization'}
          </h3>
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Name</label>
              <input
                {...register('name')}
                type="text"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
              {errors.name && (
                <p className="mt-1 text-sm text-red-600">{errors.name.message}</p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                {...register('description')}
                rows={3}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div className="flex space-x-3">
              <button
                type="submit"
                className="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-md"
              >
                {editingOrg ? 'Update' : 'Create'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowForm(false)
                  setEditingOrg(null)
                  reset()
                }}
                className="bg-gray-300 hover:bg-gray-400 text-gray-700 px-4 py-2 rounded-md"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="bg-white shadow overflow-hidden sm:rounded-md">
        <ul className="divide-y divide-gray-200">
          {organizations.map((org) => (
            <li key={org.id} className="px-6 py-4 hover:bg-gray-50">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <h3 className="text-lg font-medium text-gray-900">{org.name}</h3>
                    <button
                      onClick={() => onSelect(org.id)}
                      className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                    >
                      Select
                    </button>
                  </div>
                  {org.description && (
                    <p className="text-sm text-gray-500 mt-1">{org.description}</p>
                  )}
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => handleEdit(org)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <PencilIcon className="h-5 w-5" />
                  </button>
                  <button
                    onClick={() => handleDelete(org.id)}
                    className="text-gray-400 hover:text-red-600"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
} 
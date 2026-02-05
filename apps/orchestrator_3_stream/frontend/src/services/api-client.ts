import axios from 'axios'
import type { Agent, Task } from '@/types/models'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const axiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API error:', error.response?.status, error.response?.data)
    return Promise.reject(error)
  }
)

export class ApiClient {
  async getAgents(): Promise<Agent[]> {
    try {
      const response = await axiosInstance.get('/agents')
      return response.data || []
    } catch (error) {
      console.error('Failed to fetch agents:', error)
      return []
    }
  }

  async getAgent(id: string): Promise<Agent | null> {
    try {
      const response = await axiosInstance.get(`/agents/${id}`)
      return response.data || null
    } catch (error) {
      console.error(`Failed to fetch agent ${id}:`, error)
      return null
    }
  }

  async executeAgent(agentId: string, payload: Record<string, any> = {}): Promise<any> {
    try {
      const response = await axiosInstance.post(`/agents/${agentId}/execute`, payload)
      return response.data
    } catch (error) {
      console.error(`Failed to execute agent ${agentId}:`, error)
      throw error
    }
  }

  async getTasks(agentId: string): Promise<Task[]> {
    try {
      const response = await axiosInstance.get(`/agents/${agentId}/tasks`)
      return response.data || []
    } catch (error) {
      console.error(`Failed to fetch tasks for agent ${agentId}:`, error)
      return []
    }
  }

  async getSystemStatus(): Promise<any> {
    try {
      const response = await axiosInstance.get('/system/status')
      return response.data
    } catch (error) {
      console.error('Failed to fetch system status:', error)
      return null
    }
  }
}

export const apiClient = new ApiClient()

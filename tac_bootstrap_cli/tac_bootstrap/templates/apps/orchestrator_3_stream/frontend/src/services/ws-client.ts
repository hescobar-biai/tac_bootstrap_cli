import type { WebSocketMessage } from '@/types/models'
import { useWsStore } from '@/stores/ws-store'
import { useAgentStore } from '@/stores/agent-store'
import { apiClient } from './api-client'

const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'
const POLLING_INTERVAL = parseInt(import.meta.env.VITE_POLLING_INTERVAL || '30000')

export class WebSocketClient {
  private ws: WebSocket | null = null
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private baseDelay = 2000 // 2 seconds
  private maxDelay = 16000 // 16 seconds
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private heartbeatTimer: ReturnType<typeof setInterval> | null = null
  private pollingTimer: ReturnType<typeof setInterval> | null = null
  private wsStore = useWsStore()
  private agentStore = useAgentStore()

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        const wsUrl = `${WS_BASE_URL}/ws/orchestrator`
        this.ws = new WebSocket(wsUrl)

        this.ws.onopen = () => {
          console.log('WebSocket connected')
          this.wsStore.setConnected(true)
          this.wsStore.setUsePolling(false)
          this.reconnectAttempts = 0
          this.wsStore.setRetryCount(0)
          this.startHeartbeat()
          resolve()
        }

        this.ws.onmessage = (event) => {
          this.handleMessage(event.data)
        }

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error)
          this.handleDisconnect()
          reject(error)
        }

        this.ws.onclose = () => {
          console.log('WebSocket closed')
          this.handleDisconnect()
        }
      } catch (error) {
        console.error('Failed to create WebSocket:', error)
        this.handleDisconnect()
        reject(error)
      }
    })
  }

  private handleMessage(data: string) {
    try {
      const message: WebSocketMessage = JSON.parse(data)
      this.wsStore.updateLastMessage(new Date())

      switch (message.type) {
        case 'agent_update':
          if (message.data && 'agent' in message.data) {
            const agent = message.data.agent as any
            this.agentStore.updateAgent({
              id: agent.id,
              name: agent.name,
              status: agent.status,
              createdAt: agent.createdAt
            })
          }
          break

        case 'task_update':
          if (message.data && 'task' in message.data) {
            const task = message.data.task as any
            this.agentStore.updateTask({
              id: task.id,
              agentId: task.agentId,
              description: task.description,
              status: task.status,
              timestamp: task.timestamp
            })
          }
          break

        case 'heartbeat':
          // Acknowledge heartbeat
          break
      }
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error)
    }
  }

  private startHeartbeat() {
    this.heartbeatTimer = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(JSON.stringify({ type: 'ping' }))
      }
    }, 30000) // Every 30 seconds
  }

  private handleDisconnect() {
    this.wsStore.setConnected(false)
    this.stopHeartbeat()
    this.attemptReconnect()
  }

  private stopHeartbeat() {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer)
      this.heartbeatTimer = null
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log('Max reconnection attempts reached, falling back to polling')
      this.startPolling()
      return
    }

    const delay = Math.min(
      this.baseDelay * Math.pow(2, this.reconnectAttempts),
      this.maxDelay
    )
    this.reconnectAttempts++
    this.wsStore.setRetryCount(this.reconnectAttempts)

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`)
    this.reconnectTimer = setTimeout(() => {
      this.connect().catch((error) => {
        console.error('Reconnection failed:', error)
      })
    }, delay)
  }

  private startPolling() {
    this.wsStore.setUsePolling(true)
    console.log(`Starting polling fallback (interval: ${POLLING_INTERVAL}ms)`)

    this.pollingTimer = setInterval(async () => {
      try {
        const agents = await apiClient.getAgents()
        agents.forEach((agent) => {
          this.agentStore.updateAgent(agent)
        })
      } catch (error) {
        console.error('Polling failed:', error)
      }
    }, POLLING_INTERVAL)
  }

  send(message: WebSocketMessage) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    }
  }

  disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
    }
    this.stopHeartbeat()
    if (this.pollingTimer) {
      clearInterval(this.pollingTimer)
    }
    if (this.ws) {
      this.ws.close()
    }
  }
}

export const wsClient = new WebSocketClient()

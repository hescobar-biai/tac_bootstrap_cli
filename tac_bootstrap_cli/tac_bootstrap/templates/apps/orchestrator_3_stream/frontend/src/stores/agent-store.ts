/**
 * Pinia store for orchestrator agent and task state management.
 *
 * Provides reactive state, actions, and computed getters for the full
 * collection of agents and their associated tasks.  This store is the
 * single source of truth consumed by swimlane components (SwimlaneBoard,
 * AgentLane, TaskCard) and updated by the WebSocket / polling services.
 */

import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import type { Agent, AgentStats, Task } from '@/types/models'

export const useAgentStore = defineStore('agent', () => {
  // -----------------------------------------------------------------------
  // State
  // -----------------------------------------------------------------------

  /** Flat list of all known agents. */
  const agents = ref<Agent[]>([])

  /**
   * Tasks indexed by the owning agent's ID for O(1) lookup.
   *
   * Using a plain object (Record) rather than `Map` because Pinia's
   * reactivity system tracks object properties natively whereas `Map`
   * requires manual `triggerRef` calls.
   */
  const tasksByAgentId = ref<Record<string, Task[]>>({})

  // -----------------------------------------------------------------------
  // Getters
  // -----------------------------------------------------------------------

  /** Sorted list of all agents (by creation date, newest first). */
  const agentList = computed<Agent[]>(() =>
    [...agents.value].sort(
      (a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime(),
    ),
  )

  /**
   * Returns the task array for a given agent ID.
   * Returns an empty array when the agent has no recorded tasks.
   */
  const tasksByAgent = computed(() => {
    return (agentId: string): Task[] => tasksByAgentId.value[agentId] ?? []
  })

  /** Aggregate counts of agents grouped by their current status. */
  const agentStats = computed<AgentStats>(() => {
    const stats: AgentStats = { pending: 0, running: 0, completed: 0, failed: 0 }
    for (const agent of agents.value) {
      stats[agent.status]++
    }
    return stats
  })

  // -----------------------------------------------------------------------
  // Actions -- Agents
  // -----------------------------------------------------------------------

  /**
   * Add a new agent to the store.
   * If an agent with the same ID already exists it will be silently ignored
   * to prevent duplicates from redundant WebSocket messages.
   */
  function addAgent(agent: Agent): void {
    const exists = agents.value.some((a) => a.id === agent.id)
    if (!exists) {
      agents.value.push(agent)
    }
  }

  /**
   * Merge partial updates into an existing agent.
   * Only the supplied fields are overwritten; the rest remain unchanged.
   */
  function updateAgent(id: string, patch: Partial<Omit<Agent, 'id'>>): void {
    const index = agents.value.findIndex((a) => a.id === id)
    if (index !== -1) {
      agents.value[index] = { ...agents.value[index], ...patch }
    }
  }

  /**
   * Remove an agent and all of its associated tasks from the store.
   */
  function removeAgent(id: string): void {
    agents.value = agents.value.filter((a) => a.id !== id)
    // eslint-disable-next-line @typescript-eslint/no-dynamic-delete
    delete tasksByAgentId.value[id]
  }

  // -----------------------------------------------------------------------
  // Actions -- Tasks
  // -----------------------------------------------------------------------

  /**
   * Add a new task under its owning agent.
   * Creates the agent's task bucket if it does not already exist.
   * Silently ignores duplicate task IDs.
   */
  function addTask(task: Task): void {
    const bucket = tasksByAgentId.value[task.agentId]
    if (bucket) {
      const exists = bucket.some((t) => t.id === task.id)
      if (!exists) {
        bucket.push(task)
      }
    } else {
      tasksByAgentId.value[task.agentId] = [task]
    }
  }

  /**
   * Merge partial updates into an existing task.
   * Locates the task by its `id` within the specified agent's bucket.
   */
  function updateTask(
    agentId: string,
    taskId: string,
    patch: Partial<Omit<Task, 'id' | 'agentId'>>,
  ): void {
    const bucket = tasksByAgentId.value[agentId]
    if (!bucket) return

    const index = bucket.findIndex((t) => t.id === taskId)
    if (index !== -1) {
      bucket[index] = { ...bucket[index], ...patch }
    }
  }

  /**
   * Remove a single task from the specified agent's bucket.
   */
  function removeTask(agentId: string, taskId: string): void {
    const bucket = tasksByAgentId.value[agentId]
    if (!bucket) return

    tasksByAgentId.value[agentId] = bucket.filter((t) => t.id !== taskId)
  }

  // -----------------------------------------------------------------------
  // Public API
  // -----------------------------------------------------------------------

  return {
    // State
    agents,
    tasksByAgentId,

    // Getters
    agentList,
    tasksByAgent,
    agentStats,

    // Actions -- Agents
    addAgent,
    updateAgent,
    removeAgent,

    // Actions -- Tasks
    addTask,
    updateTask,
    removeTask,
  }
})

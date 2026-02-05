/**
 * Core TypeScript interfaces for the orchestrator frontend.
 *
 * These models represent the domain entities used across the application:
 * agents, tasks, and WebSocket messages. They are consumed by Pinia stores,
 * service clients, and Vue components.
 */

// ---------------------------------------------------------------------------
// Agent
// ---------------------------------------------------------------------------

/** Valid lifecycle statuses for an orchestrator agent. */
export type AgentStatus = 'pending' | 'running' | 'completed' | 'failed'

/**
 * Represents a single orchestrator agent displayed as a swimlane column.
 *
 * @example
 * ```ts
 * const agent: Agent = {
 *   id: 'agent-abc123',
 *   name: 'code_reviewer',
 *   status: 'running',
 *   createdAt: '2024-12-01T10:30:00Z',
 * }
 * ```
 */
export interface Agent {
  /** Unique identifier for the agent (UUID or slug). */
  id: string
  /** Human-readable display name (e.g. "code_reviewer"). */
  name: string
  /** Current lifecycle status of the agent. */
  status: AgentStatus
  /** ISO-8601 timestamp of when the agent was created. */
  createdAt: string
}

// ---------------------------------------------------------------------------
// Task
// ---------------------------------------------------------------------------

/** Valid lifecycle statuses for a task executed by an agent. */
export type TaskStatus = 'pending' | 'running' | 'completed' | 'failed'

/**
 * Represents a discrete unit of work assigned to an agent, rendered as a
 * card inside the agent's swimlane column.
 *
 * @example
 * ```ts
 * const task: Task = {
 *   id: 'task-xyz789',
 *   agentId: 'agent-abc123',
 *   description: 'Review pull request #42',
 *   status: 'completed',
 *   timestamp: '2024-12-01T10:35:00Z',
 * }
 * ```
 */
export interface Task {
  /** Unique identifier for the task. */
  id: string
  /** Identifier of the owning agent (foreign key to Agent.id). */
  agentId: string
  /** Short human-readable description of the task. */
  description: string
  /** Current lifecycle status of the task. */
  status: TaskStatus
  /** ISO-8601 timestamp of the last status change. */
  timestamp: string
}

// ---------------------------------------------------------------------------
// WebSocket Messages
// ---------------------------------------------------------------------------

/**
 * Discriminated union of WebSocket message types received from the
 * orchestrator backend (Task 12).
 *
 * The `type` field determines the shape of `data`:
 * - `agent_update`  -- An agent was created, modified, or removed.
 * - `task_update`   -- A task was created, modified, or removed.
 * - `connection_ack` -- Server acknowledged the WebSocket connection.
 * - `heartbeat`     -- Server keep-alive ping.
 */
export type WebSocketMessageType =
  | 'agent_update'
  | 'task_update'
  | 'connection_ack'
  | 'heartbeat'

/**
 * Generic envelope for all inbound WebSocket messages.
 *
 * Consumers should inspect `type` to determine how to interpret `data`.
 *
 * @example
 * ```ts
 * const msg: WebSocketMessage = {
 *   type: 'agent_update',
 *   data: { id: 'agent-abc123', name: 'linter', status: 'running', createdAt: '...' },
 * }
 * ```
 */
export interface WebSocketMessage {
  /** Discriminator indicating the kind of message. */
  type: WebSocketMessageType
  /** Payload whose shape depends on `type`. */
  data: Record<string, unknown>
}

// ---------------------------------------------------------------------------
// Aggregate statistics (used by store getters)
// ---------------------------------------------------------------------------

/**
 * Count of agents grouped by their current status.
 * Returned by the `agentStats` getter in the agent store.
 */
export interface AgentStats {
  pending: number
  running: number
  completed: number
  failed: number
}

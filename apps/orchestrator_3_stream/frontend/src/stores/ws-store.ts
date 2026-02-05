/**
 * Pinia store for WebSocket connection state.
 *
 * Tracks the health and lifecycle of the WebSocket connection to the
 * orchestrator backend (Task 12).  The ws-client service writes to this
 * store; UI components read from it to display connection indicators
 * and trigger fallback behaviour (polling) when the socket is unhealthy.
 *
 * Key design decisions:
 * - `lastMessageAt` stores a Unix-epoch millisecond timestamp so that
 *   the `isHealthy` getter can cheaply compare against `Date.now()`.
 * - `usePolling` is a flag the ws-client sets when it exhausts its
 *   reconnection budget and falls back to REST polling.
 */

import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

/** Maximum silence (in ms) before the connection is considered unhealthy. */
const HEALTHY_THRESHOLD_MS = 60_000

/** Human-readable connection status label. */
export type ConnectionStatus = 'connected' | 'disconnected' | 'reconnecting' | 'polling'

export const useWsStore = defineStore('ws', () => {
  // -----------------------------------------------------------------------
  // State
  // -----------------------------------------------------------------------

  /** Whether the WebSocket is currently in the OPEN state. */
  const connected = ref<boolean>(false)

  /** Number of consecutive reconnection attempts since the last success. */
  const retryCount = ref<number>(0)

  /**
   * Unix-epoch timestamp (ms) of the last message received from the
   * server, including heartbeats.  Initialised to 0 (no message yet).
   */
  const lastMessageAt = ref<number>(0)

  /**
   * `true` when the client has given up on WebSocket and is using
   * periodic REST polling as a fallback.
   */
  const usePolling = ref<boolean>(false)

  // -----------------------------------------------------------------------
  // Getters
  // -----------------------------------------------------------------------

  /**
   * The connection is considered healthy when it is open **and** the
   * server has sent a message within the last 60 seconds.
   */
  const isHealthy = computed<boolean>(() => {
    if (!connected.value) return false
    if (lastMessageAt.value === 0) return false
    return Date.now() - lastMessageAt.value < HEALTHY_THRESHOLD_MS
  })

  /**
   * Derived human-readable status suitable for display in a badge or
   * status bar.
   */
  const connectionStatus = computed<ConnectionStatus>(() => {
    if (usePolling.value) return 'polling'
    if (connected.value) return 'connected'
    if (retryCount.value > 0) return 'reconnecting'
    return 'disconnected'
  })

  // -----------------------------------------------------------------------
  // Actions
  // -----------------------------------------------------------------------

  /** Update the `connected` flag (called by ws-client on open / close). */
  function setConnected(value: boolean): void {
    connected.value = value
  }

  /** Set the current retry count (called by ws-client backoff logic). */
  function setRetryCount(count: number): void {
    retryCount.value = count
  }

  /**
   * Record that a message was just received.
   * Automatically updates `lastMessageAt` to the current timestamp.
   */
  function updateLastMessage(): void {
    lastMessageAt.value = Date.now()
  }

  /** Toggle fallback polling mode on or off. */
  function setUsePolling(value: boolean): void {
    usePolling.value = value
  }

  /**
   * Reset retry state after a successful reconnection.
   * Clears the retry counter and disables polling mode.
   */
  function resetRetry(): void {
    retryCount.value = 0
    usePolling.value = false
  }

  // -----------------------------------------------------------------------
  // Public API
  // -----------------------------------------------------------------------

  return {
    // State
    connected,
    retryCount,
    lastMessageAt,
    usePolling,

    // Getters
    isHealthy,
    connectionStatus,

    // Actions
    setConnected,
    setRetryCount,
    updateLastMessage,
    setUsePolling,
    resetRetry,
  }
})

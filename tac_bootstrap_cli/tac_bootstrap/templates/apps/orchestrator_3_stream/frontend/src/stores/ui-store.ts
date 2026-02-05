/**
 * Pinia store for transient UI state.
 *
 * Manages presentation concerns that are not persisted to the backend:
 * - Command palette visibility (Ctrl+K toggle)
 * - Autocomplete search filter text
 * - Currently selected / focused agent
 *
 * The `filteredAgents` getter cross-references the agent store so that
 * the command palette and autocomplete components can display a filtered
 * list without duplicating filtering logic.
 */

import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { useAgentStore } from '@/stores/agent-store'
import type { Agent } from '@/types/models'

export const useUiStore = defineStore('ui', () => {
  // -----------------------------------------------------------------------
  // State
  // -----------------------------------------------------------------------

  /** Whether the Ctrl+K command palette overlay is currently open. */
  const commandPaletteOpen = ref<boolean>(false)

  /** Current text typed into the autocomplete / search input. */
  const autocompleteFilter = ref<string>('')

  /** ID of the agent that is currently selected / focused (or `null`). */
  const selectedAgent = ref<string | null>(null)

  // -----------------------------------------------------------------------
  // Getters
  // -----------------------------------------------------------------------

  /**
   * Agents whose name contains the current `autocompleteFilter` text
   * (case-insensitive substring match).
   *
   * When the filter is empty the full sorted agent list is returned so
   * that the command palette displays all agents by default.
   */
  const filteredAgents = computed<Agent[]>(() => {
    const agentStore = useAgentStore()
    const filter = autocompleteFilter.value.trim().toLowerCase()

    if (filter === '') {
      return agentStore.agentList
    }

    return agentStore.agentList.filter((agent) =>
      agent.name.toLowerCase().includes(filter),
    )
  })

  // -----------------------------------------------------------------------
  // Actions
  // -----------------------------------------------------------------------

  /** Toggle the command palette between open and closed. */
  function toggleCommandPalette(): void {
    commandPaletteOpen.value = !commandPaletteOpen.value

    // Reset filter when opening so the user starts with a clean slate.
    if (commandPaletteOpen.value) {
      autocompleteFilter.value = ''
    }
  }

  /** Explicitly close the command palette (e.g. on Esc or outside click). */
  function closeCommandPalette(): void {
    commandPaletteOpen.value = false
    autocompleteFilter.value = ''
  }

  /** Update the autocomplete filter text (driven by input events). */
  function setAutocompleteFilter(value: string): void {
    autocompleteFilter.value = value
  }

  /**
   * Set the currently selected agent.
   * Pass `null` to deselect.
   */
  function selectAgent(agentId: string | null): void {
    selectedAgent.value = agentId
  }

  // -----------------------------------------------------------------------
  // Public API
  // -----------------------------------------------------------------------

  return {
    // State
    commandPaletteOpen,
    autocompleteFilter,
    selectedAgent,

    // Getters
    filteredAgents,

    // Actions
    toggleCommandPalette,
    closeCommandPalette,
    setAutocompleteFilter,
    selectAgent,
  }
})

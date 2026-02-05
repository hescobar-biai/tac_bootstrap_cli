import { ref, computed } from 'vue'
import type { Agent, Task } from '@/types/models'

export interface CommandResult {
  id: string
  name: string
  type: 'agent' | 'task'
  status: string
  action?: () => Promise<void>
}

export function useCommandPalette(agents: Agent[], tasks: Task[]) {
  const query = ref('')
  const selectedIndex = ref(0)

  const results = computed<CommandResult[]>(() => {
    const q = query.value.toLowerCase()
    if (!q) return []

    const agentResults: CommandResult[] = agents
      .filter((a) => a.name.toLowerCase().includes(q))
      .map((a) => ({
        id: a.id,
        name: a.name,
        type: 'agent' as const,
        status: a.status
      }))

    const taskResults: CommandResult[] = tasks
      .filter((t) => t.description.toLowerCase().includes(q))
      .map((t) => ({
        id: t.id,
        name: t.description,
        type: 'task' as const,
        status: t.status
      }))

    return [...agentResults, ...taskResults]
  })

  const selectNext = () => {
    if (results.value.length > 0) {
      selectedIndex.value = (selectedIndex.value + 1) % results.value.length
    }
  }

  const selectPrev = () => {
    if (results.value.length > 0) {
      selectedIndex.value = (selectedIndex.value - 1 + results.value.length) % results.value.length
    }
  }

  const execute = async () => {
    const result = results.value[selectedIndex.value]
    if (result?.action) {
      await result.action()
    }
  }

  const reset = () => {
    query.value = ''
    selectedIndex.value = 0
  }

  return {
    query,
    selectedIndex,
    results,
    selectNext,
    selectPrev,
    execute,
    reset
  }
}

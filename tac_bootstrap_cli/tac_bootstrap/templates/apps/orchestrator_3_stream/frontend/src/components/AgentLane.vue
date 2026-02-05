<template>
  <div class="flex flex-col rounded-lg border border-slate-700 bg-slate-800/50 backdrop-blur overflow-hidden">
    <!-- Agent Header -->
    <div
      :class="[
        'px-4 py-3 border-b border-slate-700 cursor-pointer transition-colors',
        statusColor
      ]"
    >
      <h3 class="font-semibold text-white">{{ agent.name }}</h3>
      <div class="flex items-center gap-2 mt-1">
        <span
          :class="[
            'inline-block w-2 h-2 rounded-full',
            agent.status === 'running'
              ? 'bg-blue-400 animate-pulse'
              : agent.status === 'completed'
                ? 'bg-green-400'
                : agent.status === 'failed'
                  ? 'bg-red-400'
                  : 'bg-yellow-400'
          ]"
        />
        <span class="text-xs text-slate-300 capitalize">{{ agent.status }}</span>
      </div>
    </div>

    <!-- Tasks Container -->
    <div class="flex-1 p-3 space-y-2 overflow-y-auto max-h-96">
      <div v-if="tasks.length === 0" class="text-center py-4">
        <p class="text-xs text-slate-500">No tasks yet</p>
      </div>

      <TaskCard v-for="task in tasks" :key="task.id" :task="task" />
    </div>

    <!-- Footer -->
    <div class="border-t border-slate-700 px-4 py-2 bg-slate-900/50">
      <button
        @click="executeAgent"
        class="w-full px-3 py-1 text-xs font-medium rounded bg-blue-600 hover:bg-blue-700 text-white transition-colors disabled:opacity-50"
        :disabled="isExecuting"
      >
        {{ isExecuting ? 'Executing...' : 'Execute' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import type { Agent } from '@/types/models'
import { useAgentStore } from '@/stores/agent-store'
import TaskCard from './TaskCard.vue'
import { apiClient } from '@/services/api-client'

const props = defineProps<{
  agent: Agent
}>()

const agentStore = useAgentStore()
const isExecuting = ref(false)

const tasks = computed(() => {
  return agentStore.tasksByAgent[props.agent.id] || []
})

const statusColor = computed(() => {
  switch (props.agent.status) {
    case 'running':
      return 'bg-blue-500/20 hover:bg-blue-500/30'
    case 'completed':
      return 'bg-green-500/20 hover:bg-green-500/30'
    case 'failed':
      return 'bg-red-500/20 hover:bg-red-500/30'
    default:
      return 'bg-slate-700/50 hover:bg-slate-700'
  }
})

async function executeAgent() {
  isExecuting.value = true
  try {
    await apiClient.executeAgent(props.agent.id)
  } catch (error) {
    console.error('Failed to execute agent:', error)
  } finally {
    isExecuting.value = false
  }
}
</script>

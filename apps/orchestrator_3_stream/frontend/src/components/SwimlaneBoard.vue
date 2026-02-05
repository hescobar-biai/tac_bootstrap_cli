<template>
  <div class="space-y-4">
    <!-- Empty State -->
    <div v-if="agents.length === 0" class="text-center py-12">
      <p class="text-slate-400">No agents available. Waiting for connections...</p>
    </div>

    <!-- Swimlane Grid -->
    <div v-else class="grid grid-cols-1 gap-6 lg:grid-cols-2 xl:grid-cols-3">
      <AgentLane v-for="agent in agents" :key="agent.id" :agent="agent" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAgentStore } from '@/stores/agent-store'
import { computed, onMounted } from 'vue'
import AgentLane from './AgentLane.vue'
import { wsClient } from '@/services/ws-client'

const agentStore = useAgentStore()

const agents = computed(() => agentStore.agentList)

onMounted(async () => {
  try {
    await wsClient.connect()
  } catch (error) {
    console.error('Failed to connect WebSocket:', error)
  }
})
</script>

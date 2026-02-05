<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
    <!-- Header -->
    <header class="border-b border-slate-700 bg-slate-900/50 backdrop-blur">
      <div class="px-6 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-white">Orchestrator</h1>
            <p class="text-sm text-slate-400">Real-time agent execution dashboard</p>
          </div>
          <div class="flex items-center gap-4">
            <div
              :class="[
                'px-3 py-1 rounded-full text-sm font-medium',
                wsStore.isHealthy
                  ? 'bg-green-500/20 text-green-400'
                  : 'bg-red-500/20 text-red-400'
              ]"
            >
              {{ wsStore.connectionStatus }}
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="p-6">
      <SwimlaneBoard />
    </main>

    <!-- Command Palette -->
    <CommandPalette />
  </div>
</template>

<script setup lang="ts">
import { useWsStore } from '@/stores/ws-store'
import { useAgentStore } from '@/stores/agent-store'
import { onMounted } from 'vue'
import SwimlaneBoard from '@/components/SwimlaneBoard.vue'
import CommandPalette from '@/components/CommandPalette.vue'

const wsStore = useWsStore()
const agentStore = useAgentStore()

// Initialize stores and WebSocket connection
onMounted(() => {
  // Initialize WebSocket connection (setup in ws-client)
  console.log('App initialized, stores ready')
})
</script>

<style scoped>
:deep(body) {
  @apply bg-slate-900 text-white;
}
</style>

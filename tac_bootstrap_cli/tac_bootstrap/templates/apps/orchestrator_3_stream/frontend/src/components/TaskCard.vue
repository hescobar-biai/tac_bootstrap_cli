<template>
  <div
    class="p-3 rounded border border-slate-600 bg-slate-700/40 hover:bg-slate-700/60 transition-colors cursor-pointer animate-card-enter"
  >
    <div class="flex items-start justify-between gap-2">
      <div class="flex-1 min-w-0">
        <h4 class="text-sm font-medium text-white truncate">{{ task.description }}</h4>
        <div class="flex items-center gap-2 mt-1">
          <span
            :class="[
              'inline-block px-2 py-0.5 text-xs font-semibold rounded',
              statusBadge
            ]"
          >
            {{ task.status }}
          </span>
          <span class="text-xs text-slate-400">{{ formattedTime }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Task } from '@/types/models'

const props = defineProps<{
  task: Task
}>()

const statusBadge = computed(() => {
  switch (props.task.status) {
    case 'pending':
      return 'bg-yellow-500/30 text-yellow-200'
    case 'running':
      return 'bg-blue-500/30 text-blue-200'
    case 'completed':
      return 'bg-green-500/30 text-green-200'
    case 'failed':
      return 'bg-red-500/30 text-red-200'
    default:
      return 'bg-slate-500/30 text-slate-200'
  }
})

const formattedTime = computed(() => {
  const date = new Date(props.task.timestamp)
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
})
</script>

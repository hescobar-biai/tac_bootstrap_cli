<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="uiStore.commandPaletteOpen" class="fixed inset-0 z-50 flex items-start justify-center pt-[20vh]">
        <!-- Backdrop -->
        <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" @click="close" />

        <!-- Modal -->
        <div class="relative w-full max-w-md mx-4 bg-slate-800 rounded-lg shadow-lg border border-slate-700">
          <!-- Search Input -->
          <div class="flex items-center gap-2 px-4 py-3 border-b border-slate-700">
            <span class="text-slate-400">⌘K</span>
            <input
              ref="inputRef"
              v-model="searchQuery"
              type="text"
              placeholder="Search agents or tasks..."
              class="flex-1 bg-transparent outline-none text-white placeholder-slate-500"
              @keydown.esc="close"
              @keydown.enter="executeSelected"
              @keydown.arrow-down="selectNext"
              @keydown.arrow-up="selectPrev"
            />
          </div>

          <!-- Results -->
          <div v-if="results.length > 0" class="max-h-64 overflow-y-auto">
            <div
              v-for="(result, index) in results"
              :key="result.id"
              :class="[
                'px-4 py-2 cursor-pointer transition-colors',
                index === selectedIndex
                  ? 'bg-blue-600/40 text-blue-200'
                  : 'hover:bg-slate-700/50 text-slate-300'
              ]"
              @click="selectIndex(index)"
              @click.prevent="executeSelected"
            >
              <div class="text-sm font-medium">{{ result.name }}</div>
              <div class="text-xs text-slate-400 mt-0.5">
                {{ result.type === 'agent' ? 'Agent' : 'Task' }} • {{ result.status }}
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="px-4 py-8 text-center">
            <p v-if="searchQuery" class="text-sm text-slate-400">No results found</p>
            <p v-else class="text-sm text-slate-500">Start typing to search...</p>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { useUiStore } from '@/stores/ui-store'
import { useAgentStore } from '@/stores/agent-store'
import { useKeyboard } from '@/composables/use-keyboard'
import { ref, computed, onMounted, nextTick } from 'vue'

const uiStore = useUiStore()
const agentStore = useAgentStore()
const inputRef = ref<HTMLInputElement>()
const searchQuery = ref('')
const selectedIndex = ref(0)

useKeyboard()

const results = computed(() => {
  const query = searchQuery.value.toLowerCase()
  if (!query) return []

  const agents = agentStore.agentList
    .filter((a) => a.name.toLowerCase().includes(query))
    .map((a) => ({
      id: a.id,
      name: a.name,
      type: 'agent' as const,
      status: a.status
    }))

  const allTasks = Object.values(agentStore.tasks).flat()
  const tasks = allTasks
    .filter((t) => t.description.toLowerCase().includes(query))
    .slice(0, 5)
    .map((t) => ({
      id: t.id,
      name: t.description,
      type: 'task' as const,
      status: t.status
    }))

  return [...agents, ...tasks]
})

function close() {
  uiStore.closeCommandPalette()
  searchQuery.value = ''
  selectedIndex.value = 0
}

function selectNext() {
  if (results.value.length > 0) {
    selectedIndex.value = (selectedIndex.value + 1) % results.value.length
  }
}

function selectPrev() {
  if (results.value.length > 0) {
    selectedIndex.value = (selectedIndex.value - 1 + results.value.length) % results.value.length
  }
}

function selectIndex(index: number) {
  selectedIndex.value = index
}

function executeSelected() {
  if (results.value[selectedIndex.value]) {
    const result = results.value[selectedIndex.value]
    console.log('Executing:', result)
    close()
  }
}

onMounted(async () => {
  await nextTick()
  inputRef.value?.focus()
})
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>

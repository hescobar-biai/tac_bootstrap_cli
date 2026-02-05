import { onMounted, onUnmounted } from 'vue'
import { useUiStore } from '@/stores/ui-store'

export function useKeyboard() {
  const uiStore = useUiStore()

  const handleKeydown = (event: KeyboardEvent) => {
    // Ctrl+K or Cmd+K for command palette
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
      event.preventDefault()
      uiStore.toggleCommandPalette()
    }

    // Escape to close modals
    if (event.key === 'Escape') {
      uiStore.closeCommandPalette()
    }
  }

  onMounted(() => {
    window.addEventListener('keydown', handleKeydown)
  })

  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown)
  })

  return {
    handleKeydown
  }
}

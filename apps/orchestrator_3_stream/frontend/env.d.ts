/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

interface ImportMetaEnv {
  /** REST API base URL for the orchestrator backend */
  readonly VITE_API_URL: string
  /** WebSocket URL for real-time agent status updates */
  readonly VITE_WS_URL: string
  /** Development server port */
  readonly VITE_PORT: string
  /** Fallback polling interval in milliseconds */
  readonly VITE_POLLING_INTERVAL: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

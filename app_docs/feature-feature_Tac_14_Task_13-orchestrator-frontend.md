---
doc_type: feature
adw_id: feature_Tac_14_Task_13
date: 2026-02-05
idk:
  - Vue 3 SPA
  - Pinia state management
  - WebSocket client
  - Kanban swimlane UI
  - Keyboard shortcuts
  - Command palette
  - Tailwind CSS
  - TypeScript strict mode
tags:
  - frontend
  - orchestrator
  - vue3
  - typescript
related_code:
  - apps/orchestrator_3_stream/frontend/src/main.ts
  - apps/orchestrator_3_stream/frontend/src/stores/agent-store.ts
  - apps/orchestrator_3_stream/frontend/src/services/ws-client.ts
  - apps/orchestrator_3_stream/frontend/src/components/SwimlaneBoard.vue
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Orchestrator Frontend (Vue 3 + TypeScript + Pinia)

**ADW ID:** feature_Tac_14_Task_13
**Date:** 2026-02-05
**Specification:** `specs/issue-634-adw-feature_Tac_14_Task_13-sdlc_planner-orchestrator-frontend.md`

## Overview

Implemented a Vue 3 + TypeScript single-page application with real-time Kanban swimlane visualization for orchestrator agent management. The frontend consumes WebSocket updates from the Task 12 backend, renders agents as vertical swimlanes with task cards, and provides keyboard-driven interactions via command palette (Ctrl+K) and autocomplete (Tab). Uses Pinia for state management, Shadcn/Vue + Tailwind CSS for UI, and includes resilient WebSocket client with exponential backoff + fallback polling.

## What Was Built

### Vue 3 Application Core
- Full-featured SPA with Vite build system, TypeScript strict mode, and modular architecture
- Pinia stores for agent state, UI state, and WebSocket connection management
- Services layer for REST API and WebSocket client implementations
- Vue composables for keyboard handling and command palette logic

### Kanban Swimlane UI Components
- `SwimlaneBoard.vue` - Main grid layout displaying agents as vertical lanes
- `AgentLane.vue` - Individual agent swimlane with task card container
- `TaskCard.vue` - Task display with status badge and timestamps
- `CommandPalette.vue` - Ctrl+K search interface for agent/task navigation
- Responsive layout with Tailwind CSS custom theme for agent status colors

### State Management (Pinia)
- `agent-store.ts` - Agent list, task indexing by agent, computed getters for filtering/sorting
- `ui-store.ts` - Command palette open state, autocomplete filter, keyboard shortcuts
- `ws-store.ts` - WebSocket connection state, retry count, fallback polling mode flag

### Resilient Network Layer
- WebSocket client with exponential backoff (2s → 4s → 8s → 16s max)
- Fallback polling mechanism (30s interval) when WebSocket connection fails
- Heartbeat mechanism to detect stale connections
- Connection state machine (connecting, connected, failed, polling)
- REST API client (axios) for agent queries

### Keyboard & Interaction Features
- Ctrl+K opens command palette with full-text search on agent names and task descriptions
- Tab triggers agent name autocomplete with arrow key navigation
- Esc closes modals and palettes
- Enter selects items from lists
- Real-time state updates from WebSocket messages

### CLI Template Integration
- Complete frontend scaffold templated with Jinja2 for CLI reuse
- `.env.j2` template for environment variable injection (API_URL, WS_URL, ports)
- `vite.config.ts.j2` with templated port configuration
- ScaffoldService integration to render templates with TACConfig values

## Technical Implementation

### Files Created

#### Frontend Base Application
- `apps/orchestrator_3_stream/frontend/` - Full Vue 3 SPA with 25+ source files
- `package.json` - Dependencies: Vue 3.3.4, Pinia 2.1.6, axios, shadcn-vue, Tailwind, TypeScript
- `vite.config.ts` - Vite build configuration with Vue plugin
- `tsconfig.json` - TypeScript strict mode settings
- `tailwind.config.js` - Custom theme with agent status colors (pending, running, completed, failed)
- `src/types/models.ts` - TypeScript interfaces (Agent, Task, WebSocketMessage, AgentStats)
- `src/stores/` - Three Pinia stores with computed getters and mutations
- `src/services/` - WebSocket and REST API clients
- `src/components/` - Vue SFC components for UI
- `src/composables/` - Vue logic composition functions
- `.env.example` - Reference environment variables

#### CLI Templates & Integration
- `tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/frontend/` - Full mirror with .j2 extensions
- Updated `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Frontend template registration
- Updated `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - Config model extensions for orchestrator frontend

### Key Architecture Patterns

**Services Layer**
- `ws-client.ts` - WebSocketClient class with connection lifecycle management
- `api-client.ts` - Axios instance configured from environment variables

**State Management**
- Single-store pattern: three specialized Pinia stores for agents, UI, WebSocket state
- Computed getters for derived state (agentList sorted, tasksByAgent indexed)
- Reactive updates directly update store state when receiving WebSocket messages

**Component Hierarchy**
- App.vue (root) → SwimlaneBoard (grid layout) → AgentLane (swimlane) → TaskCard (individual task)
- CommandPalette and autocomplete rendered as overlays managed by ui-store

**Environment Configuration**
- VITE_WS_URL, VITE_API_URL, VITE_POLLING_INTERVAL injected at build time
- TypeScript strict mode ensures type safety across all modules

## How to Use

### Development Server

```bash
cd apps/orchestrator_3_stream/frontend
npm install
npm run dev
```

Open http://localhost:5173 to view the application.

### Building for Production

```bash
cd apps/orchestrator_3_stream/frontend
npm install
npm run build
npm run preview
```

### Environment Configuration

Create `.env.local` or export variables:

```bash
VITE_WS_URL=ws://localhost:8000
VITE_API_URL=http://localhost:8000/api
VITE_POLLING_INTERVAL=30000
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+K` | Open command palette (search agents/tasks) |
| `Tab` | Trigger agent name autocomplete |
| `Esc` | Close modal or palette |
| `Enter` | Select item from list or execute command |
| `↑ ↓` | Navigate autocomplete/palette results |

### Using with TAC Bootstrap CLI

The frontend is fully templated for CLI scaffolding:

```bash
# CLI integration ensures new projects include working frontend setup
cd tac_bootstrap_cli
uv run tac_bootstrap --generate my-project
# Generated project includes: apps/orchestrator_3_stream/frontend/
# with .env and vite.config.ts populated from config.yml
```

## Configuration

### Build-Time Variables

**Vite Environment Variables** (define in `.env`, `.env.local`, or `.env.*.local`):

| Variable | Default | Purpose |
|----------|---------|---------|
| `VITE_WS_URL` | `ws://localhost:8000` | WebSocket endpoint for agent updates |
| `VITE_API_URL` | `http://localhost:8000/api` | REST API base URL for queries |
| `VITE_POLLING_INTERVAL` | `30000` | Fallback polling interval (ms) |

### Tailwind Theme Customization

`tailwind.config.js` includes custom colors for agent status:
- `pending` - Blue
- `running` - Green
- `completed` - Teal
- `failed` - Red

## Testing

### Type Checking

Verify TypeScript strict mode compliance:

```bash
cd apps/orchestrator_3_stream/frontend
npm run type-check
```

### Build Verification

Ensure production build succeeds:

```bash
cd apps/orchestrator_3_stream/frontend
npm run build
```

Check for TypeScript errors, CSS issues, and bundle warnings.

### Manual Testing

1. **Swimlane Rendering**: Open dev server and verify agents display as vertical lanes with task cards
2. **WebSocket Connection**: Check browser console for "WebSocket connected" message; verify agents update in real-time
3. **Command Palette**: Press `Ctrl+K`, type agent name, verify results appear and selection works
4. **Autocomplete**: Press `Tab` in agent name context, verify names filter by input
5. **Keyboard Shortcuts**: Test Esc to close modals, Enter to select items, arrow keys to navigate

### Integration with Backend

To test with Task 12 backend:

```bash
# Terminal 1: Start backend (Task 12)
cd apps/orchestrator_3_stream/backend
python -m uvicorn main:app --reload

# Terminal 2: Start frontend
cd apps/orchestrator_3_stream/frontend
npm run dev
```

Open http://localhost:5173 and observe agent updates from WebSocket messages.

## Notes

- **No Authentication (MVP)**: Current implementation targets authenticated endpoints in Phase 2
- **State Sync**: WebSocket messages update Pinia stores directly; changes cascade to components via Vue reactivity
- **Bundle Size**: Shadcn/Vue components are tree-shakeable; consider lazy-loading if bundle size exceeds 500KB
- **Polling Fallback**: Automatically activated if WebSocket fails after 5 reconnection attempts; reverts to WebSocket when available
- **Keyboard Focus Management**: Command palette and autocomplete handle focus/blur lifecycle to prevent hidden modals
- **Message Format**: WebSocket messages follow JSON schema: `{ type: "agent_update"|"task_update", data: {...} }`
- **TypeScript Strict**: All files use `strict: true` in tsconfig.json; no `any` types allowed

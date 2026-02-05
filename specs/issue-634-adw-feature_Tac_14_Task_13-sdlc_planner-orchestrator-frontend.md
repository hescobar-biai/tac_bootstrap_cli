# Feature: Implementar Orchestrator Frontend (BASE + TEMPLATES)

## Metadata
issue_number: `634`
adw_id: `feature_Tac_14_Task_13`
issue_json: `See auto-resolved clarifications above`

## Feature Description
Create Vue.js 3 + TypeScript + Vite frontend application with Kanban swimlane visualization for orchestrator agents. Application consumes WebSocket updates from Task 12 backend, renders agents as vertical swimlanes with task cards, implements command palette (Ctrl+K), agent autocomplete, and keyboard shortcuts. Uses Pinia for state management (agentStore, uiStore, wsStore), Tailwind + Shadcn/Vue for UI, and includes resilient WebSocket client with exponential backoff + fallback polling.

## User Story
As an orchestrator user
I want to visualize agent execution in real-time with swimlane cards
So that I can monitor orchestrator state without terminal interaction

## Problem Statement
Task 12 provides REST/WebSocket backend but lacks frontend visualization. Users need Kanban UI to view agents and tasks in real-time, with keyboard-driven interactions (Ctrl+K command palette, Tab autocomplete).

## Solution Statement
Build Vue 3 SPA with Pinia state management, Shadcn/Vue component library, and Tailwind CSS. Architecture: services/ (API/WS clients), composables/ (Vue logic), stores/ (Pinia), components/ (Vue SFC). No authentication for MVP. Implement in BASE location and templatize for CLI scaffold reuse.

## Relevant Files

### BASE Structure (Functional)
- `apps/orchestrator_3_stream/frontend/package.json` - Node dependencies
- `apps/orchestrator_3_stream/frontend/vite.config.ts` - Build config
- `apps/orchestrator_3_stream/frontend/src/main.ts` - Entry point
- `apps/orchestrator_3_stream/frontend/src/App.vue` - Root component
- `apps/orchestrator_3_stream/frontend/src/services/ws-client.ts` - WebSocket client
- `apps/orchestrator_3_stream/frontend/src/services/api-client.ts` - REST client
- `apps/orchestrator_3_stream/frontend/src/stores/agent-store.ts` - Agent state (Pinia)
- `apps/orchestrator_3_stream/frontend/src/stores/ui-store.ts` - UI state (Pinia)
- `apps/orchestrator_3_stream/frontend/src/stores/ws-store.ts` - WebSocket state (Pinia)
- `apps/orchestrator_3_stream/frontend/src/composables/use-keyboard.ts` - Keyboard shortcuts
- `apps/orchestrator_3_stream/frontend/src/composables/use-command-palette.ts` - Ctrl+K palette
- `apps/orchestrator_3_stream/frontend/src/components/SwimlaneBoard.vue` - Main board
- `apps/orchestrator_3_stream/frontend/src/components/AgentLane.vue` - Agent swimlane
- `apps/orchestrator_3_stream/frontend/src/components/TaskCard.vue` - Task card
- `apps/orchestrator_3_stream/frontend/src/components/CommandPalette.vue` - Command input
- `apps/orchestrator_3_stream/frontend/src/components/AgentAutocomplete.vue` - Autocomplete
- `apps/orchestrator_3_stream/frontend/.env.example` - Example env vars

### TEMPLATES Structure (Jinja2)
- `tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/frontend/` - Full structure mirrored
- `.env.j2` - Templated environment variables (ports, API endpoints)
- `vite.config.ts.j2` - Templated Vite config with port variable

### CLI Integration
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Register frontend scaffold

## Implementation Plan

### Phase 1: Project Setup
- Initialize Vite + Vue 3 + TypeScript project structure
- Install dependencies: pinia, axios, tailwind, shadcn/vue, typescript
- Create build config with environment variables (.env.j2)
- Setup TypeScript strict mode, tsconfig.json

### Phase 2: State Management
- Create Pinia stores: agent-store (agents + tasks), ui-store (palette, autocomplete), ws-store (connection state)
- Define TypeScript interfaces for AgentState, TaskState, WebSocketState
- Implement store getters for filtered/sorted agents

### Phase 3: WebSocket & API Integration
- Implement ws-client.ts with exponential backoff reconnection
- Add fallback to polling if WebSocket fails
- Implement api-client.ts for REST calls
- Handle connection state transitions and error recovery

### Phase 4: Components & Composables
- Build SwimlaneBoard.vue (grid layout, agent lanes)
- Build AgentLane.vue (vertical lane, card container)
- Build TaskCard.vue (task display with status)
- Implement composables: use-keyboard (shortcuts), use-command-palette (Ctrl+K search)
- Build CommandPalette.vue and AgentAutocomplete.vue

### Phase 5: UI Polish & Keyboard
- Implement keyboard shortcuts: Ctrl+K (palette), Tab (autocomplete), Esc (close)
- Add real-time state updates from WebSocket
- Style with Tailwind + Shadcn/Vue components
- Add loading states and error messages

### Phase 6: Templatization & CLI Integration
- Copy frontend to templates/ with .j2 extensions for env-sensitive files
- Parameterize API endpoint, WebSocket URL, ports in .env.j2
- Update scaffold_service.py to render frontend templates
- Test scaffolding generates correct .env values

## Step by Step Tasks

### Task 1: Project Initialization
- Create `apps/orchestrator_3_stream/frontend/` directory
- Initialize `package.json` with Vue 3, Vite, TypeScript, Pinia, Tailwind, axios
- Create `vite.config.ts` with TypeScript support
- Create `tsconfig.json` with strict mode
- Create `index.html` entry point
- Setup Tailwind & Shadcn/Vue configuration

### Task 2: Pinia State Management
- Create `src/stores/agent-store.ts` (agent list, task status updates)
- Create `src/stores/ui-store.ts` (command palette open, autocomplete filter)
- Create `src/stores/ws-store.ts` (connection state, retry count, fallback mode)
- Define TypeScript types for state interfaces
- Create store composition in composables if needed

### Task 3: WebSocket Client
- Implement `src/services/ws-client.ts` with exponential backoff (2s, 4s, 8s, 16s max)
- Add fallback polling mechanism (30s polling if WS fails)
- Implement connection state machine (connecting, connected, failed, polling)
- Handle message parsing and store updates
- Add heartbeat mechanism to detect stale connections

### Task 4: REST API Client
- Implement `src/services/api-client.ts` with axios instance
- Create endpoints: GET /agents, GET /agents/:id, POST /agents/:id/execute
- Add error handling and retry logic
- Setup base URL from environment variables

### Task 5: Swimlane Components
- Build `src/components/SwimlaneBoard.vue` (main grid, lane layout)
- Build `src/components/AgentLane.vue` (agent header, task cards container)
- Build `src/components/TaskCard.vue` (task title, status badge, timestamp)
- Implement Kanban card display with status colors
- Add smooth animations for card transitions

### Task 6: Keyboard & Command Palette
- Implement `src/composables/use-keyboard.ts` (Ctrl+K, Esc, Tab handlers)
- Build `src/composables/use-command-palette.ts` (search logic, action execution)
- Build `src/components/CommandPalette.vue` (search input, results list)
- Add keyboard focus management and accessibility

### Task 7: Autocomplete
- Implement `src/composables/use-autocomplete.ts` (agent name matching, filtering)
- Build `src/components/AgentAutocomplete.vue` (dropdown, keyboard navigation)
- Integrate with ui-store for state management
- Add debouncing for input

### Task 8: App Root & Styling
- Create `src/App.vue` (root layout, store initialization)
- Create `src/main.ts` (Vue app mount, plugin registration)
- Setup Tailwind CSS custom theme
- Create global styles for swimlane board

### Task 9: Environment & .env Files
- Create `src/config/env.ts` (type-safe env loading)
- Create `.env.example` with API_URL, WS_URL, PORT variables
- Create `.env.j2` for template rendering (Jinja2 variables)

### Task 10: Template Scaffolding
- Copy entire `apps/orchestrator_3_stream/frontend/` to `tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/frontend/`
- Add .j2 extensions to `.env` and `vite.config.ts`
- Templatize: `{{ config.orchestrator.frontend_port }}`, `{{ config.api_base_url }}`
- Update `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`:
  - Add frontend scaffolding logic in `create_orchestrator_frontend()` method
  - Register template rendering for `apps/orchestrator_3_stream/frontend/`
  - Pass config variables to Jinja2 context

### Task 11: Integration Testing
- Test WebSocket connection and reconnection logic
- Test command palette search functionality
- Test agent autocomplete filtering
- Test keyboard shortcut handling
- Verify swimlane rendering updates in real-time

### Task 12: Validation Commands
- `cd apps/orchestrator_3_stream/frontend && npm install && npm run build`
- `cd apps/orchestrator_3_stream/frontend && npm run preview`
- Manual UI testing: swimlane renders, Ctrl+K opens palette, Tab triggers autocomplete
- Test WebSocket connection to Task 12 backend (if available)
- Generate new project with updated CLI and verify scaffolding works

## Testing Strategy

### Unit Tests
- Pinia store logic (agent filtering, state transitions)
- Service functions (API client, WS client message parsing)
- Composables (keyboard event handling, autocomplete logic)
- Component snapshots for SwimlaneBoard, TaskCard

### Edge Cases
- WebSocket connection lost → fallback to polling
- Reconnection after network recovery
- Command palette search with special characters
- Agent autocomplete with empty input
- Multiple agents with same name prefix
- Task status updates during component unmount

### Integration Tests
- Full swimlane board update flow (WS message → store → component)
- Keyboard shortcut interaction with modal/input components
- Command palette execution of agent actions
- Real-time sync across multiple agent lanes

## Acceptance Criteria
- Vue 3 + TypeScript app builds without errors (`npm run build`)
- Swimlane board renders with agents as vertical lanes, tasks as cards
- WebSocket client connects and receives updates (or falls back to polling)
- Command palette (Ctrl+K) opens, searches agents, executes actions
- Agent autocomplete (Tab) filters by name, navigates with arrow keys
- Keyboard shortcuts (Esc closes modals) work correctly
- Environment variables properly templated in `.j2` files
- `scaffold_service.py` registers and renders frontend templates
- New projects generated via CLI include working frontend setup
- Zero TypeScript errors in strict mode

## Validation Commands
```bash
# Build verification
cd apps/orchestrator_3_stream/frontend && npm install && npm run build

# Type checking
cd apps/orchestrator_3_stream/frontend && npx tsc --noEmit

# Preview server
cd apps/orchestrator_3_stream/frontend && npm run preview

# Template validation (if scaffold_service.py is executable)
cd tac_bootstrap_cli && uv run tac_bootstrap/application/scaffold_service.py

# Integration test with backend (requires Task 12 running)
# Manual testing: curl http://localhost:5173 and verify UI loads
```

## Notes
- Architecture mirrors `orchestrator_web` backend pattern (services → stores → components)
- WebSocket uses JSON message format: `{ type: "agent_update", data: {...} }`
- Fallback polling interval: 30 seconds (configurable via .env)
- Command palette searches agent names and task descriptions (full-text match)
- Keyboard shortcuts: Ctrl+K (palette), Tab (autocomplete), Esc (close), Enter (select)
- No authentication for MVP (can add in Phase 2)
- Tailwind config includes custom colors for agent status (pending, running, completed, failed)
- Template variables use underscore case: `{{ config.orchestrator.api_base_url }}`
- Consider lazy-loading Shadcn/Vue components if bundle size becomes concern

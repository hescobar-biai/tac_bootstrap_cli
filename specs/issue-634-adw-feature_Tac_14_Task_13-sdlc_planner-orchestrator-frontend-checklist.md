# Validation Checklist: Implementar Orchestrator Frontend (BASE + TEMPLATES)

**Spec:** `specs/issue-634-adw-feature_Tac_14_Task_13-sdlc_planner-orchestrator-frontend.md`
**Branch:** `feature-issue-634-adw-feature-tac-14-task-13-orchestrator-frontend`
**Review ID:** `feature_Tac_14_Task_13`
**Date:** `2026-02-05`

## Automated Technical Validations

- [ ] Syntax and type checking - FAILED
- [x] Linting - PASSED
- [x] Unit tests - PASSED
- [x] Application smoke test - PASSED

## Acceptance Criteria

- [ ] Vue 3 + TypeScript app builds without errors (`npm run build`)
- [x] Swimlane board renders with agents as vertical lanes, tasks as cards
- [ ] WebSocket client connects and receives updates (or falls back to polling)
- [ ] Command palette (Ctrl+K) opens, searches agents, executes actions
- [ ] Agent autocomplete (Tab) filters by name, navigates with arrow keys
- [ ] Keyboard shortcuts (Esc closes modals) work correctly
- [x] Environment variables properly templated in `.j2` files
- [x] `scaffold_service.py` registers and renders frontend templates
- [ ] New projects generated via CLI include working frontend setup
- [ ] Zero TypeScript errors in strict mode

## Validation Commands Executed

```bash
cd apps/orchestrator_3_stream/frontend && npm install
cd apps/orchestrator_3_stream/frontend && npx tsc --noEmit
cd tac_bootstrap_cli && uv run python -m py_compile tac_bootstrap/application/scaffold_service.py
cd tac_bootstrap_cli && uv run pytest tests/test_cli_generate.py -v --tb=short
```

## Review Summary

Vue 3 + TypeScript frontend for orchestrator implemented with Pinia state management, WebSocket client, and Kanban swimlane UI. Project structure complete with all required components, services, stores, and composables. Frontend templates registered in scaffold service. However, blocking TypeScript compilation errors in ws-client.ts prevent the build from succeeding.

## Review Issues

### Issue 1: **BLOCKER** - ws-client.ts updateAgent() signature mismatch
- **Location:** `apps/orchestrator_3_stream/frontend/src/services/ws-client.ts:68, 150`
- **Description:** updateAgent() called with 1 arg but expects 2 (id + patch). Line 68: `this.agentStore.updateAgent({...})` should be `this.agentStore.updateAgent(agent.id, {...})`. Same issue at line 150 in polling logic.
- **Fix:** Extract agent ID and pass as separate argument to match store signature.

### Issue 2: **BLOCKER** - ws-client.ts updateTask() signature mismatch
- **Location:** `apps/orchestrator_3_stream/frontend/src/services/ws-client.ts:80`
- **Description:** updateTask() called with 1 arg but expects 2 (agentId + patch). Line 80: `this.agentStore.updateTask({...})` should match the store method signature.
- **Fix:** Check agent-store.ts updateTask() signature and fix method call accordingly.

### Issue 3: **BLOCKER** - ws-client.ts updateLastMessage() signature mismatch
- **Location:** `apps/orchestrator_3_stream/frontend/src/services/ws-client.ts:62`
- **Description:** updateLastMessage() called with Date arg but expects 0 args per ws-store signature.
- **Fix:** Remove the Date argument: `this.wsStore.updateLastMessage()`. The store will set current time internally.

### Issue 4: **BLOCKER** - Template file has same errors
- **Location:** `tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/frontend/src/services/ws-client.ts`
- **Description:** Same TypeScript errors exist in template file - need to apply fixes to both BASE and TEMPLATE versions.
- **Fix:** Apply all ws-client fixes to both `/apps/.../frontend/` and `/templates/.../frontend/` versions.

---
*Generado por el comando `/review` - TAC Bootstrap CLI*

# Feature: Implementar Test Suites (BASE + TEMPLATES)

## Metadata
- **issue_number**: 636
- **adw_id**: feature_Tac_14_Task_15
- **type**: /feature
- **workflow**: /adw_sdlc_zte_iso
- **category**: Testing
- **priority**: Alta
- **dependencies**: Tasks 7, 8, 9, 11, 12, 13 from plan_tasks_Tac_14.md

## Feature Description
Implementar suite completa de tests unitarios (pytest) y end-to-end (Playwright) para validar database modules, workflows de ADW, Agent SDK integrations, WebSockets, y orchestrator UI. Tests usan SQLite local, fixtures reales, y cobertura mínima 80%.

## User Story
As a TAC-14 developer
I want to verify all components (database, workflows, Agent SDK, WebSockets, orchestrator UI) work correctly
So that regressions are caught early and new features are validated before release

## Problem Statement
- Sin tests, cambios en database/workflows/SDK pueden romper funcionalidad silenciosamente
- Sin E2E tests, orchestrator UI puede tener bugs de interacción no detectados
- Falta de fixtures y conftest.py hace testing difícil y repetitivo
- 6 flujos críticos (agent creation, execution, log streaming, WebSocket, error handling, state persistence) sin validación

## Solution Statement
Implementar tests en dos fases:
1. **BASE (tac_bootstrap repo)**: 4 archivos pytest + conftest.py con fixtures SQLite; 6 tests Playwright E2E
2. **TEMPLATES (CLI)**: Copiar estructura completa para que nuevos proyectos incluyan tests automáticamente
3. Registrar en scaffold_service.py para inyección automática

## Relevant Files

### Existing Test Infrastructure
- `.claude/commands/test.md` - Skill para ejecutar tests
- `.claude/commands/test_e2e.md` - Skill para E2E tests
- `pyproject.toml` - pytest, pytest-asyncio, pytest-cov, aiosqlite dependencias

### Files to Create (BASE)
- `adws/adw_tests/conftest.py` - Fixtures SQLite, factories, utilities
- `adws/adw_tests/test_database.py` - Tests de database schema, CRUD operations, transactions
- `adws/adw_tests/test_workflows.py` - Tests de ADW execution, state management, logging
- `adws/adw_tests/test_agent_sdk.py` - Tests de claude-agent-sdk integration
- `adws/adw_tests/test_websockets.py` - Tests de WebSocket connections, streaming, message handling
- `adws/adw_tests/pytest.ini` - Configuration (SQLite in-memory DB path, log level)
- `apps/orchestrator_3_stream/playwright.config.ts` - Playwright configuration
- `apps/orchestrator_3_stream/playwright-tests/test-agent-creation.spec.ts` - Agent creation E2E
- `apps/orchestrator_3_stream/playwright-tests/test-agent-execution.spec.ts` - Agent execution/visualization
- `apps/orchestrator_3_stream/playwright-tests/test-log-streaming.spec.ts` - Real-time log streaming
- `apps/orchestrator_3_stream/playwright-tests/test-websocket-connection.spec.ts` - WebSocket handling
- `apps/orchestrator_3_stream/playwright-tests/test-error-scenarios.spec.ts` - Error/failure scenarios
- `apps/orchestrator_3_stream/playwright-tests/test-state-persistence.spec.ts` - State across sessions

### Files to Create (TEMPLATES)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_tests/conftest.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_tests/test_database.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_tests/test_workflows.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_tests/test_agent_sdk.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_tests/test_websockets.py.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_tests/pytest.ini.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/playwright.config.ts.j2`
- `tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/playwright-tests/` (6 test files)

### Files to Modify
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Agregar renderizado de test templates

## Implementation Plan

### Phase 1: Setup & Fixtures Foundation
**Goal**: Preparar infraestructura de testing (conftest, fixtures, SQLite)

Tasks:
1. Crear directorio `adws/adw_tests/`
2. Crear `conftest.py` con:
   - SQLite in-memory fixtures (`db_path`, `db_connection`)
   - Factory fixtures para OrchestratorAgent, Agent, Prompt, AgentLog
   - Fixtures para WebSocket mock
   - Setup/teardown hooks para schema initialization
3. Crear `pytest.ini` con configuración (testpaths, asyncio_mode, sqlite path)

### Phase 2: Pytest Unit Tests (BASE)
**Goal**: Implementar 4 archivos de unit tests validando components

Tasks:
4. `test_database.py`:
   - Test schema creation (CREATE TABLE, indexes)
   - Test CRUD operations (INSERT, SELECT, UPDATE, DELETE)
   - Test foreign key constraints
   - Test transactions y rollback
   - Fixtures: sample agents, prompts, logs

5. `test_workflows.py`:
   - Test ADW execution workflow (pending → running → completed)
   - Test state transitions (valid/invalid paths)
   - Test logging (agent_logs, system_logs)
   - Test error handling y recovery
   - Fixtures: mock ADW runner, execution context

6. `test_agent_sdk.py`:
   - Test claude-agent-sdk initialization
   - Test agent creation, execution (mock API)
   - Test message handling
   - Test error propagation
   - Fixtures: mock API client, SDK context

7. `test_websockets.py`:
   - Test WebSocket connection lifecycle
   - Test message streaming (agent logs, real-time updates)
   - Test connection recovery
   - Test broadcast to multiple clients
   - Fixtures: mock WebSocket server, client connections

### Phase 3: Playwright E2E Tests (BASE)
**Goal**: Validar 6 flujos críticos del orchestrator UI

Tasks:
8. Create `playwright.config.ts` with:
   - baseURL: `http://localhost:3000` (orchestrator_3_stream dev server)
   - browser: Chromium
   - headless mode
   - timeout: 30s
   - screenshot on failure
   - trace recording

9. `test-agent-creation.spec.ts`:
   - Navigate to orchestrator dashboard
   - Click "Create Agent" button
   - Fill form (name, description)
   - Submit and verify success toast
   - Verify agent appears in list

10. `test-agent-execution.spec.ts`:
    - Select existing agent
    - Click "Execute" button
    - Verify status changes to "running"
    - Verify execution visualization appears
    - Wait for completion and verify "completed" status

11. `test-log-streaming.spec.ts`:
    - Start agent execution
    - Monitor logs section for real-time updates
    - Verify log entries appear within 5s
    - Verify log formatting (timestamp, level, message)

12. `test-websocket-connection.spec.ts`:
    - Open orchestrator
    - Verify WebSocket connection establishes
    - Verify heartbeat messages every 30s
    - Close app and verify reconnect on reopen
    - Check console for no connection errors

13. `test-error-scenarios.spec.ts`:
    - Try creating agent with empty name (verify error)
    - Try executing non-existent agent (verify error)
    - Simulate server disconnect and verify error message
    - Verify error recovery (retry button works)

14. `test-state-persistence.spec.ts`:
    - Create and execute agent in session 1
    - Close session and reopen session 2
    - Verify agent and execution history persist
    - Verify logs are accessible across sessions

### Phase 4: Template Integration
**Goal**: Sincronizar tests con CLI templates

Tasks:
15. Copiar estructura `adws/adw_tests/` a templates con extensión `.j2`:
    - No aplicar Jinja2 (copias estáticas)
    - Preservar imports y rutas relativas

16. Copiar `apps/orchestrator_3_stream/playwright-tests/` y `playwright.config.ts` a templates:
    - Tests copias directas (sin Jinja2)
    - Config puede reemplazar `baseURL` si es necesario

17. Modificar `scaffold_service.py`:
    - Agregar método para renderizar test templates
    - Registrar templates en plan
    - Ejecutar solo si `--include-tests` flag presente

## Step by Step Tasks

### Task 1: Create conftest.py with SQLite Fixtures
- Create `adws/adw_tests/__init__.py`
- Create `adws/adw_tests/conftest.py`
- Implement `pytest` fixture for in-memory SQLite database
- Implement factory fixtures for test entities
- Initialize schema on test session startup
- Clean up after each test (rollback)

### Task 2: Create test_database.py
- Test schema validation (tables, columns, types exist)
- Test CRUD operations for each table
- Test foreign key constraints
- Test indexes exist and work
- Test transaction isolation
- Minimum 15 test cases

### Task 3: Create test_workflows.py
- Test ADW workflow state machine
- Test logging operations
- Test error handling paths
- Test async operations (if applicable)
- Minimum 10 test cases

### Task 4: Create test_agent_sdk.py
- Test Agent SDK initialization
- Test agent creation/execution with mocks
- Test message routing
- Test error propagation
- Minimum 8 test cases

### Task 5: Create test_websockets.py
- Test WebSocket server initialization
- Test message streaming
- Test connection lifecycle
- Test reconnection logic
- Minimum 10 test cases

### Task 6: Create pytest.ini
- Configure testpaths to `adws/adw_tests/`
- Set asyncio_mode to `auto`
- Set log level to DEBUG
- Configure SQLite temp directory

### Task 7: Create playwright.config.ts
- Set baseURL to `http://localhost:3000`
- Configure Chromium browser
- Set viewport to 1280x720
- Enable screenshots/videos on failure
- Set timeout to 30000ms
- Configure output directory

### Task 8-13: Create 6 Playwright Test Files
Each test file:
- Verify page loads without errors
- Verify UI elements present
- Perform user action
- Validate result/state change
- Include error assertions
- Use `test.expect()` for assertions

### Task 14: Copy to Templates
- Create `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_tests/`
- Copy all conftest.py, test_*.py, pytest.ini files
- Create `tac_bootstrap_cli/tac_bootstrap/templates/apps/orchestrator_3_stream/`
- Copy playwright.config.ts and all test files
- No Jinja2 variables (static copies)

### Task 15: Modify scaffold_service.py
- Add test template registration
- Ensure test files copied during project generation
- Document --include-tests flag in CLI help

### Task 16: Run Validation Commands
- Execute: `cd adws && uv run pytest adw_tests/ -v --cov --cov-report=term`
- Verify: All pytest tests pass (4 files, 43+ cases)
- Execute: `cd apps/orchestrator_3_stream && npx playwright test --headed`
- Verify: All 6 E2E tests pass
- Check: Coverage ≥ 80%
- Check: No warnings/errors in output

## Testing Strategy

### Unit Tests (pytest)
- **Scope**: Database operations, workflow state, SDK integration, WebSocket messaging
- **Fixtures**: SQLite in-memory, factories for test data, mock external services
- **Coverage targets**:
  - database.py: 85%+
  - workflows.py: 80%+
  - agent_sdk.py: 80%+
  - websockets.py: 75%+

### E2E Tests (Playwright)
- **Scope**: User workflows end-to-end (create agent → execute → monitor logs → persist)
- **Environment**: localhost:3000 (orchestrator dev server running)
- **Coverage**: 6 critical user journeys
- **Assertions**: Page elements visible, state transitions occur, no JS errors

### Edge Cases
- Database: Concurrent writes, transaction rollback, constraint violations
- Workflows: State machine invalid transitions, missing dependencies
- SDK: Malformed API responses, network timeouts, rate limiting
- WebSockets: Connection loss, message ordering, message loss recovery
- UI: Page reload during execution, rapid interactions, simultaneous operations

## Acceptance Criteria

1. **Base Tests Created**:
   - ✓ `adws/adw_tests/conftest.py` exists with ≥5 fixtures
   - ✓ `adws/adw_tests/test_database.py` with ≥15 tests
   - ✓ `adws/adw_tests/test_workflows.py` with ≥10 tests
   - ✓ `adws/adw_tests/test_agent_sdk.py` with ≥8 tests
   - ✓ `adws/adw_tests/test_websockets.py` with ≥10 tests
   - ✓ `adws/adw_tests/pytest.ini` configured

2. **Playwright Tests Created**:
   - ✓ `apps/orchestrator_3_stream/playwright.config.ts` exists
   - ✓ 6 test files created (agent-creation, execution, log-streaming, websocket, error, persistence)
   - ✓ Each test has ≥3 assertions

3. **Tests Passing**:
   - ✓ `pytest adws/adw_tests/ -v` → all tests PASS
   - ✓ `playwright test` → all tests PASS
   - ✓ Coverage report: ≥80% overall
   - ✓ No console errors/warnings

4. **Templates Synchronized**:
   - ✓ Test templates exist in CLI templates/ directory
   - ✓ scaffold_service.py registers test templates
   - ✓ New projects generated with `tac-bootstrap init` include tests

5. **Documentation**:
   - ✓ `adws/adw_tests/README.md` explains how to run tests locally
   - ✓ `apps/orchestrator_3_stream/playwright-tests/README.md` explains Playwright setup

## Validation Commands

All commands execute with zero failures/warnings:

```bash
# Unit tests
cd /Users/hernandoescobar/Documents/Celes/tac_bootstrap
uv run pytest adws/adw_tests/ -v --tb=short --cov=adws --cov-report=term-missing --cov-report=html

# Coverage must be ≥80%
uv run pytest adws/adw_tests/ --cov=adws --cov-report=term | grep "TOTAL" | awk '{print $NF}' | grep -E "^(100|99|98|97|96|95|94|93|92|91|90|89|88|87|86|85|84|83|82|81|80)%"

# E2E tests (requires orchestrator_3_stream running on localhost:3000)
cd apps/orchestrator_3_stream
npm install  # Ensure dependencies
npm run dev &  # Start dev server in background
cd playwright-tests
npx playwright install chromium
npx playwright test --reporter=list

# Type checking (optional but recommended)
cd adws/adw_tests
uv run mypy . --ignore-missing-imports

# Linting
uv run ruff check adws/adw_tests/
```

## Notes

### Dependencies
- **sqlite3**: Built-in Python module (no install needed)
- **aiosqlite**: Already in pyproject.toml (async SQLite)
- **pytest**: Already in pyproject.toml
- **pytest-asyncio**: Already in pyproject.toml
- **Playwright**: Install via `npx playwright install chromium` in orchestrator_3_stream

### Environment Setup
- **SQLite**: Tests use in-memory database (`:memory:`) by default
- **Orchestrator Dev Server**: Playwright tests require `npm run dev` running on `localhost:3000`
- **Database**: Schema auto-created in conftest.py on test session startup

### Handling Task Dependencies
- Task 7 (Database Models): conftest.py uses these models for fixtures
- Task 8 (Database Operations): test_database.py validates these operations
- Task 9 (ADW Workflows): test_workflows.py tests ADW execution using database ops
- Task 11 (Agent SDK): test_agent_sdk.py mocks SDK calls (real SDK must be installed)
- Task 12 (WebSockets): test_websockets.py mocks WebSocket server
- Task 13 (Orchestrator Frontend): Playwright tests validate frontend behavior

### Template Strategy
- Test files are **static copies** (no Jinja2 templating needed)
- Copied as-is to `tac_bootstrap_cli/tac_bootstrap/templates/`
- scaffold_service.py copies entire `adws/adw_tests/` and `playwright-tests/` directories
- New projects auto-include tests when generated

### Common Pitfalls
- **SQLite pragma**: Must disable `PRAGMA foreign_keys` during teardown to clean tables
- **Async tests**: Use `pytest-asyncio` with `asyncio_mode = "auto"` in pytest.ini
- **Playwright state**: Each test must be independent; avoid shared state between tests
- **WebSocket mocks**: Use `pytest-asyncio` + mock WebSocket server library
- **Path issues**: Use absolute imports from package root (e.g., `from adws.domain import ...`)

### Future Improvements (v0.9.0)
- Add pytest fixtures for database transactions/rollback
- Add Playwright visual regression testing
- Add performance benchmarks
- Add load testing (k6/locust)
- Migrate pytest from SQLite to PostgreSQL testing setup

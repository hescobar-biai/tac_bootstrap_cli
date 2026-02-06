# TAC-14: Codebase Singularity & Orchestrator - Complete Guide

**Version**: 0.8.0
**Baseline**: TAC-13 (v0.7.x)
**Database**: SQLite (zero-configuration)

## Introduction

TAC-14 is the culmination of the Tactical Agentic Coding curriculum. It elevates tac_bootstrap from **Class 1 (Agentic Layer)** to **Class 2 (Outloop Systems)** and **Class 3 (Orchestrator Agent)**, incorporating a Skills System, Agent SDK, SQLite-backed persistence, WebSockets for real-time event streaming, and a full orchestrator web application.

The core thesis of TAC-14 is the **Codebase Singularity**: the point at which your agents can run your codebase better than you can. At this stage, nothing ships to production without agents, you trust agent teams more than yourself, and engineering becomes orchestration rather than execution.

TAC-14 adds 12 new components across 3 classes to bring your agentic layer to this threshold.

---

## Architecture Overview (Class 1-3)

### Class Progression

| Class | Grade | Name | Key Capability |
|-------|-------|------|----------------|
| **1** | 7 | Agentic Layer | Skills System, Agent Experts, Progressive Disclosure |
| **2** | 1-2 | Outloop Systems | Custom Agents, Orchestrator Commands, Agent SDK, Programmatic Control |
| **3** | 1-3 | Orchestrator Agent | SQLite Database, WebSockets, Real-time UI, Zero-Touch Engineering |

### Mermaid Architecture Diagram

```mermaid
flowchart TB
    subgraph CLASS1["Class 1: Agentic Layer (Grade 7)"]
        direction TB
        SK[Skills System<br/>.claude/skills/]
        CM[25+ Slash Commands<br/>.claude/commands/]
        HK[Hook System<br/>.claude/hooks/]
        PR[Prime Prompt<br/>CLAUDE.md]
        SK --> CM
        CM --> HK
        HK --> PR
    end

    subgraph CLASS2["Class 2: Outloop Systems"]
        direction TB
        AG[7 Custom Agents<br/>.claude/agents/]
        OC[5 Orchestrator Commands<br/>.claude/commands/orch_*]
        SDK[Agent SDK<br/>adw_agent_sdk.py]
        AG --> OC
        OC --> SDK
    end

    subgraph CLASS3["Class 3: Orchestrator Agent"]
        direction TB
        DB[(SQLite Database<br/>orchestrator.db)]
        WS[WebSocket Server<br/>adw_websockets.py]
        WF[Consolidated Workflows<br/>adw_workflows/]
        BE[FastAPI Backend<br/>apps/orchestrator_3_stream/backend/]
        FE[Vue 3 Frontend<br/>apps/orchestrator_3_stream/frontend/]
        DB --> WF
        WF --> WS
        WS --> BE
        BE --> FE
    end

    CLASS1 -->|"Out of the terminal"| CLASS2
    CLASS2 -->|"Orchestrated agentic coding"| CLASS3
```

---

## Component Details

TAC-14 introduces 12 components organized across the three classes.

| # | Component | Class | Location |
|---|-----------|-------|----------|
| 1 | Skills System | 1 | `.claude/skills/` |
| 2 | Agent Definitions | 2 | `.claude/agents/` |
| 3 | Orchestrator Commands | 2 | `.claude/commands/orch_*` |
| 4 | Agent SDK | 2 | `adws/adw_modules/adw_agent_sdk.py` |
| 5 | Database Schema | 3 | `adws/schema/schema_orchestrator.sql` |
| 6 | Database Models | 3 | `adws/adw_modules/orch_database_models.py` |
| 7 | Database Operations | 3 | `adws/adw_modules/adw_database.py` |
| 8 | Database Logging | 3 | `adws/adw_modules/adw_logging.py` |
| 9 | Consolidated Workflows | 3 | `adws/adw_workflows/` |
| 10 | WebSockets | 3 | `adws/adw_modules/adw_websockets.py` |
| 11 | Orchestrator Backend | 3 | `apps/orchestrator_3_stream/backend/` |
| 12 | Orchestrator Frontend | 3 | `apps/orchestrator_3_stream/frontend/` |

---

### Component 1: Skills System (Class 1 Grade 7)

**Description**: The Skills System introduces progressive disclosure for agent expertise. Skills are markdown files with YAML frontmatter that Claude loads on-demand when relevant, keeping the context window efficient. The meta-skill is a self-referential skill that teaches agents how to create new skills.

**Key Files**:
- `.claude/skills/meta-skill/SKILL.md` -- Main skill definition with YAML frontmatter
- `.claude/skills/meta-skill/docs/claude_code_agent_skills.md` -- Complete skills guide
- `.claude/skills/meta-skill/docs/claude_code_agent_skills_overview.md` -- Architecture overview
- `.claude/skills/meta-skill/docs/blog_equipping_agents_with_skills.md` -- Design principles

**Progressive Disclosure (3 Levels)**:
1. **Metadata** (always loaded): `name` and `description` in YAML frontmatter
2. **Instructions** (loaded when triggered): Main body of SKILL.md
3. **Resources** (loaded as needed): Additional docs, scripts, templates

**Usage**:
```yaml
# .claude/skills/meta-skill/SKILL.md
---
name: creating-new-skills
description: Creates new Agent Skills for AI Agents following best practices.
---

# Purpose
Create new Agent Skills by following a structured workflow...
```

**Dependencies**: None (native Claude Code feature).

---

### Component 2: Agent Definitions (Class 2)

**Description**: Seven specialized agent definitions configured as markdown files with YAML frontmatter. Each agent follows the principle of "one agent, one prompt, one purpose" (Tactic 6) and can be invoked as sub-agents by orchestrator commands.

**Key Files** (`.claude/agents/`):

| Agent | Purpose | Model |
|-------|---------|-------|
| `build-agent.md` | Single-file implementation specialist | opus |
| `planner.md` | Implementation planning and task decomposition | sonnet |
| `scout-report-suggest.md` | Deep codebase exploration and analysis | sonnet |
| `scout-report-suggest-fast.md` | Quick codebase scanning | haiku |
| `playwright-validator.md` | E2E test validation with Playwright | sonnet |
| `meta-agent.md` | Agent creation and improvement | opus |
| `docs-scraper.md` | Documentation fetching and summarization | sonnet |

**Usage** (invoked by orchestrator commands via `Task` tool):
```yaml
# .claude/agents/build-agent.md
---
name: build-agent
description: Specialist for implementing one specific file based on detailed instructions.
tools: Write, Read, Edit, Grep, Glob, Bash, TodoWrite
model: opus
color: blue
---

# build-agent
## Purpose
You are a specialized file implementation engineer...
```

**Dependencies**: Claude Code agent system (built-in sub-agent support).

---

### Component 3: Orchestrator Commands (Class 2)

**Description**: Five orchestrator slash commands that coordinate multi-agent workflows. These commands use the `Task` tool to spawn sub-agents (from Component 2) and coordinate their execution through sequential or parallel phases.

**Key Files** (`.claude/commands/`):

| Command | Purpose |
|---------|---------|
| `orch_plan_w_scouts_build_review.md` | Full pipeline: scout, plan, build, review |
| `orch_scout_and_build.md` | Discover files, then build |
| `orch_one_shot_agent.md` | Single-agent task execution |
| `build_in_parallel.md` | Parallel file implementation |
| `parallel_subagents.md` | Coordinate multiple sub-agents concurrently |

**Usage**:
```bash
# In Claude Code terminal:
/orch_plan_w_scouts_build_review "Implement user authentication with JWT"
/orch_scout_and_build "Add dark mode toggle to settings page"
/build_in_parallel "Create the 3 API endpoint files from this plan: ..."
```

**Dependencies**: Component 2 (Agent Definitions).

---

### Component 4: Agent SDK (Class 2)

**Description**: A comprehensive Pydantic-based abstraction layer for the Claude Agent SDK. Provides type-safe models for configuring and controlling agents programmatically, including enums for models, hooks, permissions, and complete message handling.

**Key File**: `adws/adw_modules/adw_agent_sdk.py`

**Core Enums**:
- `ModelName` -- Available Claude models (OPUS, SONNET, HAIKU and versioned variants)
- `SettingSource` -- Settings loading sources (USER, PROJECT)
- `HookEventName` -- Hook event types (PreToolUse, PostToolUse, Stop, etc.)
- `PermissionDecision` -- Permission flow decisions (ALLOW, DENY, ASK)
- `BuiltInTool` -- All built-in tools (Bash, Read, Write, Grep, Glob, etc.)

**Core Models**:
- `QueryOptions` -- Complete SDK query configuration (model, tools, hooks, permissions)
- `QueryInput` / `QueryOutput` -- Input/output wrappers for SDK queries
- `TokenUsage` / `UsageAccumulator` -- Cost tracking and deduplication
- `HooksConfig` / `HookMatcher` -- Hook event configuration
- `MessageHandlers` -- Callbacks for streaming message handling
- `AdhocPrompt` -- Simple one-off query wrapper
- `SystemPromptConfig` -- Three-mode system prompt control (DEFAULT, APPEND, OVERWRITE)

**Usage**:
```python
from adw_agent_sdk import (
    QueryInput, QueryOptions, ModelName,
    query_to_completion, AdhocPrompt, quick_prompt
)

# Full query with options
result = await query_to_completion(
    QueryInput(
        prompt="Analyze this codebase",
        options=QueryOptions(
            model=ModelName.OPUS,
            allowed_tools=["Read", "Glob", "Grep"],
            max_turns=20,
        ),
    )
)

# Quick one-off prompt
answer = await quick_prompt(AdhocPrompt(
    prompt="What is the main entry point?",
    model=ModelName.HAIKU,
))
```

**Dependencies**: `pydantic>=2.0`, `claude-agent-sdk>=0.1.18`, `rich>=13.0`

---

### Component 5: Database Schema (Class 3)

**Description**: SQLite schema defining 5 tables for orchestrator state persistence. Uses WAL mode for concurrent reads, TEXT-based UUIDs and timestamps, and includes performance indexes and auto-update triggers. Zero-configuration -- auto-initializes on first access.

**Key File**: `adws/schema/schema_orchestrator.sql`

**Tables**:

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `orchestrator_agents` | Agent type definitions (templates) | id, name, agent_type, capabilities, default_model |
| `agents` | Runtime agent instances | id, orchestrator_agent_id, session_id, status, cost_usd |
| `prompts` | Individual prompt executions | id, agent_id, prompt_type, prompt_text, tokens_input/output |
| `agent_logs` | Agent lifecycle events (append-only) | id, agent_id, log_level, log_type, message, details |
| `system_logs` | System-wide events (append-only) | id, log_level, component, message, details |

**Schema snippet**:
```sql
-- Enable WAL mode for concurrent reads
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS orchestrator_agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    agent_type TEXT NOT NULL,
    capabilities TEXT,
    default_model TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),
    CHECK (agent_type IN ('planner', 'builder', 'reviewer',
                          'tester', 'orchestrator', 'utility'))
);

CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    orchestrator_agent_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    parent_agent_id TEXT,
    status TEXT NOT NULL DEFAULT 'initializing',
    context TEXT,
    config TEXT,
    started_at TEXT NOT NULL DEFAULT (datetime('now')),
    completed_at TEXT,
    cost_usd REAL DEFAULT 0.0,
    error_message TEXT,
    FOREIGN KEY (orchestrator_agent_id) REFERENCES orchestrator_agents(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_agent_id) REFERENCES agents(id) ON DELETE SET NULL,
    CHECK (status IN ('initializing', 'planning', 'executing',
                      'reviewing', 'completed', 'failed', 'cancelled'))
);
```

**Dependencies**: SQLite 3.35+ (included with Python 3.10+).

---

### Component 6: Database Models (Class 3)

**Description**: Five pure Pydantic models mapping to the SQLite schema. These are domain models with validation (UUID format, status enums, JSON serializability) but NO database operations. They handle SQLite type mappings: UUIDs as TEXT, datetimes as ISO 8601 TEXT, JSON metadata as TEXT.

**Key File**: `adws/adw_modules/orch_database_models.py`

**Models**:
- `OrchestratorAgent` -- Agent definitions (name, description, status)
- `Agent` -- Runtime instances (orchestrator_agent_id, session_id, status)
- `Prompt` -- Prompt executions (content, response, tokens, cost)
- `AgentLog` -- Agent event logs (log_type, message, metadata as JSON)
- `SystemLog` -- System event logs (log_level, source, metadata as JSON)

**Usage**:
```python
from orch_database_models import OrchestratorAgent, Agent
import uuid

agent_def = OrchestratorAgent(
    id=str(uuid.uuid4()),
    name="scout-report-suggest",
    description="Scouts codebase and suggests fixes",
    status="active"
)

# Serialize to JSON (ISO 8601 timestamps)
json_data = agent_def.model_dump_json()
```

**Dependencies**: `pydantic>=2.0`

---

### Component 7: Database Operations (Class 3)

**Description**: Async SQLite database manager providing CRUD operations for all 5 tables. Implements zero-configuration philosophy with automatic schema initialization, WAL mode for concurrency, and an async context manager pattern for clean lifecycle management. Includes graceful error handling where logging failures never crash orchestrator agents.

**Key File**: `adws/adw_modules/adw_database.py`

**Key Class**: `DatabaseManager`
- `connect()` / `close()` -- Connection lifecycle with WAL mode
- `async with DatabaseManager("orchestrator.db") as db:` -- Context manager
- `create_orchestrator_agent()` / `get_*` / `list_*` / `update_*` / `delete_*` -- Full CRUD
- `log_agent_event()` -- High-level logging with graceful error handling
- `cleanup_old_logs(days=30)` -- Manual log retention

**Usage**:
```python
from adw_database import DatabaseManager

async with DatabaseManager("orchestrator.db") as db:
    # Create agent definition
    agent_id = await db.create_orchestrator_agent(
        name="scout-report-suggest",
        description="Scouts codebase and suggests fixes",
        agent_type="utility"
    )

    # Create runtime instance
    runtime_id = await db.create_agent(
        orchestrator_agent_id=agent_id,
        session_id="550e8400-e29b-41d4-a716-446655440000"
    )

    # Log event (never raises -- graceful degradation)
    await db.log_agent_event(
        agent_id=runtime_id,
        log_type="milestone",
        message="Started code analysis",
        metadata={"files_queued": 42}
    )
```

**Dependencies**: `aiosqlite>=0.19.0`

---

### Component 8: Database Logging (Class 3)

**Description**: Structured event logging to the SQLite database through the `DatabaseManager.log_agent_event()` and `DatabaseManager.create_agent_log()` / `create_system_log()` methods. Logging is designed to be resilient -- failures are caught and written to stderr so they never crash the orchestrator workflow.

**Key File**: `adws/adw_modules/adw_database.py` (integrated into DatabaseManager)

**Log Types** (agent_logs):
- `state_change` -- Agent status transitions
- `milestone` -- Workflow phase completions
- `error` -- Error events
- `performance` -- Performance metrics
- `tool_call` -- Tool invocations
- `cost_update` -- Cost tracking updates

**Log Levels** (system_logs):
- `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

**Query Methods**:
```python
# Query by agent and type
errors = await db.get_agent_logs_by_type(agent_id, "error", limit=50)

# Query across all agents
all_errors = await db.get_logs_by_type("error", limit=200)

# Recent activity dashboard
recent = await db.get_recent_logs(limit=100)

# Manual cleanup
deleted = await db.cleanup_old_logs(days=90)
```

**Dependencies**: `aiosqlite>=0.19.0` (shared with Component 7).

---

### Component 9: Consolidated Workflows (Class 3)

**Description**: Three database-backed workflows that integrate the Agent SDK, SQLite persistence, and structured logging. These represent the next evolution beyond file-based ADWs (adw_state.json), providing persistent state, cost tracking, and observability.

**Key Files** (`adws/adw_workflows/`):

| Workflow | Phases | Description |
|----------|--------|-------------|
| `adw_plan_build.py` | Plan, Build | Two-phase: plan then execute |
| `adw_plan_build_review.py` | Plan, Build, Review | Three-phase with quality review |
| `adw_plan_build_review_fix.py` | Plan, Build, Review, Fix | Four-phase with auto-fix on review failures |

**Architecture**:
```
Workflow --> Agent SDK --> Claude Agent
    |
    +--> DatabaseManager --> SQLite (state, logs, costs)
    |
    +--> WebSocket Manager --> Connected Clients (real-time events)
```

**Dependencies**: Components 4 (Agent SDK), 7 (Database), 8 (Logging), 10 (WebSockets).

---

### Component 10: WebSockets (Class 3)

**Description**: Standalone async WebSocket server for broadcasting real-time agent lifecycle events to monitoring clients. Maintains an in-memory connection pool with keepalive ping/pong, authentication tokens, and graceful degradation where broadcast failures never crash workflows.

**Key File**: `adws/adw_modules/adw_websockets.py`

**Core Classes and Functions**:
- `WebSocketEvent` -- Event dataclass (event_type, agent_id, message, metadata, timestamp)
- `ConnectionManager` -- Connection pool with max 100 clients, 3-strike disconnect policy
- `start_server()` / `stop_server()` -- Server lifecycle
- `broadcast_agent_event()` -- Send events to all connected clients
- `map_log_to_event()` -- Convert database log entries to WebSocket events

**Configuration**:
- Max connections: 100
- Idle timeout: 60 seconds
- Ping interval: 30 seconds
- Pong timeout: 10 seconds
- Max strikes before disconnect: 3

**Usage**:
```python
from adw_websockets import start_server, stop_server, broadcast_agent_event

# Start server
server_task, manager = await start_server(
    host="127.0.0.1", port=8765, token="secret123"
)

# Broadcast during workflow
await broadcast_agent_event(
    manager=manager,
    agent_id="550e8400-...",
    event_type="agent_started",
    message="Scout agent started codebase exploration",
    metadata={"files_queued": 42}
)

# Stop server
await stop_server(server_task)
```

**Dependencies**: `websockets>=12.0`

---

### Component 11: Orchestrator Backend (Class 3)

**Description**: FastAPI REST API and WebSocket endpoint serving as the backend for the orchestrator web application. Integrates with the DatabaseManager for state persistence and the WebSocket module for real-time event streaming. Auto-initializes the SQLite database on startup.

**Key Files** (`apps/orchestrator_3_stream/backend/`):
- `main.py` -- FastAPI app with lifespan manager, REST endpoints, WebSocket endpoint
- `modules/` -- Business logic modules
- `prompts/` -- Prompt templates for orchestrator workflows
- `.env.sample` -- Environment variable template
- `pyproject.toml` -- Python dependencies

**REST Endpoints**:
- `GET /api/agents` -- List all orchestrator agent definitions
- `GET /api/agents/{id}` -- Get agent definition by ID
- `POST /api/agents` -- Create agent definition
- `GET /api/sessions` -- List workflow sessions
- `GET /api/sessions/{id}/logs` -- Get logs for a session
- `GET /api/prompts/{agent_id}` -- Get prompts for an agent
- `POST /api/workflows/start` -- Start a new workflow

**WebSocket Endpoint**:
- `WS /ws` -- Real-time event stream (connects to ConnectionManager)

**Usage**:
```bash
# Start backend server
cd apps/orchestrator_3_stream/backend
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Dependencies**: `fastapi`, `uvicorn`, `aiosqlite>=0.19.0`, `websockets>=12.0`

---

### Component 12: Orchestrator Frontend (Class 3)

**Description**: Vue 3 + TypeScript single-page application providing a swimlane visualization of agent workflows. Connects to the backend via REST API and WebSocket for real-time updates. Includes a command palette, keyboard shortcuts, and responsive task cards.

**Key Files** (`apps/orchestrator_3_stream/frontend/`):

| File/Directory | Purpose |
|----------------|---------|
| `src/App.vue` | Root component |
| `src/components/SwimlaneBoard.vue` | Swimlane layout with agent lanes |
| `src/components/AgentLane.vue` | Individual agent lane |
| `src/components/TaskCard.vue` | Task/prompt card visualization |
| `src/components/CommandPalette.vue` | Cmd+K command palette |
| `src/composables/use-keyboard.ts` | Keyboard shortcut handling |
| `src/composables/use-command-palette.ts` | Command palette logic |
| `src/services/api-client.ts` | REST API client |
| `src/services/ws-client.ts` | WebSocket client |
| `src/stores/agent-store.ts` | Pinia store for agent state |
| `src/stores/ws-store.ts` | Pinia store for WebSocket state |
| `src/stores/ui-store.ts` | Pinia store for UI state |
| `src/types/models.ts` | TypeScript type definitions |

**Usage**:
```bash
# Install dependencies and start dev server
cd apps/orchestrator_3_stream/frontend
npm install
npm run dev
# Opens at http://localhost:5173
```

**Dependencies**: Vue 3, TypeScript, Vite, Pinia, Tailwind CSS

---

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant CLI as Claude CLI / ADW
    participant SDK as Agent SDK
    participant DB as SQLite Database
    participant WS as WebSocket Server
    participant FE as Vue Frontend

    User->>CLI: Start workflow
    CLI->>SDK: QueryInput (prompt, options)
    SDK->>SDK: Execute agent query
    SDK-->>DB: Log agent_started event
    SDK-->>WS: Broadcast agent_started
    WS-->>FE: WebSocket event (real-time)
    FE->>FE: Update swimlane UI

    loop For each prompt in workflow
        SDK->>SDK: Send prompt to Claude
        SDK-->>DB: Log prompt execution
        SDK-->>WS: Broadcast prompt_sent
        WS-->>FE: WebSocket event
        SDK->>SDK: Receive response
        SDK-->>DB: Update prompt (response, tokens, cost)
        SDK-->>WS: Broadcast prompt_completed
        WS-->>FE: WebSocket event
    end

    SDK-->>DB: Log agent_completed
    SDK-->>WS: Broadcast agent_completed
    WS-->>FE: WebSocket event
    SDK-->>CLI: QueryOutput (result, usage)
    CLI-->>User: Workflow complete
```

---

## Database Schema ER Diagram

```mermaid
erDiagram
    orchestrator_agents {
        TEXT id PK "UUID"
        TEXT name UK "Unique agent name"
        TEXT description
        TEXT agent_type "planner|builder|reviewer|tester|orchestrator|utility"
        TEXT capabilities
        TEXT default_model
        TEXT created_at "ISO 8601"
        TEXT updated_at "ISO 8601 (auto-trigger)"
    }

    agents {
        TEXT id PK "UUID"
        TEXT orchestrator_agent_id FK
        TEXT session_id "UUID"
        TEXT parent_agent_id FK "nullable self-ref"
        TEXT status "initializing|planning|executing|reviewing|completed|failed|cancelled"
        TEXT context "JSON as TEXT"
        TEXT config "JSON as TEXT"
        TEXT started_at "ISO 8601"
        TEXT completed_at "ISO 8601 nullable"
        REAL cost_usd "default 0.0"
        TEXT error_message
    }

    prompts {
        TEXT id PK "UUID"
        TEXT agent_id FK
        TEXT prompt_type "adw|command|followup|correction|tool_call"
        TEXT prompt_name
        TEXT prompt_text
        TEXT response_text
        TEXT status "pending|streaming|completed|failed|cancelled"
        TEXT model_used
        INTEGER tokens_input "default 0"
        INTEGER tokens_output "default 0"
        REAL cost_usd "default 0.0"
        INTEGER latency_ms
        TEXT created_at "ISO 8601"
        TEXT completed_at "ISO 8601 nullable"
        TEXT error_message
    }

    agent_logs {
        INTEGER id PK "AUTOINCREMENT"
        TEXT agent_id FK
        TEXT log_level "DEBUG|INFO|WARNING|ERROR|CRITICAL"
        TEXT log_type "state_change|milestone|error|performance|tool_call|cost_update"
        TEXT message
        TEXT details "JSON as TEXT"
        TEXT created_at "ISO 8601"
    }

    system_logs {
        INTEGER id PK "AUTOINCREMENT"
        TEXT log_level "DEBUG|INFO|WARNING|ERROR|CRITICAL"
        TEXT component
        TEXT message
        TEXT details "JSON as TEXT"
        TEXT created_at "ISO 8601"
    }

    orchestrator_agents ||--o{ agents : "defines"
    agents ||--o{ prompts : "executes"
    agents ||--o{ agent_logs : "generates"
    agents ||--o{ agents : "parent_agent_id"
```

---

## Migration Guide (TAC-13 to TAC-14)

### What's New in TAC-14

| Feature | TAC-13 | TAC-14 |
|---------|--------|--------|
| Skills System | Not available | `.claude/skills/` with progressive disclosure |
| Custom Agents | Basic sub-agents | 7 specialized agent definitions with YAML frontmatter |
| Orchestrator Commands | Manual command chaining | 5 orchestrator commands coordinating multi-agent workflows |
| Agent SDK | Direct CLI invocation | Pydantic-typed SDK with hooks, permissions, message handlers |
| State Persistence | File-based (`adw_state.json`) | SQLite database with 5 tables |
| Real-time Events | None | WebSocket server with event broadcasting |
| Consolidated Workflows | Isolated ADW scripts | Database-backed workflows with cost tracking |
| Web UI | None | Vue 3 swimlane dashboard with real-time updates |

### Breaking Changes

**None.** TAC-14 is fully backward compatible with TAC-13.

- All existing file-based ADWs (`adw_state.json`) continue to work unchanged
- Existing slash commands remain functional
- The `adw_*_iso.py` workflows are not modified
- No configuration changes are required

### New Opt-In Features

All TAC-14 Class 3 features are **opt-in** via the `--with-orchestrator` flag:

```bash
# Default (no orchestrator) -- works exactly like TAC-13
tac-bootstrap init my-app

# With orchestrator -- adds Class 3 components
tac-bootstrap init my-app --with-orchestrator

# Add orchestrator to existing project
tac-bootstrap add-agentic --with-orchestrator
```

Class 1 and Class 2 components (Skills, Agents, Orchestrator Commands, Agent SDK) are always included.

### Migration Steps

1. **Upgrade TAC Bootstrap CLI**:
   ```bash
   git pull origin main
   uv tool install .
   ```

2. **For existing projects** (add TAC-14 features):
   ```bash
   cd your-project
   tac-bootstrap add-agentic --with-orchestrator
   ```

3. **Verify installation**:
   ```bash
   # Check skills directory exists
   ls .claude/skills/meta-skill/SKILL.md

   # Check agent definitions
   ls .claude/agents/

   # Check orchestrator commands
   ls .claude/commands/orch_*

   # If --with-orchestrator was used:
   ls adws/schema/schema_orchestrator.sql
   ls apps/orchestrator_3_stream/
   ```

4. **Initialize the database** (if using orchestrator):
   ```bash
   # The database auto-initializes on first use, but you can also:
   sqlite3 orchestrator.db < adws/schema/schema_orchestrator.sql
   ```

---

## Configuration Reference

### OrchestratorConfig (in config.yml)

```yaml
orchestrator:
  enabled: true                              # Enable orchestrator components
  api_base_url: "http://localhost:8000"       # FastAPI backend URL
  ws_base_url: "ws://localhost:8000"          # WebSocket connection URL
  frontend_port: 5173                         # Vue dev server port
  websocket_port: 8000                        # WebSocket server port
  database_url: "sqlite:///orchestrator.db"   # SQLite database path
  polling_interval: 5000                      # Fallback polling interval (ms)
```

### OrchestratorConfig Pydantic Model

```python
class OrchestratorConfig(BaseModel):
    enabled: bool = False           # Opt-in (default: disabled)
    api_base_url: str = "http://localhost:8000"
    ws_base_url: str = "ws://localhost:8000"
    frontend_port: int = 5173       # Range: 1024-65535
    websocket_port: int = 8000      # Range: 1024-65535
    database_url: str = "sqlite:///orchestrator.db"
    polling_interval: int = 5000    # Range: 100-60000 ms
```

### Environment Variables (.env.sample)

```bash
# Database
DATABASE_PATH=orchestrator.db

# WebSocket
WEBSOCKET_PORT=8765

# Web UI
WEB_UI_PORT=5173
```

---

## Quick Start

### Option A: With Orchestrator (full TAC-14)

```bash
# 1. Create new project with orchestrator
tac-bootstrap init my-app --with-orchestrator
cd my-app

# 2. Initialize database (auto-initializes, but explicit is fine)
sqlite3 orchestrator.db < adws/schema/schema_orchestrator.sql

# 3. Start backend
cd apps/orchestrator_3_stream/backend
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

# 4. Start frontend
cd ../frontend
npm install
npm run dev &

# 5. Open dashboard
open http://localhost:5173

# 6. Use orchestrator commands in Claude Code
# /orch_plan_w_scouts_build_review "Add user authentication"
```

### Option B: Without Orchestrator (default)

```bash
# 1. Create new project (no orchestrator)
tac-bootstrap init my-app
cd my-app

# 2. Use skills, agents, and orchestrator commands immediately
# /orch_scout_and_build "Implement REST API for users"

# 3. Use file-based ADWs as before
uv run adws/adw_sdlc_zte_iso.py --issue 42
```

### Running Tests

```bash
# Run all pytest tests
uv run pytest

# Run ADW module tests specifically
uv run pytest adws/adw_tests/

# Run Playwright E2E tests (requires backend + frontend running)
cd apps/orchestrator_3_stream
npx playwright test
```

---

## Troubleshooting

### Database Issues

**Problem**: `FileNotFoundError: Schema file not found`
**Cause**: The DatabaseManager looks for `schema_orchestrator.sql` relative to its own location.
**Fix**: Ensure `adws/schema/schema_orchestrator.sql` exists. Run:
```bash
ls adws/schema/schema_orchestrator.sql
```
If missing, re-run `tac-bootstrap add-agentic --with-orchestrator`.

---

**Problem**: `aiosqlite.OperationalError: database is locked`
**Cause**: Multiple writers attempting concurrent writes to SQLite.
**Fix**: SQLite supports one writer at a time. WAL mode is enabled for concurrent reads. Ensure only one workflow writes at a time, or switch to connection queueing. For production multi-writer needs, consider the PostgreSQL upgrade path in v0.9.0.

---

**Problem**: `ModuleNotFoundError: No module named 'aiosqlite'`
**Fix**: Install the dependency:
```bash
uv pip install aiosqlite>=0.19.0
```

---

### WebSocket Issues

**Problem**: WebSocket connection refused on port 8765
**Cause**: Server not running or port conflict.
**Fix**:
```bash
# Check if port is in use
lsof -i :8765

# Start WebSocket server (usually started by backend)
cd apps/orchestrator_3_stream/backend
uv run uvicorn main:app --port 8000
```

---

**Problem**: WebSocket authentication failed
**Cause**: Token mismatch between client and server.
**Fix**: Ensure the client connects with the correct token:
```
ws://localhost:8765?token=your_secret_token
```

---

### Frontend Issues

**Problem**: Frontend shows "WebSocket disconnected"
**Cause**: Backend server not running.
**Fix**: Start the backend first:
```bash
cd apps/orchestrator_3_stream/backend
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

**Problem**: `npm install` fails in frontend
**Fix**: Ensure Node.js 18+ is installed:
```bash
node --version  # Should be 18+
npm install
```

---

### Agent SDK Issues

**Problem**: `ImportError: No module named 'claude_agent_sdk'`
**Cause**: Claude Agent SDK not installed.
**Fix**:
```bash
uv pip install claude-agent-sdk>=0.1.18
```

---

**Problem**: Agent query times out
**Cause**: Model rate limiting or quota exhaustion.
**Fix**: The ADW system implements exponential backoff with model fallback (opus -> sonnet -> haiku). Wait for quota reset or reduce max_turns:
```python
QueryOptions(model=ModelName.SONNET, max_turns=10)
```

---

### Skills System Issues

**Problem**: Skill not being loaded by Claude
**Cause**: YAML frontmatter missing or malformed.
**Fix**: Ensure SKILL.md has valid frontmatter:
```yaml
---
name: my-skill-name
description: Brief description of what this skill does.
---
```

---

**Problem**: Skill description too long, consuming too many tokens
**Fix**: Keep the `description` field in frontmatter concise (one sentence). Move detailed instructions to the body of SKILL.md (Level 2 -- loaded only when triggered).

---

### General Issues

**Problem**: `tac-bootstrap: command not found`
**Fix**:
```bash
uv tool install .
# Or use with uv run:
uv run tac-bootstrap --help
```

---

**Problem**: Tests failing after TAC-14 upgrade
**Cause**: New dependencies not installed.
**Fix**:
```bash
cd tac_bootstrap_cli
uv sync
uv run pytest
```

---

## File Reference

### Class 1 Files
```
.claude/skills/meta-skill/SKILL.md
.claude/skills/meta-skill/docs/claude_code_agent_skills.md
.claude/skills/meta-skill/docs/claude_code_agent_skills_overview.md
.claude/skills/meta-skill/docs/blog_equipping_agents_with_skills.md
```

### Class 2 Files
```
.claude/agents/build-agent.md
.claude/agents/planner.md
.claude/agents/scout-report-suggest.md
.claude/agents/scout-report-suggest-fast.md
.claude/agents/playwright-validator.md
.claude/agents/meta-agent.md
.claude/agents/docs-scraper.md
.claude/agents/research-docs-fetcher.md
.claude/commands/orch_plan_w_scouts_build_review.md
.claude/commands/orch_scout_and_build.md
.claude/commands/orch_one_shot_agent.md
.claude/commands/build_in_parallel.md
.claude/commands/parallel_subagents.md
adws/adw_modules/adw_agent_sdk.py
```

### Class 3 Files
```
adws/schema/schema_orchestrator.sql
adws/adw_modules/orch_database_models.py
adws/adw_modules/adw_database.py
adws/adw_modules/adw_websockets.py
adws/adw_workflows/adw_plan_build.py
adws/adw_workflows/adw_plan_build_review.py
adws/adw_workflows/adw_plan_build_review_fix.py
apps/orchestrator_3_stream/backend/main.py
apps/orchestrator_3_stream/frontend/src/App.vue
apps/orchestrator_3_stream/frontend/src/components/SwimlaneBoard.vue
apps/orchestrator_3_stream/frontend/src/components/AgentLane.vue
apps/orchestrator_3_stream/frontend/src/components/TaskCard.vue
apps/orchestrator_3_stream/frontend/src/components/CommandPalette.vue
apps/orchestrator_3_stream/frontend/src/services/api-client.ts
apps/orchestrator_3_stream/frontend/src/services/ws-client.ts
apps/orchestrator_3_stream/frontend/src/stores/agent-store.ts
apps/orchestrator_3_stream/frontend/src/stores/ws-store.ts
apps/orchestrator_3_stream/frontend/src/stores/ui-store.ts
apps/orchestrator_3_stream/frontend/src/types/models.ts
apps/orchestrator_3_stream/playwright-tests/app-loads.spec.ts
apps/orchestrator_3_stream/playwright-tests/command-palette.spec.ts
apps/orchestrator_3_stream/playwright-tests/websocket-status.spec.ts
apps/orchestrator_3_stream/playwright-tests/swimlane-board.spec.ts
apps/orchestrator_3_stream/playwright-tests/keyboard-navigation.spec.ts
apps/orchestrator_3_stream/playwright-tests/visual-styling.spec.ts
```

---

## Dependencies Summary

### Python
| Package | Version | Purpose |
|---------|---------|---------|
| `pydantic` | >=2.0 | Data models and validation |
| `claude-agent-sdk` | >=0.1.18 | Programmatic agent control |
| `aiosqlite` | >=0.19.0 | Async SQLite driver |
| `websockets` | >=12.0 | WebSocket server |
| `fastapi` | latest | REST API backend |
| `uvicorn` | latest | ASGI server |
| `rich` | >=13.0 | Terminal formatting |

### JavaScript/TypeScript
| Package | Version | Purpose |
|---------|---------|---------|
| `vue` | 3.x | Frontend framework |
| `typescript` | 5.x | Type safety |
| `vite` | latest | Build tool and dev server |
| `pinia` | latest | State management |
| `tailwindcss` | latest | Utility CSS |

---

## Future Upgrade Path

### SQLite to PostgreSQL (v0.9.0+)

The DatabaseManager provides the same interface regardless of backend. When you need multi-user concurrency, replication, or high-availability:

1. Create `PostgresDatabaseManager` implementing the same methods
2. Use a factory pattern to select backend based on config
3. Domain layer (models, repositories) remains unchanged
4. Pydantic models already handle serialization for both backends

**When to consider PostgreSQL**:
- Multiple concurrent users (>10)
- High log volume (>1M records)
- Need for replication or high availability
- Production deployment requirements

```bash
# Future migration (v0.9.0):
pgloader orchestrator.db postgresql://user:pass@localhost/orchestrator
```

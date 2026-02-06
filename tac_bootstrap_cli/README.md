# TAC Bootstrap

CLI to bootstrap Agentic Layer for Claude Code with TAC (Tactical Agentic Coding) patterns.

Transform any repository into an AI-assisted development environment in minutes.

## Features

- **Quick Setup**: Add complete agentic layer to any project in minutes
- **Auto-Detection**: Automatically detects language, framework, and package manager
- **Smart Defaults**: Sensible defaults based on your tech stack
- **25+ Slash Commands**: Comprehensive command library for development workflows
- **Hook System**: Automated actions for logging, validation, and context tracking
- **Sub-Agents**: Specialized AI agents for documentation, research, and expert tasks
- **ADW Workflows**: AI Developer Workflows for complete SDLC automation
- **Output Styles**: Token optimization with configurable response formats

## Documentation

| Document | Description |
|----------|-------------|
| [Commands](docs/commands.md) | Complete slash command reference |
| [Hooks](docs/hooks.md) | Hook system and automation |
| [Agents](docs/agents.md) | Sub-agents and expert pattern |
| [Output Styles](docs/output-styles.md) | Response format control |
| [Utilities](docs/utilities.md) | LLM and TTS utilities |

## Installation

### Global Install (Recommended)

```bash
git clone --branch v0.9.1 --depth 1 https://github.com/celes-app/tac-cli-dist.git
cd tac-cli-dist
make install-dev

export CLAUDE_CODE_PATH=$(which claude)
uv tool install .

# Works from any directory
tac-bootstrap --help
```

### Development Install

```bash
git clone --branch v0.9.1 --depth 1 https://github.com/celes-app/tac-cli-dist.git
cd tac-cli-dist
make install-dev

# Use with "uv run" in project directory
uv run tac-bootstrap --help
```

## Quick Start

### New Project

```bash
# Interactive wizard
tac-bootstrap init my-app

# With options
tac-bootstrap init my-api \
  --language python \
  --framework fastapi \
  --architecture ddd

# With orchestrator backend and frontend (TAC-14)
tac-bootstrap init my-app --with-orchestrator
```

### Existing Project

```bash
cd your-project
tac-bootstrap add-agentic

# Preview changes
tac-bootstrap add-agentic --dry-run

# Include orchestrator components (TAC-14)
tac-bootstrap add-agentic --with-orchestrator
```

## Generated Structure

```
project/
├── .claude/
│   ├── settings.json        # Claude Code configuration
│   ├── commands/            # 25+ slash commands
│   ├── hooks/               # Automation hooks
│   ├── agents/              # Sub-agent definitions
│   └── output-styles/       # Response format presets
├── adws/
│   ├── adw_modules/         # Shared workflow modules
│   ├── adw_triggers/        # Webhook and cron triggers
│   └── adw_*_iso.py         # Isolated workflow scripts
├── agents/
│   ├── hook_logs/           # Hook execution logs
│   ├── context_bundles/     # Session context storage
│   ├── security_logs/       # Blocked command audit logs
│   └── scout_files/         # Scout exploration results
├── scripts/                 # Utility scripts
├── specs/                   # Feature specifications
├── ai_docs/                 # AI reference documentation
└── config.yml               # TAC configuration
```

## TAC-14: Codebase Singularity & Orchestrator

TAC-14 elevates tac_bootstrap from **Class 1** (Agentic Layer) to **Class 2** (Outloop Systems) and **Class 3** (Orchestrator Agent), introducing Skills System, Agent SDK, database-backed workflows, WebSockets, and a real-time orchestration web app.

### Class Architecture

| Class | Grade | Description | Key Features |
|-------|-------|-------------|--------------|
| **Class 1** | Grade 7 | Agentic Layer | Skills System, Progressive Disclosure |
| **Class 2** | - | Outloop Systems | Custom Agents, Orchestrator Commands, Agent SDK |
| **Class 3** | - | Orchestrator Agent | Database, WebSockets, Real-time UI |

### Component Table

| # | Component | Class | Location | Description |
|---|-----------|-------|----------|-------------|
| 1 | Skills System | 1 | `.claude/skills/` | Progressive disclosure skill definitions |
| 2 | Agent Definitions | 2 | `.claude/agents/` | 7 specialized agent configurations |
| 3 | Orchestrator Commands | 2 | `.claude/commands/orch_*` | Multi-agent workflow commands |
| 4 | Agent SDK | 2 | `adws/adw_modules/adw_agent_sdk.py` | Pydantic models for programmatic agents |
| 5 | Database Schema | 3 | `adws/schema/` | SQLite schema (5 tables) |
| 6 | Database Models | 3 | `adws/adw_modules/orch_database_models.py` | Pydantic ORM models |
| 7 | Database Operations | 3 | `adws/adw_modules/adw_database.py` | CRUD + connection pooling |
| 8 | Database Logging | 3 | `adws/adw_modules/adw_logging.py` | Structured event logging |
| 9 | Consolidated Workflows | 3 | `adws/adw_workflows/` | Database-backed ADW workflows |
| 10 | WebSockets | 3 | `adws/adw_modules/adw_websockets.py` | Real-time event streaming |
| 11 | Orchestrator Backend | 3 | `apps/orchestrator_3_stream/backend/` | FastAPI REST + WebSocket server |
| 12 | Orchestrator Frontend | 3 | `apps/orchestrator_3_stream/frontend/` | Vue 3 + TypeScript swimlane UI |

### Skills System

Skills provide **progressive disclosure** - users start with simple invocations and graduate to advanced features:

```bash
# Basic skill invocation
/meta-skill "create a deployment skill"

# Skills are defined in .claude/skills/{skill-name}/SKILL.md
```

**Structure:**
```
.claude/skills/
└── meta-skill/
    ├── SKILL.md              # Skill definition with YAML frontmatter
    └── docs/                 # Supporting documentation
        ├── claude_code_agent_skills.md
        └── blog_equipping_agents_with_skills.md
```

### Agent Definitions

Custom agents with YAML frontmatter for specialized tasks:

| Agent | Purpose | Tools |
|-------|---------|-------|
| `build-agent` | Single-file implementation | Write, Read, Edit, Bash |
| `planner` | Architecture planning | Glob, Grep, Read |
| `scout-report-suggest` | Codebase analysis | Read, Glob, Grep |
| `playwright-validator` | Browser automation testing | Playwright MCP tools |
| `meta-agent` | Generate new agent configs | Write, WebFetch |
| `docs-scraper` | Documentation fetching | WebFetch, Write |

### Orchestrator Commands

Multi-agent workflow orchestration:

| Command | Description |
|---------|-------------|
| `/orch_plan_w_scouts_build_review` | Full workflow: scout → plan → build → review |
| `/orch_scout_and_build` | Simplified: scout → build |
| `/orch_one_shot_agent` | Single specialized agent task |
| `/build_in_parallel` | Parallel file implementation |
| `/parallel_subagents` | Launch multiple agents concurrently |

### Database-Backed ADWs

Workflows persist state to database for reliability and observability:

**Database Tables:**
- `orchestrator_agents` - Agent registry
- `agents` - Agent instances
- `prompts` - ADW workflow state (replaces JSON files)
- `agent_logs` - Step-by-step execution logs
- `system_logs` - System events

### Orchestrator Web App

Real-time dashboard for monitoring agent execution:

**Backend (FastAPI):**
- REST endpoints for CRUD operations
- WebSocket for real-time event streaming
- Integration with ADW database modules

**Frontend (Vue 3 + TypeScript):**
- Swimlane visualization of agent tasks
- Command palette (Cmd+K) for quick navigation
- Real-time WebSocket updates
- Keyboard shortcuts

### Usage Examples

**Without Orchestrator (default):**
```bash
# Standard agentic layer
tac-bootstrap init my-app

# File-based ADW workflows
uv run adws/adw_sdlc_iso.py 123
```

**With Orchestrator (opt-in):**
```bash
# Include orchestrator components
tac-bootstrap init my-app --with-orchestrator

# Or add to existing project
tac-bootstrap add-agentic --with-orchestrator

# Database-backed workflows
uv run adws/adw_workflows/adw_plan_build_review.py --adw-id task-123
```

### Additional Structure (when enabled)

```
project/
├── .claude/
│   ├── skills/                  # Skills System (Class 1)
│   │   └── meta-skill/
│   └── agents/                  # Agent Definitions (Class 2)
│       ├── build-agent.md
│       ├── planner.md
│       └── ...
├── adws/
│   ├── adw_modules/
│   │   ├── adw_agent_sdk.py     # Agent SDK (Class 2)
│   │   ├── adw_database.py      # Database Operations (Class 3)
│   │   ├── adw_websockets.py    # WebSockets (Class 3)
│   │   └── orch_database_models.py
│   ├── adw_workflows/           # Consolidated Workflows (Class 3)
│   │   ├── adw_plan_build.py
│   │   └── adw_plan_build_review.py
│   ├── adw_tests/               # Test suites
│   └── schema/                  # Database Schema (Class 3)
│       ├── schema_orchestrator.sql
│       └── migrations/
└── apps/
    └── orchestrator_3_stream/
        ├── backend/             # Orchestrator Backend (Class 3)
        │   ├── main.py
        │   └── modules/
        ├── frontend/            # Orchestrator Frontend (Class 3)
        │   ├── src/
        │   └── package.json
        └── playwright-tests/    # E2E Tests
```

### Configuration

Configure orchestrator in `config.yml` (single source of truth):

```yaml
orchestrator:
  enabled: true
  api_base_url: "http://localhost:8000"
  ws_base_url: "ws://localhost:8000"
  frontend_port: 5173
  websocket_port: 8000
  database_url: "sqlite:///data/orchestrator.db"
  polling_interval: 5000
```

The backend reads all values from `config.yml` at startup. Environment variables can override any value (priority: env var > config.yml > hardcoded default). The frontend `.env` file is generated from `config.yml` via `make gen-env`.

### Database Setup (SQLite)

No external database required. SQLite is the default and creates the database file automatically:

```bash
# Default: database created at data/orchestrator.db (no setup needed)
# The schema is initialized automatically on first run

# To use a custom path:
# database_url: "sqlite:///path/to/custom.db"

# Initialize schema manually (optional)
sqlite3 data/orchestrator.db < adws/schema/schema_orchestrator.sql
```

### Running the Orchestrator

**Using Makefile (recommended):**

```bash
# Install dependencies
make install               # Backend + frontend
make install-backend       # Only backend (FastAPI, aiosqlite)
make install-frontend      # Only frontend (Vue 3, npm)

# Setup database
make setup-db              # Initialize SQLite with schema

# Generate frontend .env from config.yml
make gen-env               # Creates .env with API URLs and ports

# Start development servers
make dev-backend           # FastAPI backend (port from config.yml, hot reload)
make dev-frontend          # Vue 3 frontend (port 5173)

# Utilities
make health                # Check backend health endpoint
make logs                  # View recent orchestrator logs via API
make clean                 # Clean caches
```

**All Makefile targets:**

| Target | Description |
|--------|-------------|
| `make install` | Install all dependencies (backend + frontend) |
| `make install-backend` | Install FastAPI, uvicorn, aiosqlite, pydantic |
| `make install-frontend` | Run `npm install` in frontend directory |
| `make setup-db` | Initialize SQLite database with schema |
| `make reset-db` | Delete and recreate database |
| `make gen-env` | Generate frontend `.env` from `config.yml` |
| `make dev` | Start backend in development mode (alias for dev-backend) |
| `make dev-backend` | Start FastAPI backend with hot reload (port from config.yml) |
| `make dev-frontend` | Start Vue 3 frontend dev server (port 5173) |
| `make dev-all` | Show instructions for running both servers |
| `make start` | Start backend in production mode (no reload) |
| `make start-backend` | Start FastAPI in production mode |
| `make start-frontend` | Build and serve frontend for production |
| `make test` | Run all tests (backend) |
| `make test-backend` | Run ADW module pytest tests |
| `make test-frontend` | Run Playwright E2E tests |
| `make health` | Check backend health endpoint via curl |
| `make logs` | View recent logs via REST API |
| `make clean` | Clean __pycache__, .pytest_cache, .vite |

**Manual commands:**

```bash
# 1. Start backend
cd apps/orchestrator_3_stream/backend
uvicorn main:app --reload --port 8000

# 2. Start frontend (separate terminal)
cd apps/orchestrator_3_stream/frontend
npm install && npm run dev

# 3. Open dashboard
open http://localhost:5173

# API docs
open http://localhost:8000/docs

# Run E2E tests
cd apps/orchestrator_3_stream
npx playwright test
```

**CLI Makefile (from `tac_bootstrap_cli/`):**

The CLI Makefile also includes orchestrator targets prefixed with `orch-`:

```bash
cd tac_bootstrap_cli
make orch-install          # Install backend dependencies
make orch-install-frontend # Install frontend dependencies
make orch-setup-db         # Initialize SQLite database
make orch-gen-env          # Generate frontend .env from config.yml
make orch-dev              # Start backend (port from config.yml, hot reload)
make orch-dev-frontend     # Start frontend (port 5173)
make orch-health           # Check backend health
```

## Commands

### CLI Commands

| Command | Description |
|---------|-------------|
| `tac-bootstrap init <name>` | Create new project |
| `tac-bootstrap init <name> --with-orchestrator` | Create project with orchestrator (TAC-14) |
| `tac-bootstrap add-agentic` | Add to existing project |
| `tac-bootstrap add-agentic --with-orchestrator` | Add with orchestrator components (TAC-14) |
| `tac-bootstrap upgrade` | Upgrade templates |
| `tac-bootstrap doctor` | Validate setup |
| `tac-bootstrap render` | Regenerate from config |
| `tac-bootstrap generate entity` | Generate CRUD entity |

### Key Slash Commands

| Command | Description |
|---------|-------------|
| `/prime` | Load project context |
| `/feature <desc>` | Plan new feature |
| `/test` | Run tests |
| `/commit` | Create git commit |
| `/quick-plan` | Rapid planning |
| `/scout <task> [scale]` | Parallel codebase exploration |
| `/question <query>` | Read-only Q&A about project |
| `/background <task>` | Background agent delegation |

**TAC-12 Orchestration Commands:**
See [TAC-12 Multi-Agent Orchestration](#tac-12-multi-agent-orchestration) section for `/parallel_subagents`, `/scout_plan_build`, and `/implement` with TAC-12 enhancements.

See [Commands Documentation](docs/commands.md) for the complete reference.

## Hooks

Automated actions during Claude Code sessions with event-driven architecture:

### Core Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `PreToolUse` | Before tool execution | Validation, security checks |
| `PostToolUse` | After tool execution | Logging, context tracking |
| `Stop` | Session ends | Cleanup, final reporting |
| `Notification` | System notifications | External integrations |

### Security Hooks

| Hook | Purpose |
|------|---------|
| `dangerous_command_blocker` | Block destructive bash commands (rm -rf, dd, mkfs, etc.) |
| `pre_tool_use` | Custom validation and security rules |

### TAC-12 Additional Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `send_event` | Explicit call | Event transmission to remote observability servers |
| `session_start` | Session begins | Capture git branch, model, project context |
| `pre_compact` | Before context compaction | Save session snapshots |
| `subagent_stop` | Subagent completes | Aggregate and process subagent results |
| `user_prompt_submit` | User submits prompt | Audit logging and validation |

### Observability Integration

- **Hook Logs**: Comprehensive event logging to `agents/hook_logs/`
- **Context Bundles**: Session state preservation in `agents/context_bundles/`
- **Security Audit Trail**: Blocked operations logged to `agents/security_logs/`
- **Status Line Integration**: Real-time session context in editor status bar

See [Hooks Documentation](docs/hooks.md) for configuration and [Utilities Documentation](docs/utilities.md) for observability tools.

## Observability

TAC-12 provides comprehensive observability infrastructure for monitoring sessions, tracking operations, and integrating with external systems.

### Hooks System

The hook system provides event-driven observability:
- **9 Hook Types**: Core, Security, and TAC-12 Additional hooks
- **Event Triggers**: PreToolUse, PostToolUse, UserPromptSubmit, SessionStart, SessionEnd, SubagentStop, PreCompact
- **Categorized Hooks**: Core operational hooks, security validation hooks, and TAC-12 specific hooks for advanced observability

### Status Line Integration

Display real-time session context in the Claude Code editor status bar:
- **Location**: `.claude/status_lines/status_line_main.py`
- **Displays**: Agent name, Claude model, git branch, custom metrics
- **Updated**: Via environment variables and hook contributions

### Logging Infrastructure

Structured logging and context preservation:

| Directory | Purpose |
|-----------|---------|
| `agents/hook_logs/` | Comprehensive event logs from universal_hook_logger |
| `agents/context_bundles/` | Session state bundles for recovery via `/load_bundle` |
| `agents/security_logs/` | Security audit trail of blocked commands |
| `.claude/logs/` | Session-specific logs (pre_compact, subagent_stop, user_prompt_submit) |

### Observability Utilities

Located in `.claude/hooks/utils/`:

| Utility | Purpose |
|---------|---------|
| `constants.py` | Session directory management and configuration |
| `summarizer.py` | AI-powered event summarization using Claude Haiku |
| `llm/` | LLM providers (Anthropic, OpenAI, Ollama) |
| `tts/` | Text-to-speech integrations (ElevenLabs, OpenAI, pyttsx3) |

See [Utilities Documentation](docs/utilities.md) for detailed usage and configuration examples.

## Agents

Specialized AI agents for autonomous tasks:

| Agent | Purpose |
|-------|---------|
| `docs-scraper` | Fetch external documentation |
| `meta-agent` | Generate new agent definitions |
| `research-docs-fetcher` | Discover documentation sources |
| `cc_hook_expert` | Expert pattern for hook development |

See [Agents Documentation](docs/agents.md) for details.

## ADW Workflows

AI Developer Workflows automate the SDLC with **TAC-13 expert system enabled by default** in orchestrated workflows:

```bash
# Full SDLC (TAC-13 enabled, auto-detects documentation)
uv run adws/adw_sdlc_iso.py 123
# ✅ Expert guidance active in all phases
# ✅ Documentation auto-detected from issue
# ✅ Expertise updated after each phase

# Zero Touch Execution (TAC-13 enabled + auto-merge)
uv run adws/adw_sdlc_zte_iso.py 123
# ✅ Complete automation with expert guidance
# ⚠️  Auto-merges to main if all phases pass

# Disable TAC-13 if needed
uv run adws/adw_sdlc_iso.py 123 --no-experts
# ⚪ Traditional workflow without expert system

# With manual documentation override
uv run adws/adw_sdlc_iso.py 123 --load-docs ddd,api
# ✅ TAC-13 still active + manual docs

# Plan + Build
uv run adws/adw_plan_build_iso.py 123

# Quick patch
uv run adws/adw_patch_iso.py 456
```

### Intelligent Documentation Loading (TAC-9)

ADW workflows automatically detect and load relevant project documentation based on issue content. This provides context-aware guidance throughout all workflow phases (clarify, plan, build, test, review, ship).

**Hybrid Detection System:**

1. **Static Keywords (28 predefined topics)**: Fast, precise matching for common topics
2. **Dynamic File Scanning**: Automatically discovers ALL .md files in `ai_docs/` recursively
3. **Smart Loading**: Only loads relevant documentation to optimize token usage
4. **Manual Override**: Specify exact topics when needed

**How It Works:**

```
Issue Analysis
    ↓
┌───────────────────────────────────┐
│ 1. Check Static Keywords          │ ← 28 predefined topics
│    "jwt" → authentication          │
│    "ddd" → ddd                     │
└───────────────────────────────────┘
    ↓
┌───────────────────────────────────┐
│ 2. Scan ai_docs/**/*.md Files     │ ← ANY custom .md file
│    "tac 12" → plan_tasks_Tac_12   │
│    "opencode" → plan_tasks_opencode│
└───────────────────────────────────┘
    ↓
Load All Detected Topics → Pass to All Workflow Phases
```

**Example 1 - Automatic Detection:**
```bash
# Issue: "Add JWT authentication to API endpoints"
uv run adws/adw_sdlc_zte_iso.py 486 adw-id

# Auto-detects:
# - authentication (static keyword: "jwt")
# - api (static keyword: "api", "endpoints")
#
# Loads:
# - ai_docs/authentication.md
# - ai_docs/api.md
```

**Example 2 - Plan References (Dynamic Scan):**
```bash
# Issue: "Implement TAC-12 parallel build feature"
uv run adws/adw_sdlc_zte_iso.py 501 adw-id

# Auto-detects:
# - plan_tasks_Tac_12_v3_FINAL (dynamic scan: "tac 12")
#
# Loads:
# - ai_docs/doc/plan_tasks_Tac_12_v3_FINAL.md
```

**Example 3 - Architecture + Plans:**
```bash
# Issue: "Refactor using DDD patterns per TAC-10 guidelines"
uv run adws/adw_sdlc_iso.py 789 adw-id

# Auto-detects:
# - ddd (static keyword: "ddd")
# - design_patterns (static keyword: "patterns")
# - plan_tasks_Tac_10 (dynamic scan: "tac 10")
#
# Loads all 3 documentation files automatically
```

**Example 4 - Manual Override:**
```bash
# Specify exact documentation topics (comma-separated)
uv run adws/adw_sdlc_zte_iso.py 486 adw-id --load-docs ddd,solid,design_patterns

# Ignores auto-detection, loads only specified topics
```

**Supported Documentation Topics:**

| Category | Predefined Topics | Dynamic Scan |
|----------|------------------|--------------|
| **Architecture** | `ddd`, `ddd_lite`, `design_patterns`, `solid` | ✅ + ALL .md files |
| **AI/SDK** | `anthropic_quick_start`, `openai_quick_start`, `claude_code_cli_reference`, `claude_code_sdk`, `claude-code-hooks`, `mcp-python-sdk` | ✅ + ALL .md files |
| **Tools** | `uv-scripts`, `e2b`, `fractal_docs` | ✅ + ALL .md files |
| **Technical** | `authentication`, `api`, `database`, `testing`, `deployment`, `frontend`, `backend`, `security`, `performance`, `monitoring` | ✅ + ALL .md files |
| **Custom** | None (add yours!) | ✅ **ANY .md in ai_docs/** |

**Add Your Own Documentation:**

Simply place markdown files anywhere in the `ai_docs/` directory:

```bash
# Your custom documentation
ai_docs/
├── company_standards.md          # Auto-detected if issue mentions "company standards"
├── internal_api_guidelines.md    # Auto-detected if issue mentions "internal api"
├── custom/
│   └── deployment_checklist.md   # Auto-detected if issue mentions "deployment checklist"
└── doc/
    └── architecture_decisions.md # Auto-detected if issue mentions "architecture decisions"
```

**The system will automatically:**
- Scan all subdirectories recursively
- Match filename (with/without underscores) against issue text
- Load relevant files without any code changes

**Multi-Topic Loading:**

When multiple topics are detected, they are all loaded and concatenated:

```bash
# Issue mentions multiple concepts
# Auto-detects: ["ddd", "api", "testing", "plan_tasks_Tac_12"]

# Workflow receives:
"""
# Documentation: ddd
[DDD content...]

---

# Documentation: api
[API content...]

---

# Documentation: testing
[Testing content...]

---

# Documentation: plan_tasks_Tac_12
[TAC-12 plan content...]
"""
```

**Available in Both Workflows:**
- ✅ `adw_sdlc_iso.py` - Full SDLC without auto-merge
- ✅ `adw_sdlc_zte_iso.py` - Zero Touch Execution with auto-merge

### TAC-13 Integration in ADW Workflows

TAC-13 (Act → Learn → Reuse) is **enabled by default** in orchestrated workflows (SDLC and ZTE) to provide automatic expert guidance and continuous learning throughout all workflow phases.

**Default Behavior:**

| Workflow Type | TAC-13 Status | Override |
|--------------|---------------|----------|
| **Orchestrators** (adw_sdlc_iso.py, adw_sdlc_zte_iso.py) | ✅ **Enabled by default** | `--no-experts --no-expert-learn` |
| **Individual ADWs** (plan, build, review, document) | ⚪ Disabled by default | `--use-experts --expert-learn` |

**Why Default-ON for Orchestrators:**
- Complete workflows are complex and benefit most from expert guidance
- Cumulative learning across phases (plan → build → review → document)
- Simplified UX - no flags to remember
- Individual ADWs retain flexibility for fine-grained control

**Act → Learn → Reuse Cycle:**

```
PLAN Phase:
  🔄 REUSE: Consult expertise.yaml for planning patterns
  ⚙️  ACT: Generate plan with expert context
  📚 LEARN: Update expertise (focus: planning_phase)

BUILD Phase:
  🔄 REUSE: Consult expertise.yaml for implementation patterns
  ⚙️  ACT: Implement with expert guidance
  📚 LEARN: Update expertise (focus: implementation_phase)

REVIEW Phase:
  🔄 REUSE: Consult expertise.yaml for review criteria
  ⚙️  ACT: Review with expert context
  📚 LEARN: Update expertise (focus: review_phase)

DOCUMENT Phase:
  🔄 REUSE: Consult expertise.yaml for documentation patterns
  ⚙️  ACT: Generate docs with expert context
  📚 LEARN: Full validation across all phases
```

**Usage Examples:**

```bash
# Full SDLC with TAC-13 (automatic)
uv run adws/adw_sdlc_iso.py 123
# ✅ TAC-13 active in all phases
# ✅ Expertise updated after each phase
# ✅ No flags needed

# Disable TAC-13 if needed (opt-out)
uv run adws/adw_sdlc_iso.py 123 --no-experts --no-expert-learn
# ⚪ Traditional behavior without expert guidance

# Zero Touch Execution with TAC-13 (automatic)
uv run adws/adw_sdlc_zte_iso.py 123
# ✅ TAC-13 active + automatic merge
# ✅ Maximum automation level

# Individual ADW with TAC-13 (opt-in)
uv run adws/adw_plan_iso.py 123 --use-experts --expert-learn
# ✅ TAC-13 active for this phase only
```

**Benefits:**

1. **Knowledge Accumulation**: Expertise grows with each workflow execution
2. **Consistency**: All phases use the same expert knowledge base
3. **Quality**: Expert guidance improves decision-making automatically
4. **Observability**: Expert consultations logged to GitHub issues
5. **Token Tracking**: Usage tracked in ADW state summaries

**Token Impact:**

- Overhead: ~27% more tokens per workflow
- ROI: Better quality, fewer bugs, reduced rework
- Controlled: Opt-out available for simple tasks

### Agent Experts (TAC-13)

TAC-13 introduces **self-improving agent experts** that follow an Act → Learn → Reuse loop. Unlike generic agents, experts maintain domain-specific knowledge in **expertise files** (YAML-based mental models) that evolve with your codebase through self-improvement cycles.

**Key Concepts:**

- **Expertise Files**: Persistent YAML knowledge bases containing domain insights, patterns, and gotchas
- **Self-Improvement**: Experts validate their mental models against actual code and update expertise automatically
- **Specialization**: Domain-focused agents (CLI, ADW, Commands) outperform generic agents for their specific areas
- **Meta-Agentic Capabilities**: Generate new commands and agent definitions from natural language

**When to Use Experts vs Generic Agents:**

Use experts when:
- Task requires deep domain knowledge (template registration, ADW state management, command structure)
- You want accumulated wisdom from previous iterations
- Self-improvement loop adds value (expertise evolves with codebase)

Use generic agents for:
- One-off tasks without domain specialization
- Exploratory work where no expertise exists yet
- Simple operations that don't benefit from accumulated knowledge

**Usage Examples:**

```bash
# Query CLI expert about domain-specific concepts
/experts:cli:question "How does template registration work?"

# Self-improve CLI expert after making code changes
/experts:cli:self-improve true

# Orchestrate expert through full workflow (plan → build → improve)
/expert-orchestrate cli "Add new template for hooks"

# Scale experts in parallel for high-confidence results
/expert-parallel cli "Review scaffold service logic" 5
```

**Available Expert Domains:**

| Expert Domain | Expertise Coverage | Commands |
|---------------|-------------------|----------|
| `cli` | tac-bootstrap CLI, templates, scaffold service | `/experts:cli:question`, `/experts:cli:self-improve` |
| `adw` (optional) | AI Developer Workflows, state management | `/experts:adw:question`, `/experts:adw:self-improve` |
| `commands` (optional) | Slash command structure, variables | `/experts:commands:question`, `/experts:commands:self-improve` |

**Meta-Agentic Commands:**

TAC-13 includes extensibility tools for evolving your agentic layer:

- `/meta-prompt` - Generate new slash commands from natural language descriptions
- `/meta-agent` - Generate new agent definitions (.md + .j2 template files)

These enable **progressive disclosure**: start with basic expert queries, graduate to orchestration workflows, then extend the system with custom commands and agents as needs evolve.

**Integration with Other TAC Features:**

- **TAC-9 (Documentation Loading)**: Experts use expertise files as specialized documentation
- **TAC-12 (Orchestration)**: Expert agents can be orchestrated for complex multi-phase workflows
- **Progressive Path**: `/experts:cli:question` (beginner) → `/expert-orchestrate` (intermediate) → `/expert-parallel` (advanced)

## TAC-12 Multi-Agent Orchestration

TAC-12 enhances orchestration capabilities for complex, multi-phase workflows with improved parallel execution and observability.

### TAC-12 Specific Commands

| Command | Description |
|---------|-------------|
| `/parallel_subagents <task> [count]` | Launch multiple specialized agents in parallel |
| `/scout_plan_build <task> [scale] [thoroughness]` | End-to-end orchestration: discovery → planning → implementation |
| `/implement <plan>` | Execute implementation plan (TAC-12: Enhanced with parallel file delegation) |

### Parallel Subagents

Execute complex tasks by launching multiple specialized agents simultaneously:

```bash
/parallel_subagents "Analyze codebase security posture" 3
/parallel_subagents "Research best practices for distributed caching"
```

**Features:**
- Specialized prompts tailored to each agent's expertise
- Automatic result aggregation and summarization
- Progress tracking across parallel executions

### Scout-Plan-Build Orchestration

Complete end-to-end workflow with three sequential phases:

```bash
/scout_plan_build "Add authentication to API endpoints" 4
/scout_plan_build "Implement real-time notifications" 6 thorough
```

**Phases:**
1. **Scout**: Parallel exploration to identify relevant files (configurable strategies)
2. **Plan**: Create implementation plan informed by scout findings
3. **Build**: Execute plan with progress tracking and validation

**Parameters:**
- `[scale]` (2-10): Number of parallel exploration strategies
- `[thoroughness]` (quick|medium|thorough): Plan depth

## Configuration

### config.yml

```yaml
version: 1

project:
  name: "my-app"
  language: "python"
  framework: "fastapi"
  package_manager: "uv"

commands:
  start: "uv run python -m app"
  test: "uv run pytest"
  lint: "uv run ruff check ."

agentic:
  provider: "claude_code"
  model_policy:
    default: "sonnet"
    heavy: "opus"
  token_optimization:
    max_issue_body_length: 2000
    max_file_reference_size: 5000
    max_clarification_length: 1000
    max_docs_planning: 2
    max_summary_tokens_planning: 200
    max_file_references: 3
    max_screenshots: 3
```

### Token Optimization

TAC Bootstrap includes comprehensive token optimization to reduce AI costs by 45-65% while maintaining quality. All limits are configurable via `config.yml`.

**Optimization Strategy:**

| Feature | Default | Purpose | Savings |
|---------|---------|---------|---------|
| **Issue Body Truncation** | 2000 chars | Truncate long issue descriptions | ~1000-2000 tokens |
| **File Reference Limits** | 5000 chars/file, 3 files max | Limit documentation file size | ~2000-8000 tokens |
| **Clarification Limits** | 1000 chars | Cap clarification response length | ~1000-3000 tokens |
| **Doc Loading Limits** | 2 files, 200 tokens/summary | Restrict planning phase docs | ~300-600 tokens |
| **Screenshot Limits** | 3 screenshots max | Cap review phase images | ~500-1500 tokens |
| **Context Bundles** | Progressive context | Avoid re-transmitting context | ~4000-6000 tokens |
| **Doc Digests** | Cache + extraction + aggressive summarization | Smart documentation handling | ~4000-5000 tokens |

**Total Savings:** 23,000-45,000 tokens per workflow (45-65% reduction)

**Customization Example:**

```yaml
# Small project - more restrictive
agentic:
  token_optimization:
    max_file_reference_size: 3000
    max_docs_planning: 1
    max_screenshots: 2

# Large project - more permissive
agentic:
  token_optimization:
    max_file_reference_size: 10000
    max_docs_planning: 4
    max_screenshots: 5
```

**Advanced Features:**

1. **Context Bundles** - Progressive context tracking across workflow phases:
   ```
   agents/context_bundles/{adw_id}/
   ├── issue_facts.md       # Created once
   ├── decisions.md         # Accumulated per phase
   └── repo_constraints.md  # Created once
   ```

2. **Doc Digest System** - Smart documentation handling:
   - **Cache**: Reuse summaries (100% savings on repeated loads)
   - **Section Extraction**: Extract only relevant sections (60-80% reduction)
   - **Aggressive Summarization**: Ultra-concise summaries (70-85% reduction)

3. **Payload Minimization** - Only essential data sent to agents:
   - Issue body truncated with clear `[TRUNCATED]` markers
   - File references capped at configurable size
   - All truncations logged for transparency

**Observability:**

Token usage is tracked and logged in:
- ADW state files (`agents/{adw_id}/adw_state.json`)
- GitHub issue comments (per-phase summaries)
- Hook logs (`agents/hook_logs/`)

**Configuration Reference:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_issue_body_length` | int | 2000 | Maximum characters for issue body in prompts |
| `max_file_reference_size` | int | 5000 | Maximum characters per referenced file |
| `max_clarification_length` | int | 1000 | Maximum characters for clarification responses |
| `max_docs_planning` | int | 2 | Maximum documentation files in planning phase |
| `max_summary_tokens_planning` | int | 200 | Target tokens per doc summary in planning |
| `max_file_references` | int | 3 | Maximum files to load from issue references |
| `max_screenshots` | int | 3 | Maximum screenshots in review phase |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_PATH` | Path to Claude Code executable |
| `ANTHROPIC_API_KEY` | For programmatic mode |
| `GITHUB_PAT` | GitHub integration |

## Entity Generation

Generate CRUD entities for DDD projects:

```bash
tac-bootstrap generate entity Product \
  --capability catalog \
  --fields "name:str:required,price:float" \
  --architecture ddd
```

Generates:
- Domain model
- Schemas (DTOs)
- Service layer
- Repository
- API routes

## Documentation Scripts

Scripts for generating and maintaining project documentation using LLM providers.

### gen_docs_fractal.py

Generate a fractal documentation tree from code docstrings and READMEs:

```bash
# Using Claude Code CLI (recommended - no API key needed)
uv run scripts/gen_docs_fractal.py --provider claude --dry-run

# Using OpenAI API
uv run scripts/gen_docs_fractal.py --provider api --dry-run
```

| Option | Default | Description |
|--------|---------|-------------|
| `--provider` | claude | LLM provider: `claude` (CLI) or `api` (OpenAI) |
| `--claude-model` | sonnet | Claude model: sonnet, opus, haiku |
| `--mode` | complement | merge mode: complement or overwrite |
| `--dry-run` | false | Preview changes without writing |

### gen_docstring_jsdocs.py

Add IDK-format docstrings to Python/TypeScript files:

```bash
# Using Claude Code CLI (recommended - no API key needed)
uv run scripts/gen_docstring_jsdocs.py --provider claude --dry-run

# Using OpenAI API
uv run scripts/gen_docstring_jsdocs.py --provider api --dry-run
```

| Option | Default | Description |
|--------|---------|-------------|
| `--provider` | claude | LLM provider: `claude` (CLI) or `api` (OpenAI) |
| `--claude-model` | sonnet | Claude model: sonnet, opus, haiku |
| `--mode` | add | add (safe), complement, or overwrite |
| `--changed-only` | false | Process only git-changed files |
| `--public-only` | false | Skip private functions/methods |
| `--dry-run` | false | Preview changes without writing |

## Development

```bash
make install-dev   # Install dependencies
make test          # Run tests
make lint          # Check code
make format        # Format code
make typecheck     # Type checking
```

## Requirements

- Python 3.10+
- Git
- Claude Code CLI
- uv (recommended)

## License

MIT

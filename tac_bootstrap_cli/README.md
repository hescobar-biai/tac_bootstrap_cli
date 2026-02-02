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
git clone --branch v0.6.0 --depth 1 https://github.com/celes-app/tac-cli-dist.git
cd tac-cli-dist
make install-dev

export CLAUDE_CODE_PATH=$(which claude)
uv tool install .

# Works from any directory
tac-bootstrap --help
```

### Development Install

```bash
git clone --branch v0.6.0 --depth 1 https://github.com/celes-app/tac-cli-dist.git
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
```

### Existing Project

```bash
cd your-project
tac-bootstrap add-agentic

# Preview changes
tac-bootstrap add-agentic --dry-run
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

## Commands

### CLI Commands

| Command | Description |
|---------|-------------|
| `tac-bootstrap init <name>` | Create new project |
| `tac-bootstrap add-agentic` | Add to existing project |
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

AI Developer Workflows automate the SDLC:

```bash
# Full SDLC
uv run adws/adw_sdlc_iso.py --issue 123

# Plan + Build
uv run adws/adw_plan_build_iso.py --issue 123

# Quick patch
uv run adws/adw_patch_iso.py --issue 456
```

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
```

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

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
git clone --branch v0.5.1 --depth 1 https://github.com/celes-app/tac-cli-dist.git
cd tac-cli-dist
make install-dev

export CLAUDE_CODE_PATH=$(which claude)
uv tool install .

# Works from any directory
tac-bootstrap --help
```

### Development Install

```bash
git clone --branch v0.5.1 --depth 1 https://github.com/celes-app/tac-cli-dist.git
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
│   └── context_bundles/     # Session context storage
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
| `/implement <plan>` | Execute implementation |
| `/test` | Run tests |
| `/commit` | Create git commit |
| `/quick-plan` | Rapid planning |
| `/background <task>` | Background agent delegation |
| `/parallel_subagents` | Multi-agent parallel execution |

See [Commands Documentation](docs/commands.md) for the complete reference.

## Hooks

Automated actions during Claude Code sessions:

| Hook | Purpose |
|------|---------|
| `PreToolUse` | Validate before tool execution |
| `PostToolUse` | Log and track operations |
| `UserPromptSubmit` | Capture user prompts |
| `Stop` | Session cleanup |
| `universal_hook_logger` | Comprehensive event logging |
| `context_bundle_builder` | Context preservation |

See [Hooks Documentation](docs/hooks.md) for details.

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

### Workflow Phases

| Workflow | Phases |
|----------|--------|
| `adw_sdlc_iso.py` | Plan → Build → Test → Review → Document |
| `adw_sdlc_zte_iso.py` | Full SDLC + Ship (Zero Touch) |
| `adw_plan_build_iso.py` | Plan → Build |
| `adw_patch_iso.py` | Quick implementation |

### Triggers

| Trigger | Description |
|---------|-------------|
| `trigger_webhook.py` | GitHub webhook events |
| `trigger_cron.py` | Scheduled polling |
| `trigger_issue_chain.py` | Sequential issue processing |
| `trigger_issue_parallel.py` | Parallel issue processing |

#### Parallel Trigger

Process multiple issues simultaneously with configurable concurrency:

```bash
# Process issues 123, 456, 789 in parallel
uv run adws/adw_triggers/trigger_issue_parallel.py 123 456 789

# Limit to 3 concurrent workflows
uv run adws/adw_triggers/trigger_issue_parallel.py --issues 123,456,789 --max-concurrent 3

# Single execution (for testing)
uv run adws/adw_triggers/trigger_issue_parallel.py --issues 123,456,789 --once
```

| Option | Default | Description |
|--------|---------|-------------|
| `--max-concurrent` | 5 | Maximum parallel workflows |
| `--interval` | 20 | Polling interval (seconds) |
| `--once` | false | Run single cycle and exit |

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

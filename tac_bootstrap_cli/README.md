# TAC Bootstrap

CLI to bootstrap Agentic Layer for Claude Code with TAC (Tactical Agentic Coding) patterns.

Transform any repository into an AI-assisted development environment in minutes.

## Features

- **Quick Setup**: Add complete agentic layer to any project in minutes
- **Auto-Detection**: Automatically detects language, framework, and package manager
- **Smart Defaults**: Sensible defaults based on your tech stack
- **Idempotent**: Safe to run multiple times without duplicating files
- **Customizable**: Full control via config.yml

## Installation

### Option 1: Global Install from Source (Recommended)

```bash
# Clone the release
git clone --branch v0.1.0 --depth 1 https://github.com/celes-app/tac-cli-dist.git
cd tac-cli-dist

# Install globally with uv tool
uv tool install .

# Now works from ANY directory
cd ~/my-projects
tac-bootstrap --help  # ✅ Works everywhere
```

### Option 2: Development Install (for contributing)

```bash
git clone --branch v0.1.0 --depth 1 https://github.com/celes-app/tac-cli-dist.git
cd tac-cli-dist
make install-dev

# Only works inside tac-cli-dist directory with "uv run"
uv run tac-bootstrap --help  # ✅ Works
cd ..
uv run tac-bootstrap --help  # ❌ Fails - must be in project dir
```

### Option 3: From PyPI (when published)

```bash
# With uv tool (recommended)
uv tool install tac-bootstrap

# With pipx
pipx install tac-bootstrap

# With pip
pip install tac-bootstrap
```

> **Note**: Check [releases](https://github.com/celes-app/tac-cli-dist/releases) for the latest version.

## Environment Setup

Copy the example environment file and configure your variables:

```bash
cp .env.example .env
```

### Required Variables

| Variable | Description |
|----------|-------------|
| `CLAUDE_CODE_PATH` | Path to Claude Code executable. Run `which claude` to find it. |

### Optional Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | For running ADWs in programmatic mode |
| `GITHUB_PAT` | GitHub token for ADW integrations |
| `E2B_API_KEY` | For cloud sandbox execution |
| `CLOUDFLARED_TUNNEL_TOKEN` | For webhook triggers |

See [.env.example](.env.example) for the complete list with documentation.

## Development

### Quick Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make install-dev` | Install with dev dependencies |
| `make test` | Run all tests |
| `make test-v` | Run tests with verbose output |
| `make test-cov` | Run tests with coverage report |
| `make lint` | Run ruff linter |
| `make lint-fix` | Run linter with auto-fix |
| `make format` | Format code with ruff |
| `make typecheck` | Run mypy type checker |
| `make build` | Build package wheel |
| `make clean` | Clean generated files |
| `make help` | Show all commands |

### Development Workflow

```bash
# 1. Clone latest release and install
git clone --branch v0.1.0 --depth 1 https://github.com/celes-app/tac-cli-dist.git
cd tac-cli-dist
make install-dev

# 2. Make changes to the code

# 3. Lint and format
make lint-fix
make format

# 4. Run tests
make test

# 5. Commit your changes
```

### Running the CLI Locally

```bash
make cli-help           # Show CLI help
make cli-version        # Show version
make cli-init-dry       # Example init with dry-run
make cli-doctor         # Example doctor command
```

## Quick Start

> **Note**: If you installed globally with `uv tool install .`, use `tac-bootstrap` directly.
> If you installed with `make install-dev`, use `uv run tac-bootstrap` from the project directory.

### For New Projects

```bash
# Interactive wizard (recommended)
tac-bootstrap init my-awesome-app

# Preview what will be created (dry-run)
tac-bootstrap init my-app --dry-run

# Non-interactive with all options
tac-bootstrap init my-api \
  --language python \
  --framework fastapi \
  --package-manager uv \
  --architecture ddd \
  --output ./projects/my-api \
  --no-interactive
```

#### Available Options for `init`

| Option | Short | Values | Default |
|--------|-------|--------|---------|
| `--language` | `-l` | python, typescript, javascript, go, rust, java | python |
| `--framework` | `-f` | fastapi, django, flask, nextjs, express, nestjs, react, vue, gin, echo, axum, actix, spring, none | none |
| `--package-manager` | `-p` | uv, poetry, pip, pipenv, pnpm, npm, yarn, bun, go, cargo, maven, gradle | auto |
| `--architecture` | `-a` | simple, layered, ddd, clean, hexagonal | simple |
| `--output` | `-o` | PATH | ./{name} |
| `--interactive` | | | enabled |
| `--dry-run` | | | disabled |

#### Examples by Language

```bash
# Python + FastAPI + UV + DDD
tac-bootstrap init my-api -l python -f fastapi -p uv -a ddd --no-interactive

# Python + Django + Poetry
tac-bootstrap init my-webapp -l python -f django -p poetry --no-interactive

# TypeScript + Next.js + pnpm
tac-bootstrap init my-frontend -l typescript -f nextjs -p pnpm --no-interactive

# TypeScript + NestJS + npm
tac-bootstrap init my-backend -l typescript -f nestjs -p npm --no-interactive

# Go + Gin
tac-bootstrap init my-service -l go -f gin --no-interactive

# Rust + Axum
tac-bootstrap init my-rust-api -l rust -f axum --no-interactive

# Java + Spring + Maven
tac-bootstrap init my-java-app -l java -f spring -p maven --no-interactive
```

### For Existing Projects

```bash
# Navigate to your project
cd your-existing-project

# Interactive wizard (recommended) - auto-detects your stack
tac-bootstrap add-agentic

# Add to specific path
tac-bootstrap add-agentic /path/to/your/repo

# Preview changes without applying (dry-run)
tac-bootstrap add-agentic --dry-run

# Force overwrite existing agentic files
tac-bootstrap add-agentic --force

# Non-interactive with auto-detection
tac-bootstrap add-agentic --no-interactive

# Combine options
tac-bootstrap add-agentic /path/to/repo --force --no-interactive
```

#### Available Options for `add-agentic`

| Option | Short | Description |
|--------|-------|-------------|
| `--interactive` | | Use interactive wizard (default) |
| `--no-interactive` | | Skip wizard, use auto-detection |
| `--dry-run` | | Preview changes without applying |
| `--force` | `-f` | Overwrite existing files |

### Utility Commands

```bash
# Validate your agentic setup
tac-bootstrap doctor /path/to/repo

# Auto-fix common issues
tac-bootstrap doctor /path/to/repo --fix

# Regenerate from config.yml
tac-bootstrap render config.yml --output ./my-project

# Regenerate with force overwrite
tac-bootstrap render config.yml --force --dry-run

# Show version
tac-bootstrap version
```

## Commands

### `init`

Create a new project with Agentic Layer.

```bash
tac-bootstrap init <name> [options]

Options:
  -l, --language          Programming language (python, typescript, go, rust, java)
  -f, --framework         Web framework (fastapi, nextjs, etc.)
  -p, --package-manager   Package manager (uv, npm, pnpm, etc.)
  -a, --architecture      Architecture pattern (simple, layered, ddd)
  -o, --output            Output directory
  -i/-I, --interactive    Enable/disable interactive wizard
  --dry-run               Preview without creating files
```

### `add-agentic`

Inject Agentic Layer into existing repository.

```bash
tac-bootstrap add-agentic [path] [options]

Options:
  -i/-I, --interactive    Enable/disable interactive wizard
  -f, --force             Overwrite existing files
  --dry-run               Preview without creating files
```

### `doctor`

Validate Agentic Layer setup.

```bash
tac-bootstrap doctor [path] [options]

Options:
  --fix                   Attempt to fix issues automatically
```

### `render`

Regenerate Agentic Layer from config.yml.

```bash
tac-bootstrap render [config.yml] [options]

Options:
  -o, --output            Output directory
  -f, --force             Overwrite existing files
  --dry-run               Preview without creating files
```

## Generated Structure

After running `tac-bootstrap`, your project will have:

```
project/
├── .claude/
│   ├── settings.json     # Claude Code settings
│   ├── commands/         # Slash commands (/prime, /test, etc.)
│   └── hooks/            # Execution hooks
├── adws/
│   ├── adw_modules/      # Shared workflow modules
│   ├── adw_triggers/     # Webhook and cron triggers
│   └── adw_*_iso.py      # Isolated workflow scripts
├── scripts/              # Utility scripts
├── specs/                # Feature/bug specifications
├── ai_docs/              # AI reference documentation
├── app_docs/             # Application documentation
├── logs/                 # Execution logs
├── config.yml            # TAC configuration
└── .mcp.json             # MCP server config
```

## ADW (AI Developer Workflows)

The `adws/` directory contains isolated workflow scripts that automate the software development lifecycle. Each workflow runs in an isolated git worktree for parallel execution.

### Core Workflows (Single Phase)

| Workflow | Description | Usage |
|----------|-------------|-------|
| `adw_plan_iso.py` | Planning phase: fetch issue, classify type, create branch, generate implementation plan | `uv run adws/adw_plan_iso.py <issue> [adw-id]` |
| `adw_build_iso.py` | Build phase: implement solution based on plan, commit changes | `uv run adws/adw_build_iso.py <issue> <adw-id>` |
| `adw_test_iso.py` | Test phase: run unit and E2E tests, report results | `uv run adws/adw_test_iso.py <issue> <adw-id> [--skip-e2e]` |
| `adw_review_iso.py` | Review phase: review implementation against spec, capture screenshots, resolve issues | `uv run adws/adw_review_iso.py <issue> <adw-id> [--skip-resolution]` |
| `adw_document_iso.py` | Documentation phase: analyze changes, generate feature docs | `uv run adws/adw_document_iso.py <issue> <adw-id>` |
| `adw_ship_iso.py` | Ship phase: validate state, merge PR to main | `uv run adws/adw_ship_iso.py <issue> <adw-id>` |
| `adw_patch_iso.py` | Quick patch: create worktree, implement patch from issue comment with `adw_patch` keyword | `uv run adws/adw_patch_iso.py <issue> [adw-id]` |

### Composite Workflows (Multi-Phase)

| Workflow | Phases | Usage |
|----------|--------|-------|
| `adw_plan_build_iso.py` | Plan → Build | `uv run adws/adw_plan_build_iso.py <issue> [adw-id]` |
| `adw_plan_build_test_iso.py` | Plan → Build → Test | `uv run adws/adw_plan_build_test_iso.py <issue> [adw-id] [--skip-e2e]` |
| `adw_plan_build_review_iso.py` | Plan → Build → Review | `uv run adws/adw_plan_build_review_iso.py <issue> [adw-id] [--skip-resolution]` |
| `adw_plan_build_test_review_iso.py` | Plan → Build → Test → Review | `uv run adws/adw_plan_build_test_review_iso.py <issue> [adw-id] [--skip-e2e] [--skip-resolution]` |
| `adw_plan_build_document_iso.py` | Plan → Build → Document | `uv run adws/adw_plan_build_document_iso.py <issue> [adw-id]` |
| `adw_sdlc_iso.py` | Plan → Build → Test → Review → Document (full SDLC) | `uv run adws/adw_sdlc_iso.py <issue> [adw-id] [--skip-e2e] [--skip-resolution]` |
| `adw_sdlc_zte_iso.py` | Plan → Build → Test → Review → Document → Ship (Zero Touch Execution) | `uv run adws/adw_sdlc_zte_iso.py <issue> [adw-id] [--skip-e2e] [--skip-resolution]` |

### Shared Modules (`adw_modules/`)

| Module | Description |
|--------|-------------|
| `agent.py` | Agent execution and template management |
| `data_types.py` | Pydantic models for ADW state and configuration |
| `git_ops.py` | Git operations (commit, push, branch) |
| `github.py` | GitHub API integration (issues, PRs, comments) |
| `r2_uploader.py` | Cloudflare R2 upload for screenshots |
| `state.py` | Persistent ADW state management (`adw_state.json`) |
| `utils.py` | Common utilities and helpers |
| `workflow_ops.py` | Workflow orchestration utilities |
| `worktree_ops.py` | Git worktree management for isolation |

### Triggers (`adw_triggers/`)

| Trigger | Description |
|---------|-------------|
| `trigger_webhook.py` | HTTP webhook server for GitHub events |
| `trigger_cron.py` | Scheduled execution via cron |

### Key Concepts

- **Isolation**: Each workflow runs in a dedicated git worktree under `trees/<adw-id>/`
- **State**: Workflows share state via `adw_state.json` for multi-phase execution
- **Ports**: Isolated port allocation (9100-9114 backend, 9200-9214 frontend) to avoid conflicts
- **Parallel**: Multiple workflows can run simultaneously on different issues

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
  worktrees:
    enabled: true
    max_parallel: 5
```

## Workflows

### SDLC Workflow

Complete development lifecycle: Plan → Build → Test → Review → Ship

```bash
uv run adws/adw_sdlc_iso.py --issue 123
```

### Patch Workflow

Quick fixes: Build → Test → Ship

```bash
uv run adws/adw_patch_iso.py --issue 456 --fix "Fix typo in README"
```

## Slash Commands

After setup, use these commands with Claude Code:

| Command | Description |
|---------|-------------|
| `/prime` | Load project context |
| `/start` | Start the application |
| `/test` | Run tests |
| `/feature <desc>` | Plan a new feature |
| `/bug <desc>` | Plan a bug fix |
| `/implement <plan>` | Implement from plan |
| `/commit` | Create git commit |
| `/review <plan>` | Review implementation |

## Requirements

- Python 3.10+
- Git
- Claude Code CLI

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## License

MIT

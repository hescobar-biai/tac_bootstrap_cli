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

```bash
# With UV (recommended)
uv tool install tac-bootstrap

# With pip
pip install tac-bootstrap

# From source (latest release)
git clone --branch v0.1.0 --depth 1 https://github.com/celes-app/tac-cli-dist.git
cd tac-cli-dist
uv pip install -e . --link-mode=copy

# Run commands with uv run (required for source installs)
uv run tac-bootstrap --help
```

> **Note**: When installed from source, always use `uv run tac-bootstrap` instead of `tac-bootstrap` directly.
> Check [releases](https://github.com/celes-app/tac-cli-dist/releases) for the latest version.

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

### For New Projects

```bash
# Interactive wizard (recommended)
uv run tac-bootstrap init my-awesome-app

# Preview what will be created (dry-run)
uv run tac-bootstrap init my-app --dry-run

# Non-interactive with all options
uv run tac-bootstrap init my-api \
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
uv run tac-bootstrap init my-api -l python -f fastapi -p uv -a ddd --no-interactive

# Python + Django + Poetry
uv run tac-bootstrap init my-webapp -l python -f django -p poetry --no-interactive

# TypeScript + Next.js + pnpm
uv run tac-bootstrap init my-frontend -l typescript -f nextjs -p pnpm --no-interactive

# TypeScript + NestJS + npm
uv run tac-bootstrap init my-backend -l typescript -f nestjs -p npm --no-interactive

# Go + Gin
uv run tac-bootstrap init my-service -l go -f gin --no-interactive

# Rust + Axum
uv run tac-bootstrap init my-rust-api -l rust -f axum --no-interactive

# Java + Spring + Maven
uv run tac-bootstrap init my-java-app -l java -f spring -p maven --no-interactive
```

### For Existing Projects

```bash
# Navigate to your project
cd your-existing-project

# Interactive wizard (recommended) - auto-detects your stack
uv run tac-bootstrap add-agentic

# Add to specific path
uv run tac-bootstrap add-agentic /path/to/your/repo

# Preview changes without applying (dry-run)
uv run tac-bootstrap add-agentic --dry-run

# Force overwrite existing agentic files
uv run tac-bootstrap add-agentic --force

# Non-interactive with auto-detection
uv run tac-bootstrap add-agentic --no-interactive

# Combine options
uv run tac-bootstrap add-agentic /path/to/repo --force --no-interactive
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
uv run tac-bootstrap doctor /path/to/repo

# Auto-fix common issues
uv run tac-bootstrap doctor /path/to/repo --fix

# Regenerate from config.yml
uv run tac-bootstrap render config.yml --output ./my-project

# Regenerate with force overwrite
uv run tac-bootstrap render config.yml --force --dry-run

# Show version
uv run tac-bootstrap version
```

## Commands

### `init`

Create a new project with Agentic Layer.

```bash
uv run tac-bootstrap init <name> [options]

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
uv run tac-bootstrap add-agentic [path] [options]

Options:
  -i/-I, --interactive    Enable/disable interactive wizard
  -f, --force             Overwrite existing files
  --dry-run               Preview without creating files
```

### `doctor`

Validate Agentic Layer setup.

```bash
uv run tac-bootstrap doctor [path] [options]

Options:
  --fix                   Attempt to fix issues automatically
```

### `render`

Regenerate Agentic Layer from config.yml.

```bash
uv run tac-bootstrap render [config.yml] [options]

Options:
  -o, --output            Output directory
  -f, --force             Overwrite existing files
  --dry-run               Preview without creating files
```

## Generated Structure

After running `uv run tac-bootstrap`, your project will have:

```
project/
├── .claude/
│   ├── settings.json     # Claude Code settings
│   ├── commands/         # Slash commands (/prime, /test, etc.)
│   └── hooks/            # Execution hooks
├── adws/
│   ├── adw_modules/      # Shared workflow modules
│   ├── adw_sdlc_iso.py   # SDLC workflow
│   └── adw_patch_iso.py  # Quick patch workflow
├── scripts/              # Utility scripts
├── specs/                # Feature/bug specifications
├── logs/                 # Execution logs
├── config.yml            # TAC configuration
└── .mcp.json            # MCP server config
```

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

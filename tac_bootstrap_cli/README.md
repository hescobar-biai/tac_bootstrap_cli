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

# From source
git clone https://github.com/your-org/tac-bootstrap
cd tac-bootstrap/tac_bootstrap_cli
uv pip install -e .
```

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
# 1. Clone and install
git clone https://github.com/your-org/tac-bootstrap
cd tac-bootstrap/tac_bootstrap_cli
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
# Interactive wizard
tac-bootstrap init my-awesome-app

# Non-interactive with options
tac-bootstrap init my-app --language python --framework fastapi --no-interactive
```

### For Existing Projects

```bash
cd your-existing-project

# Interactive (recommended)
tac-bootstrap add-agentic .

# Auto-detect and apply
tac-bootstrap add-agentic . --no-interactive
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

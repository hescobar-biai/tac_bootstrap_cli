# Prime

Prepare context for tac-bootstrap.

## Run
```bash
git ls-files
```

## Read
- README.md
- CLAUDE.md
- config.yml
- constitution.md
- adws/README.md

## Read Conditional
Use `.claude/commands/conditional_docs.md` to determine additional documentation.

## Understand

### Project: tac-bootstrap
- **Language**: python
- **Framework**: none
- **Architecture**: ddd
- **Package Manager**: uv

### Main Structure
```
tac-bootstrap/
├── .claude/commands/       # Slash commands
├── .claude/hooks/          # Automation hooks
├── adws/                   # AI Developer Workflows
├── scripts/                # Utility scripts
├── specs/                  # Specifications
├── config.yml              # Project configuration
└── tac_bootstrap_cli/              # Application source code
```

### Development Commands
```bash
# Available commands
uv run tac-bootstrap --help           # Start application
uv run pytest            # Run tests
uv run ruff check .            # Linting
uv build           # Build

# ADW Workflows
uv run adws/adw_sdlc_iso.py --issue <num>
```

## Report
- Summary of tac-bootstrap
- Constitution principles loaded and available for reference
- Current development state
- Next task to implement
- Key files for current task

**Note**: The `constitution.md` file defines the project's governing principles for code style, testing, architecture, UX/DX, and performance. Reference these principles during development and code review.

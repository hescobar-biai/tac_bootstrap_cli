---
doc_type: folder
domain: tac_bootstrap_cli
owner: UNKNOWN
level: L1
tags:
  - level:L1
idk:
  - python-cli
  - agentic-layer-bootstrap
  - claude-code-integration
  - ddd-architecture
  - jinja2-templating
  - typer-cli
  - slash-commands
  - adw-workflows
  - hook-system
  - entity-generation
  - fractal-documentation
related_code:
  - tac_bootstrap_cli
children:
  - docs/tac_bootstrap_cli/.mypy_cache.md
  - docs/tac_bootstrap_cli/.pytest_cache.md
  - docs/tac_bootstrap_cli/.ruff_cache.md
  - docs/tac_bootstrap_cli/docs.md
  - docs/tac_bootstrap_cli/tac_bootstrap.md
  - docs/tac_bootstrap_cli/tests.md
source_readmes:
  - tac_bootstrap_cli/README.md
  - tac_bootstrap_cli/readme.md
  - tac_bootstrap_cli/README.MD
  - tac_bootstrap_cli/Readme.md
last_reviewed: 2026-02-03
---

# Overview

UNKNOWN


# Responsibilities

- Project initialization with interactive wizard or CLI flags
- Auto-detection of language, framework, package manager
- Template rendering via Jinja2 for `.claude/`, `adws/`, `scripts/` structures
- CRUD entity generation for DDD architectures
- Configuration management via `config.yml`
- Template upgrade and validation (`doctor`, `upgrade`, `render` commands)
- Fractal documentation generation from docstrings and READMEs
- IDK-format docstring injection for Python/TypeScript


# Key APIs / Components

- **CLI Interface**: Typer-based commands (`init`, `add-agentic`, `generate entity`, `upgrade`, `doctor`, `render`)
- **Template Engine**: Jinja2 templates consuming `config` variable
- **Architecture Layers** (DDD):
  - `domain/`: Pydantic models
  - `application/`: Business services
  - `infrastructure/`: Template rendering, filesystem operations
  - `interfaces/`: Typer CLI entry points
- **Generated Artifacts**:
  - `.claude/settings.json`: Claude Code permissions, hooks, agents
  - `.claude/commands/`: 25+ slash commands (`/prime`, `/feature`, `/scout`, `/test`, `/commit`, etc.)
  - `.claude/hooks/`: Pre/PostToolUse, UserPromptSubmit, Stop, universal logger
  - `adws/`: SDLC workflows (`adw_sdlc_iso.py`, `adw_patch_iso.py`, `adw_plan_build_iso.py`)
  - `adws/adw_triggers/`: Webhook, cron, parallel issue/plan triggers
  - `agents/`: Hook logs, context bundles, security logs, scout files
  - `scripts/`: `gen_docs_fractal.py`, `gen_docstring_jsdocs.py`
- **Documentation Tools**:
  - `gen_docs_fractal.py`: Claude/OpenAI-powered fractal doc tree generation
  - `gen_docstring_jsdocs.py`: IDK-format docstring injection with `--changed-only`, `--public-only`


# Invariants & Contracts

- Python 3.10+ required
- `uv` package manager recommended
- Templates use `{{ config.* }}` variable structure
- DDD folder structure enforced for generated entities
- Environment variables: `CLAUDE_CODE_PATH`, `ANTHROPIC_API_KEY` (optional), `GITHUB_PAT` (optional)
- Commands assume `.claude/` config presence after `init` or `add-agentic`
- Fractal docs merge modes: `complement` (default) or `overwrite`
- Docstring modes: `add` (safe), `complement`, `overwrite`


# Side Effects & IO

- **Filesystem Writes**: Creates directories, renders templates, writes config files
- **Git Integration**: Reads repository status, creates commits via slash commands
- **Claude Code Execution**: Invokes `claude` CLI for documentation generation (`--provider claude`)
- **API Calls**: OpenAI API when `--provider api` used (requires API key)
- **GitHub API**: PAT-based access for ADW workflow triggers
- **Process Execution**: `uv run`, `pytest`, `make` commands via generated scripts


# Operational Notes

- **Global Install**: `uv tool install .` for system-wide availability
- **Development Install**: `uv run tac-bootstrap` in project directory
- **Dry Run**: Use `--dry-run` flag to preview changes before write
- **Parallel Execution**: ADW triggers support `--max-concurrent` (default: 5)
- **Model Policy**: Config supports `default: sonnet`, `heavy: opus` for task routing
- **Validation**: `tac-bootstrap doctor` checks setup integrity
- **Upgrade Path**: `tac-bootstrap upgrade` updates templates from source

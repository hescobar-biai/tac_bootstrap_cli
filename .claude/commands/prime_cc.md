---
description: Gain a general understanding of the codebase with a focus on Claude Code improvements
---

# Prime Claude Code

Execute the `Run`, `Read` and `Report` sections to understand the codebase with Claude Code-specific optimizations, then summarize your understanding.

## Variables

None required - this command uses project configuration from tac-bootstrap.

## Instructions

**Purpose:**
This command extends `/prime` with Claude Code-specific context loading. It helps Claude Code agents understand:
- Available slash commands and their purposes
- Output formatting styles and conventions
- Automation hooks and triggers
- Claude Code permissions and settings
- CLI-based development workflows

**Claude Code Optimizations:**
- **Tool Usage**: Prefer Read, Edit, Bash, Grep, Glob tools over other approaches
- **CLI Workflows**: Understand terminal-based development patterns
- **File Navigation**: Quick access to `.claude/` configuration files
- **Command Discovery**: Learn available slash commands for efficient workflows
- **Hook System**: Awareness of automation triggers and context builders

**Execution Flow:**
1. First run `/prime` to get general project context
2. Then read Claude Code-specific configuration files
3. Understand available commands, hooks, and automation
4. Report comprehensive understanding of both project and Claude Code setup

## Run

1. **Execute standard prime command:**
   - Read and execute `.claude/commands/prime.md` top to bottom
   - This loads general project context (README, config, structure)

2. **Load Claude Code configuration:**
   - Read all files listed in the Read section below
   - Understand available slash commands and their purposes
   - Learn about output styles and formatting conventions
   - Review automation hooks and their triggers
   - Check permissions in settings.json

## Read

**Claude Code Commands:**
- `.claude/commands/**` - All available slash commands for this project

**Claude Code Configuration:**
- `.claude/settings.json` - Permissions, allowlists, and Claude Code settings
- `.claude/output-styles/**` - Output formatting styles and conventions

**Automation Hooks:**
- `.claude/hooks/context_bundle_builder.py` - Context bundling automation (if exists)
- `.claude/hooks/**` - Other automation scripts and triggers

**Project-Specific Files:**
- `adws/README.md` - AI Developer Workflows documentation
- `adws/adw_modules/` - Reusable workflow modules
- `scripts/` - Utility scripts for CLI workflows

## Understand

### Claude Code Environment
- **Project**: tac-bootstrap
- **Claude Provider**: AgenticProvider.CLAUDE_CODE
- **Working Directory**: .

### Available Commands Structure
```
.claude/commands/
├── prime.md              # General project context
├── prime_cc.md           # Claude Code-optimized context (this command)
├── start.md              # Project startup
├── test.md               # Testing workflows
├── build.md              # Build processes
├── review.md             # Code review
├── ship.md               # Deployment/shipping
└── ...                   # Additional project commands
```

### Automation Hooks
```
.claude/hooks/
├── context_bundle_builder.py    # Auto-build context bundles
└── ...                          # Additional automation scripts
```

### CLI Development Workflow
```bash
# Project Commands
uv run tac-bootstrap --help           # Start application
uv run pytest            # Run tests
uv run ruff check .            # Linting
uv run mypy tac_bootstrap_cli       # Type checking
uv build           # Build

# AI Developer Workflows
uv run adws/adw_sdlc_iso.py --issue <num>       # Full SDLC workflow
uv run adws/adw_patch_iso.py --issue <num>      # Quick patch workflow
```

### Key Directories
```
tac-bootstrap/
├── .claude/                # Claude Code configuration
│   ├── commands/           # Slash commands
│   ├── hooks/              # Automation hooks
│   ├── output-styles/      # Output formatting
│   └── settings.json       # Permissions & settings
├── tac_bootstrap_cli/              # Application source code
├── adws/                   # AI Developer Workflows
├── scripts/                # Utility scripts
├── specs/                  # Feature specifications
├── config.yml              # Project configuration
└── constitution.md         # Project principles
```

## Examples

**Example 1: Basic usage**
```
User: /prime_cc
Agent: Executing /prime command first...
       [loads general project context]

       Loading Claude Code-specific configuration...
       Reading .claude/commands/ directory...
       Found 15 slash commands available

       Reading .claude/settings.json...
       Permissions configured for shell access

       Reading automation hooks...
       Found context_bundle_builder.py hook

       Summary:
       - Project: tac-bootstrap (Python/DDD/uv)
       - 15 slash commands available
       - Shell access enabled
       - Context bundling automation active
       - ADW workflows configured
```

**Example 2: Understanding tool preferences**
```
Agent understands after /prime_cc:
  ✓ Use Read tool instead of `cat` commands
  ✓ Use Edit tool instead of `sed` or manual editing
  ✓ Use Grep tool instead of `grep` or `rg` commands
  ✓ Use Glob tool instead of `find` commands
  ✓ Use Bash tool only for actual terminal operations
```

**Example 3: Command discovery**
```
After /prime_cc, agent knows:
  - /prime - General project context
  - /prime_cc - Claude Code-optimized context
  - /start - Start the application
  - /test - Run test suite
  - /build - Build the project
  - /review - Review implementation
  - /feature - Plan new feature
  - ... and 8+ more commands
```

## Report

Report to the user:

1. **Project Summary:**
   - Project name: tac-bootstrap
   - Language: Language.PYTHON
   - Architecture: Architecture.DDD
   - Package manager: PackageManager.UV

2. **Claude Code Configuration:**
   - Number of available slash commands
   - Key commands and their purposes
   - Permissions and allowlists from settings.json
   - Output styles configured

3. **Automation & Workflows:**
   - Automation hooks discovered and their purposes
   - AI Developer Workflows available (ADW)
   - Workflow types: SDLC, Patch, etc.

4. **CLI Development Setup:**
   - Available CLI commands for development
   - Testing commands and framework
   - Build and deployment processes
   - Key directories and file structure

5. **Tool Usage Patterns:**
   - Preferred tools: Read, Edit, Bash, Grep, Glob
   - File navigation shortcuts
   - Common workflow patterns

6. **Next Steps:**
   - Current development state
   - Next task to implement (if known)
   - Key files for current work
   - Relevant slash commands to use

**Format:**
```
Claude Code context loaded for: tac-bootstrap

Project Configuration:
  - Language: Language.PYTHON
  - Architecture: Architecture.DDD
  - Package Manager: PackageManager.UV

Available Slash Commands: {count}
  - /prime - {description}
  - /start - {description}
  - /test - {description}
  - ... (list key commands)

Automation Hooks: {count}
  - context_bundle_builder.py - {purpose}
  - ... (list other hooks)

CLI Workflows:
  - uv run tac-bootstrap --help - Start application
  - uv run pytest - Run tests
  - ... (list key commands)

Tool Preferences:
  ✓ Read tool for file reading
  ✓ Edit tool for file editing
  ✓ Grep tool for searching
  ✓ Glob tool for finding files
  ✓ Bash tool for terminal commands

Constitution principles loaded from constitution.md.

Ready for Claude Code development. Ask about specific commands or workflows for more details.
```

**Note**: The constitution.md file defines project principles for code style, testing, architecture, UX/DX, and performance. Reference these during development and code review.

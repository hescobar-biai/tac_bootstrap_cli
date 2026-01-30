---
doc_type: feature
adw_id: feature_Tac_12_task_8_2
date: 2026-01-30
idk:
  - slash-command
  - context-loading
  - codebase-exploration
  - progressive-strategy
  - architectural-analysis
  - pattern-discovery
  - jinja2-template
  - ddd
tags:
  - feature
  - command
  - prime
related_code:
  - .claude/commands/prime_3.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Prime 3 - Deep Context Loading Command

**ADW ID:** feature_Tac_12_task_8_2
**Date:** 2026-01-30
**Specification:** specs/issue-460-adw-feature_Tac_12_task_8_2-sdlc_planner-create-prime-3-command.md

## Overview

Created the `/prime_3` slash command that provides deep, comprehensive codebase context loading through a progressive 3-level exploration strategy. This command extends the basic `/prime` command with architectural understanding and pattern discovery, enabling agents to understand complex codebases without requiring parallel agent orchestration.

## What Was Built

- **Base Command File** (`.claude/commands/prime_3.md`): 314-line command implementing 3-level progressive exploration
- **Jinja2 Template** (`tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2`): 362-line templated version with config variables
- **Command Registration**: Added 'prime_3' to scaffold_service.py commands list

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:323`: Added 'prime_3' to commands list between 'prime_cc' and 'quick-plan'

### Files Created

- `.claude/commands/prime_3.md`: Base implementation for TAC Bootstrap repository
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prime_3.md.j2`: Template for generated projects

### Key Changes

**Progressive 3-Level Strategy:**
- **Level 1 (Base Context)**: Executes `/prime` to load README, CLAUDE.md, config.yml, constitution.md, plan files
- **Level 2 (Architectural Structure)**: Explores directory structure via `git ls-tree` and `find`, maps module organization and architectural boundaries
- **Level 3 (Deep Patterns)**: Discovers coding patterns using Grep for class/function definitions, import patterns, decorators, and testing conventions

**Template Variables:**
The Jinja2 template uses config variables for project-specific customization:
- `{{ config.project.name }}` - Project identification
- `{{ config.project.language.value }}` - Language-specific patterns (Python/TypeScript/JavaScript)
- `{{ config.paths.plan_file }}` - Conditional plan file inclusion
- `{{ config.paths.adws_dir }}` - Conditional ADW directory inclusion
- `{{ config.paths.app_root }}` - Application root path
- `{{ config.paths.specs_dir }}` - Specifications directory

**Pattern Discovery Commands:**
- Class/function definitions: `^class |^def |^function |^export (class|function)`
- Import patterns: `^import |^from .* import|^require\(|^export .*from`
- Test patterns: Language-specific glob patterns (`**/*test*.py`, `**/*.spec.ts`)
- Decorators/annotations: `@[A-Za-z]|# type:|: [A-Z][a-zA-Z]*\[`

## How to Use

### Basic Execution

Execute the command in Claude Code:

```
/prime_3
```

### When to Use

- Before implementing complex features requiring architectural understanding
- When you need to understand module patterns and dependencies
- For tasks that will touch multiple parts of the codebase
- When you want comprehensive context without the complexity of `/scout`

### When NOT to Use

- For simple, single-file tasks (use `/prime` instead)
- When you need parallel exploration with custom search strategies (use `/scout` instead)
- For quick orientation (use `/prime` or `/prime_cc` instead)

### Expected Output

The command executes sequentially through three levels:

1. **Level 1**: Loads base project context (via `/prime`)
2. **Level 2**: Outputs directory structure and module organization
3. **Level 3**: Reports discovered patterns, common imports, test conventions

Final report includes:
- Project fundamentals summary
- Architectural structure map
- Key patterns and conventions discovered
- Module dependency relationships

## Configuration

No additional configuration required. The command uses existing project configuration variables:

- Reads from `.claude/commands/prime.md` for Level 1
- Uses project structure for Level 2 exploration
- Adapts pattern searches to project language (Python/TypeScript/JavaScript)

Optional configuration via `config.yml`:
- `paths.plan_file` - Custom plan file path (defaults to PLAN_*.md)
- `paths.adws_dir` - ADW directory (conditionally included if exists)

## Testing

### Command Registration Test

Verify the command is registered in scaffold_service.py:

```bash
cd tac_bootstrap_cli && grep -n "prime_3" tac_bootstrap/application/scaffold_service.py
```

Expected output: Line 323 with 'prime_3' in commands list

### Template Rendering Test

Test Jinja2 template rendering with sample config:

```bash
cd tac_bootstrap_cli && uv run python -c "
from jinja2 import Template
from pathlib import Path

template = Path('tac_bootstrap/templates/claude/commands/prime_3.md.j2').read_text()
config = {
    'project': {'name': 'test-project', 'language': {'value': 'Python'}},
    'paths': {'plan_file': 'PLAN.md', 'adws_dir': 'adws', 'app_root': '.'}
}
result = Template(template).render(config=config)
print('Template renders successfully' if len(result) > 0 else 'ERROR')
"
```

### Unit Tests

Run all unit tests to verify zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Linting and Type Checking

```bash
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Smoke Test

Verify CLI still works:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Manual Execution Test

Test the command in TAC Bootstrap repository:

```
/prime_3
```

Verify it:
1. Executes `/prime` successfully
2. Explores directory structure via bash commands
3. Discovers patterns via Grep searches
4. Produces comprehensive context report

## Notes

- The command provides a middle ground between `/prime` (basic) and `/scout` (parallel exploration)
- Uses sequential execution (Level 1 → Level 2 → Level 3) for simplicity, no parallel agents required
- Pattern discovery in Level 3 uses targeted grep searches, not exhaustive scans
- Template follows DRY principles by reusing existing `/prime` command for Level 1
- Future enhancement possibility: `/prime_5` for even deeper exploration with 5 levels
- The reference file mentioned in the spec was not accessible, so design is based on existing patterns in this repository
- Command uses underscore notation (`/prime_3`) consistent with other TAC Bootstrap commands

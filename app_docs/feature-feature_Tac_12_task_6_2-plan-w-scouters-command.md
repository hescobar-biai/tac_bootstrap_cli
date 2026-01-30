---
doc_type: feature
adw_id: feature_Tac_12_task_6_2
date: 2026-01-30
idk:
  - parallel-agents
  - scout-exploration
  - codebase-analysis
  - planning-workflow
  - divide-and-conquer
  - task-tool
  - jinja2-templates
tags:
  - feature
  - planning
  - exploration
related_code:
  - .claude/commands/plan_w_scouters.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Plan with Scouters Command

**ADW ID:** feature_Tac_12_task_6_2
**Date:** 2026-01-30
**Specification:** specs/issue-458-adw-feature_Tac_12_task_6_2-sdlc_planner-plan-w-scouters-command.md

## Overview

Created the `/plan_w_scouters` slash command that combines comprehensive planning with parallel scout-based codebase exploration. This command launches multiple scout agents in parallel to explore the codebase before creating an implementation plan, ensuring all relevant files are identified and architectural patterns are understood.

## What Was Built

- **Base Command File** (`.claude/commands/plan_w_scouters.md`) - Complete command specification with parallel scout exploration workflow
- **Jinja2 Template** (`tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2`) - Template for CLI generation with config variable interpolation
- **Scaffold Service Integration** - Added "plan_w_scouters" to commands list in `scaffold_service.py`

## Technical Implementation

### Files Modified

- `.claude/commands/plan_w_scouters.md`: New 476-line command file defining the scout-based planning workflow
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2`: New 478-line Jinja2 template mirroring the base command with config variables
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:329`: Added "plan_w_scouters" to commands list after "plan_w_docs"

### Key Changes

1. **9-Step Scout Exploration Workflow**: Defined comprehensive workflow from parsing issue metadata through launching parallel scouts, aggregating results, identifying patterns, and creating informed plans

2. **3-Scout Divide-and-Conquer Strategy**:
   - Base Scout 1: Architectural patterns and domain logic (medium thoroughness)
   - Base Scout 2: Infrastructure and integration patterns (medium thoroughness)
   - Fast Scout: Surface-level pattern scan (quick thoroughness)

3. **High-Confidence File Scoring**: Implements frequency-based relevance scoring where files found by 2+ scouts are marked high-confidence (66%+)

4. **Task Tool Integration**: Uses single message with multiple Task tool invocations to launch all scouts in parallel with `subagent_type="Explore"` and `model="haiku"`

5. **Graceful Failure Handling**: Continues with partial results if scouts fail, documents failures in plan's Notes section

6. **Jinja2 Template Variables**: Exposes configuration through `config.project.*`, `config.paths.*`, and `config.commands.*` variables following existing template patterns

## How to Use

### Basic Usage

```bash
/plan_w_scouters <issue_number> <adw_id> '<issue_json>'
```

### Example: Planning a New Command Feature

```bash
/plan_w_scouters 123 "feature_new_command" '{"number":123,"title":"Create new export command","body":"Add a command to export project configuration to JSON format"}'
```

This will:
1. Parse the issue metadata to understand requirements
2. Launch 3 parallel scout agents exploring different concerns
3. Aggregate scout findings to identify high-confidence relevant files
4. Create an implementation plan informed by discovered patterns
5. Save plan to `specs/issue-123-adw-feature_new_command-sdlc_planner-*.md`
6. Output only the relative path for machine parsing

### Example: Planning Infrastructure Enhancement

```bash
/plan_w_scouters 456 "feature_template_engine" '{"number":456,"title":"Enhance template engine with partials","body":"Add support for Jinja2 partials/includes in template rendering"}'
```

## Configuration

### Jinja2 Template Variables

The template exposes these configuration points:

- `{{ config.project.name }}` - Project name for context
- `{{ config.project.type }}` - Project type (affects exploration strategy)
- `{{ config.paths.specs_dir }}` - Directory for saving plans (default: "specs")
- `{{ config.paths.app_root }}` - Application source code root (optional)
- `{{ config.commands.install }}` - Package installation command
- `{{ config.commands.test }}` - Test execution command
- `{{ config.commands.lint }}` - Linting command
- `{{ config.commands.typecheck }}` - Type checking command

### Scout Configuration

Default configuration (hardcoded in command, not exposed as template variables):
- Total scouts: 3 (2 base + 1 fast)
- Base scout thoroughness: "medium"
- Fast scout thoroughness: "quick"
- Model: "haiku" for cost-effective exploration
- Execution time: ~1-2 minutes for all scouts in parallel

## Testing

### Validation Commands

Run all commands to validate with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Verify Files Exist

```bash
cat .claude/commands/plan_w_scouters.md
```

```bash
cat tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/plan_w_scouters.md.j2
```

```bash
grep -n "plan_w_scouters" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
```

### Test Command Execution

```bash
# In a project generated with tac-bootstrap
/plan_w_scouters 1 "test_feature" '{"number":1,"title":"Test Feature","body":"Test description"}'
```

Expected behavior:
1. Launches 3 scout agents in parallel
2. Outputs progress message about scout strategies
3. Waits 1-2 minutes for scouts to explore
4. Aggregates results and creates plan
5. Outputs single line with relative path: `specs/issue-1-adw-test_feature-sdlc_planner-*.md`

## Notes

### Implementation Pattern

This command follows the proven `/plan_w_docs` structure but replaces sequential documentation exploration with parallel scout-based file discovery. It combines patterns from:
- `/scout` - Parallel agent launching and result aggregation
- `/plan_w_docs` - Structured planning workflow and report format
- `/quick-plan` - Base + fast scout pattern (adapted from 3 base + 5 fast to 2 base + 1 fast)

### Scout Configuration Rationale

The 2 base + 1 fast scout pattern balances thoroughness with execution time:
- **Base scouts** (medium thoroughness): Deep analysis of patterns (~1-2 minutes each, running in parallel)
- **Fast scout** (quick thoroughness): Rapid surface scan (~30-60 seconds)
- **Total execution**: ~1-2 minutes for all scouts due to parallel execution
- **Coverage**: Architectural patterns, infrastructure patterns, and surface-level patterns

### Advantages Over /plan_w_docs

- **Discovers actual code patterns** in addition to documentation
- **Parallel execution** for faster exploration (~1-2 minutes vs sequential doc search)
- **Finds undocumented patterns** and architectural decisions embedded in code
- **Identifies similar implementations** to reference during development
- **Better for mature codebases** where code patterns are more reliable than docs

Use `/plan_w_docs` when documentation is comprehensive and up-to-date.
Use `/plan_w_scouters` when you need to discover actual implementation patterns.

### Critical Output Format

The command enforces machine-parsable output:
- Returns ONLY the relative path (e.g., `specs/issue-123-adw-feature-name.md`)
- No explanations, commentary, or markdown formatting
- Enables integration with automated workflows and ADW systems

### Future Enhancements

- Support for configurable scout count via template variables
- Custom scout strategy definitions per project type
- Scout result caching to avoid re-exploring same prompts
- Integration with `/implement` to auto-feed high-confidence files
- ML-based relevance scoring beyond frequency counting

### Related Commands

- `/scout` - General-purpose parallel codebase exploration (no planning)
- `/plan_w_docs` - Planning with sequential documentation exploration
- `/quick-plan` - Fast planning with 8 parallel scouts
- `/feature` - Basic planning without exploration (legacy)

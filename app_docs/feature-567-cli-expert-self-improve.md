---
doc_type: feature
adw_id: feature_Tac_13_Task_5
date: 2026-02-02
idk:
  - agent-expert
  - self-improve
  - mental-model
  - expertise-yaml
  - 7-phase-workflow
  - validation
  - jinja2-template
  - dual-strategy
tags:
  - feature
  - tac-13
  - agent-expert
related_code:
  - .claude/commands/experts/cli/self-improve.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# CLI Expert Self-Improve Prompt

**ADW ID:** feature_Tac_13_Task_5
**Date:** 2026-02-02
**Specification:** specs/issue-567-adw-feature_Tac_13_Task_5-sdlc_planner-cli-self-improve-prompt.md

## Overview

This feature implements the CLI Expert self-improve prompt using the TAC-13 dual strategy pattern. The prompt enables the CLI expert to automatically validate and update its mental model (expertise.yaml) by analyzing the codebase and incorporating learnings. It implements the **Learn** step in the Act → Learn → Reuse loop, allowing the expert to continuously improve after each execution.

## What Was Built

- **Jinja2 Template**: Generic self-improve template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2` for CLI generation
- **Implementation File**: Concrete self-improve prompt at `.claude/commands/experts/cli/self-improve.md` for immediate use in tac-bootstrap repository
- **Template Registration**: Updated `scaffold_service.py` to register the self-improve template for automatic inclusion in generated projects

## Technical Implementation

### Files Modified

- `.claude/commands/experts/cli/self-improve.md`: New implementation file with hardcoded tac-bootstrap values (444 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2`: New Jinja2 template using `{{ config }}` variables (411 lines)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Updated template registration to include self-improve prompt

### Key Changes

1. **7-Phase Self-Improve Workflow**: Implements a comprehensive validation and update process:
   - Phase 1: Check Git Diff (conditional) - Analyze recent changes to focus validation
   - Phase 2: Read Current Expertise - Load existing mental model
   - Phase 3: Validate Against Codebase - Compare expertise claims with actual code
   - Phase 4: Identify Discrepancies - Document gaps, outdated info, and incorrect claims
   - Phase 5: Update Expertise - Apply surgical edits to YAML file
   - Phase 6: Enforce Line Limit - Compress expertise to stay under 1000 lines
   - Phase 7: Validate YAML Syntax - Final validation and verification

2. **Dual Strategy Pattern**: Following TAC-13 methodology:
   - Jinja2 template uses generic variables for project generation
   - Implementation file has concrete values for tac-bootstrap repository
   - Single template registration in scaffold_service.py

3. **Optional Arguments Support**:
   - `CHECK_GIT_DIFF` ($1): Focus on recently changed files
   - `FOCUS_AREA` ($2): Target specific areas like "templates" or "scaffold_service"

4. **Expertise File Constraints**: Enforces 1000-line limit with compression strategies:
   - Remove old recent_changes entries
   - Consolidate similar patterns
   - Use line ranges instead of detailed descriptions
   - Remove obvious information

## How to Use

### Run Full Validation

Validate the entire CLI expertise against the codebase:

```bash
/experts:cli:self-improve false
```

### Run Git Diff Mode

Focus validation on recently changed files:

```bash
/experts:cli:self-improve true
```

### Focus on Specific Area

Validate only a specific domain:

```bash
/experts:cli:self-improve false "templates"
```

### Combine Git Diff + Focus Area

```bash
/experts:cli:self-improve true "scaffold_service"
```

## Configuration

The self-improve prompt uses these static variables:

- **EXPERTISE_FILE**: `.claude/commands/experts/cli/expertise.yaml` (mental model location)
- **CLI_ROOT**: `tac_bootstrap_cli/tac_bootstrap/` (for tac-bootstrap) or project-specific CLI root
- **MAX_LINES**: `1000` (strict line limit for expertise file)

### Frontmatter Settings

```yaml
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, TodoWrite
description: Self-improve CLI expertise by validating against codebase
argument-hint: [check_git_diff] [focus_area]
model: sonnet
```

## Testing

### Verify Template Exists

```bash
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2 && echo "✓ Template exists" || echo "✗ Template missing"
```

### Verify Template Registration

```bash
grep -A 3 "self-improve.md.j2" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered" || echo "✗ Not registered"
```

### Verify Implementation File

```bash
test -f .claude/commands/experts/cli/self-improve.md && echo "✓ Repo file exists" || echo "✗ Repo file missing"
```

### Run Unit Tests

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

### Run Linting

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

### Run Type Checking

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

### Smoke Test

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Integration with Agent Expert Methodology

The self-improve prompt implements the **Learn** phase of the Act → Learn → Reuse loop:

- **Act**: CLI expert executes tasks using mental model (expertise.yaml)
- **Learn**: Self-improve validates and updates mental model (this feature)
- **Reuse**: Updated expertise is used in subsequent executions

### Expertise File Structure

The expertise.yaml follows a 10-section structure:

1. `overview`: High-level description and key files
2. `core_implementation`: Component details with line numbers
3. `schema`: Data model definitions
4. `operations`: Key workflow patterns
5. `data_flow`: How data moves through system
6. `performance`: Optimization patterns
7. `best_practices`: Coding standards
8. `issues`: Known problems and workarounds
9. `recent_changes`: Latest modifications (max 5 entries)
10. `deprecated`: Obsolete patterns to avoid

### Compression Strategies

When expertise exceeds 1000 lines, the prompt applies these compression techniques:

1. **Remove old recent_changes**: Keep only 3-5 most recent entries
2. **Consolidate similar patterns**: Group related methods/functions
3. **Use line ranges**: Replace detailed descriptions with line number ranges
4. **Remove obvious information**: Keep only non-obvious knowledge

### Related TAC-13 Tasks

- **Task 4**: CLI Expert - Question prompt (read-only queries)
- **Task 6**: CLI Expert - Expertise seed file (initial mental model)
- **Task 13**: Meta-Prompt Generator (uses self-improve as example)

### Future Enhancements

- Automatic git diff analysis after commits
- Integration with ADW workflows (auto self-improve after builds)
- Metrics tracking (expertise quality over time)
- Automated discrepancy detection with ML

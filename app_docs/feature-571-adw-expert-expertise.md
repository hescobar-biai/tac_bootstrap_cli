---
doc_type: feature
adw_id: feature_Tac_13_Task_9
date: 2026-02-03
idk:
  - adw-workflows
  - expertise-file
  - state-management
  - worktree-isolation
  - github-integration
  - orchestration-patterns
  - agent-experts
  - template-scaffolding
tags:
  - feature
  - tac-13
  - agent-experts
  - adw
related_code:
  - .claude/commands/experts/adw/expertise.yaml
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# ADW Expert Expertise File

**ADW ID:** feature_Tac_13_Task_9
**Date:** 2026-02-03
**Specification:** specs/issue-571-adw-feature_Tac_13_Task_9-sdlc_planner-adw-expert-expertise.md

## Overview

Created a comprehensive expertise file for the ADW (AI Developer Workflows) expert system. This feature implements TAC-13's dual strategy pattern: a minimal seed template for generated projects and a comprehensive 846-line expertise file documenting ADW workflows, modules, state management, GitHub integration, and orchestration patterns.

## What Was Built

- **Seed Template**: Minimal YAML template with placeholder sections for generated projects
- **Populated Expertise File**: Comprehensive 846-line documentation of ADW system architecture, patterns, and best practices
- **Scaffold Registration**: Integration with CLI scaffold service using skip_if_exists semantics

## Technical Implementation

### Files Modified

- `.claude/commands/experts/adw/expertise.yaml`: Comprehensive ADW expertise file (846 lines) documenting 14 workflows, 11 modules, state management via ADWState class, GitHub integration patterns, and orchestration flows
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2`: Minimal seed template (14 lines) with placeholder structure
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added registration for ADW expertise template

### Key Changes

**Expertise File Structure**:
- `overview`: System description, 25 total files, 8 key files identified
- `architecture`: Composable workflow architecture with 3 layers (workflows, modules, triggers)
- `core_implementation`: 14 ADW workflows documented with execution patterns
- `key_operations`: 6 operation categories (workflow execution, state management, GitHub integration, orchestration, worktree isolation, agent execution)
- `best_practices`: 12 guidelines for ADW development
- `data_flow`: ADWState lifecycle across workflow phases
- `integrations`: TAC-9, TAC-10, TAC-12 capability integrations

**Documented Components**:
- 14 ADW workflows (SDLC, ZTE, plan, build, test, review, document, patch, ship, etc.)
- 11 ADW modules (state, workflow_ops, agent, github, git_ops, worktree_ops, data_types, tool_sequencer, utils, r2_uploader)
- ADWState class with 30+ state fields and key methods
- GitHub integration patterns for issues, comments, PRs
- Orchestration patterns: plan → build → test → review → document → ship

**Template Registration**:
- Uses `FileAction.CREATE` with skip_if_exists semantics
- Positioned after CLI expert registration in scaffold_service.py
- Static YAML (no Jinja2 variables) as expertise is domain knowledge, not project configuration

## How to Use

### For Generated Projects
When running `tac-bootstrap init`, the seed template is automatically created at `.claude/commands/experts/adw/expertise.yaml` if it doesn't exist. Developers can then populate it using the self-improve workflow:

```bash
/experts:adw:self-improve false
```

### For TAC Bootstrap Development
The populated expertise file serves as the canonical reference for ADW patterns. Agent experts can reference it when working with ADW code to understand:

1. **Workflow Patterns**: Which workflow to use for different tasks
2. **State Management**: How ADWState tracks workflow progress
3. **GitHub Integration**: How to interact with issues, PRs, comments
4. **Orchestration**: How workflows chain together (SDLC flow)
5. **Worktree Isolation**: How each workflow runs in isolated environment

### Self-Improve Workflow
The expertise file can be updated using the 7-phase self-improve workflow:

```bash
# Manual self-improve with git diff analysis
/experts:adw:self-improve false

# Automated self-improve (after PR merges)
/experts:adw:self-improve true
```

## Configuration

No configuration required. The expertise file is automatically available after:
1. Running `tac-bootstrap init` (creates seed template)
2. Running `/experts:adw:self-improve` (populates comprehensive version)

## Testing

### Validate Seed Template Exists
```bash
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2 && echo "✓ Seed template"
```

### Validate Registration
```bash
grep -A3 "ADW Expert Expertise" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py | grep "expertise.yaml" && echo "✓ Registered"
```

### Validate YAML Syntax
```bash
python3 -c "import yaml; yaml.safe_load(open('.claude/commands/experts/adw/expertise.yaml'))" && echo "✓ Valid YAML"
```

### Validate Line Count
```bash
test $(wc -l < .claude/commands/experts/adw/expertise.yaml) -lt 1000 && echo "✓ Under 1000 lines"
```

### Run Full Test Suite
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### TAC-13 Dual Strategy Pattern
This implementation follows the 3-component pattern consistently used across Tasks 7-17:
1. **Template (.j2)**: Minimal seed for generated projects
2. **Registration (scaffold_service.py)**: CLI integration with skip_if_exists
3. **Implementation (.yaml)**: Comprehensive repo root version

### Expertise File Philosophy
Per TAC-13 documentation, expertise files are "compressed mental models" not exhaustive documentation. They follow the 20/80 rule: 20% expertise context enables 80% task execution. This file focuses on:
- Patterns agents need to make decisions
- File locations for navigation
- Non-obvious design decisions
- Critical constraints and gotchas

### Line Count Strategy
The populated expertise file is 846 lines, well under the 1000-line hard limit. Compression strategies used:
- Hierarchical YAML structure (not flat)
- Concise bullet points (not paragraphs)
- References to code locations (not code snippets)
- High-level patterns (not implementation details)

### Integration with TAC Capabilities
- **TAC-9 (ai_docs)**: Auto-loads AI docs based on keyword detection in prompts
- **TAC-10 (build_w_report)**: Parallel build execution with detailed reporting
- **TAC-12 (scout)**: Parallel codebase exploration (scout agents)

These integrations are documented in the expertise file's `integrations` section with usage patterns and invocation examples.

### Self-Improve Workflow Reference
The populated expertise file serves as the baseline for the 7-phase self-improve workflow (Task 8). Agents will:
1. Check git diff for changes
2. Read current expertise
3. Validate against actual codebase
4. Identify discrepancies
5. Update expertise file
6. Enforce 1000-line limit (compress if needed)
7. Validate YAML syntax

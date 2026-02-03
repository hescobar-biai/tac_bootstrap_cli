---
doc_type: feature
adw_id: feature_Tac_13_Task_11
date: 2026-02-03
idk:
  - expert-system
  - self-improve
  - yaml-expertise
  - command-patterns
  - template-registration
  - act-learn-reuse
  - frontmatter
  - jinja2
tags:
  - feature
  - expert
  - tac-13
related_code:
  - .claude/commands/experts/commands/self-improve.md
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/self-improve.md.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
---

# Commands Expert Self-Improve Prompt

**ADW ID:** feature_Tac_13_Task_11
**Date:** 2026-02-03
**Specification:** specs/issue-573-adw-feature_Tac_13_Task_11-sdlc_planner-commands-expert-self-improve.md

## Overview

This feature implements the **Learn** step of the Act → Learn → Reuse loop for the Commands Expert. The self-improve prompt enables the Commands expert to automatically update its mental model (expertise.yaml) by analyzing recent changes to command files, validating expertise against the actual codebase, and incorporating new knowledge about command structure and patterns.

## What Was Built

- **7-Phase Self-Improve Workflow**: Systematic process for validating and updating Commands expertise
- **Commands-Specific Validation Logic**: Focused on command syntax, frontmatter, variables, phases, tool restrictions, and template registration
- **Dual Strategy Compliance**: Validates both CLI templates (.j2) and repository implementations (.md)
- **Template Registration**: Integrated into scaffold_service.py for CLI generation
- **Implementation File**: Ready-to-use command in `.claude/commands/experts/commands/self-improve.md`

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/self-improve.md.j2`: Jinja2 template for CLI generation (698 lines)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added template registration at line 532-540
- `.claude/commands/experts/commands/self-improve.md`: Implementation file for immediate use (698 lines)
- `specs/issue-573-adw-feature_Tac_13_Task_11-sdlc_planner-commands-expert-self-improve-checklist.md`: Task checklist (84 lines)
- `specs/issue-573-adw-feature_Tac_13_Task_11-sdlc_planner-commands-expert-self-improve.md`: Feature specification (275 lines)

### Key Changes

- **Template Creation**: Created comprehensive 7-phase workflow template following the pattern established by CLI and ADW expert self-improve prompts
- **Registration in scaffold_service.py**: Added entry to `expert_commands` list ensuring the template is included in generated projects
- **Commands Domain Focus**: Adapted validation logic to focus on command-specific concerns: frontmatter structure, variable patterns ($1, $2 shell expansion), phase-based workflows, tool restrictions, integration patterns, template registration, and dual strategy compliance
- **Compression Strategies**: Included guidance for maintaining 1000-line limit through strategic compression
- **YAML Validation**: Enforced YAML syntax validation before completion to ensure expertise file integrity

## How to Use

### Invoking the Self-Improve Command

The Commands expert can self-improve using the command:

```bash
# Basic usage (validate all expertise)
/experts/commands/self-improve

# Focus on recently changed files
/experts/commands/self-improve true

# Focus on specific area
/experts/commands/self-improve false frontmatter
/experts/commands/self-improve true variables
/experts/commands/self-improve false template_registration
```

### What Happens During Execution

1. **Phase 1**: Optionally analyze git diff for recent command changes
2. **Phase 2**: Read current expertise.yaml mental model
3. **Phase 3**: Validate expertise against actual command files
4. **Phase 4**: Identify discrepancies (outdated, missing, incorrect information)
5. **Phase 5**: Update expertise file with corrections
6. **Phase 6**: Enforce 1000-line limit through compression if needed
7. **Phase 7**: Validate YAML syntax before completion

### Expert Focus Areas

The Commands expert validates expertise in these areas:

- **Command Syntax**: Markdown structure, YAML frontmatter, allowed-tools, description, argument-hint, model
- **Variable Patterns**: Shell expansion ($1, $2), semantic names, argument hints
- **Phase-Based Workflows**: Multi-step execution patterns
- **Tool Restrictions**: Permission scoping via allowed-tools
- **Integration Patterns**: Command chaining, expert architecture
- **Template Registration**: scaffold_service.py patterns (lines 484-540)
- **Dual Strategy Compliance**: Template + implementation synchronization

## Configuration

No additional configuration is required. The command uses these static paths:

- **EXPERTISE_FILE**: `.claude/commands/experts/commands/expertise.yaml`
- **COMMANDS_ROOT**: `.claude/commands/`
- **TEMPLATES_ROOT**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/`
- **MAX_LINES**: `1000`

## Testing

### Template Validation

```bash
# Verify template exists
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/self-improve.md.j2 && echo "✓ Template exists" || echo "✗ Template missing"

# Verify template registration in scaffold_service.py
grep -q 'experts/commands/self-improve.md' tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Template registered" || echo "✗ Registration missing"

# Verify implementation exists
test -f .claude/commands/experts/commands/self-improve.md && echo "✓ Implementation exists" || echo "✗ Implementation missing"

# Verify frontmatter structure
head -6 .claude/commands/experts/commands/self-improve.md | grep -q "allowed-tools:" && echo "✓ Frontmatter valid" || echo "✗ Frontmatter invalid"
```

### 7-Phase Structure Validation

```bash
# Verify all 7 phases are documented
for phase in "Phase 1:" "Phase 2:" "Phase 3:" "Phase 4:" "Phase 5:" "Phase 6:" "Phase 7:"; do
  grep -q "$phase" .claude/commands/experts/commands/self-improve.md && echo "✓ $phase" || echo "✗ Missing $phase"
done
```

### Commands-Specific Validation

```bash
# Verify focus areas are documented
grep -q "command syntax\|frontmatter" .claude/commands/experts/commands/self-improve.md && echo "✓ Command syntax focus"
grep -q "variable injection\|Jinja2\|{{ config" .claude/commands/experts/commands/self-improve.md && echo "✓ Variable injection focus"
grep -q "template registration\|scaffold_service" .claude/commands/experts/commands/self-improve.md && echo "✓ Template registration focus"
grep -q "dual strategy" .claude/commands/experts/commands/self-improve.md && echo "✓ Dual strategy focus"
```

### Full Test Suite

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### TAC-13 Context

This is Task 11 of 27 in the TAC-13 Agent Experts initiative. It completes the Commands Expert duo (question + self-improve). Task 12 will create the expertise seed file. This implementation addresses the fundamental problem: "agents forget and don't learn" by providing a systematic mechanism for expertise maintenance and evolution.

### Key Implementation Details

- Follows the exact 7-phase structure from CLI/ADW experts for consistency
- Adapts validation logic to Commands domain (frontmatter, variables, phases, template registration)
- Includes validation for both template files (.j2) and implementations (.md)
- Uses bash commands that work across different shell environments
- Provides comprehensive examples for each validation pattern
- Maintains 1000-line limit through compression strategies
- Always validates YAML syntax before finishing

### Compression Strategies

When expertise exceeds 1000 lines, the self-improve workflow applies these strategies:

1. Remove old recent_changes entries (keep 3-5)
2. Consolidate similar command patterns
3. Use line ranges instead of detailed descriptions
4. Remove obvious information that's self-evident from code
5. Focus on non-obvious knowledge and relationships

### Success Criteria for Self-Improve Execution

When the prompt is invoked, it should:

1. Complete all 7 phases successfully
2. Produce valid YAML output
3. Stay under 1000-line limit
4. Document all discrepancies found
5. Update last_updated timestamp
6. Provide comprehensive report

### Related Features

- **Commands Expert Question Prompt** (.claude/commands/experts/commands/question.md): The "Act" step for answering questions
- **CLI Expert Self-Improve** (.claude/commands/experts/cli/self-improve.md): Reference pattern for self-improvement
- **ADW Expert Self-Improve** (.claude/commands/experts/adw/self-improve.md): Reference pattern for self-improvement
- **Task 12 (Upcoming)**: Commands Expert expertise seed file creation

---
doc_type: feature
adw_id: feature_Tac_13_Task_12
date: 2026-02-03
idk:
  - expertise-yaml
  - agent-expert-system
  - yaml-frontmatter
  - command-patterns
  - self-improve-workflow
  - mental-model
  - skip-if-exists
  - domain-knowledge
tags:
  - feature
  - tac-13
  - agent-experts
  - commands-expert
related_code:
  - .claude/commands/experts/commands/expertise.yaml
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/expertise.yaml.j2
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - .claude/commands/experts/commands/question.md
  - .claude/commands/experts/commands/self-improve.md
---

# Commands Expert - Expertise File

**ADW ID:** feature_Tac_13_Task_12
**Date:** 2026-02-03
**Specification:** specs/issue-574-adw-feature_Tac_13_Task_12-sdlc_planner-commands-expert-expertise.md

## Overview

Created the expertise seed template and populated instance for the Commands expert, completing the TAC-13 agent expert triad (question → self-improve → expertise). This expertise file serves as a persistent mental model documenting command structure patterns, variable injection, allowed-tools specifications, workflow conventions, and report sections across 49+ commands in the `.claude/commands/` system.

## What Was Built

- **Expertise Seed Template**: Static YAML template at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/expertise.yaml.j2`
- **Repository Instance**: Populated expertise file at `.claude/commands/experts/commands/expertise.yaml` (408 lines)
- **Template Registration**: Added to `scaffold_service.py` with `FileAction.CREATE` (preserve learning across regenerations)
- **Comprehensive Documentation**: Covers command structure, frontmatter patterns, variable injection (dynamic $1, $2 vs static), workflow patterns, report sections, integration patterns, and best practices

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/expertise.yaml.j2`: New expertise seed template (408 lines)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added registration for expertise file (lines 540-545)
- `.claude/commands/experts/commands/expertise.yaml`: Populated repository instance (408 lines)

### Key Changes

1. **Expertise Schema**: Followed CLI and ADW expert patterns with consistent top-level sections: overview, architecture, command_structure, workflow_patterns, report_sections, integration_patterns, common_sections, validation_patterns, file_action_patterns, command_categories, best_practices, examples, maintenance

2. **Command Pattern Documentation**: Documented 49+ commands across 5 categories (planning, execution, workflows, utility, expert) with detailed frontmatter patterns (allowed_tools, description, argument_hint, model)

3. **Variable Injection Patterns**: Explained dynamic variables ($1, $2, $3, $ARGUMENTS) vs static variables (hardcoded paths), with examples from feature, implement, and scout commands

4. **Report Section Patterns**: Differentiated machine-parsable output (feature, plan, classify_issue) requiring exactly ONE line vs human-readable output (implement, build, review) with bullet points and git diff stats

5. **Expert System Integration**: Documented TAC-13 expert triad pattern (question.md + self-improve.md + expertise.yaml) and cross-expert collaboration patterns

6. **File Action Strategy**: Explained `FileAction.CREATE` usage for expertise files to preserve learning through self-improve workflow updates

## How to Use

### Querying Commands Expert

Use the Commands expert question command to answer questions about command structure:

```bash
claude /experts:commands:question "How do I structure a new command with variables?"
claude /experts:commands:question "What's the difference between machine-parsable and human-readable report formats?"
```

The expert loads the expertise.yaml mental model (20% context) instead of exploring the entire codebase (100% context).

### Updating Expertise

Run the self-improve workflow to validate and update expertise after command changes:

```bash
claude /experts:commands:self-improve
```

This analyzes all `.claude/commands/*.md` files and updates expertise.yaml with new patterns.

### Creating New Projects

When running `tac-bootstrap init <project>`, the expertise file is automatically scaffolded:

```bash
uv run tac-bootstrap init my-project
# Creates .claude/commands/experts/commands/expertise.yaml in my-project/
```

## Configuration

### Template Registration

The expertise file is registered in `scaffold_service.py` with `FileAction.CREATE`:

```python
plan.add_file(
    ".claude/commands/experts/commands/expertise.yaml",
    action=FileAction.CREATE,
    template="claude/commands/experts/commands/expertise.yaml.j2",
    reason="Commands expert expertise seed file",
)
```

This preserves local modifications when regenerating the project structure, allowing the expertise to evolve through self-improve workflow updates.

### Expertise File Structure

The YAML schema includes:

- **overview**: Total files, key files, last_updated timestamp
- **architecture**: Frontmatter + Markdown workflow pattern
- **command_structure**: Frontmatter patterns, variable patterns
- **workflow_patterns**: Phase-based execution, numbered tasks
- **report_sections**: Machine-parsable vs human-readable formats
- **integration_patterns**: Expert system, command chaining
- **examples**: Detailed examples from feature, implement, and experts:question commands

## Testing

### Validate YAML Syntax

```bash
python -c "import yaml; yaml.safe_load(open('.claude/commands/experts/commands/expertise.yaml'))"
```

### Check Line Count

```bash
wc -l .claude/commands/experts/commands/expertise.yaml
# Should output ~408 lines (under 1000 soft guideline)
```

### Integration Test - Template Registration

```bash
cd tac_bootstrap_cli && uv run python -c "
from tac_bootstrap.domain.models import TACConfig
from tac_bootstrap.application.scaffold_service import ScaffoldService
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from pathlib import Path

template_repo = TemplateRepository(Path('tac_bootstrap/templates'))
service = ScaffoldService(template_repo, None)
config = TACConfig.from_file(Path('../config.yml'))
plan = service.build_plan(config)

expertise_ops = [op for op in plan.file_operations if 'experts/commands/expertise.yaml' in op.path]
assert len(expertise_ops) == 1, f'Expected 1 expertise operation, found {len(expertise_ops)}'
assert expertise_ops[0].action.value == 'create', f'Expected create, got {expertise_ops[0].action.value}'
print('✅ Template registration verified')
"
```

### Test Commands Expert Query

```bash
# Verify expert can answer questions using expertise file
claude /experts:commands:question "What are the allowed_tools patterns?"
# Should return detailed answer referencing expertise.yaml:line_numbers
```

## Notes

### TAC-13 Expert Triad Completion

This task completes the Commands expert system:
- ✅ Question prompt (Task 10): Answer questions using expertise file
- ✅ Self-improve workflow (Task 11): Validate and update expertise file
- ✅ Expertise file (Task 12 - this feature): Persistent mental model

The Commands expert now has full **Act → Learn → Reuse** capability.

### Context Usage Optimization

With expertise file in place:
- **Before**: 100% context for full codebase exploration on every query
- **After**: 20% context to load expertise.yaml mental model + 80% for task-specific work

### Design Decisions

1. **Static Template**: No Jinja2 variables needed (documents patterns, not project config)
2. **FileAction.CREATE**: Changed from SKIP_IF_EXISTS to CREATE to match convention (still preserves local changes)
3. **408 Lines**: Under 1000-line soft guideline, documents 49+ commands with examples
4. **Populated via Self-Improve**: Seed includes comprehensive patterns rather than placeholders
5. **Schema Consistency**: Follows CLI/ADW expert schema for uniformity

### Future Enhancements

- Hook integration to auto-run self-improve on command file changes
- Version tracking for expertise evolution
- Diff reporting to show what self-improve learned
- Cross-expert validation (CLI expert reviews Commands patterns)

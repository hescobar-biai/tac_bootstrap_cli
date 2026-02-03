---
doc_type: feature
adw_id: feature_Tac_13_Task_6
date: 2026-02-03
idk:
  - expertise-file
  - cli-expert
  - self-improve
  - jinja2-template
  - skip-if-exists
  - yaml-schema
  - mental-model
  - act-learn-reuse
tags:
  - feature
  - expert-system
  - cli
  - template-generation
related_code:
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/expertise.yaml.j2
  - .claude/commands/experts/cli/expertise.yaml
  - .claude/commands/experts/cli/self-improve.md
  - .claude/commands/experts/cli/question.md
---

# CLI Expert Expertise File

**ADW ID:** feature_Tac_13_Task_6
**Date:** 2026-02-03
**Specification:** specs/issue-568-adw-feature_Tac_13_Task_6-sdlc_planner-cli-expert-expertise-file.md

## Overview

This feature completes the CLI Expert's "Act → Learn → Reuse" loop by implementing the expertise.yaml file system. It creates a Jinja2 seed template for new projects and populates a comprehensive 791-line expertise file in the tac_bootstrap repo root documenting the CLI architecture, patterns, and key operations. This expertise serves as the expert's "mental model" enabling efficient question answering and continuous learning through the self-improve workflow.

## What Was Built

- **Jinja2 Seed Template**: Minimal seed structure for new projects at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/expertise.yaml.j2`
- **Template Registration**: Added expertise file registration in `scaffold_service.py` with `CREATE` action
- **Populated Expertise File**: Comprehensive 791-line YAML file at `.claude/commands/experts/cli/expertise.yaml` documenting:
  - TAC Bootstrap CLI architecture (DDD layers)
  - 24 key files with line counts and purposes
  - Core implementation details for ScaffoldService (987 lines)
  - Domain models, template patterns, and best practices
  - Key operations with file paths and code references
- **Checklist Document**: Validation checklist ensuring quality standards

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added template registration at lines 501-507 in the `_add_claude_files()` method with TAC-13 Task 6 comment for traceability

### Files Created

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/expertise.yaml.j2`: 14-line seed template with placeholder sections:
  - `overview` with `project.name` interpolation
  - `last_updated` with Jinja2-escaped date generation
  - Empty `core_implementation`, `key_operations`, and `best_practices` sections with "To be populated by self-improve" comments

- `.claude/commands/experts/cli/expertise.yaml`: 791-line populated expertise file documenting:
  - **Architecture**: DDD layers (domain, application, infrastructure, interfaces) with 24 key files
  - **ScaffoldService**: Complete documentation of 987-line service including ApplyResult model, public methods (build_plan, apply_plan), and 6 private methods
  - **Template Registration Pattern**: Code examples showing FileAction usage and SKIP_IF_EXISTS preservation
  - **Domain Models**: TACConfig schema with enums (Language, Framework, Architecture) and key models
  - **Key Operations**: Template rendering, scaffold planning, file operations with file path references
  - **Best Practices**: DDD patterns, Jinja2 conventions, validation strategies

- `specs/issue-568-adw-feature_Tac_13_Task_6-sdlc_planner-cli-expert-expertise-file-checklist.md`: 74-line validation checklist

### Key Changes

1. **Dual Strategy Implementation**: Follows TAC-13 pattern where templates work as both generation artifacts (seed template) and reference implementations (populated file in repo root)

2. **FileAction.CREATE Usage**: Uses `CREATE` action instead of `SKIP_IF_EXISTS` in scaffold_service.py registration - this ensures the seed template is deployed to new projects

3. **Expertise File Structure**: 791-line YAML organized in sections:
   - `overview`: 11 lines with description, purpose, last_updated, total_files (24), key_files list
   - `architecture`: Documents DDD pattern with 4 layers and their purposes
   - `core_implementation`: Deep dive into ScaffoldService with line numbers and integration points
   - Template registration patterns with code examples
   - Domain models, key operations, and best practices

4. **Line Count Management**: Expertise file is 791 lines, comfortably under the 1000-line limit (4-6K tokens) for context window economics

5. **Jinja2 Template Escaping**: Uses `{{ '{{' }}` and `{{ '}}' }}` to escape nested template variables in the seed file, allowing proper date generation in deployed projects

## How to Use

### For New Projects

When generating a new project with `tac-bootstrap`, the CLI expert expertise seed template will be automatically deployed:

1. Run the wizard: `cd tac_bootstrap_cli && uv run tac-bootstrap wizard`
2. Complete configuration
3. After scaffolding, the file `.claude/commands/experts/cli/expertise.yaml` will contain the seed structure
4. Run `/experts:cli:self-improve false` to populate expertise with project-specific knowledge

### For CLI Expert Question Answering

The CLI expert can now efficiently answer questions using its expertise:

1. Ask questions via the question prompt: `/experts:cli:question "Where are templates registered?"`
2. The expert reads `.claude/commands/experts/cli/expertise.yaml` to provide informed answers
3. Expertise provides file paths, line numbers, and architectural context without re-reading the entire codebase

### For Continuous Learning

Keep the expertise up-to-date using the self-improve workflow:

1. After significant CLI changes, run: `/experts:cli:self-improve false`
2. Or enable automatic updates via git hooks
3. The 7-phase workflow validates expertise against the codebase and updates discrepancies

## Configuration

### Template Variables

The seed template uses these Jinja2 variables:

- `config.project.name`: Interpolated into the overview description
- `{{ '{{' }} now().strftime('%Y-%m-%d') {{ '}}' }}`: Escaped date generation for last_updated field

### FileAction Selection

- **Seed Template Registration**: Uses `FileAction.CREATE` to deploy the seed template to new projects
- **Expertise Preservation**: The expertise file itself should use `SKIP_IF_EXISTS` when regenerating to preserve learning (note: current implementation uses CREATE, but this could be enhanced)

### Line Limit

The expertise file has a hard limit of 1000 lines to optimize context window usage:
- Current: 791 lines (~4-6K tokens)
- Limit: 1000 lines
- If exceeded, the self-improve workflow compresses sections while preserving critical knowledge

## Testing

### Validate Seed Template Deployment

Test that the seed template deploys correctly to new projects:

```bash
cd tac_bootstrap_cli
uv run tac-bootstrap wizard --test-output /tmp/test-expertise
ls -la /tmp/test-expertise/.claude/commands/experts/cli/expertise.yaml
cat /tmp/test-expertise/.claude/commands/experts/cli/expertise.yaml
```

Expected: File exists with seed structure (overview, core_implementation, key_operations, best_practices sections with placeholder comments)

### Validate YAML Syntax

Ensure the expertise file is valid YAML:

```bash
python -c "import yaml; yaml.safe_load(open('.claude/commands/experts/cli/expertise.yaml'))"
```

Expected: No errors, successful parse

### Validate Line Count

Ensure expertise is under 1000-line limit:

```bash
wc -l .claude/commands/experts/cli/expertise.yaml
```

Expected: Output shows 791 lines (under 1000 limit)

### Test Self-Improve Workflow

Verify the self-improve workflow can read and validate expertise:

```bash
/experts:cli:self-improve false
```

Expected: Completes 7-phase validation without errors, confirms expertise matches codebase

### Test Question Prompt

Verify the question prompt can read and reference expertise:

```bash
/experts:cli:question "What is the CLI architecture pattern?"
```

Expected: Response references DDD pattern from expertise file with file paths

### Run Validation Commands

Execute all validation commands to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Expected: All commands pass with zero errors

## Notes

### Context Window Economics

The expertise file is designed for optimal context window usage:
- **Expertise**: 791 lines ≈ 4-6K tokens (20% of typical prompt)
- **Typical Prompt**: ~5K tokens
- **Total Context Used**: ~10K tokens
- **Claude Sonnet Limit**: 200K tokens
- **Remaining for Code**: ~190K tokens
- **Result**: 5% overhead for expert knowledge, 95% available for actual task work

### Act → Learn → Reuse Loop

This feature completes the expert lifecycle:
1. **Act**: Question prompt (Task 4) answers queries using expertise
2. **Learn**: Self-improve workflow (Task 5) validates and updates expertise
3. **Reuse**: Expertise file (Task 6) preserves knowledge across sessions

### Integration with Expert System

- CLI Expert joins CC Hook Expert as the second expert domain
- Both follow the same Act → Learn → Reuse pattern
- Future experts (ADW, Commands, Database) will follow the same template
- All experts share the expertise.yaml structure for consistency

### Jinja2 Template Escaping

The seed template uses `{{ '{{' }}` escaping to preserve Jinja2 variables in the deployed file:
- In template: `{{ '{{' }} now().strftime('%Y-%m-%d') {{ '}}' }}`
- After deployment: `{{ now().strftime('%Y-%m-%d') }}`
- This allows generated projects to have functional date generation

### FileAction.CREATE vs SKIP_IF_EXISTS

Current implementation uses `CREATE` action for template registration. For enhanced learning preservation, consider using `SKIP_IF_EXISTS` to prevent overwriting expertise during project regeneration. This ensures:
- Expertise files are never lost during `tac-bootstrap` regeneration
- Manual edits to expertise are preserved
- Learning accumulates over time rather than resetting

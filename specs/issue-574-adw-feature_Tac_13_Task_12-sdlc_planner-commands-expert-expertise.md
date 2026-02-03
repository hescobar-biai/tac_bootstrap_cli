# Feature: Commands Expert - Expertise File

## Metadata
issue_number: `574`
adw_id: `feature_Tac_13_Task_12`
issue_json: `{"number": 574, "title": "[TAC-13] Task 12: Create Commands expert - expertise file", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_12\n```\n\n**Description:**\nCreate expertise seed template and populate for Commands expert.\n\n**Technical Steps:**\n\n#### A) Create Seed Template\n**File**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/expertise.yaml.j2`\n\n**Register**:\n```python\nplan.add_file(\n    action=\"skip_if_exists\",\n    template=\"claude/commands/experts/commands/expertise.yaml.j2\",\n    path=\".claude/commands/experts/commands/expertise.yaml\",\n    reason=\"Commands expert expertise seed\"\n)\n```\n\n#### B) Populate via Self-Improve\n\n**Should document**:\n- Command structure: YAML frontmatter + Markdown\n- Variables: dynamic ($1, $2) vs static\n- Allowed-tools specifications\n- Workflow sections (numbered steps)\n- Report sections\n- 25+ existing commands\n\n**Acceptance Criteria:**\n- \u2705 Seed template + registration (skip_if_exists)\n- \u2705 Populated repo file\n- \u2705 Valid YAML under 1000 lines\n- \u2705 Documents command patterns\n- \u2705 Variable injection explained\n\n**Impacted Paths:**\n- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/expertise.yaml.j2`\n- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`\n- `.claude/commands/experts/commands/expertise.yaml`\n"}`

## Feature Description

Create the expertise seed template for the Commands expert following the TAC-13 agent experts system architecture. This completes the Commands expert triad (question prompt, self-improve workflow, and expertise file) enabling the Commands expert to maintain a mental model of the command system across sessions.

The expertise file serves as a knowledge base documenting command structure patterns, variable injection, allowed-tools specifications, workflow conventions, and report sections. This enables the Commands expert to answer questions and make decisions based on accumulated domain knowledge rather than full codebase exploration on every execution.

## User Story

As a TAC Bootstrap CLI maintainer
I want the Commands expert to have a persistent expertise file
So that the expert can maintain mental models across sessions, reducing context usage and providing consistent answers about command structure and patterns

## Problem Statement

The Commands expert (question and self-improve prompts) exists but lacks a persistent knowledge base (expertise.yaml). Without this file:

1. The Commands expert cannot maintain mental models across sessions
2. Each query requires full codebase exploration (high context usage)
3. No standardized documentation of command patterns and conventions
4. The self-improve workflow has no target file to validate/update
5. Knowledge gained from analysis is lost between sessions

## Solution Statement

Create a static YAML expertise seed template following the established pattern from CLI and ADW experts. The template provides structured sections for:

- Command structure patterns (frontmatter + markdown)
- Variable injection patterns (dynamic $1, $2 vs static)
- Allowed-tools specifications
- Workflow patterns (phase-based execution)
- Report sections
- Integration patterns (expert system, command chaining)

Register the template with `FileAction.SKIP_IF_EXISTS` to preserve local evolution. The seed starts with placeholder sections and 2-3 example commands. Population via `/experts:commands:self-improve` happens separately to analyze all 25+ commands and populate comprehensive patterns.

## Relevant Files

### Existing Files
- `.claude/commands/experts/adw/expertise.yaml` - Reference schema for ADW expert (line 1-847)
- `.claude/commands/experts/cli/expertise.yaml` - Reference schema for CLI expert (line 1-792)
- `.claude/commands/experts/commands/question.md` - Commands expert question prompt
- `.claude/commands/experts/commands/self-improve.md` - Commands expert self-improve workflow
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Registration location (lines 490-539)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/expertise.yaml.j2` - CLI expert template reference
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2` - ADW expert template reference

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/expertise.yaml.j2` - Commands expert expertise seed template
- `.claude/commands/experts/commands/expertise.yaml` - Commands expert expertise file (populated instance)

## Implementation Plan

### Phase 1: Schema Analysis
Analyze existing expertise files (CLI and ADW) to understand the consistent schema structure and ensure Commands expert follows the same pattern.

### Phase 2: Template Creation
Create the static YAML seed template with placeholder sections covering command patterns, variables, workflows, and 2-3 example commands as references.

### Phase 3: Registration
Add registration to scaffold_service.py in the expert commands section using FileAction.SKIP_IF_EXISTS to preserve local evolution.

### Phase 4: Population
Create the repository instance by running the self-improve workflow to analyze the complete command system and populate comprehensive patterns.

## Step by Step Tasks

### Task 1: Analyze Existing Expertise Schema
Read both CLI and ADW expertise files to extract the consistent schema structure. Identify common top-level sections, data patterns, and organizational conventions.

Key patterns to extract:
- Top-level sections (overview, architecture, core_implementation, etc.)
- Metadata fields (description, purpose, last_updated, total_files, key_files)
- Nested structure patterns (how subsections are organized)
- Line number reference patterns for code locations
- Example/pattern documentation style

Commands:
```bash
# Read CLI expertise for schema reference
cat .claude/commands/experts/cli/expertise.yaml | head -100

# Read ADW expertise for schema reference
cat .claude/commands/experts/adw/expertise.yaml | head -100
```

### Task 2: Create Expertise Seed Template
Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/expertise.yaml.j2` with structured placeholder sections.

Template structure:
```yaml
overview:
  description: ".claude/commands/ system - Slash commands for agent workflows"
  purpose: "Composable command system with frontmatter configuration"
  last_updated: "YYYY-MM-DD"
  total_files: <count>
  key_files:
    - ".claude/commands/feature.md"
    - ".claude/commands/implement.md"
    # 2-3 more examples

architecture:
  pattern: "YAML Frontmatter + Markdown Workflow"
  layers:
    frontmatter:
      purpose: "Configuration and tool permissions"
      # Details
    workflow:
      purpose: "Numbered execution phases"
      # Details

command_structure:
  frontmatter_patterns:
    allowed_tools: "Comma-separated tool list"
    description: "Single-line command purpose"
    argument_hint: "Variable placeholders"
    model: "sonnet/opus/haiku"
    # More patterns

  variable_patterns:
    dynamic_variables:
      purpose: "$1, $2, $3 for user-provided arguments"
      # Examples
    static_variables:
      purpose: "Predefined paths and constants"
      # Examples

workflow_patterns:
  phase_based:
    pattern: "Numbered sections (Phase 1, Phase 2, etc.)"
    # Examples from 2-3 commands

# More sections...
```

Template should be static (no Jinja2 variables like `{{ config.project.name }}`).

### Task 3: Register Template in Scaffold Service
Add registration in `scaffold_service.py` after the Commands expert self-improve prompt registration (around line 538).

Add this code block:
```python
        # TAC-13 Task 12: Commands Expert Expertise Seed
        plan.add_file(
            ".claude/commands/experts/commands/expertise.yaml",
            action=FileAction.SKIP_IF_EXISTS,  # Preserve learning
            template="claude/commands/experts/commands/expertise.yaml.j2",
            reason="Commands expert expertise seed file",
        )
```

Location: After line 538 in `_add_claude_files()` method.

### Task 4: Create Repository Instance
Create `.claude/commands/experts/commands/expertise.yaml` by copying the template content directly (without Jinja2 processing since template is static).

This serves as the initial instance that self-improve will enhance.

### Task 5: Populate via Self-Improve (Manual Step)
Run the Commands expert self-improve workflow to analyze the complete command system and populate the expertise file with comprehensive patterns.

Command:
```bash
# Execute self-improve to populate expertise
claude /experts:commands:self-improve
```

This step happens AFTER template creation and is documented for the user to execute manually. The self-improve workflow will:
1. Analyze current expertise
2. Read all .claude/commands/*.md files
3. Extract patterns (frontmatter, variables, workflows, reports)
4. Validate against reality
5. Update expertise.yaml with findings
6. Verify accuracy

### Task 6: Validate Expertise File
Verify the populated expertise.yaml meets acceptance criteria:
- Valid YAML syntax
- Under 1000 lines (soft guideline)
- Documents command patterns clearly
- Includes variable injection explanations
- Covers allowed-tools specifications
- Documents workflow and report sections

Commands:
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('.claude/commands/experts/commands/expertise.yaml'))"

# Check line count
wc -l .claude/commands/experts/commands/expertise.yaml

# Manual review of content structure
cat .claude/commands/experts/commands/expertise.yaml
```

### Task 7: Run Validation Commands
Execute all validation commands to ensure zero regressions:
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Testing Strategy

### Unit Tests
No new unit tests required - this is a template registration task. Existing scaffold_service tests cover the registration mechanism.

### Integration Tests
Manual verification:
1. Run `tac-bootstrap init test-project` and verify `.claude/commands/experts/commands/expertise.yaml` is created
2. Modify the generated expertise.yaml
3. Re-run `tac-bootstrap init test-project` in the same directory
4. Verify existing expertise.yaml is NOT overwritten (SKIP_IF_EXISTS behavior)

### Edge Cases
1. **Missing template file**: Handled by ValidationService template layer
2. **Invalid YAML syntax**: Will be caught during population via self-improve
3. **Expertise file exists**: SKIP_IF_EXISTS preserves it (correct behavior)
4. **Expertise file exceeds 1000 lines**: Soft guideline, not enforced - document but don't block

## Acceptance Criteria

- ✅ Template file exists: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/expertise.yaml.j2`
- ✅ Registration added to `scaffold_service.py` with `FileAction.SKIP_IF_EXISTS`
- ✅ Repository instance exists: `.claude/commands/experts/commands/expertise.yaml`
- ✅ Valid YAML syntax (parseable)
- ✅ Under 1000 lines (soft guideline for initial seed)
- ✅ Documents command structure patterns (frontmatter + markdown)
- ✅ Explains variable injection (dynamic $1, $2 vs static)
- ✅ Covers allowed-tools specifications
- ✅ Documents workflow patterns
- ✅ Includes report section patterns
- ✅ All validation commands pass with zero regressions

## Validation Commands

Execute all commands to validate with cero regresiones:

```bash
# Unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Linting
cd tac_bootstrap_cli && uv run ruff check .

# Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help

# YAML validation
python -c "import yaml; yaml.safe_load(open('.claude/commands/experts/commands/expertise.yaml'))"

# Integration test - verify template registration
cd tac_bootstrap_cli && uv run python -c "
from tac_bootstrap.domain.models import TACConfig
from tac_bootstrap.application.scaffold_service import ScaffoldService
from tac_bootstrap.infrastructure.template_repo import TemplateRepository
from pathlib import Path

template_repo = TemplateRepository(Path('tac_bootstrap/templates'))
service = ScaffoldService(template_repo, None)
config = TACConfig.from_file(Path('../config.yml'))
plan = service.build_plan(config)

# Check expertise file is in plan
expertise_ops = [op for op in plan.file_operations if 'experts/commands/expertise.yaml' in op.path]
assert len(expertise_ops) == 1, f'Expected 1 expertise operation, found {len(expertise_ops)}'
assert expertise_ops[0].action.value == 'skip_if_exists', f'Expected skip_if_exists, got {expertise_ops[0].action.value}'
print('✅ Template registration verified')
"
```

## Notes

### Key Design Decisions

1. **Static Template**: No Jinja2 variables needed - expertise documents command patterns, not project-specific config
2. **SKIP_IF_EXISTS**: Preserves learning across regenerations per TAC-13 architecture
3. **Focus on Patterns**: Seed includes 2-3 example commands, not all 25+ (aligns with 1000-line guideline)
4. **Separate Population**: Self-improve runs separately to populate comprehensive patterns
5. **Schema Consistency**: Follows CLI/ADW expert schema for uniformity across expert system

### TAC-13 Integration

This task completes the Commands expert triad:
- ✅ Question prompt (Task 10)
- ✅ Self-improve workflow (Task 11)
- 🔄 Expertise file (Task 12 - this feature)

After this task, the Commands expert has full Act → Learn → Reuse capability:
- **Act**: Answer questions using expertise file
- **Learn**: Self-improve validates and updates expertise
- **Reuse**: Updated expertise used for future decisions

### Context Usage Optimization

With expertise file in place, Commands expert queries will use:
- 20% context: Load expertise.yaml mental model
- 80% context: Task-specific work

Versus baseline:
- 100% context: Full codebase exploration every time

### Future Enhancements

- Hook integration to auto-run self-improve on command file changes
- Version tracking for expertise evolution
- Diff reporting to show what self-improve learned
- Cross-expert validation (CLI expert reviews Commands patterns)

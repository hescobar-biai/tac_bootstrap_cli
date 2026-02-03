# Feature: CLI Expert Self-Improve Prompt

## Metadata
issue_number: `567`
adw_id: `feature_Tac_13_Task_5`
issue_json: `{"number": 567, "title": "[TAC-13] Task 5: Create CLI expert - self-improve prompt", "body": "Create self-improve prompt for CLI expert as both Jinja2 template (for CLI generation) and implementation file (for repo root use)."}`

## Feature Description
Implement the CLI Expert self-improve prompt using the TAC-13 dual strategy pattern. This prompt enables the CLI expert to automatically validate and update its mental model (expertise.yaml) by analyzing the codebase and incorporating learnings. It implements the **Learn** step in the Act → Learn → Reuse loop, allowing the expert to evolve its knowledge after each execution.

The self-improve prompt follows a 7-phase workflow: Analyze → Read → Validate → Identify Discrepancies → Update → Enforce Constraints → Validate. It can operate in two modes: full codebase scan or targeted git diff analysis.

## User Story
As a CLI expert agent
I want to automatically validate and update my expertise file
So that my mental model stays synchronized with the actual codebase and I continuously improve from each execution

## Problem Statement
Agent experts need to maintain accurate mental models of their domain (CLI, ADW, Commands) over time. As codebases evolve, expertise files can become stale, leading to incorrect assumptions and poor decision-making. Manual maintenance of expertise files is inefficient and error-prone. There needs to be an automated mechanism for experts to:
- Detect discrepancies between their mental model and actual code
- Incorporate new knowledge from recent changes
- Validate expertise against source of truth (the code)
- Maintain YAML constraints (≤1000 lines, valid syntax)
- Learn from git diffs after modifications

## Solution Statement
Create a comprehensive self-improve prompt that implements a 7-phase validation and update workflow. The prompt analyzes the codebase (full scan or git diff), compares findings against the expertise file, identifies gaps/discrepancies, updates the expertise YAML, and enforces constraints. This is implemented using the TAC-13 dual strategy:

1. **Jinja2 Template**: Generic self-improve template in CLI generator using `{{ config.project.name }}` variables
2. **Scaffold Registration**: Register template in `scaffold_service.py` for automatic inclusion in generated projects
3. **Implementation File**: Concrete self-improve prompt for tac-bootstrap repository (repo root) for immediate local use

The prompt supports optional arguments:
- `CHECK_GIT_DIFF` (default: false) - Focus on recently changed files
- `FOCUS_AREA` (optional) - Target specific areas (e.g., "templates", "scaffold_service")

## Relevant Files

### Existing Files (for reference/registration)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Template registration (add self-improve registration)
- `ai_docs/doc/plan_tasks_tac_13.md:1150-1450` - Complete Task 5 specification with full prompt content
- `ai_docs/doc/Tac-13-agent-experts.md` - Agent expert methodology and 7-phase workflow
- `ai_docs/doc/expertise-file-structure.md` - YAML schema and 1000-line constraint rules

### Related Expert Files (for pattern matching)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2` - Advanced expert pattern example
- `.claude/commands/experts/cli/question.md` (if exists) - Related CLI expert prompt

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2` - Jinja2 template
- `.claude/commands/experts/cli/self-improve.md` - Implementation file for repo root

## Implementation Plan

### Phase 1: Foundation
1. Read Task 5 specification from `ai_docs/doc/plan_tasks_tac_13.md` (lines 1150-1450) to get complete prompt content
2. Read expert methodology from `ai_docs/doc/Tac-13-agent-experts.md` to understand 7-phase workflow
3. Review expertise file constraints from `ai_docs/doc/expertise-file-structure.md` (1000-line limit, YAML validation)
4. Examine existing expert templates for patterns (cc_hook_expert examples)
5. Locate registration method in `scaffold_service.py` (_add_claude_code_commands or similar)

### Phase 2: Core Implementation
1. **Create Jinja2 Template** (`tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2`):
   - Add frontmatter with allowed-tools, description, argument-hint, model
   - Define variables: CHECK_GIT_DIFF ($1), FOCUS_AREA ($2), EXPERTISE_FILE, CLI_ROOT (use `{{ config.project.name }}`)
   - Implement 7 phases:
     - Phase 1: Analyze Scope (git diff or full scan)
     - Phase 2: Read Codebase (targeted file reads)
     - Phase 3: Validate Expertise (compare mental model vs code)
     - Phase 4: Identify Discrepancies (gaps, outdated info, false claims)
     - Phase 5: Update Expertise (surgical YAML edits)
     - Phase 6: Enforce Constraints (validate ≤1000 lines, YAML syntax)
     - Phase 7: Validate Result (re-read and verify)
   - Use `{{ config.project.name }}` for project-specific references
   - Keep static logic (7-phase workflow) identical to implementation file

2. **Create Implementation File** (`.claude/commands/experts/cli/self-improve.md`):
   - Same structure as Jinja2 template but with hardcoded values:
     - CLI_ROOT: `tac_bootstrap_cli/tac_bootstrap/`
     - Project name: `tac-bootstrap`
   - Complete 7-phase workflow with detailed instructions
   - Include example executions and validation commands

3. **Register Template in scaffold_service.py**:
   - Find `_add_claude_code_commands()` method
   - Add registration call:
     ```python
     # TAC-13: CLI Expert Self-Improve
     plan.add_file(
         action="create",
         template="claude/commands/experts/cli/self-improve.md.j2",
         path=".claude/commands/experts/cli/self-improve.md",
         reason="CLI expert 7-phase self-improve workflow"
     )
     ```

### Phase 3: Integration
1. Verify template directory structure exists: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/`
2. Verify repo directory structure exists: `.claude/commands/experts/cli/`
3. Create directories if missing (mkdir -p)
4. Test template rendering (if test infrastructure exists)
5. Validate registration with grep check

## Step by Step Tasks

### Task 1: Read Task 5 Specification
- Read `ai_docs/doc/plan_tasks_tac_13.md` lines 1150-1450
- Extract complete prompt content for self-improve
- Note variables, phases, and workflow structure

### Task 2: Review Expert Patterns
- Read `ai_docs/doc/Tac-13-agent-experts.md` for 7-phase methodology
- Read `ai_docs/doc/expertise-file-structure.md` for YAML constraints
- Review `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2` for template patterns

### Task 3: Create Jinja2 Template
- Create directory: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/`
- Write `self-improve.md.j2` with complete 7-phase workflow
- Use `{{ config.project.name }}` for project-specific references
- Add frontmatter: `allowed-tools: Read, Grep, Glob, Bash, Edit, Write, TodoWrite`

### Task 4: Create Implementation File
- Create directory: `.claude/commands/experts/cli/`
- Write `self-improve.md` with hardcoded tac-bootstrap values
- CLI_ROOT: `tac_bootstrap_cli/tac_bootstrap/`
- EXPERTISE_FILE: `.claude/commands/experts/cli/expertise.yaml`

### Task 5: Register Template
- Read `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate `_add_claude_code_commands()` method
- Add registration call with action="create"
- Use template path: `claude/commands/experts/cli/self-improve.md.j2`

### Task 6: Execute Validation Commands
- Run all validation commands to ensure zero regressions
- Verify template exists
- Verify registration in scaffold_service.py
- Verify repo implementation file exists
- Run pytest, ruff, mypy, smoke test

## Testing Strategy

### Unit Tests
- If test infrastructure exists for template rendering, add test case for `self-improve.md.j2`
- Verify Jinja2 variables render correctly with sample config
- Test template path resolution

### Edge Cases
- Missing expertise.yaml file (should prompt to create with Task 6 - seed file)
- Git diff mode with no changes (should report "no changes to analyze")
- Expertise file exceeds 1000 lines (should compress/remove deprecated sections)
- Invalid YAML syntax after update (should validate and fix)
- FOCUS_AREA that doesn't match any code sections (should report and fall back to full scan)

## Acceptance Criteria

1. **Jinja2 Template Created**:
   - File exists: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2`
   - Contains 7-phase workflow (Analyze, Read, Validate, Identify, Update, Enforce, Validate)
   - Uses `{{ config.project.name }}` for project-specific values
   - Frontmatter includes: allowed-tools, description, argument-hint, model

2. **Template Registered**:
   - Registration exists in `scaffold_service.py`
   - Uses `action="create"` (not skip_if_exists, since prompts regenerate)
   - Template path: `claude/commands/experts/cli/self-improve.md.j2`
   - Output path: `.claude/commands/experts/cli/self-improve.md`
   - Reason: "CLI expert 7-phase self-improve workflow"

3. **Implementation File Created**:
   - File exists: `.claude/commands/experts/cli/self-improve.md`
   - Hardcoded for tac-bootstrap project
   - CLI_ROOT: `tac_bootstrap_cli/tac_bootstrap/`
   - Same 7-phase workflow as template

4. **Validation Passes**:
   ```bash
   # Template exists
   test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2 && echo "✓ Template"

   # Registration exists
   grep -A 3 "self-improve.md.j2" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered"

   # Repo file exists
   test -f .claude/commands/experts/cli/self-improve.md && echo "✓ Repo file"
   ```

5. **All Tests Pass**:
   - Unit tests: 100% pass
   - Linting: zero errors
   - Type checking: zero errors
   - Smoke test: CLI runs without errors

## Validation Commands
Execute all validation commands to ensure zero regressions:

- `test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2 && echo "✓ Template exists" || echo "✗ Template missing"`
- `grep -A 3 "self-improve.md.j2" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered" || echo "✗ Not registered"`
- `test -f .claude/commands/experts/cli/self-improve.md && echo "✓ Repo file exists" || echo "✗ Repo file missing"`
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short` - Unit tests
- `cd tac_bootstrap_cli && uv run ruff check .` - Linting
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/` - Type checking
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help` - Smoke test

## Notes

**TAC-13 Dual Strategy Pattern**:
- This task follows the dual strategy: template (.j2) + registration + implementation file
- Template is for CLI generation (generic, uses Jinja2 variables)
- Implementation file is for immediate use in tac-bootstrap repo (hardcoded values)
- Registration ensures template is included when generating new projects

**7-Phase Self-Improve Workflow**:
1. **Analyze Scope**: Determine what to analyze (git diff or full scan)
2. **Read Codebase**: Read relevant files based on scope
3. **Validate Expertise**: Compare mental model against actual code
4. **Identify Discrepancies**: Find gaps, outdated info, false claims
5. **Update Expertise**: Make surgical edits to YAML
6. **Enforce Constraints**: Validate ≤1000 lines, YAML syntax
7. **Validate Result**: Re-read and verify changes

**Expertise File Constraints**:
- Maximum 1000 lines (strict limit to preserve context budget)
- Valid YAML syntax (must parse correctly)
- 10-section structure: overview, core_implementation, schema, operations, data_flow, performance, best_practices, issues, changes, deprecated
- Mental model (working memory), not source of truth (code is truth)

**Integration with Other Tasks**:
- Task 4: CLI Expert - Question prompt (read-only queries)
- Task 6: CLI Expert - Expertise seed file (initial mental model)
- Task 13: Meta-Prompt Generator (uses self-improve as example)

**Future Enhancements**:
- Automatic git diff analysis after commits
- Integration with ADW workflows (auto self-improve after builds)
- Metrics tracking (expertise quality over time)

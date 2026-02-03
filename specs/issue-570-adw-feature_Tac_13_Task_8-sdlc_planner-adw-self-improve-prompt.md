# Feature: ADW Expert Self-Improve Prompt

## Metadata
issue_number: `570`
adw_id: `feature_Tac_13_Task_8`
issue_json: `{"number": 570, "title": "[TAC-13] Task 8: Create ADW expert - self-improve prompt", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_8\n```\n\n**Description:**\nCreate self-improve prompt for ADW expert as both template and implementation.\n\n**Technical Steps:**\n\n#### A) Create Jinja2 Template in CLI\n\n1. **Create template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2`\n\n2. **Register in scaffold_service.py**:\n   ```python\n   # TAC-13: ADW Expert Self-Improve\n   plan.add_file(\n       action=\"create\",\n       template=\"claude/commands/experts/adw/self-improve.md.j2\",\n       path=\".claude/commands/experts/adw/self-improve.md\",\n       reason=\"ADW expert 7-phase self-improve workflow\"\n   )\n   ```\n\n#### B) Create Implementation in Repo Root\n\n**File**: `.claude/commands/experts/adw/self-improve.md`\n- 7-phase workflow (same as CLI expert)\n- Variables: `CHECK_GIT_DIFF: $1`, `FOCUS_AREA: $2`, `MAX_LINES: 1000`\n- Focus areas: state management, GitHub integration, workflow orchestration\n\n**Acceptance Criteria:**\n- \u2705 **Template (.j2)** created and registered\n- \u2705 **Implementation** in repo root\n- \u2705 Follows TAC-13 7-phase pattern\n- \u2705 Focus areas documented: state, GitHub, orchestration\n\n**Validation Commands:**\n```bash\ntest -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2 && echo \"\u2713 Template\"\ngrep \"experts/adw/self-improve.md.j2\" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo \"\u2713 Registered\"\ntest -f .claude/commands/experts/adw/self-improve.md && echo \"\u2713 Repo file\"\n```\n\n**Impacted Paths:**\n- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2` (template)\n- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` (registration)\n- `.claude/commands/experts/adw/self-improve.md` (repo root)"}`

## Feature Description

Create a self-improvement prompt for the ADW (AI Developer Workflow) expert agent following the TAC-13 dual strategy pattern. This enables the ADW expert to validate and update its mental model (expertise.yaml) by comparing it against the actual codebase, implementing the "Learn" phase in the Act → Learn → Reuse cycle.

The feature follows the TAC-13 7-phase self-improve workflow established for expert agents:
1. Check git diff (optional)
2. Read current expertise
3. Validate against codebase
4. Identify discrepancies
5. Update expertise
6. Enforce line limit (1000 lines max)
7. Validate YAML syntax

This implementation must be delivered as:
- **Template (.j2)**: Jinja2 template for CLI generation
- **Registration**: Entry in scaffold_service.py
- **Implementation**: Working file in repo root `.claude/commands/`

## User Story

As an ADW expert agent
I want to automatically validate and update my mental model against the actual codebase
So that my expertise stays current and accurate as the ADW system evolves

## Problem Statement

The ADW expert needs a systematic way to maintain its expertise.yaml mental model. Without a self-improve workflow, the expertise file becomes stale as the codebase evolves, leading to:
- Outdated line numbers and file references
- Missing new workflows or modules
- Incorrect workflow orchestration patterns
- Gaps in coverage for new ADW features

The agent needs a standardized, repeatable process to validate its knowledge against reality and automatically update its mental model while enforcing constraints (line limits, YAML validity).

## Solution Statement

Create a self-improve prompt (`.claude/commands/experts/adw/self-improve.md`) that implements the TAC-13 7-phase validation workflow specifically tailored for ADW domain expertise. The prompt will:

1. Optionally analyze git diffs to focus on recently changed ADW files
2. Read and parse the current expertise.yaml file
3. Systematically validate expertise claims against actual ADW codebase files
4. Identify discrepancies (outdated, missing, incorrect information)
5. Apply surgical updates to expertise file using Edit/Write tools
6. Compress expertise if over 1000 lines while preserving high-value knowledge
7. Validate YAML syntax and structure before completing

The prompt will be delivered as:
- **Jinja2 template** for CLI generation (can be customized per project)
- **Registered** in scaffold_service.py for automatic scaffolding
- **Implementation** in repo root for immediate use

Focus areas specific to ADW domain:
- State management (adw_modules/state.py)
- GitHub integration (adw_modules/github.py, git_ops.py)
- Workflow orchestration (adw_modules/workflow_ops.py, tool_sequencer.py)
- Worktree management (adw_modules/worktree_ops.py)
- Core isolated workflows (adw_*_iso.py patterns)

## Relevant Files

Files to understand patterns and implement the feature:

### Existing Expert Self-Improve Files (Reference Patterns)
- `.claude/commands/experts/cli/self-improve.md` - CLI expert self-improve (reference for structure)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/self-improve.md.j2` - CLI template (reference pattern)

### ADW Expert Files (Same Domain)
- `.claude/commands/experts/adw/question.md` - ADW expert question prompt (same domain)
- `.claude/commands/experts/adw/expertise.yaml` - The mental model this prompt will update

### ADW Codebase Files (Validation Targets)
- `adws/adw_modules/` - All ADW infrastructure modules
  - `state.py` - State persistence
  - `github.py` - GitHub API operations
  - `git_ops.py` - Git operations
  - `workflow_ops.py` - Workflow orchestration
  - `worktree_ops.py` - Worktree management
  - `tool_sequencer.py` - Tool sequence orchestration
- `adws/adw_*_iso.py` - Isolated ADW workflows

### Scaffold Service (Registration)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Where registration happens (lines 480-540)

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2` - Jinja2 template
- `.claude/commands/experts/adw/self-improve.md` - Implementation in repo root

## Implementation Plan

### Phase 1: Foundation
1. Analyze CLI expert self-improve prompt structure and workflow
2. Identify ADW-specific focus areas and validation patterns
3. Map ADW codebase structure for validation targets

### Phase 2: Core Implementation
1. Create Jinja2 template with 7-phase workflow
2. Adapt validation phase for ADW domain (modules, workflows, state management)
3. Create implementation file in repo root
4. Register template in scaffold_service.py

### Phase 3: Integration
1. Verify template registration follows existing patterns
2. Test template can be properly rendered
3. Validate YAML expertise file can be read/updated by prompt

## Step by Step Tasks

### Task 1: Create Jinja2 Template
Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2` based on CLI expert pattern but customized for ADW domain:
- Use CLI self-improve template as base structure
- Customize Phase 3 validation for ADW files (adws/ directory)
- Update focus areas to: state management, GitHub integration, workflow orchestration, worktree operations
- Update file paths to use ADW-specific locations
- Keep generic Jinja2 variables for project customization

### Task 2: Register Template in Scaffold Service
Add registration entry in `scaffold_service.py` within the expert_commands list (around line 490-512):
```python
# TAC-13 Task 8: ADW Expert Self-Improve
("experts/adw/self-improve.md", "ADW expert 7-phase self-improve workflow"),
```
This follows the pattern established for CLI expert self-improve.

### Task 3: Create Implementation in Repo Root
Create `.claude/commands/experts/adw/self-improve.md` as the working implementation:
- Copy structure from Jinja2 template but with concrete values
- Set expertise file path: `.claude/commands/experts/adw/expertise.yaml`
- Set ADW root: `adws/` and `adws/adw_modules/`
- Document ADW-specific focus areas in Phase 1
- Customize validation commands in Phase 3 for ADW structure

### Task 4: Validate Template Registration
Verify the template is properly registered:
```bash
# Check template file exists
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2 && echo "✓ Template exists"

# Check registration in scaffold service
grep -n "experts/adw/self-improve.md" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered"
```

### Task 5: Validate Implementation File
Verify the implementation file works:
```bash
# Check implementation exists
test -f .claude/commands/experts/adw/self-improve.md && echo "✓ Implementation exists"

# Validate frontmatter and structure
head -20 .claude/commands/experts/adw/self-improve.md | grep -E "^(allowed-tools|description|model):" && echo "✓ Valid frontmatter"

# Check for 7 phases
grep -c "^### Phase" .claude/commands/experts/adw/self-improve.md
# Should output: 7
```

### Task 6: Run Validation Commands
Execute all validation commands from acceptance criteria:
```bash
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2 && echo "✓ Template"
grep "experts/adw/self-improve.md.j2" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered"
test -f .claude/commands/experts/adw/self-improve.md && echo "✓ Repo file"
```

All commands should pass with checkmarks.

## Testing Strategy

### Unit Tests
Not applicable - this is a prompt template, not executable code. Validation is done through:
1. File existence checks
2. Grep pattern matching for registration
3. YAML frontmatter validation
4. Manual review of 7-phase structure

### Integration Tests
Manual integration test:
1. Run CLI generation in a test project to verify template renders correctly
2. Verify generated prompt can read ADW expertise.yaml
3. Test prompt can validate against ADW codebase structure
4. Confirm prompt can update expertise file without breaking YAML

### Edge Cases
1. **Empty expertise file**: Prompt should handle missing or empty expertise.yaml
2. **Over 1000 lines**: Compression strategies should activate in Phase 6
3. **Invalid YAML**: Phase 7 should catch and fix syntax errors
4. **Missing ADW files**: Validation should report missing files gracefully
5. **Git diff with no changes**: Phase 1 should skip cleanly when no diffs

## Acceptance Criteria

- ✅ Template file exists at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2`
- ✅ Template is registered in `scaffold_service.py` within expert_commands list
- ✅ Implementation file exists at `.claude/commands/experts/adw/self-improve.md`
- ✅ Implementation follows 7-phase TAC-13 workflow pattern
- ✅ Frontmatter includes: allowed-tools, description, argument-hint, model
- ✅ Variables defined: CHECK_GIT_DIFF ($1), FOCUS_AREA ($2), MAX_LINES (1000)
- ✅ Focus areas documented: state management, GitHub integration, workflow orchestration, worktree operations
- ✅ Phase 3 validation targets ADW-specific files (adws/ directory structure)
- ✅ Report format includes all 7 phases with specific ADW context
- ✅ All validation commands pass successfully

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Template existence
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2 && echo "✓ Template exists"

# Registration check
grep "experts/adw/self-improve.md" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered in scaffold service"

# Implementation existence
test -f .claude/commands/experts/adw/self-improve.md && echo "✓ Implementation exists"

# Frontmatter validation
grep -E "^(allowed-tools|description|argument-hint|model):" .claude/commands/experts/adw/self-improve.md && echo "✓ Valid frontmatter"

# Phase count validation
phase_count=$(grep -c "^### Phase" .claude/commands/experts/adw/self-improve.md)
[ "$phase_count" -eq 7 ] && echo "✓ Has 7 phases" || echo "✗ Expected 7 phases, found $phase_count"

# Variables validation
grep -E "CHECK_GIT_DIFF.*\$1" .claude/commands/experts/adw/self-improve.md && echo "✓ CHECK_GIT_DIFF variable"
grep -E "FOCUS_AREA.*\$2" .claude/commands/experts/adw/self-improve.md && echo "✓ FOCUS_AREA variable"
grep -E "MAX_LINES.*1000" .claude/commands/experts/adw/self-improve.md && echo "✓ MAX_LINES constraint"

# ADW-specific focus areas
grep -i "state management" .claude/commands/experts/adw/self-improve.md && echo "✓ State management focus area"
grep -i "github integration" .claude/commands/experts/adw/self-improve.md && echo "✓ GitHub integration focus area"
grep -i "workflow orchestration" .claude/commands/experts/adw/self-improve.md && echo "✓ Workflow orchestration focus area"

# Standard validation commands (from issue)
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/self-improve.md.j2 && echo "✓ Template"
grep "experts/adw/self-improve.md.j2" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Registered"
test -f .claude/commands/experts/adw/self-improve.md && echo "✓ Repo file"

# Unit tests (if applicable)
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short -k "adw or expert" 2>/dev/null || echo "⚠ No tests found (expected for prompts)"

# Linting (template syntax)
cd tac_bootstrap_cli && uv run ruff check . 2>/dev/null || echo "⚠ No Python linting needed for markdown"

# Type checking (not applicable for markdown)
echo "⚠ Type checking skipped (markdown files)"

# Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help >/dev/null && echo "✓ CLI smoke test passed"
```

## Notes

### ADW-Specific Considerations
- ADW expertise should focus on workflow orchestration patterns
- State management is critical (state.py patterns)
- GitHub integration patterns are high-value (github.py, git_ops.py)
- Worktree operations are complex and worth documenting
- Tool sequencer patterns should be captured

### Focus Areas for ADW Expert
1. **State Management**: How ADW persists workflow state across executions
2. **GitHub Integration**: API patterns, authentication, operations
3. **Workflow Orchestration**: How isolated workflows coordinate
4. **Worktree Operations**: Complex git worktree patterns
5. **Tool Sequencing**: How tools are orchestrated in workflows

### Template Variables
The Jinja2 template should support customization:
- Project-specific paths
- Custom focus areas
- Different expertise file locations
- Variable ADW module structures

### Compression Strategies
If expertise exceeds 1000 lines:
1. Consolidate similar workflow patterns
2. Remove old recent_changes entries (keep latest 5)
3. Use line ranges instead of detailed method listings
4. Focus on non-obvious patterns (remove self-evident information)

### Next Steps After Implementation
1. Test self-improve prompt with actual ADW expertise.yaml
2. Run self-improve after ADW changes to validate it catches updates
3. Consider implementing ADW expert expertise.yaml seed (Task 9)
4. Document ADW expert usage patterns in fractal docs

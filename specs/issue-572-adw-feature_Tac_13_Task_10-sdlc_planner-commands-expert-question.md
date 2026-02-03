# Feature: Commands Expert - Question Prompt

## Metadata
issue_number: `572`
adw_id: `feature_Tac_13_Task_10`
issue_json: `{"number": 572, "title": "[TAC-13] Task 10: Create Commands expert - question prompt", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_10\n```\n\n**Description:**\nCreate question prompt for Commands expert as template and implementation.\n\n**Technical Steps:**\n\n#### A) Create Template in CLI\n**File**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2`\n\n**Register**:\n```python\nplan.add_file(\n    action=\"create\",\n    template=\"claude/commands/experts/commands/question.md.j2\",\n    path=\".claude/commands/experts/commands/question.md\",\n    reason=\"Commands expert question prompt\"\n)\n```\n\n#### B) Create Implementation in Repo Root\n**File**: `.claude/commands/experts/commands/question.md`\n- 3-phase workflow\n- Variables: `USER_QUESTION: $1`, `EXPERTISE_PATH`\n\n**Acceptance Criteria:**\n- ✅ Template + registration + repo file\n- ✅ Follows TAC-13 question pattern\n- ✅ Answers about command structure, variables, workflows\n\n**Impacted Paths:**\n- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2`\n- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`\n- `.claude/commands/experts/commands/question.md`"}`

## Feature Description

Create a Commands expert question prompt that follows the TAC-13 Agent Expert pattern for self-improving agents. This prompt enables agents to answer questions about the `.claude/commands/*` ecosystem by leveraging a mental model (expertise file) while validating against actual command files as the source of truth.

The Commands expert will understand:
- Command file structure and naming conventions
- Variable usage patterns (`$1`, `$2`, etc.)
- Phase-based workflow patterns
- Tool restrictions and permissions
- Integration patterns between commands
- Expert command architecture

This is the "Reuse" phase of the Act → Learn → Reuse loop, where the agent reads existing expertise and validates it against code before answering.

## User Story

As a developer using tac-bootstrap generated projects
I want to ask questions about slash commands and get accurate, evidence-based answers
So that I can understand command patterns, variables, workflows, and integration points without manually exploring all command files

## Problem Statement

When working with `.claude/commands/` directory:
- Developers need to understand command structure and conventions
- Variable usage patterns (`$1`, `$2`) are not immediately obvious
- Phase-based workflow patterns require context
- Tool restrictions vary across commands
- Integration patterns between commands are complex
- Expert commands have specialized patterns that need explanation

Without a Commands expert, developers must:
- Manually read multiple command files
- Reverse-engineer patterns from examples
- Risk missing non-obvious conventions
- Lack understanding of "why" behind patterns

## Solution Statement

Implement a Commands expert question prompt following the TAC-13 3-phase pattern:

**Phase 1: REUSE** - Read `.claude/expertise/commands.yaml` mental model
**Phase 2: VALIDATE** - Check actual `.claude/commands/*` files as source of truth
**Phase 3: ANSWER** - Provide evidence-based response with file:line citations

The prompt will:
- Be read-only (tools: Bash, Read, Grep, Glob, TodoWrite)
- Mirror ADW expert structure from Task 9
- Answer questions about command structure, variables, workflows
- Validate expertise against actual command files
- Report discrepancies between mental model and code

## Relevant Files

### Existing Reference Files
- `.claude/commands/experts/adw/question.md` - Reference implementation to mirror
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2` - Template pattern to follow
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:515-522` - Registration pattern for ADW expert
- `ai_docs/doc/plan_tasks_tac_13.md` - Complete TAC-13 task specifications
- `ai_docs/doc/Tac-13-agent-experts.md` - Agent expert methodology

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2` - Jinja2 template for CLI generation
- `.claude/commands/experts/commands/question.md` - Concrete implementation in repo root

### Modified Files
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Add registration for Commands expert question prompt

## Implementation Plan

### Phase 1: Foundation
1. Create directory structure for Commands expert templates
2. Review ADW expert question prompt structure (reference implementation)
3. Identify Commands-specific terminology and patterns
4. Define variables: `USER_QUESTION: $1`, `EXPERTISE_PATH: .claude/expertise/commands.yaml`
5. Define read-only tool restrictions: Bash, Read, Grep, Glob, TodoWrite

### Phase 2: Core Implementation
1. Create Jinja2 template: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2`
   - Copy structure from ADW expert template
   - Adapt frontmatter (allowed-tools, description, argument-hint)
   - Customize Phase 1 (read expertise) for Commands domain
   - Customize Phase 2 (validate) for `.claude/commands/*` patterns
   - Customize Phase 3 (report) for command-specific evidence format
   - Update edge cases and key concepts for Commands domain

2. Create concrete implementation: `.claude/commands/experts/commands/question.md`
   - No Jinja2 variables (except project name if needed)
   - Use shell variable expansion for runtime args (`$1`)
   - Ensure identical structure to template

3. Register in scaffold service: `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
   - Add to expert_commands list after ADW expert registration
   - Follow pattern: `("experts/commands/question.md", "Commands expert question prompt for command structure queries")`

### Phase 3: Integration
1. Verify template renders correctly
2. Ensure registration creates file at correct path
3. Validate read-only tool restrictions
4. Confirm variable substitution works correctly
5. Test that expertise file path reference is correct (even though file doesn't exist yet)

## Step by Step Tasks

### Task 1: Create Template Directory
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/` directory
- Verify directory structure mirrors ADW expert pattern

### Task 2: Analyze ADW Expert Reference
- Read `.claude/commands/experts/adw/question.md` (lines 1-289)
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2`
- Identify structural components: frontmatter, phases, report format, edge cases
- Note ADW-specific terminology to replace with Commands-specific terms

### Task 3: Create Jinja2 Template
- File: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2`
- Copy ADW expert structure
- Update frontmatter:
  - `description: Answer questions about command structure and workflows without coding`
  - Keep `allowed-tools: Bash, Read, Grep, Glob, TodoWrite`
- Update variables section:
  - `USER_QUESTION: $1`
  - `EXPERTISE_PATH: .claude/commands/experts/commands/expertise.yaml`
  - `COMMANDS_ROOT: .claude/commands/`
- Update Phase 1 instructions for Commands expertise YAML structure
- Update Phase 2 validation for command file patterns
- Update Phase 3 report format for command-specific evidence
- Update edge cases for Commands domain
- Update key concepts section for command patterns

### Task 4: Create Concrete Implementation
- File: `.claude/commands/experts/commands/question.md`
- Copy from Jinja2 template
- Replace `{{ config.project.name }}` with `tac_bootstrap` (if used)
- Ensure no Jinja2 syntax remains
- Keep shell variable `$1` for runtime expansion

### Task 5: Register in Scaffold Service
- File: `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate expert_commands list (around line 510-522)
- Add after ADW expert question registration:
```python
# TAC-13 Task 10: Commands Expert - Question Prompt
expert_commands.append(
    ("experts/commands/question.md", "Commands expert question prompt for command structure queries")
)
```

### Task 6: Validation Commands
- Run all validation commands to ensure zero regressions
- Verify template file exists and has valid YAML frontmatter
- Verify concrete implementation exists
- Verify registration code compiles
- Test template rendering (if possible without full CLI run)

## Testing Strategy

### Unit Tests
No unit tests required - this is a prompt template, not executable code.

### Validation Tests
1. **File Existence**:
   - `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2` exists
   - `.claude/commands/experts/commands/question.md` exists

2. **Frontmatter Validation**:
   - YAML frontmatter parses correctly
   - `allowed-tools` only includes: Bash, Read, Grep, Glob, TodoWrite
   - `description` is accurate and concise
   - `argument-hint: [question]` is present
   - `model: sonnet` is set

3. **Variable Validation**:
   - `$1` is used for USER_QUESTION
   - `EXPERTISE_PATH` points to `.claude/expertise/commands.yaml`
   - `COMMANDS_ROOT` points to `.claude/commands/`

4. **Structure Validation**:
   - Phase 1: Read Expertise File
   - Phase 2: Validate Expertise Against Codebase
   - Phase 3: Report Findings
   - Report Format section exists
   - Example Execution section exists
   - Edge Cases section exists
   - Key Concepts section exists

5. **Registration Validation**:
   - scaffold_service.py compiles without errors
   - Registration follows existing pattern
   - Comment includes "TAC-13 Task 10"

### Edge Cases
1. **Missing Commands Directory**: Handle case where `.claude/commands/` doesn't exist
2. **Empty Expertise File**: Work gracefully with empty or missing expertise
3. **Malformed YAML**: Parse errors should fall back to code-only analysis
4. **Non-existent Commands**: Guide user to available commands
5. **Nested Command Structure**: Handle subdirectories like `experts/*/`, `e2e/*`

## Acceptance Criteria

1. ✅ **Template Created**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2` exists with valid structure
2. ✅ **Implementation Created**: `.claude/commands/experts/commands/question.md` exists and mirrors template
3. ✅ **Registration Complete**: scaffold_service.py includes Commands expert question registration
4. ✅ **TAC-13 Pattern Followed**: 3-phase workflow (Reuse → Validate → Answer)
5. ✅ **Read-Only Tools**: Only Bash, Read, Grep, Glob, TodoWrite allowed
6. ✅ **Variables Defined**: USER_QUESTION ($1), EXPERTISE_PATH, COMMANDS_ROOT
7. ✅ **Answers Command Topics**: Structure, variables, workflows, tool restrictions, integration patterns
8. ✅ **Evidence-Based**: Report format includes file:line citations
9. ✅ **Mirrors ADW Expert**: Consistent structure with ADW expert from Task 9
10. ✅ **No Jinja2 in Implementation**: Concrete file has no template syntax

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Test 1: File existence
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/question.md.j2 && echo "✅ Template exists" || echo "❌ Template missing"

test -f .claude/commands/experts/commands/question.md && echo "✅ Implementation exists" || echo "❌ Implementation missing"

# Test 2: YAML frontmatter validation
head -6 .claude/commands/experts/commands/question.md | grep -q "allowed-tools: Bash, Read, Grep, Glob, TodoWrite" && echo "✅ Read-only tools verified" || echo "❌ Wrong tools"

# Test 3: Registration verification
grep -q "experts/commands/question.md" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✅ Registration found" || echo "❌ Not registered"

# Test 4: Unit tests (if applicable)
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Test 5: Linting
cd tac_bootstrap_cli && uv run ruff check .

# Test 6: Type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Test 7: Smoke test
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

1. **Expertise File Not Created**: Task 12 will create `.claude/expertise/commands.yaml`. This task only creates the question prompt that references it.

2. **Consistent Pattern**: Mirror ADW expert structure exactly to maintain architectural consistency across expert domains.

3. **Commands-Specific Knowledge**:
   - Command frontmatter: `allowed-tools`, `description`, `argument-hint`, `model`
   - Variable patterns: `$1`, `$2`, etc. for shell expansion
   - Phase-based workflows: multi-step instructions with Phase 1, 2, 3
   - Tool restrictions: Different commands have different tool permissions
   - Integration patterns: Commands call other commands or trigger workflows

4. **Read-Only Focus**: Question prompts never modify code - they only read expertise, validate against code, and report findings.

5. **Evidence-Based Answers**: Always include file:line citations in answers to ensure traceability to source code.

6. **Validation Priority**: "Code is the source of truth; expertise files are auxiliary mental models."

7. **Future Integration**: When expertise file is created (Task 12), this question prompt will immediately work without modifications.

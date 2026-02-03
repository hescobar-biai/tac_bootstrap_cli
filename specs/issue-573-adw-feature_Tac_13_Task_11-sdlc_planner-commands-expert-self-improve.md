# Feature: Commands Expert Self-Improve Prompt

## Metadata
issue_number: `573`
adw_id: `feature_Tac_13_Task_11`
issue_json: `{"number": 573, "title": "[TAC-13] Task 11: Create Commands expert - self-improve prompt", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_11\n```\n\n**Description:**\nCreate self-improve prompt for Commands expert.\n\n**Technical Steps:**\n\n#### A) Create Template in CLI\n**File**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/self-improve.md.j2`\n\n**Register**:\n```python\nplan.add_file(\n    action=\"create\",\n    template=\"claude/commands/experts/commands/self-improve.md.j2\",\n    path=\".claude/commands/experts/commands/self-improve.md\",\n    reason=\"Commands expert 7-phase workflow\"\n)\n```\n\n#### B) Create Implementation\n**File**: `.claude/commands/experts/commands/self-improve.md`\n- 7-phase workflow\n- Focus: command syntax, variable injection, patterns\n\n**Acceptance Criteria:**\n- ✅ Template + registration + repo file\n- ✅ 7-phase pattern\n- ✅ Focus areas documented\n\n**Impacted Paths:**\n- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/self-improve.md.j2`\n- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`\n- `.claude/commands/experts/commands/self-improve.md`\n"}`

## Feature Description

This feature implements the **Learn** step of the Act → Learn → Reuse loop for the Commands Expert. The self-improve prompt enables the Commands expert to automatically update its mental model (expertise.yaml) by analyzing recent changes to command files, validating expertise against the actual codebase, and incorporating new knowledge about command structure and patterns.

The Commands expert focuses on the `.claude/commands/` domain, which includes:
- Command frontmatter structure (YAML with allowed-tools, description, argument-hint, model)
- Variable patterns (shell expansion with $1, $2, etc.)
- Phase-based workflow patterns
- Tool restrictions and permission scoping
- Integration patterns (command chaining, expert workflows)
- Template registration in scaffold_service.py
- Dual strategy compliance (CLI templates + repo implementations)

## User Story

As a TAC Bootstrap maintainer or generated project user
I want the Commands expert to self-improve its understanding of command patterns
So that the expert's knowledge stays synchronized with the evolving command structure and can provide accurate guidance

## Problem Statement

The Commands expert needs a systematic way to learn from changes to command files. Currently, expertise files become stale as commands are added, modified, or refactored. Without a self-improve mechanism, the expert's mental model drifts from reality, leading to outdated answers and recommendations.

This is part of the TAC-13 Agent Experts initiative to build self-improving agents that address the fundamental problem: "agents forget and don't learn."

## Solution Statement

Implement a 7-phase self-improve workflow that:
1. Analyzes recent git changes to command files (optional)
2. Reads the current expertise.yaml mental model
3. Validates expertise claims against actual command files
4. Identifies discrepancies (outdated, missing, incorrect information)
5. Updates the expertise file with corrections
6. Enforces the 1000-line limit through compression
7. Validates YAML syntax before completion

The prompt follows the proven pattern established by CLI and ADW expert self-improve prompts, adapted to focus on Commands-specific concerns: command syntax, variable injection patterns, template registration, and dual strategy compliance.

## Relevant Files

Files necessary for implementing this feature:

### Existing Reference Files
- `.claude/commands/experts/cli/self-improve.md` - CLI expert self-improve pattern (reference)
- `.claude/commands/experts/adw/self-improve.md` - ADW expert self-improve pattern (reference)
- `.claude/commands/experts/commands/question.md` - Commands expert question prompt (domain context)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Template registration (lines 484-540)
- `.claude/commands/` - Command files to validate against (entire directory)
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/` - Template source files

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/self-improve.md.j2` - Jinja2 template for CLI generation
- `.claude/commands/experts/commands/self-improve.md` - Implementation file for immediate use

## Implementation Plan

### Phase 1: Foundation
Create the template infrastructure and directory structure.

**Actions:**
1. Create directories if needed: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/`
2. Create the Jinja2 template file with standard frontmatter
3. Implement the 7-phase workflow structure based on CLI/ADW patterns

### Phase 2: Core Implementation
Build the self-improve workflow with Commands-specific validation.

**Actions:**
1. Adapt the 7-phase workflow to Commands domain:
   - Phase 1: Git diff analysis for `.claude/commands/` changes
   - Phase 2: Read current Commands expertise
   - Phase 3: Validate command frontmatter, variables, phases, tool restrictions
   - Phase 4: Identify discrepancies in command patterns
   - Phase 5: Update expertise with corrections
   - Phase 6: Enforce 1000-line limit
   - Phase 7: YAML syntax validation

2. Add Commands-specific validation logic:
   - Frontmatter structure (allowed-tools, description, argument-hint, model)
   - Variable patterns ($1, $2 usage and documentation)
   - Phase-based workflow patterns
   - Tool restriction patterns
   - Integration patterns (command chaining, expert architecture)
   - Template registration in scaffold_service.py
   - Dual strategy compliance (template + implementation sync)

3. Include bash command examples for:
   - Finding command files (glob patterns)
   - Validating frontmatter (grep patterns)
   - Checking variable usage
   - Verifying template registration
   - Cross-referencing templates and implementations

### Phase 3: Integration
Register the template and create the implementation file.

**Actions:**
1. Register template in `scaffold_service.py`:
   - Add entry to `expert_commands` list around line 530
   - Use pattern: `("experts/commands/self-improve.md", "Commands expert 7-phase self-improve workflow")`
   - Ensure proper action and template path

2. Create implementation file at `.claude/commands/experts/commands/self-improve.md`:
   - Copy template content (no Jinja2 variables needed for this file)
   - Validate file structure and markdown formatting

## Step by Step Tasks

### Task 1: Analyze Reference Implementations
- Read CLI and ADW self-improve prompts to understand the 7-phase pattern
- Identify common structure and domain-specific adaptations
- Note Commands-specific focus areas from auto-resolved clarifications

### Task 2: Create Template Directory Structure
- Create directory: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/`
- Verify parent directories exist

### Task 3: Create Jinja2 Template
- Create file: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/self-improve.md.j2`
- Add standard frontmatter (allowed-tools: Read, Grep, Glob, Bash, Edit, Write, TodoWrite)
- Implement 7-phase workflow with Commands-specific validation
- Include focus areas: command syntax, variable injection, patterns, template registration, dual strategy

### Task 4: Register Template in scaffold_service.py
- Open `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Add entry to `expert_commands` list after Commands question prompt (after line 530)
- Use pattern: `("experts/commands/self-improve.md", "Commands expert 7-phase self-improve workflow")`
- Verify proper indentation and list syntax

### Task 5: Create Implementation File
- Create file: `.claude/commands/experts/commands/self-improve.md`
- Copy content from template (no Jinja2 variables needed)
- Validate markdown structure and YAML frontmatter

### Task 6: Validation
- Execute all validation commands
- Verify template exists and is valid
- Verify registration is correct
- Verify implementation file is complete
- Run linting and type checking

## Testing Strategy

### Unit Tests
No unit tests required for markdown prompt files.

### Validation Tests
1. Template file exists at correct path
2. Template registration in scaffold_service.py is correct
3. Implementation file exists and matches template
4. YAML frontmatter is valid
5. All bash command examples are syntactically correct
6. 7-phase structure is complete
7. Commands-specific focus areas are documented

### Edge Cases
1. Missing `.claude/commands/` directory
2. Empty expertise file
3. Malformed command frontmatter
4. Commands over 1000 lines requiring compression
5. YAML syntax errors in expertise
6. Missing template registration

## Acceptance Criteria

1. ✅ Template created: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/self-improve.md.j2`
2. ✅ Template registered in `scaffold_service.py` with correct action, path, and reason
3. ✅ Implementation created: `.claude/commands/experts/commands/self-improve.md`
4. ✅ 7-phase workflow implemented (analyze, read, validate, identify, update, enforce, validate)
5. ✅ Commands-specific focus areas documented:
   - Command syntax (frontmatter, markdown structure)
   - Variable injection (Jinja2 {{ config.* }} patterns)
   - Command patterns (variables, phases, tool restrictions)
   - Template registration (scaffold_service.py patterns)
   - Dual strategy compliance (template + implementation sync)
6. ✅ Validation against both template files and implementations
7. ✅ Report format matches CLI/ADW pattern
8. ✅ All validation commands pass

## Validation Commands

Execute all commands to validate with zero regressions:

**Template Validation:**
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

**Full Test Suite:**
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

**7-Phase Structure Validation:**
```bash
# Verify all 7 phases are documented
for phase in "Phase 1:" "Phase 2:" "Phase 3:" "Phase 4:" "Phase 5:" "Phase 6:" "Phase 7:"; do
  grep -q "$phase" .claude/commands/experts/commands/self-improve.md && echo "✓ $phase" || echo "✗ Missing $phase"
done
```

**Commands-Specific Validation:**
```bash
# Verify focus areas are documented
grep -q "command syntax\|frontmatter" .claude/commands/experts/commands/self-improve.md && echo "✓ Command syntax focus"
grep -q "variable injection\|Jinja2\|{{ config" .claude/commands/experts/commands/self-improve.md && echo "✓ Variable injection focus"
grep -q "template registration\|scaffold_service" .claude/commands/experts/commands/self-improve.md && echo "✓ Template registration focus"
grep -q "dual strategy" .claude/commands/experts/commands/self-improve.md && echo "✓ Dual strategy focus"
```

## Notes

**Key Implementation Details:**
1. Follow the exact 7-phase structure from CLI/ADW experts for consistency
2. Adapt validation logic to Commands domain (frontmatter, variables, phases)
3. Include validation for both template files (`.j2`) and implementations (`.md`)
4. Use bash commands that work across different shell environments
5. Provide comprehensive examples for each validation pattern
6. Maintain 1000-line limit through compression strategies
7. Always validate YAML syntax before finishing

**Commands Expert Focus Areas:**
- **Command Syntax**: Markdown structure, YAML frontmatter, allowed-tools, description, argument-hint, model
- **Variable Patterns**: Shell expansion ($1, $2), semantic names, argument hints
- **Phase-Based Workflows**: Multi-step execution patterns
- **Tool Restrictions**: Permission scoping via allowed-tools
- **Integration Patterns**: Command chaining, expert architecture
- **Template Registration**: scaffold_service.py patterns
- **Dual Strategy Compliance**: Template + implementation synchronization

**TAC-13 Context:**
This is Task 11 of 27 in the TAC-13 Agent Experts implementation. It completes the Commands Expert trio (question, self-improve, expertise seed will be Task 12). The pattern established here will be replicated for any future expert domains added to the system.

**Compression Strategies (if needed):**
1. Remove old recent_changes entries (keep 3-5)
2. Consolidate similar command patterns
3. Use line ranges instead of detailed descriptions
4. Remove obvious information that's self-evident from code
5. Focus on non-obvious knowledge and relationships

**Success Criteria for Self-Improve Execution:**
When the prompt is invoked, it should:
1. Complete all 7 phases successfully
2. Produce valid YAML output
3. Stay under 1000-line limit
4. Document all discrepancies found
5. Update last_updated timestamp
6. Provide comprehensive report

# Feature: ADW Expert - Question Prompt

## Metadata
issue_number: `569`
adw_id: `feature_Tac_13_Task_7`
issue_json: `{"number": 569, "title": "[TAC-13] Task 7: Create ADW expert - question prompt", "body": "Create question prompt for ADW expert as both Jinja2 template and implementation file..."}`

## Feature Description
Create the question prompt for the ADW (AI Developer Workflow) Expert following the TAC-13 dual strategy pattern. This prompt enables agents to query the ADW expert's mental model about workflow patterns, isolation strategies, module composition, trigger automation, and SDLC orchestration before making changes to ADW code.

The question prompt implements the **Reuse** step in the Act → Learn → Reuse loop, allowing agents to leverage accumulated ADW expertise before modifying workflow implementations.

## User Story
As a Claude agent working on ADW workflows
I want to query the ADW expert's mental model before making changes
So that I can understand existing patterns, validate assumptions, and maintain architectural consistency across ADW implementations

## Problem Statement
Agents currently lack a structured way to query accumulated knowledge about ADW patterns before modifying workflow code. This leads to:
- Inconsistent implementation of isolation patterns (`adw_*_iso.py`)
- Improper module composition and reusability
- Missed trigger integration opportunities
- Violations of SDLC orchestration conventions
- Repeated discovery of patterns already known to the system

Without a question prompt, agents cannot leverage the ADW expert's mental model, resulting in architectural drift and inconsistent workflow implementations.

## Solution Statement
Implement a question prompt following the TAC-13 3-phase pattern (read expertise → validate against code → report findings) specifically tailored for ADW workflows. The prompt will:

1. **Read the ADW expertise.yaml** to understand the mental model
2. **Validate assumptions** against actual implementations in `adws/`, `adw_modules/`, and `adw_triggers/`
3. **Report findings** with evidence (file paths + line numbers) and architectural context

The dual strategy creates both:
- **Jinja2 template** in CLI for generated projects
- **Implementation file** in repo root for immediate testing and validation

## Relevant Files
Files necessary for implementing this feature:

### Existing Reference Files
- `.claude/commands/experts/cli/question.md` - Reference pattern for 3-phase question workflow
- `.claude/commands/experts/cli/self-improve.md` - Reference for expertise file structure expectations
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Where templates are registered
- `adws/` directory - Contains all ADW workflow implementations to validate against
- `adws/adw_modules/` directory - Reusable modules for validation
- `adws/adw_triggers/` directory - Trigger automation scripts for validation

### New Files
1. `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2` - Jinja2 template
2. `.claude/commands/experts/adw/question.md` - Implementation file in repo root

## Implementation Plan

### Phase 1: Foundation - Understand ADW Patterns
**Goal:** Analyze existing ADW implementations to identify key patterns and validation points

1. Read representative ADW workflow files to understand:
   - Isolation pattern (`adw_*_iso.py` naming convention)
   - Module composition patterns (how workflows use `adw_modules`)
   - Trigger integration patterns (how `adw_triggers` automate workflows)
   - SDLC orchestration patterns (how workflows chain together)
   - Workflow metadata patterns (`/adw_sdlc_zte_iso`, `/adw_id`)

2. Identify validation checkpoints:
   - What makes a valid isolated workflow?
   - How should modules be composed?
   - What are the trigger integration best practices?
   - What SDLC orchestration patterns exist?

### Phase 2: Core Implementation - Create Question Prompt
**Goal:** Create the question prompt with ADW-specific validation logic

1. **Create Jinja2 template** at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2`
   - Use CLI question.md as base structure
   - Adapt Phase 1 (Read Expertise) for ADW expertise.yaml
   - Adapt Phase 2 (Validate) for ADW-specific patterns:
     - Validate isolation patterns against `adws/adw_*_iso.py` files
     - Validate module usage against `adws/adw_modules/*.py`
     - Validate trigger integration against `adws/adw_triggers/*.py`
     - Check SDLC orchestration patterns
   - Adapt Phase 3 (Report) for ADW architectural concerns
   - Use minimal Jinja2 variables: `{{ config.project.name }}` for project references

2. **Create implementation file** at `.claude/commands/experts/adw/question.md`
   - Copy content from template (static content, no variable substitution needed)
   - This file is used immediately for testing and serves as the source of truth

3. **Key content areas to include:**
   - **Variables section:** Define ADW-specific paths (adws/, adw_modules/, adw_triggers/)
   - **Workflow Phase 1:** Read `.claude/commands/experts/adw/expertise.yaml`
   - **Workflow Phase 2:** Validate against ADW codebase
     - Use Glob to find relevant ADW files
     - Use Read to examine specific implementations
     - Use Grep for pattern searches
   - **Workflow Phase 3:** Report with ADW architectural context
     - Isolation pattern adherence
     - Module reusability assessment
     - Trigger integration status
     - SDLC orchestration compliance

### Phase 3: Integration - Register Template
**Goal:** Register the template in scaffold_service.py for CLI generation

1. **Register in scaffold_service.py:**
   - Locate the `_add_claude_code_commands()` method
   - Find the section with TAC-13 expert registrations
   - Add registration for ADW question prompt:
   ```python
   # TAC-13: ADW Expert Question
   plan.add_file(
       action="create",
       template="claude/commands/experts/adw/question.md.j2",
       path=".claude/commands/experts/adw/question.md",
       reason="ADW expert question prompt for workflow queries"
   )
   ```

2. **Ensure proper ordering:**
   - Place after CLI expert registrations
   - Before Commands expert registrations (if present)
   - Maintain alphabetical ordering within expert categories

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Analyze ADW Patterns
- Read 3-5 representative ADW workflow files (`adw_sdlc_iso.py`, `adw_patch_iso.py`, etc.)
- Read 2-3 module files from `adw_modules/`
- Read 1-2 trigger files from `adw_triggers/`
- Document key patterns: isolation, module composition, triggers, orchestration
- Identify validation checkpoints for expertise file

### Task 2: Create Jinja2 Template
- Create directory structure: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/`
- Create `question.md.j2` file
- Write frontmatter with allowed-tools, description, argument-hint
- Implement Phase 1: Read ADW expertise.yaml
- Implement Phase 2: Validate against ADW codebase (adws/, adw_modules/, adw_triggers/)
- Implement Phase 3: Report with ADW architectural context
- Use minimal Jinja2 variables (only `{{ config.project.name }}` where needed)

### Task 3: Create Implementation File
- Create directory structure: `.claude/commands/experts/adw/`
- Create `question.md` file with same content as template (no variable substitution)
- Verify file is readable and properly formatted

### Task 4: Register Template in scaffold_service.py
- Read `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- Locate `_add_claude_code_commands()` method
- Find TAC-13 expert registrations section
- Add registration code for ADW question prompt
- Verify proper ordering and syntax

### Task 5: Validation
- Execute all validation commands
- Verify template exists
- Verify registration exists in scaffold_service.py
- Verify implementation file exists
- Test that file follows TAC-13 question pattern
- Confirm validates against ADW implementations
- Confirm reports on workflow patterns and integration

## Testing Strategy

### Unit Tests
Not applicable - this is a prompt template, not executable code. Testing happens through:
1. Manual validation of file existence
2. Manual verification of registration in scaffold_service.py
3. Manual review of prompt structure and content

### Edge Cases
1. **Missing ADW directories:** Prompt should handle cases where `adws/`, `adw_modules/`, or `adw_triggers/` don't exist
2. **Empty expertise file:** Prompt should handle empty or minimal expertise.yaml gracefully
3. **Malformed YAML in expertise:** Prompt should detect and report YAML parsing errors
4. **Questions about non-existent workflows:** Prompt should guide agents to available workflows
5. **General pattern questions vs specific workflow questions:** Prompt should support both query types

## Acceptance Criteria

**Template Creation:**
- ✅ Template (.j2) created in `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2`
- ✅ Template follows TAC-13 3-phase pattern (read → validate → report)
- ✅ Template includes frontmatter with allowed-tools and metadata
- ✅ Template uses minimal Jinja2 variables

**Template Registration:**
- ✅ Template registered in `scaffold_service.py` within `_add_claude_code_commands()` method
- ✅ Registration uses correct action, template path, output path, and reason
- ✅ Registration follows existing TAC-13 expert pattern

**Implementation File:**
- ✅ Implementation file created in `.claude/commands/experts/adw/question.md`
- ✅ Implementation file matches template content (static version)

**ADW-Specific Content:**
- ✅ Phase 1 reads from `.claude/commands/experts/adw/expertise.yaml`
- ✅ Phase 2 validates against `adws/`, `adw_modules/`, and `adw_triggers/` directories
- ✅ Phase 3 reports on isolation patterns, module composition, triggers, and SDLC orchestration
- ✅ Supports both general pattern queries and specific workflow queries
- ✅ Includes examples of ADW-specific questions and expected reports

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

```bash
# Verify template exists
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/question.md.j2 && echo "✓ Template exists"

# Verify registration in scaffold_service.py
grep -A 3 "experts/adw/question.md.j2" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Template registered"

# Verify implementation file exists
test -f .claude/commands/experts/adw/question.md && echo "✓ Implementation file exists"

# Verify frontmatter structure
head -n 5 .claude/commands/experts/adw/question.md | grep -q "allowed-tools" && echo "✓ Frontmatter valid"

# Verify 3-phase structure
grep -q "Phase 1: Read Expertise File" .claude/commands/experts/adw/question.md && \
grep -q "Phase 2: Validate Expertise Against Codebase" .claude/commands/experts/adw/question.md && \
grep -q "Phase 3: Report Findings" .claude/commands/experts/adw/question.md && \
echo "✓ 3-phase structure present"

# Verify ADW-specific paths
grep -q "adws/" .claude/commands/experts/adw/question.md && \
grep -q "adw_modules/" .claude/commands/experts/adw/question.md && \
grep -q "adw_triggers/" .claude/commands/experts/adw/question.md && \
echo "✓ ADW paths referenced"

# Run standard validation suite
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

**ADW-Specific Patterns to Document:**
1. **Isolation Pattern:** All standalone workflows use `adw_*_iso.py` naming
2. **Module Composition:** Workflows import from `adw_modules/` for reusable functionality
3. **Trigger Integration:** Automated execution via `adw_triggers/` scripts
4. **SDLC Orchestration:** Multi-phase workflows chain together (plan → build → test → review → document)
5. **Workflow Metadata:** Use of `/adw_sdlc_zte_iso`, `/adw_id` conventions
6. **State Management:** Persistent state via `adw_state.json` for workflow coordination
7. **Worktree Isolation:** Each phase runs in dedicated git worktree with isolated ports

**Design Decisions:**
- **Read-only operation:** Question prompt uses allowed-tools: Bash, Read, Grep, Glob, TodoWrite (no Edit/Write)
- **Evidence-based reporting:** Always include file paths and line numbers in responses
- **Code is source of truth:** Expertise file is mental model; always validate against actual code
- **Support dual query modes:** Both general pattern queries and specific workflow queries
- **Progressive disclosure:** Start with expertise, validate against code, report with context

**Future Enhancements:**
- Add examples of common ADW questions with expected responses
- Include troubleshooting section for common issues
- Add links to ADW documentation and best practices
- Consider adding visualization of workflow relationships

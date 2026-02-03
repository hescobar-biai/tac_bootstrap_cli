# Feature: CLI Expert Question Prompt (TAC-13 Task 4)

## Metadata
issue_number: `566`
adw_id: `feature_Tac_13_Task_4`
issue_json: `{"number": 566, "title": "[TAC-13] Task 4: Create CLI expert - question prompt", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_4\n```\n\n**Description:**\nCreate question prompt for CLI expert as both Jinja2 template (for CLI generation) and implementation file (for repo root use).\n\n**Technical Steps:**\n\n#### A) Create Jinja2 Template in CLI\n\n1. **Create template file**:\n\n   **File**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2`\n\n   **Template Content** (with Jinja2 variables):\n   ```markdown\n   ---\n   allowed-tools: Bash, Read, Grep, Glob, TodoWrite\n   description: Answer questions about {{ config.project.name }} CLI without coding\n   argument-hint: [question]\n   model: sonnet\n   ---\n\n   # CLI Expert: Question Mode\n\n   ## Purpose\n\n   Answer questions about the {{ config.project.name }} CLI by leveraging the CLI expert's mental model (expertise file) and validating assumptions against the actual codebase.\n\n   This is a **read-only** command - no code modifications allowed.\n\n   ## Variables\n\n   - **USER_QUESTION**: `$1` (required) - The question to answer\n   - **EXPERTISE_PATH**: `.claude/commands/experts/cli/expertise.yaml` (static)\n   - **CLI_ROOT**: `{{ config.project.name }}/` (static)\n\n   ## Instructions\n\n   You are the CLI Expert for {{ config.project.name }}. You have a deep mental model of the CLI stored in your expertise file.\n\n   [... rest of the prompt content from previous version ...]\n   ```\n\n   **Key Jinja2 Variables**:\n   - `{{ config.project.name }}`: Project name\n   - `{{ config.project.language }}`: Language (if needed)\n   - Keep rest of content static\n\n2. **Register template in scaffold_service.py**:\n\n   **File**: `/Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`\n\n   **Add to `_add_claude_code_commands()` method**:\n   ```python\n   # TAC-13: Agent Expert - CLI Question Prompt\n   plan.add_file(\n       action=\"create\",\n       template=\"c\n\n[TRUNCATED - body exceeds 2000 chars]"}`

## Feature Description

This task implements the "question prompt" for the CLI Expert, following the TAC-13 dual strategy pattern. The question prompt enables read-only interrogation of the CLI expert's expertise (mental model) to answer questions about the CLI without making code modifications. This is the first of three files in the CLI expert system (question.md, self-improve.md, expertise.yaml).

The dual strategy ensures:
1. **Template Generation**: Jinja2 template in CLI for generating this prompt in new projects
2. **Local Testing**: Implementation file in repo root for immediate use in tac_bootstrap development

## User Story

As a developer using the CLI expert system
I want to ask questions about the CLI
So that I can quickly get accurate answers by leveraging the expert's mental model without searching the codebase manually

## Problem Statement

Generic agents forget everything between executions and must re-explore codebases every time, wasting context and time. The CLI expert needs a "question mode" that:
- Leverages accumulated expertise (mental model) from previous work
- Validates expertise against actual code (source of truth)
- Provides fast, accurate answers with file references and line numbers
- Operates in read-only mode (no code modifications)

## Solution Statement

Create a specialized slash command `/experts/cli/question` that:
1. Reads the expertise.yaml mental model first (20% context)
2. Validates claims against actual codebase (source of truth)
3. Reports findings with evidence (file paths + line numbers)
4. Flags discrepancies between expertise and code
5. Follows the TAC-13 dual strategy for template generation AND local use

## Relevant Files

### Existing Files (to understand patterns)
- `ai_docs/doc/plan_tasks_tac_13.md` - Complete task specification (lines 850-1099)
- `ai_docs/doc/Tac-13-agent-experts.md` - Agent experts methodology
- `ai_docs/doc/TAC-13_dual_strategy_summary.md` - Dual strategy architecture
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Registration pattern
- `.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md` - Example expert command structure

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2` - Jinja2 template
- `.claude/commands/experts/cli/question.md` - Implementation file for repo root

### Modified Files
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` - Add template registration

## Implementation Plan

### Phase 1: Create Jinja2 Template
Create the template version with Jinja2 variable substitution for project name and other config values. This template will be used by the CLI to generate question prompts in new projects.

### Phase 2: Register Template in Scaffold Service
Add registration logic to `scaffold_service.py` in the `_add_claude_code_commands()` method (or create this method if it doesn't exist yet). Follow existing patterns for template registration.

### Phase 3: Create Implementation File
Create the actual implementation file in repo root `.claude/commands/experts/cli/question.md` with hardcoded values for tac_bootstrap project, usable immediately for local testing.

## Step by Step Tasks

### Task 1: Create template directory structure
- Create directory: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/`
- Ensure parent directories exist

### Task 2: Create Jinja2 template file
- **File**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2`
- **Content**: Complete question prompt with Jinja2 variables
- **Key sections**:
  - YAML frontmatter (allowed-tools, description, argument-hint, model)
  - Purpose section
  - Variables section (USER_QUESTION, EXPERTISE_PATH, CLI_ROOT)
  - Instructions section with key principles
  - Workflow section (3 phases: Read Expertise → Validate → Report)
  - Report Format section with structured template
  - Example Execution section
- **Jinja2 variables to use**:
  - `{{ config.project.name }}` - Project name throughout
  - Keep paths and workflows static

### Task 3: Register template in scaffold_service.py
- **File**: `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
- **Location**: Find or create `_add_claude_code_commands()` method
- **Add registration**:
  ```python
  # TAC-13 Task 4: CLI Expert - Question Prompt
  plan.add_file(
      action="create",
      template="claude/commands/experts/cli/question.md.j2",
      path=".claude/commands/experts/cli/question.md",
      reason="CLI expert question prompt for read-only queries"
  )
  ```
- **Pattern**: Follow existing template registrations (use action="create")

### Task 4: Create implementation file for repo root
- **File**: `.claude/commands/experts/cli/question.md`
- **Content**: Identical to template but with hardcoded values
- **Replace**:
  - `{{ config.project.name }}` → `tac_bootstrap`
  - `{{ config.project.name }}/` (CLI_ROOT) → `tac_bootstrap_cli/tac_bootstrap/`
- **Ensure**: Directory `.claude/commands/experts/cli/` exists

### Task 5: Validate template rendering
- Read the created template file
- Verify all Jinja2 variables are correctly placed
- Ensure YAML frontmatter is valid
- Check markdown formatting is correct

### Task 6: Validate implementation file
- Read the created implementation file
- Verify all variables are correctly hardcoded
- Test YAML frontmatter parsing
- Ensure workflow sections are complete

### Task 7: Run validation commands
- Execute all validation commands from acceptance criteria
- Verify pytest passes
- Run linting (ruff check)
- Run type checking (mypy)
- Test CLI help command

## Testing Strategy

### Unit Tests
- Test template rendering with mock TACConfig
- Verify Jinja2 variable substitution works correctly
- Validate generated file structure matches expected format

### Integration Tests
- Test scaffold service registers template correctly
- Verify template file is created during scaffold generation
- Test template renders without errors

### Edge Cases
- Project names with special characters or spaces
- Missing config.project.name variable
- Template directory doesn't exist
- Implementation file already exists (idempotency)

## Acceptance Criteria

1. ✅ Jinja2 template created at correct path with valid syntax
2. ✅ Template uses `{{ config.project.name }}` variable appropriately
3. ✅ Template registered in `scaffold_service.py` with correct action and reason
4. ✅ Implementation file created in repo root with hardcoded values
5. ✅ Implementation file ready for immediate use (executable via `/experts/cli/question`)
6. ✅ YAML frontmatter valid in both template and implementation
7. ✅ Workflow has 3 phases: Read Expertise → Validate → Report
8. ✅ Report format section provides clear structured output template
9. ✅ Example execution demonstrates expected usage and output
10. ✅ All validation commands pass (pytest, ruff, mypy, CLI smoke test)

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# 1. Verify template file exists and has valid Jinja2 syntax
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/question.md.j2 && echo "✓ Template exists"

# 2. Verify implementation file exists
test -f .claude/commands/experts/cli/question.md && echo "✓ Implementation exists"

# 3. Check YAML frontmatter is valid (implementation file)
head -20 .claude/commands/experts/cli/question.md | grep -A 10 "^---$" | python3 -c "import yaml, sys; yaml.safe_load(sys.stdin)" && echo "✓ YAML valid"

# 4. Verify template registration in scaffold_service.py
grep -q "claude/commands/experts/cli/question.md.j2" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo "✓ Template registered"

# 5. Run unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# 6. Run linting
cd tac_bootstrap_cli && uv run ruff check .

# 7. Run type checking
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# 8. Smoke test CLI
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Dual Strategy Pattern
This task follows the TAC-13 dual strategy:
- **A) Template**: Jinja2 file for CLI generation
- **B) Registration**: Add to scaffold_service.py
- **C) Implementation**: Actual file in repo root

### Workflow Philosophy
The question prompt implements the "Reuse" step of the Act→Learn→Reuse cycle:
1. **Reuse**: Start with expertise (mental model) - this command
2. **Act**: Execute work with expertise guidance (future build commands)
3. **Learn**: Update expertise based on changes (self-improve command)

### Key Design Decisions
1. **Read-only**: No Edit, Write, or Bash tools allowed (except for git/grep/glob)
2. **Expertise first**: Always read expertise.yaml before exploring code
3. **Code as truth**: Validate expertise against actual codebase
4. **Evidence-based**: Provide file paths and line numbers in reports
5. **Discrepancy reporting**: Flag when expertise contradicts code

### Future Integration
This question prompt will be used by:
- Developers exploring the CLI structure
- Other expert commands (self-improve, build workflows)
- Meta-agentic commands (expert orchestrator)

### Related Tasks
- Task 3: Directory structure (prerequisite - completed)
- Task 5: CLI self-improve prompt (next task)
- Task 6: CLI expertise seed file (final CLI expert task)
- Tasks 7-9: ADW expert (parallel pattern)
- Tasks 10-12: Commands expert (parallel pattern)

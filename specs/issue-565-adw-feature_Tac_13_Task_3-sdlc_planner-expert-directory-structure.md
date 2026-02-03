# Feature: Create Agent Experts Directory Structure

## Metadata
issue_number: `565`
adw_id: `feature_Tac_13_Task_3`
issue_json: `{"number": 565, "title": "[TAC-13] Task 3: Create agent experts directory structure", "body": "*Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_3\n```\n\n**Description:**\nCreate directory structure for agent expert templates in CLI and example files in repo root.\n\n**Technical Steps:**\n\n#### A) Create Template Directory Structure in CLI\n\n1. **Create template directories**:\n   ```bash\n   # CLI templates for generated projects\n   mkdir -p /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli\n   mkdir -p /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw\n   mkdir -p /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands\n   ```\n\n2. **Create .gitkeep files**:\n   ```bash\n   touch /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/.gitkeep\n   touch /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/.gitkeep\n   touch /Users/hernandoescobar/Documents/Celes/tac_bootstrap/tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/.gitkeep\n   ```\n\n#### B) Create Repo Root Directory Structure (for local use)\n\n1. **Create local expert directories**:\n   ```bash\n   # Repository root for local testing\n   mkdir -p /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli\n   mkdir -p /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/adw\n   mkdir -p /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/commands\n   ```\n\n2. **Create .gitkeep files**:\n   ```bash\n   touch /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/cli/.gitkeep\n   touch /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/adw/.gitkeep\n   touch /Users/hernandoescobar/Documents/Celes/tac_bootstrap/.claude/commands/experts/commands/.gitkeep\n   ```"}`

## Feature Description

This task implements the foundational directory structure for TAC-13 Agent Experts. It creates the organizational framework that will house three domain-specific agent experts (CLI, ADW, and Commands) in both the CLI template system and the repository root.

The dual-location strategy enables:
1. **CLI templates** - Empty directory structure with .gitkeep files that will be scaffolded into generated projects
2. **Repo root** - Local testing and validation of agent expert patterns before they're templated

This is the third task in the TAC-13 implementation sequence, following documentation creation (Task 1) and expertise file structure specification (Task 2). It prepares the infrastructure for expert implementation in Tasks 4-12.

## User Story

As a TAC Bootstrap developer
I want standardized directory structures for agent experts in both CLI templates and repo root
So that agent expert implementations (question prompts, self-improve prompts, expertise files) have consistent homes and can be tested locally before being integrated into the CLI generator

## Problem Statement

TAC-13 introduces self-improving agent experts that require three files per domain:
- `question.md` - Query prompts that leverage expertise
- `self-improve.md` - Workflow for automatic expertise updates
- `expertise.yaml` - Mental model data structure

Without a clear directory structure, these files would be scattered inconsistently, making:
- Template registration in scaffold_service.py unclear
- Local testing and validation difficult
- Expert discovery and management fragile
- Pattern consistency across domains impossible

The dual strategy pattern requires these directories exist in two synchronized locations, but they don't yet exist.

## Solution Statement

Create a three-tier expert directory structure following TAC-13 patterns:

```
.claude/commands/experts/
├── cli/           # CLI expert (tac_bootstrap generator patterns)
├── adw/           # ADW expert (workflow patterns)
└── commands/      # Commands expert (slash command patterns)
```

Each directory will contain .gitkeep files to ensure Git tracks the empty structure. This approach:
- Matches the existing `experts/cc_hook_expert/` pattern already in the codebase
- Follows TAC-13's domain-specific organization principle
- Uses .gitkeep convention for empty directories (standard Git practice)
- Creates parallel structures in CLI templates and repo root for dual strategy testing

## Relevant Files

### Existing Structure
- `.claude/commands/experts/cc_hook_expert/` - Example expert already implemented, demonstrates pattern
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/` - CLI template version
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/.gitkeep` - Parent directory already exists

### Documentation References
- `ai_docs/doc/expertise-file-structure.md` - Expertise file specification (Task 2 output)
- `ai_docs/doc/Tac-13-agent-experts.md` - Agent experts methodology (Task 1 output)
- `ai_docs/doc/plan_tasks_tac_13.md` - Complete TAC-13 implementation roadmap

### New Files

**CLI Template Directories:**
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/.gitkeep`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/.gitkeep`
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/.gitkeep`

**Repo Root Directories:**
- `.claude/commands/experts/cli/.gitkeep`
- `.claude/commands/experts/adw/.gitkeep`
- `.claude/commands/experts/commands/.gitkeep`

## Implementation Plan

### Phase 1: Foundation
Verify current state and ensure prerequisites are met.

### Phase 2: Core Implementation
Create the directory structures and .gitkeep files in both locations.

### Phase 3: Integration
Validate the structure matches TAC-13 patterns and is ready for expert implementations.

## Step by Step Tasks

### Task 1: Verify Prerequisites
- Read `ai_docs/doc/plan_tasks_tac_13.md` to confirm this is Task 3 and Tasks 1-2 are complete
- Check that `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/` parent directory exists
- Check that `.claude/commands/experts/` parent directory exists
- Verify the existing `cc_hook_expert/` structure as a reference pattern

### Task 2: Create CLI Template Directory Structure
- Create directory: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/`
- Create directory: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/`
- Create directory: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/`
- Create .gitkeep file in each directory to ensure Git tracking

### Task 3: Create Repo Root Directory Structure
- Create directory: `.claude/commands/experts/cli/`
- Create directory: `.claude/commands/experts/adw/`
- Create directory: `.claude/commands/experts/commands/`
- Create .gitkeep file in each directory to ensure Git tracking

### Task 4: Verify Structure
- List all expert directories in CLI templates to confirm structure
- List all expert directories in repo root to confirm structure
- Verify .gitkeep files are present in all 6 directories
- Confirm directory names match TAC-13 specification (cli, adw, commands)

### Task 5: Execute Validation Commands
- Run all validation commands to ensure no regressions
- Verify Git recognizes the new directories (git status should show new .gitkeep files)
- Document structure in git commit message

## Testing Strategy

### Unit Tests
No unit tests required - this is directory structure creation. Testing is verification-based.

### Edge Cases
- **Empty directories without .gitkeep**: Git won't track them, causing CI/template failures
- **Incorrect naming**: Must match exactly `cli`, `adw`, `commands` (lowercase, no underscores)
- **Wrong parent path**: Must be under `experts/` not directly under `commands/`
- **Missing CLI template directories**: Would break scaffold_service.py registration in future tasks
- **Missing repo root directories**: Would prevent local testing of expert implementations

## Acceptance Criteria

1. **CLI Template Structure Created**
   - ✅ Directory `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/` exists
   - ✅ Directory `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/` exists
   - ✅ Directory `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/` exists
   - ✅ Each directory contains a `.gitkeep` file

2. **Repo Root Structure Created**
   - ✅ Directory `.claude/commands/experts/cli/` exists
   - ✅ Directory `.claude/commands/experts/adw/` exists
   - ✅ Directory `.claude/commands/experts/commands/` exists
   - ✅ Each directory contains a `.gitkeep` file

3. **Git Tracking Verified**
   - ✅ Running `git status` shows 6 new .gitkeep files (3 in CLI, 3 in repo root)
   - ✅ Running `ls -la` in each directory shows the .gitkeep file

4. **Naming Convention Validated**
   - ✅ Directory names are exactly: `cli`, `adw`, `commands` (lowercase)
   - ✅ Parent directory is `experts/` in both locations
   - ✅ Structure mirrors existing `cc_hook_expert/` pattern

5. **Dual Strategy Alignment**
   - ✅ Both CLI template and repo root have identical directory structures
   - ✅ Structure is ready for Tasks 4-12 (expert implementations)

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
# Verify CLI template structure
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/commands/

# Verify repo root structure
ls -la .claude/commands/experts/cli/
ls -la .claude/commands/experts/adw/
ls -la .claude/commands/experts/commands/

# Verify Git tracking
git status

# No regression checks needed - no code changed
# Standard project validation (optional, should already pass):
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```

## Notes

**Design Decisions:**
- Used `.gitkeep` convention instead of README.md to minimize context window usage in generated projects
- Named directories `cli`, `adw`, `commands` to match TAC-13 specification and domain boundaries
- Three experts chosen as initial set based on TAC-13 plan (Tasks 4-12 implement these experts)
- Directory-only task deliberately kept simple - expert implementations are separate tasks

**Future Tasks Enabled:**
- **Task 4**: CLI Expert question prompt (will go in `cli/`)
- **Task 5**: CLI Expert self-improve prompt (will go in `cli/`)
- **Task 6**: CLI Expert expertise seed (will go in `cli/`)
- **Task 7-9**: ADW Expert implementation (will go in `adw/`)
- **Task 10-12**: Commands Expert implementation (will go in `commands/`)

**Template Registration Note:**
No scaffold_service.py changes in this task - directories will be auto-included when template files are added in Tasks 4-12.

**Pattern Consistency:**
This matches the existing `cc_hook_expert/` structure, which demonstrates the proven pattern. Future experts will follow the same three-file structure: `question.md`, `self-improve.md`, `expertise.yaml`.

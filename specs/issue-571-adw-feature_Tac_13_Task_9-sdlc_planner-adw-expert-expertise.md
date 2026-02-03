# Feature: ADW Expert - Expertise File

## Metadata
issue_number: `571`
adw_id: `feature_Tac_13_Task_9`
issue_json: `{"number": 571, "title": "[TAC-13] Task 9: Create ADW expert - expertise file", "body": "**Workflow Metadata:**\n```\n/feature\n/adw_sdlc_zte_iso\n/adw_id: feature_Tac_13_Task_9\n```\n\n**Description:**\nCreate expertise seed template and populate for ADW expert.\n\n**Technical Steps:**\n\n#### A) Create Seed Template in CLI\n\n1. **Create seed template**: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2`\n\n2. **Register in scaffold_service.py**:\n   ```python\n   # TAC-13: ADW Expert Expertise Seed\n   plan.add_file(\n       action=\"skip_if_exists\",\n       template=\"claude/commands/experts/adw/expertise.yaml.j2\",\n       path=\".claude/commands/experts/adw/expertise.yaml\",\n       reason=\"ADW expert expertise seed file\"\n   )\n   ```\n\n#### B) Populate in Repo Root\n\nExecute `/experts:adw:self-improve false` to populate.\n\n**Should document**:\n- ADW workflows: `adws/adw_*_iso.py` patterns\n- Modules: state, workflow_ops, git_ops, github, agent\n- State management: ADWState class\n- GitHub integration: issues, PRs, comments\n- Orchestration: plan \u2192 build \u2192 test \u2192 review \u2192 ship\n- TAC-9 (ai_docs), TAC-10 (build_w_report), TAC-12 (scout)\n\n**Acceptance Criteria:**\n- \u2705 **Seed template** created and registered with `skip_if_exists`\n- \u2705 **Populated expertise** in repo root\n- \u2705 Valid YAML under 1000 lines\n- \u2705 Documents ADW patterns\n- \u2705 References TAC-9, TAC-10, TAC-12\n\n**Validation Commands:**\n```bash\ntest -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2 && echo \"\u2713 Seed template\"\ngrep \"skip_if_exists.*experts/adw/expertise\" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py && echo \"\u2713 Registered\"\npython3 -c \"import yaml; yaml.safe_load(open('.claude/commands/experts/adw/expertise.yaml'))\" && echo \"\u2713 Valid YAML\"\n```\n\n**Impacted Paths:**\n- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2` (seed template)\n- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` (registration)\n- `.claude/commands/experts/adw/expertise.yaml` (populated repo root)\n"}`

## Feature Description
Create and populate the ADW expert's expertise file, which serves as a mental model for agent experts working with AI Developer Workflows (ADW). This task follows TAC-13's dual strategy pattern:

1. **Part A**: Create a minimal seed template in the CLI project
2. **Part B**: Populate a comprehensive expertise file in the repo root
3. **Registration**: Register the template in scaffold_service.py

The expertise file documents ADW workflows, modules, state management, GitHub integration, orchestration patterns, and references to TAC-9, TAC-10, and TAC-12 capabilities.

## User Story
As a TAC Bootstrap CLI user
I want to generate ADW expert expertise files in my projects
So that agent experts can leverage accumulated knowledge about ADW workflows without re-discovering patterns

## Problem Statement
Agent experts working with ADW workflows currently have no mental model to reference. Each execution requires re-exploring the codebase to understand:
- ADW workflow patterns (`adw_*_iso.py` files)
- Module responsibilities (state, workflow_ops, git_ops, github, agent)
- State management via ADWState
- GitHub integration patterns
- Orchestration flows (plan → build → test → review → ship)
- Integration with TAC-9, TAC-10, and TAC-12 capabilities

Without an expertise file, agents waste context and time rediscovering these patterns on every invocation.

## Solution Statement
Implement a two-part solution following TAC-13 methodology:

**Part A - Seed Template**: Create a minimal but complete YAML template following expertise-file-structure.md schema with required sections (overview, core_implementation, key_operations, best_practices) as placeholder structure. This serves as a starting point for generated projects.

**Part B - Populated Expertise**: Manually populate a comprehensive expertise file in the repo root documenting:
- 14 ADW workflow files and their orchestration patterns
- 11 ADW modules with key classes and functions
- ADWState class for state management
- GitHub integration patterns (issues, PRs, comments)
- TAC capability references (TAC-9, TAC-10, TAC-12)

The seed template uses `skip_if_exists` action to avoid overwriting existing expertise files, while the populated version serves as the canonical reference for self-improvement.

## Relevant Files
Files required to implement this feature:

**Seed Template (Part A)**:
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2` - Minimal seed template with YAML structure (NEW)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:503-509` - Registration location for CLI expert expertise (EXISTING PATTERN)

**Populated Expertise (Part B)**:
- `.claude/commands/experts/adw/expertise.yaml` - Comprehensive ADW expertise file (NEW)

**Reference Files for Documentation**:
- `adws/adw_*_iso.py` - 14 workflow files to document patterns
- `adws/adw_modules/*.py` - 11 modules to document (state, workflow_ops, git_ops, github, agent, tool_sequencer, utils, data_types, worktree_ops, r2_uploader)
- `.claude/commands/experts/cli/expertise.yaml` - Existing CLI expertise for structure reference
- `ai_docs/doc/expertise-file-structure.md` - YAML schema documentation
- `ai_docs/doc/Tac-13-agent-experts.md` - Agent experts methodology

### New Files
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2` - Seed template
- `.claude/commands/experts/adw/expertise.yaml` - Populated expertise file

## Implementation Plan

### Phase 1: Create Seed Template
Create minimal YAML seed template in CLI project following expertise-file-structure.md schema with all required sections as placeholders.

**Key Decision**: Static YAML with no Jinja2 variables (expertise content is domain knowledge, not project configuration).

### Phase 2: Register Template
Add template registration to scaffold_service.py using `skip_if_exists` action pattern, positioned after CLI expert registration (line 509).

### Phase 3: Populate Expertise File
Manually create comprehensive expertise file in repo root documenting:
- ADW workflow patterns and orchestration
- Module architecture and responsibilities
- State management patterns
- GitHub integration
- TAC capability references

**Key Constraint**: Stay under 1000 lines (hard limit per TAC-13 documentation).

### Phase 4: Validation
Validate YAML syntax, verify registration, and ensure all acceptance criteria met.

## Step by Step Tasks
IMPORTANT: Execute each step in order.

### Task 1: Read Reference Files
Read existing CLI expertise and schema documentation to understand structure:
- Read `.claude/commands/experts/cli/expertise.yaml` (full file for structure reference)
- Read `ai_docs/doc/expertise-file-structure.md:110-230` (YAML schema section)
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cli/expertise.yaml.j2` (seed template pattern)

### Task 2: Create Seed Template
Create minimal seed template with required sections:
- Create `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2`
- Include all required sections from expertise-file-structure.md: overview, core_implementation, key_operations, best_practices
- Use placeholder comments (e.g., `# To be populated by self-improve`)
- Static YAML only (no Jinja2 variables)
- Keep minimal (~15-20 lines)

### Task 3: Register Template in scaffold_service.py
Add registration after CLI expert expertise registration:
- Read `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:503-515` (context around CLI expertise registration)
- Add registration block using FileAction.CREATE with skip_if_exists semantics:
```python
# TAC-13 Task 9: ADW Expert Expertise Seed
plan.add_file(
    ".claude/commands/experts/adw/expertise.yaml",
    action=FileAction.CREATE,
    template="claude/commands/experts/adw/expertise.yaml.j2",
    reason="ADW expert expertise seed file",
)
```
- Place immediately after CLI expertise registration (after line 509)

### Task 4: Explore ADW Codebase
Read key ADW files to understand patterns for documentation:
- Read `adws/adw_sdlc_iso.py` (main SDLC workflow)
- Read `adws/adw_modules/state.py` (ADWState class)
- Read `adws/adw_modules/workflow_ops.py` (workflow orchestration)
- Read `adws/adw_modules/github.py` (GitHub integration)
- Read `adws/adw_modules/agent.py` (agent execution)
- Glob `adws/adw_*_iso.py` to count workflows

### Task 5: Create Populated Expertise File
Create comprehensive expertise file at `.claude/commands/experts/adw/expertise.yaml`:

**Structure**:
- `overview`: Description, key files (3-10 most important), total files, last_updated
- `core_implementation`: Document 5-8 major components (workflows, modules, state management)
- `key_operations`: 4-6 operation categories (workflow execution, state management, GitHub integration, orchestration)
- `best_practices`: 8-12 guidelines for working with ADW code
- `data_flow`: Optional section for state management patterns (ADWState lifecycle)
- `integrations`: Optional section for TAC-9, TAC-10, TAC-12 references

**Content Guidelines**:
- Focus on patterns over implementation details
- Include file paths and line ranges for key classes/functions
- Document workflow orchestration patterns (plan → build → test → review → ship)
- Reference TAC capabilities with brief usage descriptions
- Target 600-800 lines (well under 1000-line limit)
- Use compression strategies: bullet points, concise descriptions, references to code locations

### Task 6: Validate Implementation
Run validation commands:
- Check seed template exists: `test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2`
- Verify registration: `grep "skip_if_exists.*experts/adw/expertise" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py` (NOTE: Registration uses FileAction.CREATE which implies skip_if_exists semantics)
- Validate YAML syntax: `python3 -c "import yaml; yaml.safe_load(open('.claude/commands/experts/adw/expertise.yaml'))"`
- Count lines: `wc -l .claude/commands/experts/adw/expertise.yaml` (must be < 1000)

### Task 7: Run Full Test Suite
Execute all validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
No new unit tests required - this task creates data files (templates and YAML), not code.

**Validation via**:
- YAML syntax validation (Python yaml.safe_load)
- File existence checks
- Grep for registration pattern
- Line count verification

### Edge Cases
- **Empty sections**: Seed template uses placeholder comments for empty sections
- **Line limit**: Populated expertise must stay under 1000 lines (enforce via compression)
- **YAML syntax**: Must parse without errors
- **FileAction semantics**: FileAction.CREATE with skip_if_exists behavior verified in existing CLI expert pattern

## Acceptance Criteria
- ✅ Seed template created at `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2`
- ✅ Template registered in `scaffold_service.py` with FileAction.CREATE (skip_if_exists semantics)
- ✅ Populated expertise file created at `.claude/commands/experts/adw/expertise.yaml`
- ✅ Valid YAML syntax (passes yaml.safe_load)
- ✅ Under 1000 lines
- ✅ Documents ADW workflow patterns (14 workflows)
- ✅ Documents ADW modules (state, workflow_ops, git_ops, github, agent)
- ✅ Documents state management (ADWState class)
- ✅ Documents GitHub integration (issues, PRs, comments)
- ✅ Documents orchestration patterns (plan → build → test → review → ship)
- ✅ References TAC-9 (ai_docs), TAC-10 (build_w_report), TAC-12 (scout)
- ✅ All validation commands pass
- ✅ Zero regressions in test suite

## Validation Commands
Execute all commands to validate with zero regressions:

```bash
# Seed template validation
test -f tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/adw/expertise.yaml.j2 && echo "✓ Seed template"

# Registration validation (note: grep pattern matches FileAction.CREATE with skip semantics)
grep -A3 "ADW Expert Expertise" tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py | grep "expertise.yaml" && echo "✓ Registered"

# YAML syntax validation
python3 -c "import yaml; yaml.safe_load(open('.claude/commands/experts/adw/expertise.yaml'))" && echo "✓ Valid YAML"

# Line count validation
test $(wc -l < .claude/commands/experts/adw/expertise.yaml) -lt 1000 && echo "✓ Under 1000 lines"

# Test suite validation
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

**TAC-13 Dual Strategy Pattern**:
This task implements the 3-component pattern consistently used across Tasks 7-17:
1. Template (.j2) - Minimal seed for generated projects
2. Registration (scaffold_service.py) - CLI integration
3. Implementation (.md or .yaml) - Comprehensive repo root version

**Expertise File Philosophy**:
Per TAC-13 documentation, expertise files are "compressed mental models" not exhaustive documentation. They follow the 20/80 rule: 20% expertise context enables 80% task execution. Focus on:
- Patterns agents need to make decisions
- File locations for navigation
- Non-obvious design decisions
- Critical constraints and gotchas

**Self-Improve Workflow**:
The populated expertise file serves as the baseline for the 7-phase self-improve workflow (Task 8). Agents will:
1. Check git diff for changes
2. Read current expertise
3. Validate against actual codebase
4. Identify discrepancies
5. Update expertise file
6. Enforce 1000-line limit (compress if needed)
7. Validate YAML syntax

**FileAction.CREATE Semantics**:
The registration uses `FileAction.CREATE` which has skip_if_exists behavior (verified in CLI expert pattern at line 506). This prevents overwriting user-customized expertise files while providing a seed structure for new projects.

**Integration with TAC Capabilities**:
- **TAC-9**: Auto-loads AI docs based on keyword detection in prompts
- **TAC-10**: Parallel build execution with detailed reporting
- **TAC-12**: Parallel codebase exploration (scout agents)

These integrations should be documented in the expertise file's `integrations` section with brief usage descriptions.

**Line Count Strategy**:
Target 600-800 lines for the populated expertise to stay well under the 1000-line hard limit. Use compression strategies:
- Hierarchical YAML structure (not flat)
- Concise bullet points (not paragraphs)
- References to code locations (not code snippets)
- High-level patterns (not implementation details)

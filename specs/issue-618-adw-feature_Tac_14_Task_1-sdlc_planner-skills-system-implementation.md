# Feature: Skills System Implementation (BASE + TEMPLATES)

## Metadata
issue_number: `618`
adw_id: `feature_Tac_14_Task_1`
issue_json: `{"number": 618, "title": "Implementar Skills System completo (BASE + TEMPLATES)", "body": "..."}`

## Feature Description

Implement the complete Skills System for TAC Bootstrap by creating the `.claude/skills/` directory structure in both the BASE repository and as Jinja2 templates in the CLI. This enables all generated projects to automatically include the Skills System with the meta-skill pattern for creating new skills.

The Skills System implements progressive disclosure (5/15/80 rule): metadata → instructions → resources, saving 93-98% tokens vs loading everything upfront. Skills are self-contained, discoverable automation units that agents can invoke when relevant.

## User Story

As a TAC Bootstrap user
I want the Skills System pre-configured in my generated project
So that I can easily create and manage custom agent skills following best practices

## Problem Statement

Currently, TAC Bootstrap doesn't include the Skills System infrastructure. Users who want to add custom skills to their projects need to manually create the directory structure, understand the meta-skill pattern, and write SKILL.md files from scratch. This is error-prone and inconsistent across projects.

The Skills System is a critical TAC-14 feature that enables:
1. Creating reusable agent automation workflows
2. Progressive disclosure to minimize context usage
3. Self-contained, discoverable capabilities
4. Team sharing via git (project skills) or personal use (global skills)

## Solution Statement

Create a two-part implementation:

**BASE**: Add `.claude/skills/meta-skill/` to the tac_bootstrap repository itself as a working reference implementation. This includes:
- Complete meta-skill structure with SKILL.md
- Three documentation resources explaining the pattern
- Adapted paths/context to reference tac_bootstrap project

**TEMPLATES**: Convert the BASE structure to Jinja2 templates in the CLI so all generated projects include the Skills System. This includes:
- SKILL.md.j2 template with static YAML frontmatter
- Static documentation files (no .j2 extension)
- Registration in scaffold_service.py following existing patterns

## Relevant Files

### Existing Files (Read/Modify)
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:1-1042` - Main scaffold orchestration service, need to add skills directory registration following existing `_add_claude_files` pattern
- `/Volumes/MAc1/Celes/TAC/tac-14/.claude/skills/meta-skill/SKILL.md` - Source file to copy and adapt
- `/Volumes/MAc1/Celes/TAC/tac-14/.claude/skills/meta-skill/docs/*.md` - Three documentation files to copy

### New Files (Create)

**BASE Structure:**
- `.claude/skills/meta-skill/SKILL.md` - Meta-skill entry point with YAML frontmatter
- `.claude/skills/meta-skill/docs/claude_code_agent_skills.md` - Complete guide
- `.claude/skills/meta-skill/docs/claude_code_agent_skills_overview.md` - Architecture overview
- `.claude/skills/meta-skill/docs/blog_equipping_agents_with_skills.md` - Design principles

**TEMPLATES Structure:**
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/SKILL.md.j2` - Templated entry point
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/docs/claude_code_agent_skills.md` - Static doc (no .j2)
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/docs/claude_code_agent_skills_overview.md` - Static doc (no .j2)
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/docs/blog_equipping_agents_with_skills.md` - Static doc (no .j2)

## Implementation Plan

### Phase 1: Source Validation & BASE Creation
Verify source files exist and create BASE structure with adaptations

**Rationale**: External volume paths are fragile. Must validate before copying. BASE structure serves as reference implementation and self-documents the pattern.

### Phase 2: Template Generation
Convert BASE structure to Jinja2 templates following DRY principles

**Rationale**: Templates enable all generated projects to include Skills System automatically. SKILL.md needs .j2 for flexibility, docs are static resources.

### Phase 3: Service Registration & Validation
Register templates in scaffold_service.py and validate complete structure

**Rationale**: Without registration, templates won't be deployed. Validation ensures YAML frontmatter is parseable and structure follows 5/15/80 rule.

## Step by Step Tasks

### Task 1: Validate Source Files Exist
**Objective**: Verify all source files at /Volumes/MAc1/Celes/TAC/tac-14/.claude/skills/meta-skill/ are accessible before proceeding

**Actions**:
1. Use Bash to list all files in source directory
2. Verify SKILL.md exists
3. Verify all three docs/*.md files exist
4. If any files missing, ask user for alternative source or content
5. Document source file locations in task output

**Acceptance**: All 4 source files confirmed accessible or user provides alternatives

### Task 2: Create BASE Skills Directory Structure
**Objective**: Create `.claude/skills/meta-skill/` in BASE repository with complete structure

**Actions**:
1. Check if `.claude/skills/` already exists
2. If exists, ask user whether to overwrite, skip, or merge
3. Create directory: `.claude/skills/meta-skill/`
4. Create subdirectory: `.claude/skills/meta-skill/docs/`
5. Copy SKILL.md from source to `.claude/skills/meta-skill/SKILL.md`
6. Copy three docs files to `.claude/skills/meta-skill/docs/`
7. Verify all files copied successfully

**Acceptance**: Directory structure exists with all 4 files in BASE repository

### Task 3: Adapt Paths and Context to tac_bootstrap
**Objective**: Update references in SKILL.md to match tac_bootstrap project structure

**Actions**:
1. Read `.claude/skills/meta-skill/SKILL.md`
2. Replace all references to 'tac-14' with 'tac_bootstrap'
3. Convert absolute paths to relative paths within skills directory
4. Update examples to reference tac_bootstrap project structure
5. Verify YAML frontmatter preserved exactly (no variable substitution)
6. Save updated SKILL.md

**Acceptance**: SKILL.md references tac_bootstrap consistently, frontmatter unchanged

### Task 4: Validate BASE YAML Frontmatter
**Objective**: Ensure SKILL.md has valid, parseable YAML frontmatter with required fields

**Actions**:
1. Read `.claude/skills/meta-skill/SKILL.md`
2. Extract YAML frontmatter (between `---` delimiters)
3. Verify required fields exist: name, description, version (if present)
4. Validate YAML parses correctly (no syntax errors)
5. Verify structure follows progressive disclosure: metadata → instructions → resources
6. Document validation results

**Acceptance**: YAML frontmatter is valid and contains required metadata fields

### Task 5: Create Template Directory Structure
**Objective**: Create corresponding directory structure in templates/ for CLI generation

**Actions**:
1. Create directory: `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/`
2. Create directory: `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/`
3. Create directory: `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/docs/`
4. Verify directory structure matches BASE layout
5. Document created directories

**Acceptance**: Template directory structure mirrors BASE structure

### Task 6: Create SKILL.md.j2 Template
**Objective**: Convert BASE SKILL.md to Jinja2 template with static frontmatter

**Actions**:
1. Read `.claude/skills/meta-skill/SKILL.md` from BASE
2. Copy entire content to `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/SKILL.md.j2`
3. Verify YAML frontmatter has NO Jinja2 variables (preserve as-is)
4. Add file to template repo following existing patterns
5. Document template location

**Acceptance**: SKILL.md.j2 exists with static frontmatter, no variable substitution

### Task 7: Copy Documentation as Static Files
**Objective**: Copy three documentation files to templates as static resources (no .j2)

**Actions**:
1. Copy `claude_code_agent_skills.md` to `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/docs/claude_code_agent_skills.md` (no .j2)
2. Copy `claude_code_agent_skills_overview.md` to templates/docs/ (no .j2)
3. Copy `blog_equipping_agents_with_skills.md` to templates/docs/ (no .j2)
4. Verify all three files copied without .j2 extension
5. Document copied files

**Acceptance**: Three docs exist in templates/ as static .md files

### Task 8: Register Skills Directory in scaffold_service.py
**Objective**: Add skills directory registration following existing pattern for .claude subdirectories

**Actions**:
1. Read `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`
2. Locate `_add_claude_files` method (around line 288)
3. Add directory registration in `_add_directories` method:
   ```python
   (".claude/skills", "Agent skills directory"),
   (".claude/skills/meta-skill", "Meta-skill for creating new skills"),
   (".claude/skills/meta-skill/docs", "Meta-skill documentation resources"),
   ```
4. Add file registration in `_add_claude_files` method after line 497 (after status_lines):
   ```python
   # Skills
   plan.add_file(
       ".claude/skills/meta-skill/SKILL.md",
       action=action,
       template=".claude/skills/meta-skill/SKILL.md.j2",
       reason="Meta-skill for creating agent skills",
   )
   # Skills documentation
   docs = [
       ("claude_code_agent_skills.md", "Complete skills guide"),
       ("claude_code_agent_skills_overview.md", "Skills architecture"),
       ("blog_equipping_agents_with_skills.md", "Skills design principles"),
   ]
   for doc, reason in docs:
       plan.add_file(
           f".claude/skills/meta-skill/docs/{doc}",
           action=action,
           template=f".claude/skills/meta-skill/docs/{doc}",
           reason=reason,
       )
   ```
5. Save updated scaffold_service.py

**Acceptance**: Skills directory and files registered recursively following DRY pattern

### Task 9: Verify Progressive Disclosure Structure
**Objective**: Validate that SKILL.md follows 5/15/80 rule (metadata → instructions → resources)

**Actions**:
1. Read `.claude/skills/meta-skill/SKILL.md` from BASE
2. Verify structure has three levels:
   - Level 1: YAML frontmatter with name, description (≤5% of content)
   - Level 2: Main instructions in SKILL.md body (≤15% of total knowledge)
   - Level 3: Detailed resources in docs/ (≥80% of knowledge)
3. Verify SKILL.md ≤500 lines (progressive disclosure requirement)
4. Verify docs/ contains detailed implementation guides
5. Document verification results

**Acceptance**: Structure follows 5/15/80 rule, enables on-demand resource loading

### Task 10: Execute Validation Commands
**Objective**: Run all validation commands to ensure zero regressions

**Actions**:
1. Run: `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
2. Run: `cd tac_bootstrap_cli && uv run ruff check .`
3. Run: `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
4. Run: `cd tac_bootstrap_cli && uv run tac-bootstrap --help`
5. Verify all commands pass with zero errors
6. Document results

**Acceptance**: All validation commands pass, no regressions introduced

## Testing Strategy

### Unit Tests
No new unit tests required for this task - structural change only. Existing scaffold_service tests validate template registration patterns.

### Integration Testing
1. Generate a new project with `uv run tac-bootstrap init --wizard`
2. Verify `.claude/skills/meta-skill/` exists in generated project
3. Verify SKILL.md has valid YAML frontmatter
4. Verify all three docs exist in `docs/` subdirectory
5. Verify structure mirrors BASE implementation

### Edge Cases
1. **Source files inaccessible**: Use /scout to verify, ask user for alternatives
2. **Directory already exists in BASE**: Ask user to overwrite/skip/merge
3. **YAML parse errors**: Validate frontmatter and report specific syntax issues
4. **Template registration conflicts**: Follow existing pattern in scaffold_service.py
5. **Progressive disclosure validation**: Ensure SKILL.md ≤500 lines, resources in docs/

## Acceptance Criteria

### BASE Criteria
- [x] Directory `.claude/skills/meta-skill/` exists with complete structure
- [x] SKILL.md contains valid, parseable YAML frontmatter
- [x] YAML frontmatter has required fields: name, description
- [x] All references to 'tac-14' replaced with 'tac_bootstrap'
- [x] Absolute paths converted to relative paths
- [x] Three documentation files exist in `docs/` subdirectory
- [x] Progressive disclosure structure validated (5/15/80 rule)

### TEMPLATES Criteria
- [x] Template directory structure mirrors BASE layout
- [x] SKILL.md.j2 exists with static YAML frontmatter (no Jinja2 variables)
- [x] Three docs copied as static .md files (no .j2 extension)
- [x] Skills directory registered in scaffold_service.py recursively
- [x] Registration follows existing DRY pattern for .claude subdirectories
- [x] Generated projects include complete skills structure

### Validation Criteria
- [x] All validation commands pass (pytest, ruff, mypy, smoke test)
- [x] Generated project includes `.claude/skills/meta-skill/` with all files
- [x] SKILL.md ≤500 lines (progressive disclosure requirement)
- [x] Structure enables on-demand resource loading

## Validation Commands

Execute all commands to validate with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Source File Context
- Source files from tac-14 are working implementations that have been validated in production
- YAML frontmatter structure is standardized and must be preserved exactly
- Documentation files are comprehensive (80% of knowledge) and static content

### Template Design Decisions
1. **SKILL.md.j2**: Gets .j2 extension for potential future parametrization, but currently static
2. **Documentation files**: No .j2 extension because they're static resources referenced by relative paths
3. **Registration pattern**: Follows existing scaffold_service.py pattern for recursive directory handling
4. **Progressive disclosure**: Critical for context efficiency - metadata always loaded, instructions on trigger, resources on-demand

### DDD Architecture Alignment
- **Domain**: No models needed (structural change only)
- **Application**: scaffold_service.py orchestrates template registration
- **Infrastructure**: template_repo.py handles file rendering
- **Interfaces**: No CLI changes needed

### Future Enhancements (Not in Scope)
- Skill discovery mechanism (keyword matching, fuzzy search)
- Skill validation command (verify YAML, check structure)
- Interactive skill creation wizard
- Global skills support (~/.claude/skills/)

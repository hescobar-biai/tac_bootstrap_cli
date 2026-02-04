---
doc_type: feature
adw_id: feature_Tac_14_Task_1
date: 2026-02-04
idk:
  - agent-skills
  - progressive-disclosure
  - meta-skill
  - jinja2-templates
  - scaffold-service
  - yaml-frontmatter
  - claude-code
tags:
  - feature
  - tac-14
  - skills-system
  - templates
related_code:
  - tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py
  - tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/SKILL.md.j2
  - .claude/skills/meta-skill/SKILL.md
  - .claude/skills/meta-skill/docs/claude_code_agent_skills.md
  - .claude/skills/meta-skill/docs/claude_code_agent_skills_overview.md
  - .claude/skills/meta-skill/docs/blog_equipping_agents_with_skills.md
---

# Skills System Implementation (BASE + TEMPLATES)

**ADW ID:** feature_Tac_14_Task_1
**Date:** 2026-02-04
**Specification:** specs/issue-618-adw-feature_Tac_14_Task_1-sdlc_planner-skills-system-implementation.md

## Overview

Implemented the complete Skills System for TAC Bootstrap by creating the `.claude/skills/` directory structure in both the BASE repository and as Jinja2 templates in the CLI. This enables all generated projects to automatically include the Skills System with the meta-skill pattern for creating new custom agent skills following best practices.

The Skills System implements progressive disclosure (5/15/80 rule): metadata → instructions → resources, saving 93-98% tokens vs loading everything upfront. Skills are self-contained, discoverable automation units that agents can invoke when relevant.

## What Was Built

### BASE Structure
- Created `.claude/skills/meta-skill/` directory with complete meta-skill implementation
- Added SKILL.md with valid YAML frontmatter following progressive disclosure pattern
- Included three comprehensive documentation resources in `docs/` subdirectory:
  - `claude_code_agent_skills.md` - Complete guide to creating and managing skills
  - `claude_code_agent_skills_overview.md` - Skills architecture and how they work
  - `blog_equipping_agents_with_skills.md` - Design principles and best practices

### TEMPLATES Structure
- Created mirrored template structure in `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/`
- Converted SKILL.md to SKILL.md.j2 template with static YAML frontmatter (no variable substitution)
- Copied three documentation files as static resources (no .j2 extension)
- Registered skills directory and files in scaffold_service.py following existing DRY patterns

### Service Integration
- Added skills directory registration in scaffold_service.py with three new directories
- Registered SKILL.md.j2 template and three static documentation files
- Added comprehensive TAC-14 comment block documenting the Skills System architecture

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py:118-530` - Added skills directory registration in `_add_directories` method and file registration in `_add_claude_files` method following existing patterns

### Files Created

**BASE Structure:**
- `.claude/skills/meta-skill/SKILL.md` - Meta-skill entry point with YAML frontmatter and progressive disclosure structure
- `.claude/skills/meta-skill/docs/claude_code_agent_skills.md` - 640-line complete guide with examples
- `.claude/skills/meta-skill/docs/claude_code_agent_skills_overview.md` - 329-line architecture overview
- `.claude/skills/meta-skill/docs/blog_equipping_agents_with_skills.md` - 109-line design principles

**TEMPLATES Structure:**
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/SKILL.md.j2` - Templated entry point (435 lines)
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/docs/claude_code_agent_skills.md` - Static doc
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/docs/claude_code_agent_skills_overview.md` - Static doc
- `tac_bootstrap_cli/tac_bootstrap/templates/.claude/skills/meta-skill/docs/blog_equipping_agents_with_skills.md` - Static doc

### Key Changes

1. **Progressive Disclosure Architecture**: SKILL.md follows the 5/15/80 rule with metadata in YAML frontmatter (≤5%), instructions in main body (≤15%), and detailed resources in docs/ (≥80%)

2. **Static YAML Frontmatter**: SKILL.md.j2 template preserves frontmatter exactly with no Jinja2 variable substitution, ensuring YAML parsability across all generated projects

3. **Recursive Directory Registration**: Added three-level directory structure (`.claude/skills/`, `.claude/skills/meta-skill/`, `.claude/skills/meta-skill/docs/`) following existing scaffold_service.py patterns

4. **Static Documentation Resources**: Three docs copied as .md files (not .j2) since they're static reference content loaded on-demand

5. **DRY Pattern Compliance**: File registration uses loop for documentation files to avoid repetition, following existing codebase patterns

## How to Use

### For TAC Bootstrap Developers

1. **BASE structure is the reference implementation**:
   ```bash
   cat .claude/skills/meta-skill/SKILL.md
   ```

2. **Templates auto-deploy to all generated projects**:
   ```bash
   cd tac_bootstrap_cli
   uv run tac-bootstrap init my-project
   cd my-project
   ls -la .claude/skills/meta-skill/
   ```

### For Generated Project Users

1. **Invoke the meta-skill** when you need to create a new skill:
   ```bash
   /meta-skill  # Claude Code will load the SKILL.md instructions
   ```

2. **Read the comprehensive guides** for deep context:
   ```bash
   cat .claude/skills/meta-skill/docs/claude_code_agent_skills.md
   ```

3. **Create custom skills** following the pattern:
   ```
   .claude/skills/
   ├── meta-skill/        # Meta-skill for creating skills
   └── my-custom-skill/   # Your new skill
       ├── SKILL.md       # Skill entry point with YAML frontmatter
       └── resources/     # Optional supporting files
   ```

## Configuration

### YAML Frontmatter Structure

All SKILL.md files must include valid YAML frontmatter:

```yaml
---
name: skill-name-kebab-case
description: Brief description of what the skill does (shown in skill list)
---
```

### Progressive Disclosure Levels

1. **Level 1 (Metadata)**: YAML frontmatter - always loaded, used for discovery
2. **Level 2 (Instructions)**: SKILL.md body - loaded when skill triggered
3. **Level 3 (Resources)**: Files in docs/ or resources/ - loaded on-demand via explicit references

### Directory Structure Requirements

- Skills must be in `.claude/skills/` (project) or `~/.claude/skills/` (personal)
- Each skill is a directory containing a `SKILL.md` file
- YAML frontmatter must be valid and parseable
- Documentation resources should be in subdirectories (e.g., `docs/`, `resources/`)

## Testing

### Validate BASE Structure

```bash
# Check BASE skills directory exists
ls -la .claude/skills/meta-skill/

# Verify YAML frontmatter is valid
head -10 .claude/skills/meta-skill/SKILL.md

# Count documentation resources
ls .claude/skills/meta-skill/docs/ | wc -l
```

### Validate Template Registration

```bash
# Run unit tests
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short

# Check code quality
cd tac_bootstrap_cli && uv run ruff check .

# Verify type safety
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/

# Smoke test CLI
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

### Integration Test - Generate New Project

```bash
# Generate a project
cd tac_bootstrap_cli
uv run tac-bootstrap init test-project --name "Test Project" --project-path ./test-project

# Verify skills directory was created
cd test-project
ls -la .claude/skills/meta-skill/

# Verify SKILL.md has valid YAML
head -10 .claude/skills/meta-skill/SKILL.md

# Verify all documentation files exist
ls .claude/skills/meta-skill/docs/
```

## Notes

### Design Decisions

1. **SKILL.md.j2 with Static Frontmatter**: Gets .j2 extension for potential future parametrization, but currently static to ensure YAML parsability

2. **Documentation as Static Files**: Three docs have no .j2 extension because they're static resources referenced by relative paths - no template variables needed

3. **Registration Pattern**: Follows existing scaffold_service.py pattern for recursive directory handling with `_add_directories` and `_add_claude_files`

4. **Progressive Disclosure**: Critical for context efficiency - metadata always loaded (discovery), instructions on trigger (execution), resources on-demand (deep learning)

### Three Sources of Skills

1. **Personal Skills**: `~/.claude/skills/` - Available across all your projects (not yet implemented)
2. **Project Skills**: `.claude/skills/` - Shared with team via git (implemented in this feature)
3. **Plugin Skills**: Bundled with Claude Code plugins (future enhancement)

### Token Efficiency

The progressive disclosure pattern saves 93-98% of tokens:
- Without: Load 100% of content upfront (e.g., 50,000 tokens for comprehensive guides)
- With: Load 5% metadata (250 tokens), 15% instructions on trigger (7,500 tokens), 80% resources on-demand (40,000 tokens only when explicitly referenced)

### DDD Architecture Alignment

- **Domain**: No new models needed (structural change only)
- **Application**: scaffold_service.py orchestrates template registration
- **Infrastructure**: Template files in `templates/.claude/skills/` directory
- **Interfaces**: No CLI changes needed - transparent to end users

### Future Enhancements (Out of Scope)

- Skill discovery mechanism (keyword matching, fuzzy search)
- Skill validation command (verify YAML, check structure)
- Interactive skill creation wizard via CLI
- Global skills support (~/.claude/skills/) for personal use
- Skill versioning and dependency management

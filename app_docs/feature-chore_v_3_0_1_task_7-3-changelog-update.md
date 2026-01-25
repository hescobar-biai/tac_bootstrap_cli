---
doc_type: feature
adw_id: chore_v_3_0_1_task_7-3
date: 2026-01-25
idk:
  - changelog
  - semantic-versioning
  - keep-a-changelog
  - documentation
  - jinja2-template
  - version-management
tags:
  - feature
  - documentation
  - changelog
related_code:
  - CHANGELOG.md
  - tac_bootstrap_cli/tac_bootstrap/templates/CHANGELOG.md.j2
---

# CHANGELOG Update and Template Creation

**ADW ID:** chore_v_3_0_1_task_7-3
**Date:** 2026-01-25
**Specification:** /Users/hernandoescobar/Documents/Celes/tac_bootstrap/trees/chore_v_3_0_1_task_7-3/specs/issue-210-adw-chore_v_3_0_1_task_7-3-sdlc_planner-update-changelog-new-version.md

## Overview

Updated the project CHANGELOG.md to document version 0.4.0 changes following Keep a Changelog and Semantic Versioning standards. Created a Jinja2 template for CHANGELOG.md that will be used by the TAC Bootstrap CLI when generating new projects.

## What Was Built

- CHANGELOG.md entry for version 0.4.0 with detailed Added and Fixed sections
- CHANGELOG.md.j2 Jinja2 template for generated projects
- Proper version bump from 0.3.0 to 0.4.0 (MINOR version increment)

## Technical Implementation

### Files Modified

- `CHANGELOG.md`: Added new version 0.4.0 entry documenting 5 additions and 4 fixes from tasks 1-6
- `tac_bootstrap_cli/tac_bootstrap/templates/CHANGELOG.md.j2`: Created new template with Keep a Changelog structure

### Key Changes

- Version incremented from 0.3.0 to 0.4.0 due to new features (--once flags)
- Documented `--once` flag additions for trigger_cron.py and trigger_issue_chain.py
- Documented trigger documentation enhancements in ADWs README
- Documented config.yml schema alignment fixes
- Created reusable CHANGELOG template with Jinja2 variables for project name

## How to Use

### Viewing the Updated CHANGELOG

1. View the recent changelog entries:

```bash
head -30 CHANGELOG.md
```

2. Verify the changelog format:

```bash
grep -E "^\## \[.+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}" CHANGELOG.md
```

3. Confirm the --once feature is documented:

```bash
grep "\-\-once" CHANGELOG.md
```

### Using the CHANGELOG Template in Generated Projects

When generating a new project with TAC Bootstrap CLI, the CHANGELOG.md.j2 template will be processed and included in the generated project structure. The template includes:

- Keep a Changelog format
- Semantic Versioning references
- Pre-structured sections (Added, Changed, Deprecated, Removed, Fixed, Security)
- Project name variable: `{{ config.project.name }}`
- Initial 0.1.0 version placeholder

## Configuration

The CHANGELOG follows these standards:

- **Format**: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- **Versioning**: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
- **Date Format**: ISO 8601 (YYYY-MM-DD)
- **Version Format**: [MAJOR.MINOR.PATCH]

### Semantic Versioning Rules

- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

## Testing

Verify the CHANGELOG structure:

```bash
head -30 CHANGELOG.md
```

Verify date format compliance:

```bash
grep -E "^\## \[.+\] - [0-9]{4}-[0-9]{2}-[0-9]{2}" CHANGELOG.md
```

Verify feature documentation:

```bash
grep "\-\-once" CHANGELOG.md
```

Verify template exists:

```bash
cat tac_bootstrap_cli/tac_bootstrap/templates/CHANGELOG.md.j2
```

## Notes

- This task only updates CHANGELOG.md and creates the template; it does NOT update pyproject.toml version
- The CHANGELOG.md.j2 template provides initial structure for generated projects
- Changelog maintenance is typically manual - the template provides a starting point, not automated version management
- Version 0.4.0 represents a MINOR bump due to new `--once` flags in trigger scripts (new features)
- All changes documented in version 0.4.0 were implemented in prior tasks (1-6) of the v3.0.1 improvement set

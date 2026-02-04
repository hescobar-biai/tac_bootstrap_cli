---
doc_type: feature
adw_id: chore_Tac_13_Task_27
date: 2026-02-04
idk:
  - changelog
  - semantic-versioning
  - release-management
  - version-bump
  - documentation
tags:
  - feature
  - general
  - release
related_code:
  - CHANGELOG.md
  - tac_bootstrap_cli/pyproject.toml
---

# Changelog and Version Bump to 0.8.0

**ADW ID:** chore_Tac_13_Task_27
**Date:** 2026-02-04
**Specification:** specs/issue-589-adw-chore_Tac_13_Task_27-chore_planner-changelog-version-bump.md

## Overview

This is the final task of the TAC-13 implementation. The feature documents the completion of the Agent Experts milestone by updating the project CHANGELOG with comprehensive TAC-13 feature documentation and bumping the semantic version from 0.7.1 to 0.8.0. This release represents a minor version bump as it introduces significant new functionality while maintaining backward compatibility.

## What Was Built

- **CHANGELOG.md update**: Added comprehensive [0.8.0] section documenting all TAC-13 Agent Experts features
- **Version bump**: Updated package version from 0.7.1 to 0.8.0 in pyproject.toml
- **Release documentation**: Detailed changelog entries covering core capabilities, agent experts, meta-agentics, orchestration, documentation, and templates

## Technical Implementation

### Files Modified

- `CHANGELOG.md`: Added new [0.8.0] section at the top with 42 lines of comprehensive TAC-13 documentation
- `tac_bootstrap_cli/pyproject.toml`: Bumped version field from "0.7.1" to "0.8.0"

### Key Changes

- **CHANGELOG structure**: Follows Keep a Changelog format with Added/Changed sections for semantic versioning
- **TAC-13 documentation**: Comprehensive coverage of Agent Experts including:
  - Core capabilities (self-improving expertise files, Act → Learn → Reuse loop)
  - Three agent experts: CLI Expert, ADW Expert, Commands Expert
  - Meta-agentic commands: /meta-prompt and /meta-agent
  - Orchestration workflows: /expert-orchestrate and /expert-parallel
  - Documentation and templates added to the system
- **Semantic versioning**: Minor version bump (0.7.1 → 0.8.0) indicates new features with backward compatibility
- **Release date**: 2026-02-03 matching the completion of TAC-13 work

## How to Use

### Viewing the Changelog

1. Open CHANGELOG.md from the repository root
2. The [0.8.0] section appears at the top after the header
3. Review sections under "Added - TAC-13: Agent Experts" and "Changed"

### Verifying Version

```bash
cd tac_bootstrap_cli && grep version pyproject.toml
```

Expected output: `version = "0.8.0"`

### Building and Installing Updated Version

```bash
cd tac_bootstrap_cli
uv build
uv pip install -e .
tac-bootstrap --version
```

Expected output should show version 0.8.0

## Configuration

No configuration changes required. This is a documentation and metadata update only.

## Testing

Verify CHANGELOG.md structure is valid:

```bash
cat CHANGELOG.md | head -n 60
```

Verify version bump in pyproject.toml:

```bash
cd tac_bootstrap_cli && grep -A 3 "^\[project\]" pyproject.toml
```

Run validation suite to ensure no regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run linting checks:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Smoke test CLI functionality:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This represents Task 27 of 27 in the TAC-13 implementation, marking completion of the Agent Experts milestone
- Version 0.8.0 follows semantic versioning principles: minor version bump for new features while maintaining backward compatibility
- The CHANGELOG follows the Keep a Changelog format (https://keepachangelog.com/en/1.1.0/)
- No code changes were required; this is purely a documentation and metadata update
- The comprehensive CHANGELOG entry ensures users understand the full scope of TAC-13 Agent Experts features
- All validation commands passed with zero regressions

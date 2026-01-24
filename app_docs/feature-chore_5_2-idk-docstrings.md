# IDK Docstrings for CLI Modules

**ADW ID:** chore_5_2
**Date:** 2026-01-24
**Specification:** specs/issue-167-adw-chore_5_2-sdlc_planner-apply-idk-docstrings.md

## Overview

Added Information Dense Keywords (IDK) docstrings to all CLI modules and public classes in the `application/` and `infrastructure/` layers. IDK docstrings facilitate semantic search by AI agents through a standardized three-line format: keywords, responsibility, and invariants.

## What Was Built

This chore enhanced documentation across 11 Python modules without changing any implementation logic:

- **Application Services** (8 modules): Core business logic services including scaffold, detect, generate, validation, doctor, upgrade, entity generator, and exceptions
- **Infrastructure** (3 modules): Template repository, filesystem operations, and Git adapter

## Technical Implementation

### Files Modified

All modifications were documentation-only (docstring replacements):

- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added IDK docstrings to module, ScaffoldService class, and ApplyResult class
- `tac_bootstrap_cli/tac_bootstrap/application/detect_service.py`: Added IDK docstrings to module, DetectService class, and DetectedProject class
- `tac_bootstrap_cli/tac_bootstrap/application/entity_generator_service.py`: Added IDK docstrings to module and EntityGeneratorService class
- `tac_bootstrap_cli/tac_bootstrap/application/exceptions.py`: Added IDK docstrings to module and all exception classes
- `tac_bootstrap_cli/tac_bootstrap/application/generate_service.py`: Added IDK docstrings to module and GenerateService class
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Added IDK docstrings to module and service classes
- `tac_bootstrap_cli/tac_bootstrap/application/upgrade_service.py`: Added IDK docstrings to module and UpgradeService class
- `tac_bootstrap_cli/tac_bootstrap/application/validation_service.py`: Added IDK docstrings to module and all validation-related classes
- `tac_bootstrap_cli/tac_bootstrap/application/doctor_service.py`: Added IDK docstrings to module and doctor classes
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/fs.py`: Added IDK docstrings to module and filesystem utilities
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/git_adapter.py`: Added IDK docstrings to module and GitAdapter class
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py`: Added IDK docstrings to module and TemplateRepository class

### Key Changes

- **Standardized Format**: All docstrings follow the three-line IDK format with keywords, responsibility statement, and invariants
- **Semantic Keywords**: Each module/class has 5-12 carefully chosen keywords in kebab-case, ordered by importance
- **Actionable Invariants**: Documented operational constraints that always hold true (e.g., "Detection is read-only, never modifies files")
- **Line Reduction**: Replaced verbose multi-paragraph docstrings with concise IDK format (331 lines removed, 319 added)
- **Zero Logic Changes**: No code logic was modified, ensuring zero regression risk

### IDK Format Structure

```python
"""
IDK: keyword-1, keyword-2, keyword-3, keyword-4, keyword-5
Responsibility: One-line description of module/class purpose
Invariants: Operational constraints that always hold true
"""
```

### Example Transformations

**Before** (scaffold_service.py):
```python
"""Scaffold Service for building and applying generation plans.

This service is responsible for:
1. Building a ScaffoldPlan from TACConfig
2. Applying the plan to create directories and files
3. Handling idempotency and existing files
"""
```

**After**:
```python
"""
IDK: scaffold-service, plan-builder, code-generation, template-rendering, file-operations
Responsibility: Builds scaffold plans from TACConfig and applies them to filesystem
Invariants: Plans are idempotent, templates must exist, output directory must be writable
"""
```

## How to Use

### For AI Agents: Semantic Code Search

AI agents can now search for relevant code using semantic keywords:

1. **Search by Capability**: Use Grep tool to find keywords like `auto-detection`, `template-rendering`, `validation-service`
2. **Understand Contracts**: Read invariants to understand module guarantees (e.g., "Detection is read-only")
3. **Navigate by Responsibility**: Quickly identify which module handles which concern

Example search patterns:
```bash
# Find code generation modules
grep -r "code-generation" tac_bootstrap_cli/

# Find validation logic
grep -r "validation-service" tac_bootstrap_cli/

# Find filesystem operations
grep -r "filesystem-operations" tac_bootstrap_cli/
```

### For Developers: Quick Module Understanding

When exploring the codebase, read the IDK docstring at the top of each module/class to understand:
- **IDK line**: What this module does (capability keywords)
- **Responsibility line**: Primary purpose in one sentence
- **Invariants line**: Operational guarantees and constraints

## Configuration

No configuration changes required. IDK docstrings are passive documentation enhancements.

## Testing

All tests passed with zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Linting verification:
```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Smoke test:
```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- **Scope**: Only module-level and public class docstrings were modified; no function/method docstrings were added
- **Keyword Count**: Targeted 6-8 keywords per docstring (acceptable range: 5-12)
- **Keyword Ordering**: Keywords are ordered by importance, with primary responsibility first
- **No Redundancy**: Avoided semantic overlap between keywords (e.g., not using both `validation` and `validator`)
- **Pure Documentation**: This was a documentation-only chore with zero code logic changes
- **Future Signal**: If a module requires >12 keywords to describe, it may have too many responsibilities (noted but not refactored in this task)

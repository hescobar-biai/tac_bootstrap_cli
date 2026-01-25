---
doc_type: feature
adw_id: feature_7_2
date: 2026-01-25
idk:
  - fractal-documentation
  - workflow-integration
  - adw-document
  - non-blocking-execution
  - documentation-automation
tags:
  - feature
  - documentation
  - adw
  - workflow
related_code:
  - adws/adw_document_iso.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_document_iso.py.j2
  - .claude/commands/generate_fractal_docs.md
---

# Integrate Fractal Docs in Documentation Workflow

**ADW ID:** feature_7_2
**Date:** 2026-01-25
**Specification:** specs/issue-185-adw-feature_7_2-sdlc_planner-integrate-fractal-docs-workflow.md

## Overview

This feature enhances the automated documentation workflow (ADW Document Iso) by integrating fractal documentation generation alongside feature documentation. When code changes are documented, the workflow now automatically updates both feature-level docs in `app_docs/` and module-level fractal docs in `docs/`, keeping all documentation synchronized without manual intervention.

## What Was Built

- Enhanced `generate_documentation()` function in `adw_document_iso.py` with fractal docs integration
- Updated template `adw_document_iso.py.j2` to mirror the changes for new projects
- Non-blocking execution pattern for fractal docs (failures logged as warnings, don't block workflow)
- Automatic inclusion of both doc types in the documentation commit

## Technical Implementation

### Files Modified

- `adws/adw_document_iso.py:157-180`: Added Step 2 fractal docs integration after feature doc validation
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_document_iso.py.j2:157-180`: Mirrored changes in template for new projects

### Key Changes

1. **Step 2 Integration**: After successful feature doc creation, the workflow now executes `/generate_fractal_docs` with `args=['changed']` to update only the docs for modified files.

2. **Non-Blocking Execution**: Wrapped in try-except to ensure fractal docs failures don't block the entire workflow. Failures are logged as warnings, not errors.

3. **AgentTemplateRequest**: Uses the existing agent template execution pattern with:
   - `agent_name='fractal_docs_generator'`
   - `slash_command='/generate_fractal_docs'`
   - `args=['changed']` to scope updates to changed files only
   - Same `adw_id` and `working_dir` as the parent workflow

4. **Result Handling**: Checks `fractal_result.success` and logs appropriate messages:
   - Success: "Fractal documentation updated successfully"
   - Failure: "Fractal docs update failed (non-blocking): {error}"

5. **Automatic Commit**: The existing `git add -A` in `commit_changes()` automatically stages fractal docs files in `docs/` directory alongside feature docs.

## How to Use

The integration is automatic and transparent. When running the documentation workflow:

```bash
uv run adws/adw_document_iso.py --adw-id <your-adw-id>
```

The workflow will:
1. Generate feature documentation in `app_docs/`
2. Automatically update fractal documentation in `docs/` for changed files
3. Commit both documentation types together
4. Log the status of both operations

No additional flags or manual steps are required.

## Configuration

No configuration changes needed. The integration uses the existing `/generate_fractal_docs` slash command which internally calls `scripts/run_generators.sh`.

## Testing

### Manual Testing

Test the enhanced workflow with code changes:

```bash
# Make some code changes in the project
# Then run the document workflow
uv run adws/adw_document_iso.py --adw-id test_workflow_123
```

Verify:
- Feature documentation created in `app_docs/`
- Fractal documentation updated in `docs/` for changed files
- Both committed together in the same commit
- Log shows "Fractal documentation updated successfully" (or warning on failure)

### Error Handling Test

To verify non-blocking behavior, temporarily break the fractal docs generator:

```bash
# Rename the generator script to cause failure
mv scripts/run_generators.sh scripts/run_generators.sh.backup

# Run workflow
uv run adws/adw_document_iso.py --adw-id test_error_handling

# Restore script
mv scripts/run_generators.sh.backup scripts/run_generators.sh
```

Expected behavior:
- Warning logged: "Fractal docs update failed (non-blocking): ..."
- Workflow completes successfully
- Feature docs are committed
- Workflow does NOT exit with error

## Notes

### Design Decisions

- **Non-blocking by design**: Fractal docs are supplementary to feature docs. A failure in fractal generation should not prevent feature documentation from being created and committed.

- **Changed scope**: Uses `args=['changed']` instead of `args=['full']` to only update docs for files affected by the current changes, improving performance.

- **No explicit staging**: Leverages the existing `git add -A` command which automatically includes all new/modified files in `docs/` directory.

- **Template synchronization**: Both the working file (`adws/adw_document_iso.py`) and the template file (`adw_document_iso.py.j2`) are updated identically to ensure new projects generated by TAC Bootstrap inherit this enhancement.

### Related Features

This integration completes the fractal documentation system (FASE 6) by closing the loop between generation and consumption:
- `/generate_fractal_docs` generates the docs
- ADW workflows automatically update them when code changes
- Agents discover the docs via `conditional_docs.md` guidance

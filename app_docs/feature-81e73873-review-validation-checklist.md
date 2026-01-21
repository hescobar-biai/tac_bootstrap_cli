# Review Validation Checklist

**ADW ID:** 81e73873
**Date:** 2026-01-21
**Specification:** specs/issue-64-adw-81e73873-sdlc_planner-review-validation-checklist.md

## Overview

Extended the `/review` command in TAC Bootstrap CLI to automatically generate validation checklists from specification files. This feature extracts acceptance criteria and validation commands from spec files and creates GitHub-compatible markdown checklists that can be used in PR reviews, serving as "unit tests for requirements in English."

## What Was Built

- Enhanced `/review` command template to generate validation checklists alongside JSON reports
- Spec file parser that extracts acceptance criteria and validation commands
- Automated mapping from validation results (syntax, linting, tests, smoke tests) to checklist items
- GitHub-compatible markdown checklist format with proper checkbox rendering
- Backward-compatible implementation that maintains existing JSON output

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/review.md.j2`: Enhanced template with checklist generation instructions, including spec file parsing logic, validation result mapping, and markdown formatting
- `.claude/commands/review.md`: Generated command file updated from the enhanced template
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/prepare_app.md.j2`: Enhanced with Django-specific build steps and application preparation improvements
- `tac_bootstrap_cli/tac_bootstrap/application/scaffold_service.py`: Code formatting improvements for better readability
- `.gitignore`: Additional patterns for temporary files and build artifacts

### Key Changes

1. **Dual Output Format**: The `/review` command now generates both JSON report (backward compatible) and validation checklist markdown
2. **Spec File Parsing**: Template instructs agent to parse spec files for:
   - Feature name from first heading
   - Acceptance criteria items from `## Acceptance Criteria` section
   - Validation commands from `## Validation Commands` section
   - Current branch and date information
3. **Validation Result Mapping**: Automated validations (syntax, linting, tests, smoke test) are mapped to checkbox states:
   - `passed` → `- [x] Check name - PASSED`
   - `failed` → `- [ ] Check name - FAILED`
4. **Checklist File Naming**: Checklists saved as `<spec_file>-checklist.md` in same directory as spec
5. **GitHub Compatibility**: Proper markdown formatting with checkboxes, code blocks, and metadata

## How to Use

1. Run the `/review` command with a plan file that has an associated spec:
   ```bash
   /review <plan_file>
   ```

2. The command will:
   - Execute all automated technical validations (syntax, linting, tests, smoke test)
   - Generate a JSON report (as before)
   - Parse the associated spec file for acceptance criteria
   - Generate a validation checklist markdown file
   - Save checklist as `<spec_file>-checklist.md`

3. Use the generated checklist:
   - Copy the checklist content into GitHub PR comments
   - Review each acceptance criterion manually
   - Check off items as they are validated
   - Share with reviewers for systematic validation

Example checklist output location:
```
specs/issue-64-adw-81e73873-sdlc_planner-review-validation-checklist.md
specs/issue-64-adw-81e73873-sdlc_planner-review-validation-checklist-checklist.md  ← Generated
```

## Configuration

No additional configuration required. The feature works with the existing review command workflow.

### Spec File Format Requirements

For optimal checklist generation, spec files should include:
- `## Acceptance Criteria` section with `- [ ]` checkbox items
- `## Validation Commands` section with executable bash commands
- Clear, atomic acceptance criteria (one requirement per checkbox)

### Edge Case Handling

- If spec file has no "## Acceptance Criteria" section, checklist notes "No acceptance criteria found in spec"
- If validation commands section is missing, notes "No validation commands specified"
- Special characters in criteria text are properly escaped for markdown
- Exact formatting of acceptance criteria from spec is preserved

## Testing

### Manual Testing Performed

1. Tested with the feature's own spec file (specs/issue-64-adw-81e73873-sdlc_planner-review-validation-checklist.md)
2. Verified checklist generation with all sections populated correctly
3. Confirmed automated validations mapped correctly to checkbox states
4. Validated GitHub markdown compatibility

### Test Command

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v -k "test"
```

All existing tests pass, confirming backward compatibility.

### Validation Results

From the generated checklist (specs/issue-64-adw-81e73873-sdlc_planner-review-validation-checklist-checklist.md):
- ✅ Syntax and type checking - PASSED
- ✅ Linting - PASSED
- ✅ Unit tests - PASSED
- ✅ Application smoke test - PASSED

## Notes

### Design Decisions

- **Template-based approach**: Checklist generation uses agent instructions in the template rather than Python code for maximum flexibility
- **Separate file**: Checklist saved separately from spec to avoid modifying source specification files
- **Backward compatibility**: Existing JSON output format unchanged, checklist is additive
- **GitHub focus**: Markdown format optimized for GitHub PR comments and issue tracking

### Related Work

- Inspired by spec-kit's `/speckit.checklist` concept
- Similar to BDD acceptance testing but at the specification level
- Complements existing validation workflow rather than replacing it

### Future Enhancements

- Interactive checklist mode where agent checks items as it validates them
- Checklist diff between runs to show validation progress over time
- Integration with GitHub API to automatically post checklist as PR comment
- Custom checklist templates for different project types (backend, frontend, CLI, etc.)

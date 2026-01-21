# Feature: Review Validation Checklist

## Metadata
issue_number: `64`
adw_id: `81e73873`
issue_json: `{"number":64,"title":"Tarea 1: Checklist de Validación en /review","body":"### Descripción\nExtender el comando `/review` para generar checklists de validación automáticos basados en la especificación. Concepto inspirado en `/speckit.checklist` - \"unit tests para requisitos en inglés\".\n\n### Beneficio\n- Validación sistemática antes de ship\n- Reduce bugs escapados a producción\n- Documenta criterios de aceptación verificables\n\n### Prompt para Ejecutar\n\n```\nNecesito extender el comando /review en TAC Bootstrap CLI para que genere un checklist de validación automático.\n\nEl checklist debe:\n1. Leer el archivo de especificación (spec file)\n2. Extraer los requisitos y criterios de aceptación\n3. Generar una lista de verificación con formato:\n   - [ ] Requisito 1 - Descripción\n   - [ ] Requisito 2 - Descripción\n   ...\n4. Incluir validaciones técnicas automáticas:\n   - [ ] Tests pasan\n   - [ ] Linting sin errores\n   - [ ] Build exitoso\n5. Guardar el checklist en el mismo directorio que el spec\n\nArchivos a modificar:\n- tac_bootstrap_cli/tac_bootstrap/templates/commands/review.md.j2\n- Posiblemente crear un nuevo template para el checklist\n\nEl output del checklist debe poder usarse como comentario en GitHub PR.\n```\n\n### Archivos Involucrados\n- `templates/commands/review.md.j2`\n- Nuevo: `templates/checklist.md.j2` (opcional)\n\n### Criterios de Aceptación\n- [ ] `/review` genera checklist basado en spec\n- [ ] Checklist incluye requisitos del spec\n- [ ] Checklist incluye validaciones técnicas\n- [ ] Formato compatible con GitHub markdown\n"}`

## Feature Description
Extend the `/review` command in TAC Bootstrap CLI to automatically generate validation checklists based on specification files. This feature extracts acceptance criteria from spec files and creates structured checklists that serve as "unit tests for requirements in English," ensuring systematic validation before shipping.

The checklist will:
1. Parse spec files to extract acceptance criteria and validation commands
2. Generate GitHub-compatible markdown checklist with automated technical validations
3. Save checklist alongside spec file for PR usage
4. Integrate with existing review validation workflow

## User Story
As a developer using TAC Bootstrap CLI
I want the `/review` command to automatically generate validation checklists from spec files
So that I can systematically verify all acceptance criteria are met, reduce bugs escaping to production, and have clear documentation of what was validated before merging

## Problem Statement
Currently, the `/review` command performs automated technical validations (syntax, linting, tests, smoke tests) and outputs a JSON report with `validation_results` and `review_issues`. However, it does not:
- Extract and validate against acceptance criteria from spec files
- Generate human-readable checklists for manual verification
- Create a reusable checklist output for GitHub PR comments
- Provide a systematic way to verify that all spec requirements were met

This makes it easy to miss requirements and hard to document what was verified during review.

## Solution Statement
Extend the `/review` command template to generate a validation checklist by:
1. Parsing the spec file's "Acceptance Criteria" and "Validation Commands" sections
2. Extracting each criterion as a checklist item
3. Mapping automated validation results (syntax, linting, tests) to checklist items
4. Generating a markdown checklist file alongside the spec
5. Including both automated and manual verification items
6. Formatting output as GitHub-compatible markdown for easy PR commenting

The implementation will:
- Enhance `review.md.j2` template to include checklist generation instructions
- Create a checklist output format that maps to spec acceptance criteria
- Maintain backward compatibility with existing JSON output
- Use existing `validation_results` structure as foundation for automated checks

## Relevant Files

**Existing Templates to Modify:**
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/review.md.j2` - Main review command template that needs checklist generation logic
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/in_loop_review.md.j2` - Quick review variant (may need similar enhancement)

**Reference Templates:**
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/feature.md.j2` - Example of spec file format and acceptance criteria structure
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/bug.md.j2` - Bug spec format
- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/chore.md.j2` - Chore spec format

**Spec Files for Reference:**
- `specs/issue-*.md` - 30+ existing spec files with acceptance criteria sections
- Example: `specs/issue-37-adw-e4dc9574-sdlc_planner-complete-unit-tests.md` - Shows acceptance criteria format

**Infrastructure:**
- `tac_bootstrap_cli/tac_bootstrap/infrastructure/template_repo.py` - Template rendering engine (no changes needed)
- `tac_bootstrap_cli/tac_bootstrap/domain/models.py` - TACConfig model (provides config context to templates)

**Rendered Commands:**
- `.claude/commands/review.md` - Generated command file (will be updated when template changes)

### New Files
Optional: Create a separate checklist template if checklist format should be reusable
- `tac_bootstrap_cli/tac_bootstrap/templates/checklists/validation_checklist.md.j2` - Reusable checklist template (optional)

## Implementation Plan

### Phase 1: Template Enhancement Design
Design the enhanced review template structure to include checklist generation logic while maintaining existing validation workflow.

**Tasks:**
1. Analyze current `review.md.j2` structure and JSON output format
2. Design checklist parsing logic for extracting acceptance criteria from spec
3. Define checklist markdown format compatible with GitHub
4. Plan integration with existing validation results

### Phase 2: Checklist Generation Implementation
Implement the checklist generation logic in the review template.

**Tasks:**
1. Add spec file parsing instructions to extract "Acceptance Criteria" section
2. Add spec file parsing to extract "Validation Commands" section
3. Map automated validation results to checklist items
4. Generate combined checklist with both automated and manual items
5. Add file save logic to write checklist alongside spec

### Phase 3: Template Integration & Testing
Integrate the enhanced template and validate it works correctly.

**Tasks:**
1. Update `review.md.j2` with checklist generation logic
2. Regenerate `.claude/commands/review.md` from template
3. Test checklist generation with example spec file
4. Verify GitHub markdown compatibility
5. Ensure backward compatibility with existing JSON output

## Step by Step Tasks
IMPORTANTE: Ejecutar cada paso en orden.

### Task 1: Analyze Current Review Template
- Read `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/review.md.j2` to understand current structure
- Review existing validation steps and JSON output format
- Identify where to inject checklist generation logic
- Note available Jinja2 template variables: `config.*` (TACConfig instance)

### Task 2: Design Checklist Format
- Define checklist markdown structure based on spec acceptance criteria
- Design mapping from `validation_results` to checklist items
- Plan checklist sections:
  - **Automated Technical Validations** (from validation_results)
  - **Acceptance Criteria** (from spec file)
  - **Manual Verification Items** (from spec notes/instructions)
- Ensure format is GitHub markdown compatible

### Task 3: Implement Spec Parsing Logic
- Add instructions to parse spec file and extract:
  - `## Acceptance Criteria` section with all `- [ ]` items
  - `## Validation Commands` section with all commands
  - `## Testing Strategy` section for test-related criteria
- Design robust parsing that handles variations in spec format
- Extract checklist items while preserving markdown formatting

### Task 4: Implement Checklist Generation
- Enhance `review.md.j2` with checklist generation instructions:
  - Read and parse the spec file (`spec_file` variable)
  - Extract acceptance criteria items
  - Map `validation_results` to automated checklist items
  - Combine into unified checklist
- Add instructions to save checklist to:
  - `{{ config.paths.specs_dir }}/<spec_basename>-checklist.md`
  - Or same directory as spec file

### Task 5: Design Checklist Output Format
Create the checklist markdown format:
```markdown
# Validation Checklist: <Feature Name>

**Spec:** `<spec_file_path>`
**Branch:** `<current_branch>`
**Review ID:** `<adw_id>`
**Date:** `<current_date>`

## Automated Technical Validations

- [x] Syntax and type checking - PASSED
- [x] Linting - PASSED
- [x] Unit tests - PASSED
- [x] Application smoke test - PASSED

## Acceptance Criteria

<!-- Extracted from spec file -->
- [ ] Criterion 1 from spec
- [ ] Criterion 2 from spec
...

## Validation Commands Executed

```bash
<commands from spec Validation Commands section>
```

## Review Summary

<2-4 sentence summary from review_summary>

## Review Issues

<issues from review_issues array with severity>

---
Generated by `/review` command - TAC Bootstrap CLI
```

### Task 6: Integrate with Review Template
- Modify `review.md.j2` to add checklist generation after JSON output
- Add instructions for the agent to:
  1. Generate JSON report as before (backward compatible)
  2. Parse spec file for acceptance criteria
  3. Generate checklist markdown
  4. Save checklist to `<spec_file>-checklist.md`
  5. Report checklist file path to user

### Task 7: Test Checklist Generation
- Regenerate `.claude/commands/review.md` using scaffold command
- Test `/review` command manually with an existing spec file
- Verify checklist is generated with:
  - Automated validations correctly mapped
  - Acceptance criteria correctly extracted
  - Proper GitHub markdown format
  - File saved in correct location

### Task 8: Validate GitHub Compatibility
- Copy generated checklist markdown
- Test in GitHub PR comment preview
- Verify checkboxes render correctly
- Verify code blocks and formatting work
- Ensure special characters are properly escaped

### Task 9: Update Documentation
- Add checklist generation documentation to `review.md.j2` header comments
- Document expected spec file format for checklist extraction
- Note optional vs required sections in spec
- Add example of generated checklist

### Task 10: Run Validation Commands
Execute all validation commands to ensure zero regressions:
- `cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short`
- `cd tac_bootstrap_cli && uv run ruff check .`
- `cd tac_bootstrap_cli && uv run mypy tac_bootstrap/`
- `cd tac_bootstrap_cli && uv run tac-bootstrap --help`

## Testing Strategy

### Unit Tests
No new unit tests needed - this is a template enhancement, not code logic.

### Manual Testing
1. **Test with existing spec file:**
   - Use `specs/issue-37-adw-e4dc9574-sdlc_planner-complete-unit-tests.md`
   - Run `/review` command
   - Verify checklist generated at `specs/issue-37-adw-e4dc9574-sdlc_planner-complete-unit-tests-checklist.md`
   - Verify acceptance criteria extracted correctly

2. **Test with spec file variations:**
   - Test with spec missing "Acceptance Criteria" section
   - Test with spec using different checkbox formats
   - Test with spec having nested criteria
   - Verify graceful handling of edge cases

3. **Test GitHub compatibility:**
   - Copy generated checklist
   - Paste into GitHub PR comment
   - Verify rendering is correct
   - Test checkbox interaction

### Edge Cases
- Spec file not found → Error message with guidance
- Spec file missing "Acceptance Criteria" section → Use empty checklist or default items
- Validation commands fail → Mark automated items as failed in checklist
- Special characters in criteria → Proper markdown escaping
- Very long spec files → Efficient parsing without truncation

## Acceptance Criteria
- [ ] `/review` command generates validation checklist from spec file
- [ ] Checklist includes all items from spec's "Acceptance Criteria" section
- [ ] Checklist includes automated technical validations (syntax, linting, tests, smoke)
- [ ] Checklist maps `validation_results` (passed/failed) to checkbox states
- [ ] Checklist saved as `<spec_file>-checklist.md` in same directory as spec
- [ ] Checklist format is GitHub markdown compatible (renders correctly in PR comments)
- [ ] Checklist includes review summary and issues from JSON output
- [ ] Backward compatibility maintained - JSON output still generated
- [ ] Template documentation updated with checklist generation instructions
- [ ] Manual testing confirms checklist works with existing spec files

## Validation Commands
Ejecutar todos los comandos para validar con cero regresiones:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```
Tests unitarios

```bash
cd tac_bootstrap_cli && uv run ruff check .
```
Linting

```bash
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
```
Type checking

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```
Smoke test

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap scaffold --help
```
Verify scaffold command works

## Notes

**Design Decisions:**
- Checklist generation is template-based (agent instructions) rather than Python code to maintain flexibility
- Checklist saved separately from spec to avoid modifying source files
- Backward compatible - existing JSON output unchanged
- Uses existing `validation_results` structure as foundation

**Future Enhancements:**
- Interactive checklist mode where agent checks items as it validates
- Checklist diff between runs to show progress
- Integration with GitHub API to post checklist as PR comment automatically
- Checklist templates for different project types

**Spec File Format Requirements:**
For optimal checklist generation, spec files should include:
- `## Acceptance Criteria` section with `- [ ]` checkbox items
- `## Validation Commands` section with executable commands
- Clear, atomic acceptance criteria (one requirement per checkbox)

**Related Work:**
- This feature is inspired by spec-kit's `/speckit.checklist` concept
- Similar to BDD acceptance testing but at the specification level
- Complements existing validation workflow rather than replacing it

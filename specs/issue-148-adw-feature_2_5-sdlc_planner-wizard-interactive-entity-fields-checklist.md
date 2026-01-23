# Validation Checklist: Wizard Interactivo para Entity Fields

**Spec:** `specs/issue-148-adw-feature_2_5-sdlc_planner-wizard-interactive-entity-fields.md`
**Branch:** `feature-issue-148-adw-feature_2_5-wizard-interactive-entity-fields`
**Review ID:** `feature_2_5`
**Date:** `2026-01-23`

## Automated Technical Validations

- [x] Syntax and type checking - PASSED
- [x] Linting - PASSED
- [x] Unit tests - PASSED (425 passed, 2 skipped)
- [x] Application smoke test - PASSED

## Acceptance Criteria

- [ ] El wizard guía al usuario paso a paso desde entity name hasta confirmación final
- [ ] Muestra tabla de resumen usando Rich Table antes de confirmar, incluyendo tabla de campos
- [ ] Valida entity name como PascalCase en tiempo real con re-prompt en caso de error
- [ ] Valida field names como snake_case en tiempo real con re-prompt en caso de error
- [ ] Valida que capability sea kebab-case con conversión automática desde entity name
- [ ] Permite cancelar en cualquier momento retornando None sin errores
- [ ] Muestra prompt de max_length solo para tipos FieldType.STRING y FieldType.TEXT
- [ ] Permite agregar múltiples campos mediante loop con confirmación "Agregar otro campo?"
- [ ] Requiere al menos 1 campo antes de permitir confirmación final
- [ ] Retorna EntitySpec válido que pasa todas las validaciones de Pydantic
- [ ] No permite nombres de campo reservados (id, created_at, etc.) ni keywords de Python
- [ ] Usa componentes Rich consistentes con el resto de wizard.py (Prompt, Confirm, Table)
- [ ] Opciones adicionales (auth, async, events) funcionan correctamente como boolean flags
- [ ] Si el usuario no confirma el resumen, ofrece "Edit or Cancel" con funcionalidad correcta

## Validation Commands Executed

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Review Summary

The implementation successfully adds the `run_entity_wizard()` function to wizard.py with all required helper functions (_to_kebab_case, _validate_entity_name_format, _validate_field_name_format, _show_entity_summary). The wizard provides step-by-step guidance for creating entity specifications with real-time validation, Rich table summaries, and proper error handling. All automated tests pass without regressions. However, there are no specific unit tests for the new wizard functionality itself - only the automated validation commands passed. The implementation follows the spec closely and uses the correct imports from entity_config.py. A duplicate EntitySpec class was removed from models.py as indicated in the git diff.

## Review Issues

1. **Issue #1 - Missing Unit Tests for Entity Wizard**
   - **Description:** The spec's Testing Strategy section requires comprehensive unit tests for the entity wizard in `tests/test_wizard.py`, including tests for helper functions (_to_kebab_case, _validate_entity_name_format, _validate_field_name_format) and wizard flow tests. These tests are not present in the implementation.
   - **Resolution:** Add unit tests as specified in the Testing Strategy section (lines 213-230 of spec). Tests should cover: kebab-case conversion, entity/field name validation (valid and invalid cases), complete wizard flow, cancellation scenarios, minimum fields requirement, and max_length for string fields.
   - **Severity:** tech_debt

2. **Issue #2 - Missing Manual Test Script**
   - **Description:** The spec's Phase 3 Integration tasks (lines 157-162) require creating a manual test script in scratchpad (`scratchpad/test_entity_wizard.py`) to verify the UX and wizard flow interactively. This script was not created.
   - **Resolution:** Create the test script as specified to enable manual testing and UX validation of the wizard before integration with CLI commands.
   - **Severity:** skippable

3. **Issue #3 - Duplicate EntitySpec Classes in Codebase**
   - **Description:** There are now TWO EntitySpec classes in the codebase - one in `entity_config.py` (comprehensive, used by wizard) and one in `models.py` (simpler version). While the implementation correctly uses entity_config.EntitySpec, having duplicate classes with the same name creates potential confusion and maintenance burden.
   - **Resolution:** Consider consolidating to a single EntitySpec class, or clearly document why two versions exist and when to use each. The git diff shows a duplicate was removed from models.py (lines 286-359), but another EntitySpec still exists in models.py (starting at line 529).
   - **Severity:** tech_debt

---
*Generado por el comando `/review` - TAC Bootstrap CLI*

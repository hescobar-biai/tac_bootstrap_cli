# Validation Checklist: Actualizar conditional_docs template con reglas de Documentación Fractal

**Spec:** `specs/issue-181-adw-feature_6_6-sdlc_planner-update-conditional-docs-template.md`
**Branch:** `feature-issue-181-adw-feature_6_6-update-conditional-docs-template`
**Review ID:** `feature_6_6`
**Date:** `2026-01-24`

## Automated Technical Validations

- [x] Syntax and type checking - PASSED
- [x] Linting - PASSED
- [x] Unit tests - PASSED
- [x] Application smoke test - PASSED

## Acceptance Criteria

- [x] Template `conditional_docs.md.j2` tiene nueva sección `## Fractal Documentation` al final
- [x] Sección incluye las cuatro reglas condicionales especificadas (documentation, new modules, refactoring, canonical terminology)
- [x] Referencias a paths usan variable Jinja2 con default: `{{ config.paths.app_root | default("src") }}`
- [x] Archivo `.claude/commands/conditional_docs.md` en raíz tiene nueva sección agregada al final
- [x] Formato markdown es consistente en ambos archivos (sin errores de sintaxis)
- [x] Contenido existente de ambos archivos está preservado sin cambios
- [x] Validation commands pasan sin errores (pytest, ruff, mypy, --help)

## Validation Commands Executed

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Review Summary

The implementation successfully adds the Fractal Documentation section to both the Jinja2 template (`conditional_docs.md.j2`) and the rendered file in the root (`.claude/commands/conditional_docs.md`). All four conditional rules are present: reading `docs/` for understanding code structure, running `/generate_fractal_docs changed` after creating modules, running `/generate_fractal_docs full` when refactoring, and reading `canonical_idk.yml` for canonical terminology. The Jinja2 template correctly uses the parameterized variable `{{ config.paths.app_root | default("src") }}` while the root file uses the concrete path `tac_bootstrap_cli/` as appropriate for the bootstrap project itself. All existing content is preserved, markdown formatting is clean, and all validation commands pass with zero regressions.

## Review Issues

*No issues found - implementation is complete and correct*

---
*Generado por el comando `/review` - TAC Bootstrap CLI*

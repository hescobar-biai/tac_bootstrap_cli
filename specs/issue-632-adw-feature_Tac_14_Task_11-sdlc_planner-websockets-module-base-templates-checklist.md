# Validation Checklist: Implementar WebSockets module (BASE + TEMPLATES)

**Spec:** `specs/issue-632-adw-feature_Tac_14_Task_11-sdlc_planner-websockets-module-base-templates.md`
**Branch:** `feature-issue-632-adw-feature_Tac_14_Task_11-websockets-module-base-templates`
**Review ID:** `feature_Tac_14_Task_11`
**Date:** `2026-02-05`

## Automated Technical Validations

- [x] Syntax and type checking - PASSED
- [x] Linting - PASSED
- [x] Unit tests - PASSED (765 passed, 2 skipped)
- [x] Application smoke test - PASSED

## Acceptance Criteria

- [x] `adw_websockets.py` created in BASE with PEP 723 header
- [x] WebSocket server implements localhost-only binding (127.0.0.1)
- [x] ConnectionManager maintains max 100 connections with 60s timeout
- [x] Keepalive implements 30s ping, 10s pong timeout, 3-strike disconnect
- [x] Event broadcasting matches adw_logging.py schema (log_type, log_level)
- [x] Failed broadcasts remove dead connections without crashing
- [x] `start_server()` and `stop_server()` functions for orchestrator control
- [x] Optional token authentication in connection query params
- [ ] Template `.j2` created with `{{ config.websocket_port }}` variable - **BLOCKER**: Template still has hardcoded port 8765
- [x] Template registered in `scaffold_service.py` `_add_adw_modules()` method
- [x] Module docstring documents usage, architecture, SQLite integration
- [x] Import test passes: `python -c "from adws.adw_modules import adw_websockets"` (websockets dependency expected)
- [x] No syntax errors, all validation commands pass

## Validation Commands Executed

```bash
python -c "from adws.adw_modules import adw_websockets"
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/ --ignore-missing-imports
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Review Summary

The WebSocket server module implementation is comprehensive and well-structured, providing real-time event broadcasting with connection management, keepalive, and integration with the SQLite logging system. However, there is one BLOCKING issue: the Jinja2 template still has a hardcoded port value (8765) instead of using the {{ config.websocket_port }} variable as specified in the acceptance criteria.

## Review Issues

### Issue 1 (BLOCKER)
**Description:** The Jinja2 template file (adw_websockets.py.j2) still contains hardcoded port value '8765' instead of using the Jinja2 variable {{ config.websocket_port }}. Found at lines 45, 351, 362, 374, and 400 in the template file.

**Resolution:** Replace all occurrences of hardcoded '8765' with '{{ config.websocket_port }}' in the template file. Specifically: line 45 in usage example, line 351 in function signature default value, line 362 in docstring, line 374 in example, and line 400 in error message.

**Severity:** blocker

---
*Generado por el comando `/review` - TAC Bootstrap CLI*

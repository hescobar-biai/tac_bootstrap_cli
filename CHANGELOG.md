# Changelog

## [0.2.2] - 2026-01-22

### Fixed
- `tac-bootstrap upgrade` now works with projects using legacy `tac_version` field
- Config field normalized from `tac_version` to `version` for consistency

### Changed
- Template `config.yml.j2` now generates `version` instead of `tac_version`
- Upgrade service normalizes legacy field names automatically


## [0.2.1] - 2026-01-22

### Added
- `resolve_clarifications()` function for auto-resolving ambiguity questions
- ADW workflows now auto-resolve clarifications instead of pausing

### Changed
- Workflows continue automatically with AI-generated decisions
- Clarification responses posted to GitHub issues for transparency

### Removed
- Port management from ADW workflows (not applicable to all app types)
- `--clarify-continue` flag (replaced by auto-resolution)
- `backend_port` and `frontend_port` from state management

### Technical
- Updated `workflow_ops.py` and `workflow_ops.py.j2`
- Updated `adw_plan_iso.py` and `adw_plan_iso.py.j2`
- Removed port functions from `worktree_ops.py`
- Cleaned up `data_types.py` and `state.py`

---

## [0.2.0] - 2026-01-21

### Added
- `tac-bootstrap upgrade` command for updating existing projects
- Version tracking in `config.yml`
- `target_branch` configuration in `config.yml`
- `--version` flag for CLI

### Changed
- All ADW templates synchronized with latest modules
- Improved worktree port management
- Enhanced agent retry logic with rate limiting

### Fixed
- Jinja2 template escaping for JSON examples
- Template synchronization issues

### Upgrade Notes
Projects created with v0.1.0 can upgrade using:
```bash
tac-bootstrap upgrade
```

This will update adws/, .claude/, and scripts/ while preserving your code.

## [0.1.0] - Initial Release

- Initial TAC Bootstrap CLI
- Project scaffolding for Python and TypeScript
- ADW workflow templates
- Claude Code integration

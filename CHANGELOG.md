# Changelog

## [0.2.0] - 2025-XX-XX

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

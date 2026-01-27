---
doc_type: feature
adw_id: chore_Tac_11_task_20
date: 2026-01-27
idk:
  - changelog
  - semantic-versioning
  - documentation
  - release-management
  - tac-11
  - security-hook
  - parallel-workflow
  - scout-command
tags:
  - feature
  - documentation
  - chore
related_code:
  - CHANGELOG.md
  - .claude/hooks/dangerous_command_blocker.py
  - .claude/commands/scout.md
  - .claude/commands/question.md
  - adws/adw_triggers/trigger_issue_parallel.py
---

# CHANGELOG Version 0.6.0 Update

**ADW ID:** chore_Tac_11_task_20
**Date:** 2026-01-27
**Specification:** specs/issue-363-adw-chore_Tac_11_task_20-chore_planner-update-changelog-version-0-6-0.md

## Overview

Updated CHANGELOG.md to version 0.6.0, documenting all TAC-11 integration changes including security features, new commands, and parallel workflow execution capabilities. This represents a minor version bump following Semantic Versioning principles due to significant new features without breaking changes.

## What Was Built

- Version 0.6.0 section in CHANGELOG.md with release date 2026-01-27
- Comprehensive documentation of security features including dangerous_command_blocker.py hook
- Documentation of new /scout and /question commands
- Documentation of parallel trigger capabilities (trigger_issue_parallel.py)
- Documentation of new directory structures (agents/security_logs/, agents/scout_files/)
- Template file references for all new TAC-11 features

## Technical Implementation

### Files Modified

- `CHANGELOG.md`: Added 33 lines documenting version 0.6.0 release with TAC-11 features
- `.mcp.json`: Minor configuration update
- `playwright-mcp-config.json`: Minor configuration update

### Key Changes

- **Version Increment**: Bumped from 0.5.1 to 0.6.0 following Semantic Versioning (new features, backward compatible)
- **Security Features Section**: Documented dangerous_command_blocker.py hook with detailed description of blocked operations (rm -rf, dd, mkfs, chmod -R 777), safer alternatives, and audit trail logging to agents/security_logs/
- **New Commands Section**:
  - /scout: Multi-model parallel exploration using TAC-10 Level 4 delegation, 2-10 Explore agents with frequency-scored reports
  - /question: Read-only Q&A mode for project structure queries
- **Parallel Workflow Execution**: Documented trigger_issue_parallel.py with ThreadPoolExecutor, concurrent processing, configurable workers (default: 5), and graceful shutdown
- **Template References**: Listed all Jinja2 templates (.j2) for generated projects
- **Technical Details Section**: Architecture patterns (pre-execution blocking, TAC-10 Level 4 delegation, thread-safe tracking)

## How to Use

This documentation update serves as the authoritative release notes for version 0.6.0.

### For Users

1. Review CHANGELOG.md to understand new features in 0.6.0:
```bash
cat CHANGELOG.md | head -50
```

2. New security hook blocks dangerous commands automatically - check audit trail:
```bash
ls -la agents/security_logs/
```

3. Use new /scout command for parallel codebase exploration:
```bash
# Example in Claude Code session
/scout "find authentication logic"
```

4. Use new /question command for read-only queries:
```bash
# Example in Claude Code session
/question "What is the project structure?"
```

### For Developers

1. Verify version consistency across project:
```bash
grep -r "0.6.0" pyproject.toml tac_bootstrap_cli/
```

2. Ensure all documented features exist:
```bash
# Security hook
ls -la .claude/hooks/dangerous_command_blocker.py

# Commands
ls -la .claude/commands/scout.md .claude/commands/question.md

# Parallel trigger
ls -la adws/adw_triggers/trigger_issue_parallel.py

# Templates
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/hooks/dangerous_command_blocker.py.j2
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/scout.md.j2
ls -la tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/question.md.j2
ls -la tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_triggers/trigger_issue_parallel.py.j2
```

## Configuration

This changelog follows:
- **Keep a Changelog**: https://keepachangelog.com/en/1.1.0/
- **Semantic Versioning**: https://semver.org/spec/v2.0.0.html

Version format: `[MAJOR.MINOR.PATCH] - YYYY-MM-DD`
- MAJOR: Breaking changes
- MINOR: New features (backward compatible) ← 0.6.0
- PATCH: Bug fixes

## Testing

### Verify Changelog Format
```bash
cat CHANGELOG.md | head -50
```

### Verify Feature Existence
```bash
# Security features
test -f .claude/hooks/dangerous_command_blocker.py && echo "✓ Security hook exists"
test -d agents/security_logs && echo "✓ Security logs directory exists"

# Commands
test -f .claude/commands/scout.md && echo "✓ Scout command exists"
test -f .claude/commands/question.md && echo "✓ Question command exists"
test -d agents/scout_files && echo "✓ Scout files directory exists"

# Parallel trigger
test -f adws/adw_triggers/trigger_issue_parallel.py && echo "✓ Parallel trigger exists"
```

### Run Validation Suite
```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- TAC-11 represents a comprehensive integration of security, exploration, and parallel execution features
- Version 0.6.0 maintains backward compatibility with 0.5.x versions
- All new features include corresponding Jinja2 templates for CLI scaffold generation
- Security hook uses exit code 2 for blocking (pre-execution validation pattern)
- Scout command optimizes cost by using Haiku agents for parallel exploration
- Parallel trigger enables concurrent processing vs sequential trigger_issue_chain.py
- This changelog update consolidates documentation for multiple related TAC-11 tasks

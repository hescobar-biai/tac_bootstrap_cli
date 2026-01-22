# CHANGELOG.md Document Creation

**ADW ID:** 816b4f02
**Date:** 2026-01-22
**Specification:** /Volumes/MAc1/Celes/tac_bootstrap/trees/816b4f02/specs/issue-91-adw-816b4f02-chore_planner-create-changelog-document.md

## Overview

Created the CHANGELOG.md file in the repository root to document version changes, features, and fixes for TAC Bootstrap CLI. This changelog follows the Keep a Changelog standard format and documents the transition from v0.1.0 (initial release) to v0.2.0 (upgrade features release), providing users with clear upgrade instructions and comprehensive change tracking.

## What Was Built

- CHANGELOG.md file in repository root
- Version 0.2.0 documentation with Added, Changed, Fixed, and Upgrade Notes sections
- Version 0.1.0 initial release documentation
- Clear upgrade instructions for existing v0.1.0 projects

## Technical Implementation

### Files Modified

- `CHANGELOG.md`: New file created with version history documentation
- `specs/issue-91-adw-816b4f02-chore_planner-create-changelog-document.md`: Specification file
- `specs/issue-91-adw-816b4f02-chore_planner-create-changelog-document-checklist.md`: Implementation checklist

### Key Changes

- Documented v0.2.0 features: upgrade command, version tracking, target_branch configuration, --version flag
- Documented template synchronization improvements: ADW templates sync, worktree port management, agent retry logic with rate limiting
- Documented bug fixes: Jinja2 template escaping for JSON examples, template synchronization issues
- Provided clear upgrade path for v0.1.0 users with example command and preservation guarantees
- Documented v0.1.0 initial release components as baseline reference

## How to Use

### For End Users

Users can reference the CHANGELOG to understand:

1. What features were added in each version
2. What changed between versions
3. What bugs were fixed
4. How to upgrade their existing projects

### For Developers

When making releases or adding features:

1. Update CHANGELOG.md following the Keep a Changelog format
2. Add entries under appropriate sections (Added, Changed, Fixed, etc.)
3. Update the release date placeholder before publishing
4. Ensure upgrade notes are clear and actionable

## Configuration

No configuration needed. The CHANGELOG.md is a static documentation file in the repository root.

## Testing

The changelog is validated through:

```bash
# Verify file exists and has correct content
cat CHANGELOG.md

# Verify CLI version matches changelog
cd tac_bootstrap_cli && uv run tac-bootstrap --version
```

## Notes

**CHANGELOG Structure:**
- Follows Keep a Changelog standard (https://keepachangelog.com)
- Versions in descending order (newest first)
- Date format: YYYY-MM-DD (placeholder: 2025-XX-XX until release)
- Categorized sections: Added, Changed, Fixed, Upgrade Notes

**Upgrade Strategy Documented:**
- OVERWRITE strategy: adws/, .claude/, scripts/ are completely replaced
- Preservation: Everything outside those directories (src/, tests/, config.yml content) remains untouched
- Backup: Created before upgrade allows manual recovery of custom modifications
- No breaking changes: v0.1.0 projects continue working without upgrade

**Version Detection:**
- If config.yml has no version field: assumes "0.1.0"
- If config.yml doesn't exist: error "Not a TAC Bootstrap project"
- Upgrade is optional: v0.1.0 projects work without upgrading

**Future Considerations:**
- Date placeholder (2025-XX-XX) to be updated at actual release time
- URL pattern for version comparison tags can be added later if published to GitHub
- Technical details intentionally kept concise for user readability

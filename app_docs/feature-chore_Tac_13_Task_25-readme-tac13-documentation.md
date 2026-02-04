---
doc_type: feature
adw_id: chore_Tac_13_Task_25
date: 2026-02-04
idk:
  - documentation
  - readme
  - agent-experts
  - tac-13
  - self-improving-agents
  - expertise-files
  - act-learn-reuse
tags:
  - feature
  - documentation
related_code:
  - README.md
---

# TAC-13 Agent Experts README Documentation

**ADW ID:** chore_Tac_13_Task_25
**Date:** 2026-02-04
**Specification:** specs/issue-587-adw-chore_Tac_13_Task_25-chore_planner-update-readme-tac13.md

## Overview

Updated the main README.md to document the TAC-13 Agent Experts feature, adding references to the self-improving agent framework that uses expertise files and the ACT → LEARN → REUSE loop. This documentation update makes TAC-13 discoverable and understandable from the repository's main entry point.

## What Was Built

- Added TAC-13 reference to agentic layer structure showing `.claude/commands/experts/` directory
- Updated TAC-12 Integration section from "three core capabilities" to "four core capabilities" including Agent Experts
- Added TAC-13 entry to the "Referencia: Curso TAC" table
- Documented the ACT → LEARN → REUSE loop pattern and expertise file constraints

## Technical Implementation

### Files Modified

- `README.md`: Main repository documentation
  - Added experts directory to project structure tree (line ~26)
  - Updated TAC-12 Integration section to include fourth pillar for Agent Experts (line ~378-386)
  - Added TAC-13 row to course reference table (line ~416)

### Key Changes

- **Project Structure Update**: Added `.claude/commands/experts/` directory with brief description "Agent Experts (TAC-13)"
- **TAC-12 Integration Section**: Changed from "three core capabilities" to "four core capabilities" and added comprehensive Agent Experts description
- **Agent Experts Description**: Documented as "Self-improving agents that evolve domain-specific mental models through an ACT → LEARN → REUSE loop. Expert agents maintain expertise files (max 1000 lines YAML) that capture patterns, decisions, and institutional knowledge for high-risk domains like security, billing, and complex architectures."
- **Course Reference Table**: Added `| TAC-13 | Agent Experts | .claude/commands/experts/ |` entry

## How to Use

The updated README now provides clear documentation for discovering and understanding TAC-13:

1. **Discover the feature**: Users can see the `experts/` directory in the project structure
2. **Understand the pattern**: The TAC-12 Integration section explains the ACT → LEARN → REUSE loop
3. **Reference course material**: The TAC reference table links to the experts implementation location
4. **Explore implementation**: Follow the path to `.claude/commands/experts/` for actual expert commands

## Configuration

No configuration changes required - this is documentation-only update.

## Testing

Validate the README changes are correct:

```bash
git diff origin/main README.md
```

Run regression tests to ensure no code impact:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run linting to verify code quality remains unchanged:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Execute smoke test to verify CLI functionality:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

- This is purely documentation work with no code changes
- TAC-13 Agent Experts framework is already implemented in `.claude/commands/experts/` directory
- The documentation focuses on making TAC-13 discoverable and understandable from the main README
- Follows the pattern established by TAC-1 through TAC-12 documentation
- Emphasizes the ACT → LEARN → REUSE loop as the core concept of Agent Experts
- Highlights the 1000-line YAML constraint and focus on high-risk domains (security, billing, complex architectures)

---
doc_type: feature
adw_id: chore_Tac_13_Task_26
date: 2026-02-04
idk:
  - agent-expert
  - expertise-file
  - keyword-mapping
  - auto-detection
  - tac-13
  - workflow-ops
  - doc-keywords
tags:
  - feature
  - documentation
  - automation
related_code:
  - adws/adw_modules/workflow_ops.py
  - tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2
---

# AI Docs Keyword Mappings for TAC-13

**ADW ID:** chore_Tac_13_Task_26
**Date:** 2026-02-04
**Specification:** specs/issue-588-adw-chore_Tac_13_Task_26-chore_planner-update-ai-docs-keyword-mappings.md

## Overview

Enhanced the AI documentation auto-detection system to support TAC-13 Agent Experts pattern by adding keyword mappings for agent expert concepts, expertise file structure, and meta-skill patterns. This enables automatic loading of relevant TAC-13 documentation during ADW workflows when issues contain keywords like "agent expert", "expertise file", "self-improving", or "mental model".

## What Was Built

- Added three new keyword mapping entries to the `doc_keywords` dictionary in `detect_relevant_docs()` function
- Synchronized keyword mappings between live implementation and Jinja2 template
- Introduced TAC-13 specific section in the keyword mappings structure

## Technical Implementation

### Files Modified

- `adws/adw_modules/workflow_ops.py`: Added TAC-13 keyword mappings to `detect_relevant_docs()` function (lines 685-687)
- `tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2`: Synchronized template with identical keyword mappings

### Key Changes

- Added `"Tac-13-agent-experts"` mapping with keywords: "agent expert", "expertise file", "self-improving", "mental model", "act learn reuse"
- Added `"expertise-file-structure"` mapping with keywords: "expertise yaml", "expertise structure", "expertise schema"
- Added `"meta-skill-pattern"` mapping with keywords: "meta-skill", "progressive disclosure", "skill levels"
- Created new "# TAC-13 - Agent Experts" comment section in the keyword dictionary for logical organization
- Maintained dual strategy pattern: updated both live implementation and CLI generator template

## How to Use

The keyword mappings work automatically during ADW workflows:

1. Create a GitHub issue with TAC-13 related keywords in the title or body
2. Execute an ADW workflow (e.g., `uv run adws/adw_sdlc_iso.py --issue <num>`)
3. The `detect_relevant_docs()` function automatically scans issue content for keywords
4. Matching documentation topics are loaded and provided to the agent as context
5. Maximum of 8 topics can be loaded automatically (configurable via `MAX_TOPICS`)

### Example Triggers

Issues containing these phrases will auto-load TAC-13 docs:
- "implement agent expert pattern"
- "create expertise file for validation"
- "add self-improving agent capability"
- "design meta-skill for deployment"
- "expertise yaml structure"

## Configuration

The keyword matching behavior can be adjusted in `adws/adw_modules/workflow_ops.py`:

- `MAX_TOPICS = 8`: Maximum number of documentation topics to auto-load
- Keywords are case-insensitive (issue content is lowercased before matching)
- Multiple keyword matches increase confidence for topic selection
- Title matches are weighted higher than body matches

## Testing

Verify the keyword mappings are correctly added:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
```

Run code quality checks:

```bash
cd tac_bootstrap_cli && uv run ruff check .
```

Verify CLI functionality:

```bash
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

Manual verification:

```bash
# Check both files have identical keyword mappings
diff <(grep -A 3 "TAC-13" adws/adw_modules/workflow_ops.py) <(grep -A 3 "TAC-13" tac_bootstrap_cli/tac_bootstrap/templates/adws/adw_modules/workflow_ops.py.j2)
```

## Notes

- The `detect_relevant_docs()` function uses keyword matching to provide context-aware documentation loading during automated workflows
- TAC-13 introduces Agent Experts pattern, expertise files (YAML-based mental models), and meta-skills (progressive disclosure patterns)
- Keywords enable automatic context loading without manual specification in issue descriptions
- The dual strategy pattern ensures CLI generator templates stay synchronized with live implementation
- Future TAC documentation topics can follow the same pattern by adding entries to `doc_keywords` dictionary
- The template file (`.j2`) maintains identical structure to source file in the keyword mapping section

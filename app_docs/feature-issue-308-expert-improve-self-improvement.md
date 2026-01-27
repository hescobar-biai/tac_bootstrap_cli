---
doc_type: feature
adw_id: feature_Tac_10_task_3
date: 2026-01-26
idk:
  - expert-system
  - self-improvement
  - template
  - jinja2
  - git-analysis
  - workflow
  - report-generation
tags:
  - feature
  - expert-system
  - template
related_code:
  - tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2
  - .claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md
  - specs/issue-308-adw-feature_Tac_10_task_3-sdlc_planner-cc-hook-expert-improve-self-improvement-template.md
---

# Expert Self-Improvement Template (Level 7)

**ADW ID:** feature_Tac_10_task_3
**Date:** 2026-01-26
**Specification:** specs/issue-308-adw-feature_Tac_10_task_3-sdlc_planner-cc-hook-expert-improve-self-improvement-template.md

## Overview

This feature completes the Claude Code hook expert system by implementing the self-improvement workflow (Level 7). The cc_hook_expert_improve template enables AI agents to analyze recent git commits, identify learnings in expert/automation layers, and generate structured markdown reports with actionable recommendations for updating expert knowledge. This creates a feedback loop for continuous improvement while maintaining safety through human review of critical prompt modifications.

## What Was Built

- **Updated Jinja2 Template:** Modified `cc_hook_expert_improve.md.j2` to implement manual-trigger, report-only workflow
- **Re-rendered Expert Command:** Updated `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md` with new specifications
- **Git Analysis Workflow:** Implemented 5-phase process analyzing last 5 commits with path-based relevance filtering
- **Structured Report Format:** Defined markdown report sections for Summary, Relevant Changes, Recommendations, and Suggested Actions
- **Safety Mechanisms:** Removed Edit tool access, implemented early-return logic, and console-only output

## Technical Implementation

### Files Modified

- `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2`: Updated template with manual-trigger workflow, git analysis logic, path filtering, and report generation structure (467 lines modified)
- `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md`: Re-rendered command with updated workflow (463 lines modified)
- `specs/issue-308-adw-feature_Tac_10_task_3-sdlc_planner-cc-hook-expert-improve-self-improvement-template.md`: Comprehensive specification document (317 lines added)
- `specs/issue-308-adw-feature_Tac_10_task_3-sdlc_planner-cc-hook-expert-improve-self-improvement-template-checklist.md`: Implementation checklist (48 lines added)

### Key Changes

1. **YAML Frontmatter Updates:**
   - Removed `Edit` from allowed-tools (now: Read, Bash, Grep, Glob only)
   - Changed from automatic hook execution to manual skill invocation
   - Added skill registration documentation for `/cc_hook_expert_improve`

2. **Git Analysis Scope:**
   - Changed from analyzing uncommitted/staged changes to analyzing last 5 commits via `git log -5 --stat`
   - Simplified scope to deterministic, meaningful batch of work
   - Added commit hash tracking and file statistics parsing

3. **Path-Based Relevance Filtering:**
   - Implemented explicit filter for `.claude/commands/experts/cc_hook_expert/`, `adws/adw_modules/`, and `scripts/` directories
   - Added early-return logic when no matching files found
   - Documented rationale: changes to business logic don't improve expert system itself

4. **Report-Only Approach:**
   - Removed all Edit tool usage from workflow
   - Changed from auto-updating expert prompts to generating recommendations
   - Implemented structured markdown report format with 5 sections
   - Output to console only (user can redirect with `> report.md`)

5. **Jinja2 Variables:**
   - Added `{{ config.project.name }}` for project name
   - Added `{{ config.paths.experts_dir }}` for expert commands directory
   - Added `{{ config.commands.expert_improve }}` for command name reference

6. **New Expertise Section:**
   - Documented when to run the command (after milestone work, not after every commit)
   - Explained manual trigger mechanism and safety rationale
   - Added git analysis best practices and pattern identification tips
   - Detailed report structure and content guidance

## How to Use

### For TAC Bootstrap Users (Generating Projects)

1. Generate a new project with TAC Bootstrap CLI:
   ```bash
   uv run tac-bootstrap generate --project-name my-project
   ```

2. The generated project will include `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md`

3. After completing milestone work in expert/automation layers, manually trigger:
   ```bash
   /cc_hook_expert_improve
   ```

4. Review the generated report in console output

5. Manually apply recommendations to expert prompt files as appropriate

### For Template Developers

1. Modify the Jinja2 template:
   ```bash
   vim tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2
   ```

2. Re-render in TAC Bootstrap repository:
   ```bash
   # Template system automatically re-renders during development
   ```

3. Test the rendered command:
   ```bash
   /cc_hook_expert_improve
   ```

## Configuration

### Jinja2 Template Variables

- `config.project.name`: Project name (e.g., "tac_bootstrap")
- `config.paths.experts_dir`: Path to expert commands directory (e.g., ".claude/commands/experts")
- `config.commands.expert_improve`: Expert improve command name (e.g., "/cc_hook_expert_improve")

### Skill Registration

The command should be registered in the Skill tool for invocation via slash command. Add to skills configuration:

```json
{
  "cc_hook_expert_improve": {
    "description": "Review hook changes and update expert knowledge with improvements",
    "path": ".claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md"
  }
}
```

## Testing

### Manual Testing in TAC Bootstrap Repository

Test the expert improve command with real git history:

```bash
# Ensure you're on a branch with at least 5 commits
git log -5 --oneline

# Trigger the expert improve command manually
/cc_hook_expert_improve
```

Expected behavior:
- Analyzes last 5 commits via git log
- Filters for files in `.claude/commands/experts/cc_hook_expert/`, `adws/adw_modules/`, or `scripts/`
- Generates structured markdown report with recommendations
- Outputs to console only

### Test Early Return Logic

Create a test branch with changes only to business logic files:

```bash
# Create test branch
git checkout -b test-early-return

# Make changes to non-expert files only
echo "test" >> README.md
git add README.md
git commit -m "test: non-expert change"

# Trigger command - should return early
/cc_hook_expert_improve
```

Expected output: "No expertise updates needed" message in report summary.

### Validation Commands

Run all validation commands to ensure zero regressions:

```bash
cd tac_bootstrap_cli && uv run pytest tests/ -v --tb=short
cd tac_bootstrap_cli && uv run ruff check .
cd tac_bootstrap_cli && uv run mypy tac_bootstrap/
cd tac_bootstrap_cli && uv run tac-bootstrap --help
```

## Notes

### Workflow Context

This completes the Plan-Build-Improve expert workflow cycle:

- **Plan** (cc_hook_expert_plan): Design the hook implementation approach
- **Build** (cc_hook_expert_build): Execute the planned implementation
- **Improve** (cc_hook_expert_improve): Analyze work and generate improvement recommendations

The improve phase creates a feedback loop that enhances expert commands based on real-world usage, while maintaining safety through human review.

### Design Decisions

1. **Manual Trigger Only:** Self-improvement should be deliberate, not automatic. Running after every commit would be noisy and expensive. Manual control allows users to trigger after meaningful milestone work.

2. **Last 5 Commits Scope:** Simple, deterministic, and covers typical feature/fix scope. Users can run more frequently if needed. Avoids complexity of tracking last-run timestamps.

3. **Path-Based Relevance Filter:** These are the expert/automation layers. Changes to business logic elsewhere don't improve the expert system itself. Simple path-based filter is easy to implement and understand.

4. **Report-Only (No Auto-Edits):** Self-modifying prompts risk corruption or drift. Human-in-the-loop ensures quality control. Safer for critical infrastructure like expert prompts.

5. **Console Output Only:** Simplest approach. No need to manage report file lifecycle, locations, or cleanup. Unix philosophy: output to stdout.

### Future Enhancements

- Could add `--commits N` argument to analyze more/fewer commits
- Could add `--paths` argument to override default filter paths
- Could add `--output FILE` argument to save report to file automatically
- Could integrate with CI/CD to auto-generate reports after merges to main
- Could add metrics tracking (learnings captured count over time)
- Could support analyzing specific commit ranges via arguments

### Related Documentation

- Specification: `specs/issue-308-adw-feature_Tac_10_task_3-sdlc_planner-cc-hook-expert-improve-self-improvement-template.md`
- Previous implementation: `specs/issue-298-adw-feature_Tac_9_task_31-sdlc_planner-cc-hook-expert-improve-template.md` (issue 298)
- Template location: `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md.j2`
- Rendered command: `.claude/commands/experts/cc_hook_expert/cc_hook_expert_improve.md`

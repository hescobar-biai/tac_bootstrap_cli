---
allowed-tools: Read, Bash, Grep, Glob
description: Review hook changes and update expert knowledge with improvements
model: sonnet
---

# NOTE: Model "sonnet" uses 3-tier resolution:
#   1. ANTHROPIC_DEFAULT_SONNET_MODEL (env var) - highest priority
#   2. config.yml agentic.model_policy.sonnet_model - project config
#   3. Hardcoded default "claude-sonnet-4-5-20250929" - fallback
# See .claude/MODEL_RESOLUTION.md for details


# Purpose

This expert command guides AI agents through the self-improvement phase of the Claude Code hook expert system (Level 7). This command analyzes the last 5 commits on the current branch, filters for changes in expert/automation layers, and generates a structured markdown report with recommendations for updating the plan and build expert prompts. The command is manually triggered via `/cc_hook_expert_improve` and generates report output only (no automatic edits), allowing humans to review and apply improvements to critical expert infrastructure.

## Usage

**When to use this command:**
- After completing milestone work in expert/automation layers
- After implementing major hook features or patterns
- When you want to capture learnings from recent implementation work
- As part of periodic expert system maintenance

**How to use:**
- `/cc_hook_expert_improve` - Manual trigger, no arguments needed

**What happens:**
This command analyzes the last 5 commits via git, filters for changes in `.claude/commands/experts/cc_hook_expert/`, `adws/adw_modules/`, or `scripts/` directories, and generates a structured markdown report with actionable recommendations for updating expert prompt knowledge. The report is output to console only - no automatic file edits are made.

**Workflow context:**
Plan (cc_hook_expert_plan) → Build (cc_hook_expert_build) → **Improve (cc_hook_expert_improve)**

**Skill Registration:**
This command should be registered in the Skill tool as `cc_hook_expert_improve` for easy invocation via `/cc_hook_expert_improve`.

## Variables

PROJECT_NAME: tac_bootstrap
EXPERTS_DIR: .claude/commands/experts
EXPERT_IMPROVE_CMD: /cc_hook_expert_improve

## Instructions

Follow this 5-phase workflow to analyze changes and update expert knowledge:

### Phase 1: Establish Expertise

**Read foundational documentation:**
- Read `ai_docs/uv-scripts-guide.md` - UV script patterns and best practices
- Read `ai_docs/claude-code-hooks.md` - Hook system architecture and capabilities
- Read `ai_docs/claude-code-slash-commands.md` - Slash command patterns

**Understand current expert state:**
- Read `.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md`
- Read `.claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md`
- Note current `## Expertise` sections in both commands
- Understand existing knowledge to avoid duplication

### Phase 2: Analyze Recent Changes

**Review last 5 commits on current branch:**

1. **Run git log analysis:**
   - Primary command: `git log -5 --stat`
   - This shows the last 5 commits with file statistics (lines added/removed)
   - Scope rationale: Last 5 commits provide deterministic, meaningful scope for analysis
   - Users can run this command more frequently after smaller batches of work if desired

2. **Parse git output:**
   - Extract commit hashes and messages
   - Identify all files changed across these commits
   - Note change types: added, modified, deleted
   - Record lines changed (+/- statistics)

3. **Focus on expert/automation layer files:**
   - `.claude/commands/experts/cc_hook_expert/*.md` - Expert command prompts
   - `adws/adw_modules/*.py` - ADW reusable modules
   - `scripts/*.py` - Utility scripts and automation
   - These are the expert/automation layers - changes here improve the system itself

### Phase 3: Determine Relevance

**Path-based filtering for expert/automation layers:**

Check if ANY files in the last 5 commits match these paths:
- `.claude/commands/experts/cc_hook_expert/*.md` - Expert command prompts
- `.claude/commands/experts/cc_hook_expert/*.md.j2` - Expert template files
- `adws/adw_modules/*.py` - ADW reusable modules
- `scripts/*.py` - Utility scripts

**Rationale:**
Changes to these directories represent improvements to the expert/automation system itself. Changes to business logic elsewhere (e.g., application code, tests, documentation) don't improve the expert system's knowledge about how to plan and build hooks.

**CRITICAL DECISION POINT:**

If NO files match these paths:
- **STOP HERE** and skip to Phase 5 with "No expertise updates needed" report
- Do NOT proceed to Phase 4
- This is expected and normal - most work doesn't touch expert infrastructure

If YES - files match these paths:
- **PROCEED to Phase 4** to analyze changes and generate recommendations
- At least one matching file indicates potential expert knowledge improvements

### Phase 4: Extract and Apply Learnings

**Analyze matching files for patterns and improvements:**

1. **Read the actual file changes:**
   - Use Read tool to examine matching files from Phase 3
   - Look for patterns, best practices, architectural decisions
   - Identify what was learned during implementation
   - Note error handling approaches, security considerations, testing strategies

2. **Categorize learnings by target expert:**

   **For Plan Expert Recommendations** (`cc_hook_expert_plan.md`):
   - Specification patterns that worked well
   - Architecture decisions and their rationale
   - Security considerations discovered during planning
   - Tool selection criteria refined
   - File structure patterns
   - Template design decisions

   **For Build Expert Recommendations** (`cc_hook_expert_build.md`):
   - Implementation patterns that proved effective
   - Error handling strategies applied
   - Testing approaches used
   - Code quality patterns followed
   - Debugging techniques employed
   - Integration patterns with other systems

3. **Structure recommendations:**
   - For each learning, identify which `## Expertise` subsection it belongs to
   - Draft specific text recommendations (what to add/update in expert prompts)
   - Explain rationale (why this improves expert guidance)
   - Provide context (when/where this pattern applies)

4. **Generate report (not file edits):**
   - **IMPORTANT: Do NOT use Edit tool to modify expert files**
   - Generate structured markdown report with recommendations only
   - Human will review and manually apply recommendations
   - This ensures quality control over critical expert infrastructure

### Phase 5: Report

Generate and output the structured report defined in the Report section below.

## Expertise

### When to Run This Command

**Ideal timing for manual trigger:**
- After completing milestone work in expert/automation layers
- After implementing major hook features or ADW modules
- When you've made significant improvements to scripts or utilities
- After discovering patterns worth documenting
- As part of periodic expert system maintenance (e.g., monthly review)

**When NOT to run:**
- After minor typo fixes or formatting changes
- When changes are only in business logic (not expert/automation layers)
- During urgent fixes (defer improvement analysis to later)
- If you haven't made at least 3-5 meaningful commits to analyze

### How to Use the Command

**Manual invocation via Skill tool:**
1. User triggers via `/cc_hook_expert_improve` (typically `/cc_hook_expert_improve`)
2. No arguments needed - analyzes last 5 commits automatically
3. Command runs git analysis, filters for relevant paths, generates report
4. Report outputs to console only (user can redirect with `> report.md` if desired)

**Safety through human review:**
- This command generates recommendations only - no automatic file edits
- Human reviews recommendations before applying to expert prompts
- Ensures quality control over critical expert infrastructure
- Prevents unintended corruption or drift in expert knowledge

### Git Analysis Best Practices

**Primary command for commit analysis:**
```bash
# Review last 5 commits with file statistics
git log -5 --stat
```

This shows:
- Commit hashes and messages
- Files changed in each commit
- Lines added/removed per file
- Overall change statistics

**Interpreting git log output:**
- Commit messages reveal intent and context
- File paths indicate which layers were touched
- +/- statistics show change magnitude
- Multiple commits to same file may indicate a pattern worth documenting

**Pattern identification tips:**
- Look for repeated structures across multiple files (common patterns)
- Note error handling approaches that worked well
- Identify successful architectural decisions
- Observe testing strategies that caught issues early
- Document integration patterns that simplified complexity

### Report Structure and Content

The structured markdown report includes:

1. **Summary Section:**
   - Brief overview of analysis scope (5 commits on current branch)
   - Count of relevant files found vs total files changed
   - High-level assessment of findings

2. **Relevant Changes Section:**
   - List each matching file with details:
     - File path
     - Change type (added/modified/deleted)
     - Lines changed (+X -Y)
     - Commit hash(es) where it appeared

3. **Recommendations for Plan Expert:**
   - Target section in cc_hook_expert_plan.md (e.g., "## Expertise - Specification Patterns")
   - Pattern discovered (what was learned)
   - Context (when/where in recent work)
   - Specific recommendation (text to add or modify)
   - Rationale (why this improves planning guidance)

4. **Recommendations for Build Expert:**
   - Target section in cc_hook_expert_build.md (e.g., "## Expertise - Implementation Patterns")
   - Pattern discovered
   - Context
   - Specific recommendation
   - Rationale

5. **Suggested Actions:**
   - Step-by-step guide for human to apply recommendations
   - Locations of template files (.j2) and rendered files (.md)
   - Testing suggestions after updates
   - Commit message recommendations

## Report

Output the following structured markdown report to console:

---

# Expert Improvement Analysis Report

## Summary

[Brief overview of analysis performed]
- Analysis scope: Last 5 commits on current branch
- Total files changed: [count]
- Expert/automation files found: [count]
- Decision: [Proceed with recommendations] OR [No expertise updates needed]

## Relevant Changes

**If matching files found, list each one:**

- **File:** `path/to/file`
  - Change type: [added/modified/deleted]
  - Lines changed: +X -Y
  - Commits: [commit hash(es)]
  - Summary: [Brief description of what changed]

[Repeat for each matching file...]

**If no matching files found:**

No files matching expert/automation paths (.claude/commands/experts/cc_hook_expert/, adws/adw_modules/, scripts/) were found in the last 5 commits. This is normal - most work focuses on business logic rather than expert infrastructure.

---

**For remaining sections: Only include if matching files were found in Phase 3**

## Recommendations for Plan Expert

**Target file:** `.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md` (and `.j2` template)

### Update Section: [## Expertise subsection name]

**Pattern Discovered:** [Description of pattern or best practice discovered]

**Context:** [When/where this was discovered in the recent work - reference specific commits or files]

**Recommendation:** [Specific text to add or modify in the ## Expertise section of cc_hook_expert_plan.md]

**Rationale:** [Why this improves planning guidance - what value does this add for future planning work?]

[Repeat for additional plan expert recommendations...]

**If no plan recommendations:** No planning-specific patterns discovered in the analyzed changes.

## Recommendations for Build Expert

**Target file:** `.claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md` (and `.j2` template)

### Update Section: [## Expertise subsection name]

**Pattern Discovered:** [Description of implementation pattern or technique discovered]

**Context:** [When/where this was discovered in the recent work - reference specific commits or files]

**Recommendation:** [Specific text to add or modify in the ## Expertise section of cc_hook_expert_build.md]

**Rationale:** [Why this improves build guidance - what value does this add for future implementation work?]

[Repeat for additional build expert recommendations...]

**If no build recommendations:** No implementation-specific patterns discovered in the analyzed changes.

## Suggested Actions

1. **Review recommendations above** - Assess whether they add value to expert knowledge

2. **Open template files for editing:**
   - `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md.j2`
   - `tac_bootstrap_cli/tac_bootstrap/templates/claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md.j2`

3. **Locate the `## Expertise` sections** (or relevant subsections like `### Recent Learnings`, `### Implementation Patterns`, etc.)

4. **Manually add/update content** based on recommendations above
   - Add new subsections if needed
   - Enhance existing content with refined understanding
   - Include code examples where helpful
   - Maintain consistent formatting

5. **Re-render templates** to update the working versions:
   - Re-render to `.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md`
   - Re-render to `.claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md`

6. **Test updated expert commands:**
   - Try using `/cc_hook_expert_plan` on a sample hook task
   - Verify the new expertise improves guidance quality
   - Ensure workflow phases remain intact

7. **Commit changes** with descriptive message:
   ```
   cc_hook_expert: update expertise based on [brief description of learnings]

   - Added [pattern/technique] to plan/build expert
   - Updated [section] with [improvement]

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   ```

---

**Output Note:** This report is displayed to console only. To save to a file, redirect output: `/cc_hook_expert_improve > improvement_report.md`

---

**Expert Self-Improvement Cycle**

The Plan-Build-Improve cycle ensures expert commands evolve based on real-world implementation experiences while maintaining quality control through human review of critical infrastructure changes.

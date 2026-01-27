---
allowed-tools: Read, Edit, Bash, Grep, Glob
description: Review hook changes and update expert knowledge with improvements
model: sonnet
---

# Purpose

This expert command guides AI agents through the improvement (continuous learning) phase of Claude Code hooks. This is the third step in the Plan-Build-Improve workflow cycle for hook development. The agent will analyze recent hook-related changes, extract learnings and best practices, and update the plan and build expert commands with new knowledge to maintain cutting-edge expertise while keeping workflows stable.

## Usage

**When to use this command:**
- After completing hook implementation (`/cc_hook_expert_build`)
- When you've made changes to hooks and want to capture learnings
- To update expert knowledge with discovered patterns and best practices
- As part of regular expert workflow maintenance

**How to use:**
- `/cc_hook_expert_improve` - Analyzes recent work automatically via git

**What happens:**
This command reviews recent git changes to hook-related files, determines if new expertise was discovered, and selectively updates the `## Expertise` sections of plan and build expert commands with new knowledge while preserving workflow stability.

**Workflow context:**
Plan (cc_hook_expert_plan) → Build (cc_hook_expert_build) → **Improve (cc_hook_expert_improve)**

## Variables

None required - this command analyzes recent work automatically

PROJECT_NAME: tac_bootstrap

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
- Note current expertise sections in both commands

### Phase 2: Analyze Recent Changes

**Review git history for hook-related changes:**

1. **Check uncommitted changes:**
   - Run: `git diff` to examine working directory changes
   - Identify modified hook files

2. **Check staged changes:**
   - Run: `git diff --cached` to examine staged changes
   - Identify hook files ready for commit

3. **Review recent commits:**
   - Run: `git log --oneline -10` to see recent commit messages
   - Run: `git log --name-only -5` to see changed files in recent commits
   - Identify hook-related commits

**Focus on hook-related files:**
- `.claude/hooks/*.py` - Hook implementations
- `.claude/settings*.json` - Hook configurations
- `specs/experts/cc_hook_expert/*.md` - Hook specifications
- `specs/hook-*.md` - Hook implementation plans
- `ai_docs/*hooks*.md` - Hook documentation updates

### Phase 3: Determine Relevance

**Evaluate if changes contain new expertise worth capturing:**

Ask yourself:
- Were new hook patterns or techniques discovered during implementation?
- Did we encounter and solve error handling or security challenges?
- Were performance optimizations or testing approaches improved?
- Did we learn better ways to use UV script dependencies or configurations?
- Were new hook types or matcher patterns explored?
- Did we discover integration patterns with settings.json?
- Were debugging techniques or validation strategies refined?
- Has a new file been added or deleted that warrants an update to expertise?

**CRITICAL DECISION POINT:**

If NO relevant learnings found (e.g., only typo fixes, minor tweaks, unrelated changes):
- **STOP HERE** and skip to Phase 5 to report "No expertise updates needed"
- Do NOT proceed to Phase 4
- Avoid unnecessary work and maintain workflow stability

If YES - relevant learnings found:
- **PROCEED to Phase 4** to extract and apply those learnings

### Phase 4: Extract and Apply Learnings

**Categorize learnings by expert command:**

**For Planning Knowledge** (update `.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md`):
- New hook event usage patterns discovered
- Specification structure improvements identified
- Security planning considerations learned
- Output format decision criteria refined
- Matcher pattern best practices found
- Hook type selection guidance improved

**For Building Knowledge** (update `.claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md`):
- Implementation patterns and coding standards discovered
- UV script configurations and dependency management improved
- Error handling techniques and graceful failure patterns refined
- Testing approaches and validation strategies enhanced
- Settings.json integration patterns learned
- Debugging techniques and troubleshooting steps improved
- Code quality patterns identified

**Update expertise sections:**

1. **Read target expert command file:**
   - For planning learnings: Read `.claude/commands/experts/cc_hook_expert/cc_hook_expert_plan.md`
   - For building learnings: Read `.claude/commands/experts/cc_hook_expert/cc_hook_expert_build.md`

2. **Locate the ## Expertise section** (or equivalent knowledge section)
   - This may be titled differently (e.g., "## Hook Patterns", "## Implementation Patterns")
   - Identify where new knowledge should be added

3. **Use Edit tool to update ONLY expertise sections:**
   - Add new patterns discovered
   - Enhance existing guidance with refined understanding
   - Add examples from successful implementations
   - Document edge cases and solutions found
   - Include code snippets if helpful

4. **Preserve workflow stability:**
   - **NEVER modify ## Workflow sections** - these define the stable process
   - **NEVER change ## Instructions** - these are the core methodology
   - **ONLY update knowledge/expertise/patterns sections** - these evolve with learning
   - Maintain existing formatting and structure

**Documentation best practices:**
- Be specific: Reference actual patterns from the work analyzed
- Be concise: Add value without bloating the expert command
- Be actionable: Ensure learnings can be applied in future work
- Be contextual: Explain when and why to use new patterns

### Phase 5: Report

Follow the Report section below to summarize your work.

## Expertise

### When to Improve Expert Knowledge

**Trigger conditions:**
- After implementing a new hook successfully
- After solving challenging hook-related problems
- After discovering better patterns or approaches
- When documentation reveals gaps in expert knowledge
- After refactoring hook code for improvements

**When NOT to improve:**
- After minor typo fixes or formatting changes
- When changes are unrelated to hooks
- When no new patterns were discovered
- If expertise is already well-documented
- During urgent fixes (defer improvement to later)

### Criteria for Determining Relevance

**High relevance - update expertise:**
- New hook type usage or integration pattern
- Security vulnerability discovered and fixed
- Performance optimization technique found
- Better error handling approach identified
- Improved testing or validation strategy
- UV script dependency insight gained
- Settings.json integration pattern refined

**Low relevance - skip update:**
- Variable renaming or code formatting
- Typo corrections in comments or docs
- Refactoring without behavioral change
- Changes to non-hook files only
- Routine maintenance without discoveries

### Best Practices for Updating Expertise

1. **Selective updates:**
   - Target specific expertise sections
   - Avoid wholesale rewrites
   - Preserve proven patterns

2. **Clear attribution:**
   - Reference the specific implementation that taught the lesson
   - Provide concrete examples
   - Explain the "why" behind the pattern

3. **Maintain stability:**
   - Never change workflow phase definitions
   - Preserve instruction structure
   - Keep report formats consistent

4. **Quality over quantity:**
   - Add valuable insights, not verbose descriptions
   - Consolidate similar patterns
   - Remove outdated advice if discovered

### Git Analysis Techniques

**Effective commands for change analysis:**

```bash
# See uncommitted changes to specific directory
git diff .claude/hooks/

# See staged changes with more context
git diff --cached -U5

# Review recent commits with file changes
git log --stat -5

# Search for specific file patterns in history
git log --oneline --all -- .claude/hooks/*.py

# See what changed in a specific file
git log -p --follow .claude/hooks/pre_tool_use.py
```

**Identifying patterns in changes:**
- Look for repeated code structures (potential patterns)
- Note error handling approaches (potential best practices)
- Identify configuration patterns (settings.json insights)
- Observe testing strategies (validation improvements)

## Report

Provide improvement summary:

### 1. Changes Analyzed

**Git analysis performed:**
- Uncommitted changes: [Yes/No] - [Number of hook files modified]
- Staged changes: [Yes/No] - [Number of hook files staged]
- Recent commits: [Number reviewed] - [Hook-related commits found]

**Hook-related files reviewed:**
- List files examined with change type (modified/added/deleted)

**Relevance determination:**
- [Relevant learnings found] or [No relevant learnings found]
- Brief explanation of decision

### 2. Learnings Extracted

**If relevant learnings found:**
- **Pattern 1:** [Description of pattern discovered]
  - Context: [When/where discovered]
  - Value: [Why this matters]

- **Pattern 2:** [Description of another pattern]
  - Context: [When/where discovered]
  - Value: [Why this matters]

**If no relevant learnings found:**
- "No relevant learnings found - current expert knowledge remains current"
- Explanation: [Why changes didn't warrant expertise updates]

### 3. Expert Updates Made

**If expertise was updated:**

**Updates to cc_hook_expert_plan.md:**
- [Section updated] - [What was added/changed]
- [Another section] - [What was added/changed]
- Or: "No plan expertise updates needed"

**Updates to cc_hook_expert_build.md:**
- [Section updated] - [What was added/changed]
- [Another section] - [What was added/changed]
- Or: "No build expertise updates needed"

**If no updates made:**
- "No expertise updates needed - current knowledge remains current"
- Workflows remain stable and effective

---

**Continuous Improvement Cycle Complete**

The expert workflow cycle (Plan → Build → Improve) ensures hook development expertise continuously evolves based on real-world implementation experiences while maintaining stable, proven workflows.